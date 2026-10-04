"""Destructive, allowlisted fixture smoke. Leaves a fresh active generation."""
import json
import multiprocessing
import time
from pathlib import Path

from demo import (LOCAL, SERVICES, TABLES, assert_seed, compose, es, index_name, inspect,
                  literal, retention, run, seed, snapshot, sql, start)
from fixtures import DEFAULT_REFERENCE, DAY, canonical, expected, generate, parse_reference, stamp
from gate import Gate


def resources():
    ids = compose('ps','-q').stdout.split()
    stats = run(['docker','stats','--no-stream','--format','{{json .}}',*ids]).stdout
    sizes = {}
    for source in TABLES:
        sizes[source] = int(sql(source,'SELECT pg_database_size(current_database());').stdout)
    sizes['search'] = es('GET','_stats/store')['indices']
    return dict(containers=[json.loads(line) for line in stats.splitlines()], database_bytes=sizes,
                volumes={s:compose('exec','-T',s,'du','-sk',
                    '/usr/share/elasticsearch/data' if s=='search' else '/var/lib/postgresql/data').stdout.strip() for s in SERVICES})


def _worker(directory, generation, ready, release):
    with Gate(directory).lease(generation):
        sql('support',f"INSERT INTO demo_operation_ledger VALUES ({literal(generation)},'in-flight','{{}}');")
        ready.set()
        if not release.wait(20):
            raise TimeoutError('smoke worker release missing')


def _reset(directory, ready, result):
    ready.set()
    state = seed(DEFAULT_REFERENCE,reset=True)
    Path(result).write_text(json.dumps(state))


def attached_reset(state):
    ready, release, reset_ready = multiprocessing.Event(), multiprocessing.Event(), multiprocessing.Event()
    worker = multiprocessing.Process(target=_worker,args=(str(LOCAL),state['generation'],ready,release))
    target = LOCAL/'reset-worker-result.json'
    target.unlink(missing_ok=True)
    resetter = multiprocessing.Process(target=_reset,args=(str(LOCAL),reset_ready,str(target)))
    worker.start()
    try:
        assert ready.wait(10), 'attached worker did not acquire source lease'
        resetter.start()
        assert reset_ready.wait(5)
        time.sleep(.3)
        assert resetter.is_alive(), 'reset failed to wait for source worker'
        assert Gate(LOCAL).read()['generation'] == state['generation'], 'reset touched sources before drain'
    finally:
        release.set()
        worker.join(10)
        if resetter.pid:
            resetter.join(120)
        if worker.is_alive(): worker.terminate(); worker.join()
        if resetter.pid and resetter.is_alive(): resetter.terminate(); resetter.join()
    assert worker.exitcode == 0 and resetter.exitcode == 0
    new = json.loads(target.read_text())
    assert new['generation'] != state['generation']
    try:
        with Gate(LOCAL).lease(state['generation']):
            raise AssertionError('retired command admitted')
    except ValueError:
        pass
    assert sql('support','SELECT count(*) FROM demo_operation_ledger;').stdout.strip() == '0'
    assert_seed(new)
    return new


def smoke():
    timing = start()
    state = seed(DEFAULT_REFERENCE, reset=True)
    before = assert_seed(state)
    # Normalize only the intentionally fresh generation. Exact IDs and dates stay equal.
    expectation = expected(generate(DEFAULT_REFERENCE,state['generation']))
    state2 = seed(DEFAULT_REFERENCE, reset=True)
    expectation2 = expected(generate(DEFAULT_REFERENCE,state2['generation']))
    expectation['generation'] = expectation2['generation']
    # Generation occurs in serialized search bytes; UUID hex has fixed width.
    assert expectation == expectation2, 'repeat seeding changed deterministic expectations'
    assert_seed(state2)
    state = state2
    r = parse_reference(state['reference'])
    lo, hi = literal(stamp(r-7*DAY)), literal(stamp(r-5*DAY))
    historical = f"""SELECT s.shipment_id FROM shipment s JOIN depot_assignment a ON a.depot_id=s.depot_id
      AND s.dispatched_at>=a.valid_from AND (a.valid_to IS NULL OR s.dispatched_at<a.valid_to)
      WHERE a.realm='north' AND a.account_id=7 AND s.dispatched_at>={lo} AND s.dispatched_at<{hi}"""
    selected = sql('fulfillment',historical+' ORDER BY 1;').stdout.split()
    assert selected == ['F-held','F-late','F-start'], selected
    harbor = sql('fulfillment',historical.replace("a.realm='north'","a.realm='harbor'")+' ORDER BY 1;').stdout.split()
    assert harbor == ['F-other','F-switch'], harbor
    overlap = sql('fulfillment',f"INSERT INTO depot_assignment VALUES ('bad','D-transfer','north',7,{lo},{hi},1);",check=False)
    assert overlap.returncode != 0 and 'nonoverlapping_ownership' in overlap.stderr
    # Actual runtime role and independent passwords, over TCP with scram authentication.
    for source in TABLES:
        script = 'read PGPASSWORD; export PGPASSWORD; exec psql -h localhost -U demo_adapter -d demo_'+source+' -XqAt -v ON_ERROR_STOP=1'
        password = (LOCAL/f'{source}_adapter_password').read_text().strip()
        roles = compose('exec','-T',source,'sh','-c',script,data=password+"\nSELECT rolsuper,rolbypassrls FROM pg_roles WHERE rolname=current_user;\n")
        assert roles.stdout.strip() == 'f|f', roles.stdout
        denied = compose('exec','-T',source,'sh','-c',script,data=password+'\nDELETE FROM demo_generation;\n',check=False)
        assert denied.returncode != 0 and 'permission denied' in denied.stderr
        other = 'support' if source=='fulfillment' else 'fulfillment'
        denied = compose('exec','-T',source,'sh','-c',script,data=(LOCAL/f'{other}_adapter_password').read_text(),check=False)
        assert denied.returncode != 0 and 'password authentication failed' in denied.stderr
    # Real child-first cleanup, kept separate from future proposal/receipt behavior.
    sql('fulfillment',f"""BEGIN; CREATE TEMP TABLE chosen AS {historical}
      AND NOT EXISTS (SELECT FROM invoice_hold h WHERE h.shipment_id=s.shipment_id);
      DELETE FROM scan WHERE parcel_id IN (SELECT parcel_id FROM parcel WHERE shipment_id IN (SELECT * FROM chosen));
      DELETE FROM parcel WHERE shipment_id IN (SELECT * FROM chosen);
      DELETE FROM shipment WHERE shipment_id IN (SELECT * FROM chosen); COMMIT;""")
    sql('support',f"""BEGIN; CREATE TEMP TABLE chosen AS SELECT ticket_id FROM ticket
      WHERE realm='north' AND account_id=7 AND opened_at>={lo} AND opened_at<{hi};
      DELETE FROM ticket_message WHERE ticket_id IN (SELECT * FROM chosen);
      DELETE FROM ticket WHERE ticket_id IN (SELECT * FROM chosen); COMMIT;""")
    index = index_name(state['generation'])
    selection = {'query':{'bool':{'filter':[{'term':{'realm':'north'}},{'term':{'account_key':'7'}},
                    {'range':{'event_day':{'gte':stamp(r-7*DAY),'lt':stamp(r-5*DAY)}}}]}}}
    hits = es('POST',index+'/_search?seq_no_primary_term=true',selection)['hits']['hits']
    assert sorted(h['_id'] for h in hits) == ['E-mid','E-start']
    for h in hits:
        es('DELETE',index+f"/_doc/{h['_id']}?if_seq_no={h['_seq_no']}&if_primary_term={h['_primary_term']}")
    es('POST',index+'/_refresh')
    after = snapshot(state)
    for source,counts in [('fulfillment',{'shipment':2,'parcel':4,'scan':8}),('support',{'ticket':2,'ticket_message':4})]:
        for table, count in counts.items():
            assert len(before[source][table])-len(after[source][table]) == count,(source,table)
    for source, stable in [('fulfillment',['account','depot','depot_assignment','invoice_hold']),('support',['account','notification_preference'])]:
        for table in stable:
            assert before[source][table] == after[source][table],(source,table)
    # Every nonselected record remains byte-for-byte equal, including Harbor and held trees.
    for source, tables in TABLES.items():
        for table in tables:
            removed = [row for row in before[source][table] if row not in after[source][table]]
            prefixes = ('F-start','F-late') if source=='fulfillment' else ('S-start','S-mid')
            assert all(any(str(v).startswith(prefixes) for v in row.values()) for row in removed),(source,table)
            assert all(row in before[source][table] for row in after[source][table])
    assert after['search'] == {eid:doc for eid,doc in generate(state['reference'],state['generation'])['search'].items() if eid not in ['E-start','E-mid']}
    # Changed and same-index recreated documents reject an old sequence identity.
    state = seed(DEFAULT_REFERENCE,reset=True)
    index = index_name(state['generation'])
    frozen = es('GET',index+'/_doc/E-mid')
    es('PUT',index+'/_doc/E-mid',frozen['_source'] | {'payload':'changed after selection'})
    conflict = es('DELETE',index+f"/_doc/E-mid?if_seq_no={frozen['_seq_no']}&if_primary_term={frozen['_primary_term']}",allowed=(409,))
    assert conflict['status'] == 409
    es('DELETE',index+'/_doc/E-mid')
    es('PUT',index+'/_doc/E-mid',frozen['_source'])
    es('DELETE',index+f"/_doc/E-mid?if_seq_no={frozen['_seq_no']}&if_primary_term={frozen['_primary_term']}",allowed=(409,))
    es('POST',index+'/_refresh')
    result = retention(1)
    assert result['search_purged'] == ['E-horizon']
    search = snapshot(state)['search']
    assert 'E-after-horizon' in search and 'E-horizon' not in search
    assert sql('fulfillment',"SELECT count(*) FROM shipment WHERE shipment_id='F-old-held';").stdout.strip() == '1'
    # Stale approvals cannot use a recreated index or restored operation ledger.
    old_uuid = state['index_uuid']
    audit = LOCAL/'saved-audit-example.json'
    audit.write_text('{"synthetic_saved_evidence":true}\n')
    state = attached_reset(state)
    assert state['index_uuid'] != old_uuid
    assert audit.read_text() == '{"synthetic_saved_evidence":true}\n'
    result = dict(status='passed', version='dispatchworks-v1', reference=DEFAULT_REFERENCE,generation=state['generation'],
                  checks=['repeat-seed-exact-expectations','real-store-fixture-equality','historical-ownership','cross-tenant-preservation',
                          'overlap-constraint','independent-credentials','nonprivileged-runtime-role','held-child-first-cleanup',
                          'conditional-search-changed-and-recreated','retention-horizon','standalone-reset','attached-worker-drain',
                          'retired-command-rejection','index-identity-change','ledger-restoration','saved-audit-preservation'],
                  integration='real PostgreSQL and Elasticsearch; cooperative worker harness; application integration deferred',
                  **timing, resources=resources())
    (LOCAL/'smoke-result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
