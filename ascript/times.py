from .stable_hash import stable_hash
from dataclasses import dataclass


DEFAULT_TIMES = (
    [0.217, 0.103, 0.112, 0.177, 0.072, 0.16, 0.072, 0.184]
    + [0.104, 0.159, 0.225, 0.328, 0.321, 0.591, 0.168, 0.08]
    + [0.099, 0.11, 0.064, 0.209, 0.127, 0.288, 0.047, 0.16]
    + [0.384, 0.175, 0.05, 0.136, 0.296, 0.225, 0.295]
)


@dataclass
class Times:
    keystroke_max: float = 0.7
    keystroke_scale: float = 1 / 3
    after_read: float = 1
    at_end: float = 5
    to_print_one_line: float = 0.05
    to_read_one_char: float = 0.01
    before_typing: float = 2
    after_typing: float = 2


class KeyTimes:
    def __init__(self, times=None, keystroke_times=DEFAULT_TIMES):
        times = times or Times()
        kt = (t * times.keystroke_scale for t in keystroke_times)
        self.keystroke_times = [t for t in kt if t <= times.keystroke_max]
        self.times = times

    def to_read(self, chars):
        return chars * self.times.to_read_one_char + self.times.after_read

    def to_type(self, line, to_hash=None):
        yield '', self.times.before_typing

        index = int(stable_hash(to_hash or line)[:8], 16)
        for char in line:
            index = (index + 1) % len(self.keystroke_times)
            time = self.keystroke_times[index]
            yield char, time

        yield '', self.times.after_typing
