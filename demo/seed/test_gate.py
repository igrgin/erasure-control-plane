import multiprocessing
import tempfile
import unittest
from gate import Gate


def hold_worker(directory, ready, release):
    with Gate(directory).lease('old'):
        ready.set()
        release.wait(10)


class GateTests(unittest.TestCase):
    def test_attached_worker_drains_and_old_commands_are_fenced(self):
        with tempfile.TemporaryDirectory() as d:
            gate = Gate(d)
            gate.write({'status':'active','generation':'old'})
            ready, release = multiprocessing.Event(), multiprocessing.Event()
            p = multiprocessing.Process(target=hold_worker,args=(d, ready, release))
            p.start()
            try:
                self.assertTrue(ready.wait(5))
                with self.assertRaises(TimeoutError):
                    with gate.lock(exclusive=True, timeout=.1):
                        self.fail('reset acquired lock while worker was active')
                self.assertEqual(gate.read()['generation'], 'old')
            finally:
                release.set()
                p.join(5)
            self.assertEqual(p.exitcode, 0)
            with gate.lock(exclusive=True):
                gate.write({'status':'resetting','generation':'new'})
            for generation in ['old','new']:
                with self.assertRaises(ValueError):
                    with gate.lease(generation):
                        self.fail('reset in progress')
            gate.write({'status':'active','generation':'new'})
            with self.assertRaises(ValueError):
                with gate.lease('old'):
                    self.fail('old command executed')
            with gate.lease('new'):
                pass


if __name__ == '__main__':
    unittest.main()
