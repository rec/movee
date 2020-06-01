"""
Takes a text and then adds a certain percentage of typing errors to it
using a crude model based on the layout of a standard keyboard.
"""
from . import constants
import hashlib
import random

KEYCHART = [
    ['`1234567890-=', ' qwertyuiop[]\\', ' asdfghjkl;\'', ' zxcvbnm,./'],
    ['~!@#$%^&*()_+', ' QWERTYUIOP{}|', ' ASDFGHJKL:"', ' ZXCVBNM<>?'],
]


def make_errors(line, shift_p=0, row_p=0, column_p=0):
    def _error(key):
        shift, row, column = KEYMAP[key]

        if random.random() < shift_p:
            shift = 1 - shift
        if random.random() < row_p:
            row += -1 + 2 * (random.random() < 0.5)
        if random.random() < column_p:
            column += -1 + 2 * (random.random() < 0.5)

        new_key = KEYCHART[shift][row][column]
        if new_key != key and new_key != ' ':
            yield new_key
            yield constants.BACKSPACE

    rstate = random.getstate()
    seed = hashlib.blake2s(line.encode()).hexdigest()
    random.seed(seed)

    try:
        for key in line:
            try:
                yield from _error(key)
            except (IndexError, KeyError):
                pass
            yield key
    finally:
        random.setstate(rstate)


def _invert(keychart):
    for shift, keys in enumerate(keychart):
        for row, row_keys in enumerate(keys):
            for column, key in enumerate(row_keys):
                yield key, (shift, row, column)


KEYMAP = dict(_invert(KEYCHART))
