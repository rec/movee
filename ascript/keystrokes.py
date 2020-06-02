from . import constants
from .cast import Cast
import statistics

DEFAULT_TIMES = (
    [0.217, 0.103, 0.112, 0.177, 0.072, 0.16, 0.072, 0.184]
    + [0.104, 0.159, 0.225, 0.328, 0.321, 0.591, 0.168, 0.08]
    + [0.099, 0.11, 0.064, 0.209, 0.127, 0.288, 0.047, 0.16]
    + [0.384, 0.175, 0.05, 0.136, 0.296, 0.225, 0.295]
)


def all_keystrokes(files):
    for f in files:
        yield from Cast.read(f).keystroke_times()


def print_keystrokes():
    data = list(all_keystrokes())

    print(statistics.mean(data), statistics.stdev(data))
    print()

    for d in data:
        print(round(d, 3))


def text_to_cast(text, prompt, times, post_delay=0):
    cast = Cast()
    index = constants.stable_hash(text)

    entries = [prompt, ''] + list(text) + [constants.RETURN]
    for i, e in enumerate(entries):
        delta_time = times[(index + i) % len(times)]
        cast.append(e, delta_time)

    if post_delay:
        cast.append('', post_delay)

    return cast


if __name__ == '__main__':
    print_keystrokes()
