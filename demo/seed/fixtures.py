"""Versioned synthetic fixtures. No clock, random input, or external dependency."""
import json
from datetime import datetime, timedelta, timezone

VERSION = 'dispatchworks-v1'
DEFAULT_REFERENCE = '2026-10-04T00:00:00Z'
DAY = timedelta(days=1)


def parse_reference(value):
    if not value.endswith('T00:00:00Z'):
        raise ValueError('reference must be an explicit UTC midnight, YYYY-MM-DDT00:00:00Z')
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def stamp(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def generate(reference=DEFAULT_REFERENCE, generation='oracle'):
    r = parse_reference(reference)
    t = lambda days, seconds=0: stamp(r + days * DAY + timedelta(seconds=seconds))
    accounts = [{'realm': realm, 'account_id': 7} for realm in ['north', 'harbor']]
    f = {'account': accounts, 'depot': [{'depot_id': d} for d in ['D-north', 'D-harbor', 'D-transfer']],
         'depot_assignment': [], 'shipment': [], 'parcel': [], 'scan': [], 'invoice_hold': []}
    for depot, realm, start, end in [('D-north', 'north', -100, None), ('D-harbor', 'harbor', -100, None),
                                    ('D-transfer', 'north', -100, -6), ('D-transfer', 'harbor', -6, None)]:
        f['depot_assignment'].append(dict(assignment_id=depot+'-'+realm, depot_id=depot, realm=realm,
                                         account_id=7, valid_from=t(start), valid_to=t(end) if end else None, revision=1))
    for sid, depot, days, seconds, held in [
        ('F-before', 'D-north', -7, -1, False), ('F-start', 'D-transfer', -7, 0, False),
        ('F-late', 'D-transfer', -6, -1, False), ('F-switch', 'D-transfer', -6, 0, False),
        ('F-held', 'D-north', -6, 3600, True), ('F-end', 'D-north', -5, 0, False),
        ('F-other', 'D-harbor', -7, 3600, False), ('F-old-held', 'D-north', -91, 0, True)]:
        f['shipment'].append(dict(shipment_id=sid, depot_id=depot, dispatched_at=t(days, seconds), revision=1))
        for p in range(2):
            pid = f'{sid}-P{p}'
            f['parcel'].append(dict(parcel_id=pid, shipment_id=sid))
            for s in range(2):
                f['scan'].append(dict(scan_id=f'{pid}-S{s}', parcel_id=pid,
                                      scanned_at=t(days+(3 if s else 0), seconds), payload=f'synthetic scan {sid}/{p}/{s}'))
        if held:
            f['invoice_hold'].append(dict(invoice_reference='INV-'+sid, shipment_id=sid, reason='synthetic invoice hold', revision=1))
    support = {'account': accounts, 'ticket': [], 'ticket_message': [], 'notification_preference': []}
    for tid, realm, days in [('S-start', 'north', -7), ('S-mid', 'north', -6), ('S-end', 'north', -5), ('S-other', 'harbor', -6)]:
        support['ticket'].append(dict(ticket_id=tid, realm=realm, account_id=7, opened_at=t(days), revision=1))
        for m in range(2):
            support['ticket_message'].append(dict(message_id=f'{tid}-M{m}', ticket_id=tid, written_at=t(days+(4 if m else 0)), body=f'synthetic message {tid}/{m}'))
    for realm in ['north', 'harbor']:
        support['notification_preference'].append(dict(realm=realm, account_id=7, channel='email', enabled=True, revision=1))
    search = {}
    for eid, realm, days in [('E-start', 'north', -7), ('E-mid', 'north', -6), ('E-end', 'north', -5),
                             ('E-other', 'harbor', -6), ('E-horizon', 'north', -30), ('E-after-horizon', 'north', -29)]:
        search[eid] = dict(realm=realm, account_key='7', attribution_version=VERSION, event_day=t(days),
                           shipment_reference='synthetic-'+eid, run_generation=generation, payload='synthetic event '+eid)
    return dict(version=VERSION, seed=1, reference=reference, generation=generation, mapping_version=VERSION,
                policy_version=VERSION, fulfillment=f, support=support, search=search,
                pre_purge=[dict(source='fulfillment', id='F-expired', source_time=t(-91)),
                           dict(source='support', id='S-expired', source_time=t(-61)),
                           dict(source='delivery-search', id='E-old', source_time=t(-31))])


def owner(f, shipment):
    matches = [a for a in f['fulfillment']['depot_assignment'] if a['depot_id'] == shipment['depot_id']
               and a['valid_from'] <= shipment['dispatched_at']
               and (a['valid_to'] is None or shipment['dispatched_at'] < a['valid_to'])]
    if len(matches) != 1:
        raise ValueError('missing or ambiguous historical ownership')
    return matches[0]['realm']


def expected(f):
    r = parse_reference(f['reference'])
    start, end = stamp(r-7*DAY), stamp(r-5*DAY)
    selected = {s: {realm: [] for realm in ['north', 'harbor']} for s in ['fulfillment', 'support', 'delivery-search']}
    buckets = {s: {realm: {} for realm in ['north', 'harbor']} for s in selected}
    def add(source, realm, time, counts, value):
        bucket = time[:13]+':00:00Z' if source != 'delivery-search' else time[:10]+'T00:00:00Z'
        measures = buckets[source][realm].setdefault(bucket, {key: 0 for key in counts} | {'serialized_bytes': 0})
        for key, count in counts.items():
            measures[key] += count
        measures['serialized_bytes'] += len(canonical(value).encode())
    for s in f['fulfillment']['shipment']:
        realm = owner(f, s)
        parcels = [p for p in f['fulfillment']['parcel'] if p['shipment_id'] == s['shipment_id']]
        scans = [x for x in f['fulfillment']['scan'] if x['parcel_id'] in {p['parcel_id'] for p in parcels}]
        add('fulfillment', realm, s['dispatched_at'], dict(shipments=1, parcels=len(parcels), scans=len(scans)), [s, parcels, scans])
        if start <= s['dispatched_at'] < end:
            selected['fulfillment'][realm].append(s['shipment_id'])
    for t in f['support']['ticket']:
        messages = [m for m in f['support']['ticket_message'] if m['ticket_id'] == t['ticket_id']]
        add('support', t['realm'], t['opened_at'], dict(tickets=1, messages=len(messages)), [t, messages])
        if start <= t['opened_at'] < end:
            selected['support'][t['realm']].append(t['ticket_id'])
    for eid, doc in f['search'].items():
        add('delivery-search', doc['realm'], doc['event_day'], dict(documents=1), doc)
        if start <= doc['event_day'] < end:
            selected['delivery-search'][doc['realm']].append(eid)
    inventory = {}
    for source, horizon, units in [('fulfillment', 90, ['shipments','parcels','scans']), ('support', 60, ['tickets','messages']), ('delivery-search',30,['documents'])]:
        for realm in buckets[source]:
            # Explicit complete zero observations across a day; absence elsewhere is not zero.
            for hour in range(1 if source == 'delivery-search' else 24):
                buckets[source][realm][stamp(r-2*DAY+timedelta(hours=hour))] = dict.fromkeys(units+['serialized_bytes'], 0)
            selected[source][realm].sort()
        inventory[source] = dict(observed_at=f['reference'], coverage_from=stamp(r-horizon*DAY), coverage_to=f['reference'],
                                 complete=True, before_horizon='unknown', buckets=buckets[source],
                                 retained_outside_coverage=['F-old-held'] if source == 'fulfillment' else [],
                                 unavailable_example=dict(observed_at=None, complete=False, buckets=None),
                                 stale_example=dict(observed_at=stamp(r-DAY), complete=False, reason='publication withheld'))
    return {k:f[k] for k in ['version','seed','reference','generation','mapping_version','policy_version']} | dict(
        request=dict(realm='north', account_id=7, from_utc=start, to_utc=end), selected=selected, inventory=inventory,
        cleanup={'fulfillment':dict(deleted=dict(shipments=2,parcels=4,scans=8), retained=dict(shipments=1,parcels=2,scans=4,invoice_holds=1)),
                 'support':dict(deleted=dict(tickets=2,messages=4), excluded=['notification_preference']),
                 'delivery-search':dict(deleted=dict(documents=2), limits=['independent copies have no invoice hold','upstream re-ingestion remains possible'])},
        pre_purge=f['pre_purge'], bytes_unit='UTF-8 canonical JSON fixture bytes, not engine disk size')
