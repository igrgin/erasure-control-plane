"""Cooperative local worker fencing for the synthetic environment.

Every attached worker holds lease() from precondition checks through its last
source effect and receipt. Never release it while a child process is writing.
"""
import fcntl
import json
import os
import time
from contextlib import contextmanager
from pathlib import Path


class Gate:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.state_path = self.directory / 'generation.json'

    def read(self):
        if not self.state_path.exists():
            return {'status': 'unseeded', 'generation': None}
        return json.loads(self.state_path.read_text())

    def write(self, value):
        tmp = self.state_path.with_suffix('.tmp')
        with tmp.open('w') as stream:
            json.dump(value, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, self.state_path)
        fd = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    @contextmanager
    def lock(self, exclusive=False, timeout=30):
        with (self.directory / 'workers.lock').open('a') as stream:
            mode = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            deadline = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(stream, mode | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError('workers did not quiesce; no source reset performed')
                    time.sleep(.05)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    @contextmanager
    def lease(self, generation):
        with self.lock():
            state = self.read()
            if state['status'] != 'active' or state['generation'] != generation:
                raise ValueError('retired generation or reset incomplete; command rejected')
            yield state
