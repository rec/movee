from . import constants
from .cast import Cast
import statistics

ACCEPTED_KEYS = {constants.BACKSPACE, constants.RETURN}

DEFAULT_TIMES = (
    [0.217, 0.103, 0.112, 0.177, 0.072, 0.16, 0.072, 0.184]
    + [0.104, 0.159, 0.225, 0.328, 0.321, 0.591, 0.168, 0.08]
    + [0.099, 0.11, 0.064, 0.209, 0.127, 0.288, 0.047, 0.16]
    + [0.384, 0.175, 0.05, 0.136, 0.296, 0.225, 0.295]
)


def keystroke_times(cast):
    last_time = None
    for line in cast.lines:
        time, _, keys = line
        if len(keys) == 1 or keys in ACCEPTED_KEYS:
            if last_time is not None:
                yield time - last_time
            last_time = time
        else:
            last_time = None


def all_keystrokes(files):
    for f in files:
        yield from keystroke_times(Cast.read(f))


def print_keystrokes():
    data = list(all_keystrokes())

    print(statistics.mean(data), statistics.stdev(data))
    print()

    for d in data:
        print(round(d, 3))


def text_to_cast(
    text, post_delay=0, prompt=constants.PROMPT, times=DEFAULT_TIMES
):
    index = hash(text) % len(times)
    entries = [prompt, ''] + list(text) + [constants.RETURN]

    time = 0
    lines = []

    for i, e in enumerate(entries):
        lines.append([time, 'o', e])
        time += times[(index + i) % len(times)]

    if post_delay:
        lines.append([time + post_delay, 'o', ''])

    return Cast(lines)


if __name__ == '__main__':
    print_keystrokes()
