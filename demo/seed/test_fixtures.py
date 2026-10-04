import unittest
from fixtures import generate, expected, parse_reference


class FixtureTests(unittest.TestCase):
    def test_deterministic_oracle(self):
        a = generate('2026-10-04T00:00:00Z', 'oracle')
        self.assertEqual(a, generate('2026-10-04T00:00:00Z', 'oracle'))
        e = expected(a)
        self.assertEqual(e['cleanup']['fulfillment']['deleted'],
                         {'shipments': 2, 'parcels': 4, 'scans': 8})
        self.assertEqual(e['cleanup']['support']['deleted'], {'tickets': 2, 'messages': 4})
        self.assertEqual(e['cleanup']['delivery-search']['deleted'], {'documents': 2})
        self.assertEqual(e['cleanup']['fulfillment']['retained'],
                         {'shipments': 1, 'parcels': 2, 'scans': 4, 'invoice_holds': 1})

    def test_reference_requires_utc_midnight(self):
        for value in ['2026-10-04', '2026-10-04T01:00:00Z', '2026-10-04T00:00:00+02:00']:
            with self.assertRaises(ValueError):
                parse_reference(value)

    def test_historical_ownership_and_overlapping_ids(self):
        f = generate('2026-10-04T00:00:00Z', 'oracle')
        e = expected(f)
        self.assertEqual(e['selected']['fulfillment']['north'], ['F-held', 'F-late', 'F-start'])
        self.assertEqual(e['selected']['fulfillment']['harbor'], ['F-other', 'F-switch'])
        self.assertEqual([a['account_id'] for a in f['fulfillment']['account']], [7, 7])

    def test_retention_keeps_old_held_tree(self):
        f = generate('2026-10-04T00:00:00Z', 'oracle')
        ids = {x['shipment_id'] for x in f['fulfillment']['shipment']}
        self.assertNotIn('F-expired', ids)
        self.assertIn('F-old-held', ids)
        self.assertNotIn('E-old', f['search'])
        self.assertNotIn('S-expired', {x['ticket_id'] for x in f['support']['ticket']})


if __name__ == '__main__':
    unittest.main()


class CoverageTests(unittest.TestCase):
    def test_committed_oracle_is_current(self):
        import json
        from pathlib import Path
        oracle = json.loads((Path(__file__).resolve().parents[1]/'expected/dispatchworks-v1.json').read_text())
        self.assertEqual(oracle, expected(generate()))

    def test_bucket_time_inherits_parent_and_zero_is_explicit(self):
        e = expected(generate())
        inv = e['inventory']['fulfillment']
        self.assertEqual(inv['buckets']['north']['2026-09-27T00:00:00Z']['scans'], 4)
        self.assertEqual(inv['buckets']['north']['2026-10-02T00:00:00Z']['shipments'], 0)
        self.assertEqual(inv['observed_at'], '2026-10-04T00:00:00Z')
        self.assertEqual(inv['before_horizon'], 'unknown')
        self.assertIsNone(inv['unavailable_example']['buckets'])
        self.assertFalse(inv['stale_example']['complete'])

    def test_custom_clock_and_ownership_gap(self):
        from fixtures import owner
        f = generate('2027-01-01T00:00:00Z')
        self.assertEqual(expected(f)['request']['from_utc'],'2026-12-25T00:00:00Z')
        shipment = next(x for x in f['fulfillment']['shipment'] if x['shipment_id']=='F-start')
        f['fulfillment']['depot_assignment'] = []
        with self.assertRaises(ValueError):
            owner(f,shipment)
