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


class CredentialTests(unittest.TestCase):
    def test_existing_state_directory_is_private_before_secret_creation(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        import demo
        from gate import Gate
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)/'state'
            Gate(directory)
            directory.chmod(0o755)
            with patch.object(demo,'LOCAL',directory):
                demo.initialize()
            self.assertEqual(directory.stat().st_mode & 0o777,0o700)
            self.assertEqual((directory/'search_curl').stat().st_mode & 0o777,0o444)
            self.assertEqual((directory/'support_adapter_password').stat().st_mode & 0o777,0o600)
            self.assertNotEqual((directory/'support_password').read_text(),
                                (directory/'fulfillment_password').read_text())
