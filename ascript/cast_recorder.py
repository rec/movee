import time
from .cast import Cast
from . import keystrokes
from . import constants
from . import util


class CastRecorder:
    def __init__(self, keystroke_times=keystrokes.DEFAULT_TIMES):
        self.keystroke_times = keystroke_times
        self.cast = Cast()
        self.index = 0
        self.start_time = time.time()

    def hash_line(self, line):
        self.index = util.stable_hash(line)

    def add(self, *keys):
        for k in keys:
            delta_time = (time.time() - self.start_time) - self.cast.length
            self.cast.append(k, delta_time)

    def add_line(self, line):
        self.add(line)
        self.add(constants.RETURN)

    def add_key(self, key):
        self.index %= len(self.keystroke_times)
        self.start_time -= self.keystroke_times[self.index]
        self.index += 1
        self.add(key)

    def wait(self, delta):
        self.start_time -= delta
        self.add('')
