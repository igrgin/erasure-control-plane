import fcntl
import time
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


def reset_waiter(directory, finished):
    gate = Gate(directory)
    with gate.lock(exclusive=True):
        gate.write({'status':'active','generation':'new'})
    finished.set()


def late_worker(directory, admitted, rejected):
    try:
        with Gate(directory).lease('old'):
            admitted.set()
    except ValueError:
        rejected.set()


class AdmissionTests(unittest.TestCase):
    def test_late_worker_cannot_extend_reset_drain(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            gate = Gate(directory)
            gate.write({'status':'active','generation':'old'})
            ready, release, finished = [multiprocessing.Event() for _ in range(3)]
            admitted, rejected = multiprocessing.Event(), multiprocessing.Event()
            active = multiprocessing.Process(target=hold_worker,args=(directory,ready,release))
            reset = multiprocessing.Process(target=reset_waiter,args=(directory,finished))
            late = multiprocessing.Process(target=late_worker,args=(directory,admitted,rejected))
            active.start()
            try:
                self.assertTrue(ready.wait(5))
                reset.start()
                # Observe the admission mutex rather than assuming process timing.
                deadline = time.monotonic()+5
                while True:
                    with (Path(directory)/'admission.lock').open('a') as stream:
                        try:
                            fcntl.flock(stream,fcntl.LOCK_EX | fcntl.LOCK_NB)
                        except BlockingIOError:
                            break
                        fcntl.flock(stream,fcntl.LOCK_UN)
                    self.assertLess(time.monotonic(),deadline,'reset did not close admission')
                    time.sleep(.01)
                late.start()
                self.assertFalse(admitted.wait(.2))
                self.assertFalse(finished.is_set())
                self.assertEqual(gate.read()['generation'],'old')
                release.set()
                self.assertTrue(finished.wait(5))
                self.assertTrue(rejected.wait(5))
                self.assertFalse(admitted.is_set())
            finally:
                release.set()
                for process in [active,reset,late]:
                    if process.pid:
                        process.join(5)
                        if process.is_alive():
                            process.terminate()
                            process.join()
            self.assertEqual([p.exitcode for p in [active,reset,late]],[0,0,0])
