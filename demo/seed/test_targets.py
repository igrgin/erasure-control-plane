import unittest
from demo import index_name, sql


class TargetTests(unittest.TestCase):
    def test_rejects_unapproved_databases_and_index_generations(self):
        with self.assertRaises(ValueError):
            sql('production', 'DROP DATABASE production')
        for name in ['*','_all','../production','demo-x','a'*31,'a'*33]:
            with self.assertRaises(ValueError):
                index_name(name)
        self.assertEqual(index_name('a'*32),'demo-'+('a'*32)+'-delivery-v1-events')
