#!/usr/bin/env python3
"""Local fixture administration, intentionally separate from production adapters."""
import argparse
import json
from pathlib import Path
import re
import secrets
import subprocess
import sys
import time
import uuid

from fixtures import DEFAULT_REFERENCE, VERSION, DAY, canonical, expected, generate, parse_reference, stamp
from gate import Gate

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / 'deploy/demo-sources'
LOCAL = DEPLOY / '.local'
PROJECT = 'erasure-demo-sources'
SERVICES = ('fulfillment', 'support', 'search')
TABLES = {s: tuple(generate()[s]) for s in ('fulfillment','support')}


def run(args, data=None, timeout=240, check=True):
    p = subprocess.run(args, input=data, text=True, capture_output=True, timeout=timeout)
    if check and p.returncode:
        # Commands contain no secrets. SQL stdin can contain passwords; do not echo it.
        raise RuntimeError(f'{args[:4]} failed ({p.returncode}): {p.stderr[-3000:]}')
    return p


def compose(*args, data=None, check=True):
    return run(['docker','compose','--project-name',PROJECT,'--file',str(DEPLOY/'compose.yaml'),
                '--profile','sources',*args], data, check=check)


def initialize():
    LOCAL.mkdir(mode=0o700, parents=True, exist_ok=True)
    LOCAL.chmod(0o700)
    for source in SERVICES:
        path = LOCAL / f'{source}_password'
        if not path.exists():
            path.write_text(secrets.token_hex(24)+'\n')
        # Compose file secrets are bind mounts on Linux; the container UID
        # differs from the host owner. The containing directory stays 0700.
        path.chmod(0o444)
    path = LOCAL/'search_curl'
    if not path.exists():
        path.write_text('user = "elastic:'+ (LOCAL/'search_password').read_text().strip()+'"\n')
    path.chmod(0o444)
    for source in ('fulfillment','support'):
        path = LOCAL / f'{source}_adapter_password'
        if not path.exists():
            path.write_text(secrets.token_hex(24)+'\n')
            path.chmod(0o600)


def start():
    initialize()
    begin = time.monotonic()
    compose('up','-d','--wait','--wait-timeout','180')
    return {'startup_seconds':round(time.monotonic()-begin,2)}


def sql(source, query, check=True):
    if source not in TABLES:
        raise ValueError('database not allowlisted')
    return compose('exec','-T',source,'psql','-X','-qAt','-v','ON_ERROR_STOP=1',
                   '-U','demo_admin','-d','demo_'+source, data=query, check=check)


def literal(value):
    if value is None:
        return 'NULL'
    if isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def index_name(generation):
    if not re.fullmatch(r'[a-f0-9]{32}', generation):
        raise ValueError('generation must be a generated UUID hex value')
    return f'demo-{generation}-delivery-v1-events'


def es(method, path, body=None, allowed=(200,201)):
    p = compose('exec','-T','search','curl','-sS','--max-time','30','--config','/run/secrets/search_curl',
                '-X',method,'-H','Content-Type: application/json','--data-binary','@-',
                '-w','\n%{http_code}','http://localhost:9200/'+path, data=canonical(body) if body is not None else '')
    payload, code = p.stdout.rsplit('\n',1)
    result = json.loads(payload) if payload else {}
    if int(code) not in allowed:
        raise RuntimeError(f'Elasticsearch {method} {path}: HTTP {code}: {payload[:500]}')
    return result


def seed(reference, reset=False):
    parse_reference(reference)
    gate = Gate(LOCAL)
    with gate.lock(exclusive=True):
        old = gate.read()
        if old['status'] != 'unseeded' and not reset:
            raise ValueError('already seeded or interrupted: use reset, which fences old commands')
        generation = uuid.uuid4().hex
        # Persist retirement BEFORE the first source write. Failure leaves dispatch closed.
        retired = list(dict.fromkeys(old.get('retired_generations', []) + ([old['generation']] if old['generation'] else [])))
        state = dict(status='resetting', generation=generation, reference=reference, version=VERSION, retired_generations=retired)
        gate.write(state)
        f = generate(reference, generation)
        for source in TABLES:
            schema = (ROOT/'demo/catalog'/f'{source}.sql').read_text()
            schema += (ROOT/'demo/sources'/f'{source}-invariants.sql').read_text()
            schema += (ROOT/'demo/sources/metadata.sql').read_text()
            password = (LOCAL/f'{source}_adapter_password').read_text().strip()
            statements = ['BEGIN;', 'DROP SCHEMA public CASCADE;', 'CREATE SCHEMA public;', schema]
            statements += ["DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='demo_adapter') THEN CREATE ROLE demo_adapter LOGIN NOSUPERUSER NOBYPASSRLS; END IF; END $$;",
                           f'ALTER ROLE demo_adapter PASSWORD {literal(password)};',
                           'GRANT USAGE ON SCHEMA public TO demo_adapter;']
            for table, rows in f[source].items():
                for row in rows:
                    statements.append(f'INSERT INTO {table} ({",".join(row)}) VALUES ({",".join(map(literal,row.values()))});')
            statements += [f'INSERT INTO demo_generation VALUES (true,{literal(generation)},{literal(reference)},{literal(VERSION)});',
                           'GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO demo_adapter;',
                           'REVOKE INSERT, UPDATE, DELETE ON demo_generation FROM demo_adapter;', 'COMMIT;']
            sql(source, '\n'.join(statements))
        # Exact names only. No wildcard deletion and no caller-supplied endpoints.
        for previous in retired:
            es('DELETE', index_name(previous), allowed=(200,404))
        mapping = json.loads((ROOT/'demo/catalog/delivery-search.json').read_text())
        mapping['settings'] = {'number_of_shards':1,'number_of_replicas':0}
        index = index_name(generation)
        es('PUT', index, mapping)
        for eid, doc in f['search'].items():
            es('PUT', index+'/_doc/'+eid, doc)
        es('POST', index+'/_refresh')
        # Fixture metadata records index identity for future conditional-delete scenarios.
        state['index_uuid'] = es('GET', index+'/_settings')[index]['settings']['index']['uuid']
        (LOCAL/'fixtures.json').write_text(json.dumps(f,indent=2)+'\n')
        (LOCAL/'expected.json').write_text(json.dumps(expected(f),indent=2,sort_keys=True)+'\n')
        state['status'] = 'active'
        gate.write(state)
        return state


def snapshot(state):
    result = {}
    for source, tables in TABLES.items():
        result[source] = {}
        for table in tables:
            rows = json.loads(sql(source, f"SELECT coalesce(json_agg(t),'[]'::json) FROM {table} t;").stdout)
            # Normalize PostgreSQL timestamp serialization to the fixture UTC format.
            for row in rows:
                for k,v in row.items():
                    if isinstance(v,str) and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00',v):
                        row[k] = v[:-6]+'Z'
            result[source][table] = sorted(rows,key=canonical)
    hits = es('GET', index_name(state['generation'])+'/_search?size=1000', {'query':{'match_all':{}}})['hits']['hits']
    result['search'] = {hit['_id']:hit['_source'] for hit in hits}
    return result


def inspect():
    gate = Gate(LOCAL)
    with gate.lease(gate.read()['generation']) as state:
        return {'state':state, 'sources':snapshot(state)}


def assert_seed(state):
    actual = snapshot(state)
    f = generate(state['reference'],state['generation'])
    for source,tables in TABLES.items():
        for table in tables:
            assert actual[source][table] == sorted(f[source][table],key=canonical), (source,table)
    assert actual['search'] == f['search'], 'search fixture mismatch'
    return actual


def retention(days):
    if days < 1 or days > 365:
        raise ValueError('advance days must be between 1 and 365')
    gate = Gate(LOCAL)
    with gate.lock(exclusive=True):
        state = gate.read()
        if state['status'] != 'active':
            raise ValueError('seed/reset must finish first')
        at = parse_reference(state.get('retention_time',state['reference'])) + days*DAY
        index = index_name(state['generation'])
        hits = es('GET',index+'/_search?size=1000',{'query':{'range':{'event_day':{'lt':stamp(at-30*DAY)}}}})['hits']['hits']
        for hit in hits:
            es('DELETE',index+'/_doc/'+hit['_id'])
        es('POST',index+'/_refresh')
        sql('fulfillment',f"""BEGIN;
          CREATE TEMP TABLE purge AS SELECT shipment_id FROM shipment s
          WHERE dispatched_at < {literal(stamp(at-90*DAY))} AND NOT EXISTS
            (SELECT FROM invoice_hold h WHERE h.shipment_id=s.shipment_id);
          DELETE FROM scan WHERE parcel_id IN (SELECT parcel_id FROM parcel WHERE shipment_id IN (SELECT * FROM purge));
          DELETE FROM parcel WHERE shipment_id IN (SELECT * FROM purge);
          DELETE FROM shipment WHERE shipment_id IN (SELECT * FROM purge); COMMIT;""")
        sql('support',f"""BEGIN;
          CREATE TEMP TABLE purge AS SELECT ticket_id FROM ticket WHERE opened_at < {literal(stamp(at-60*DAY))};
          DELETE FROM ticket_message WHERE ticket_id IN (SELECT * FROM purge);
          DELETE FROM ticket WHERE ticket_id IN (SELECT * FROM purge); COMMIT;""")
        state['retention_time'] = stamp(at)
        gate.write(state)
        return dict(observed_at=stamp(at), search_purged=[h['_id'] for h in hits],
                    coverage_from={s:stamp(at-days*DAY) for s,days in [('fulfillment',90),('support',60),('delivery-search',30)]},
                    erasure_execution=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['start','seed','inspect','reset','advance','smoke','resources'])
    parser.add_argument('--reference',default=DEFAULT_REFERENCE)
    parser.add_argument('--days',type=int,default=1)
    args = parser.parse_args()
    if args.command == 'start': result = start()
    elif args.command in ('seed','reset'): result = seed(args.reference,args.command=='reset')
    elif args.command == 'inspect': result = inspect()
    elif args.command == 'advance': result = retention(args.days)
    elif args.command == 'smoke':
        from smoke import smoke
        result = smoke()
    else:
        from smoke import resources
        result = resources()
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, TimeoutError, subprocess.TimeoutExpired) as e:
        print(str(e),file=sys.stderr)
        sys.exit(1)
