from . import constants
from . import util
from .cast import Cast
from dataclasses import dataclass


DEFAULT_TIMES = (
    [0.217, 0.103, 0.112, 0.177, 0.072, 0.16, 0.072, 0.184]
    + [0.104, 0.159, 0.225, 0.328, 0.321, 0.591, 0.168, 0.08]
    + [0.099, 0.11, 0.064, 0.209, 0.127, 0.288, 0.047, 0.16]
    + [0.384, 0.175, 0.05, 0.136, 0.296, 0.225, 0.295]
)


def text_to_cast(text, prompt, times, post_delay=0):
    cast = Cast()
    index = util.stable_hash(text)

    entries = [prompt, ''] + list(text) + [constants.RETURN]
    for i, e in enumerate(entries):
        delta_time = times[(index + i) % len(times)]
        cast.append(e, delta_time)

    if post_delay:
        cast.append('', post_delay)

    return cast


@dataclass
class KeyTiming:
    max_keystroke_time: float = 0.7
    keystroke_time_scale: float = 0.32
    time_to_think: float = 1
    time_at_end: float = 5
    time_to_read_one_char: float = 0.005

    def filter(self, times):
        for t in times:
            t *= self.keystroke_time_scale
            if t <= self.max_keystroke_time:
                yield t

    def read_text(self, chars):
        return self.time_to_think + chars * self.time_to_read_one_char
