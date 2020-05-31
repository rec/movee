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


class ErrorAdder:
    def __init__(self, shift=0, row=0, column=0):
        assert 0 <= shift <= 1
        assert 0 <= row <= 1
        assert 0 <= column <= 1

        self.shift = shift
        self.row = row
        self.column = column

    def __call__(self, line):
        rstate = random.getstate()
        seed = hashlib.blake2s(line.encode()).hexdigest()
        random.seed(seed)
        try:
            for k in line:
                errored = self._apply(k)
                if errored != k:
                    yield errored
                    yield constants.BACKSPACE
                yield k
        finally:
            random.setstate(rstate)

    def _apply(self, k):
        try:
            shift, row, column = KEYMAP[k]

            if random.random() < self.shift:
                shift = 1 - shift
            if random.random() < self.row:
                row += -1 + 2 * (random.random() < 0.5)
            if random.random() < self.column:
                column += -1 + 2 * (random.random() < 0.5)

            result = KEYCHART[shift][row][column]
            return k if result == ' ' else result

        except (IndexError, KeyError):
            return k


def _invert(keychart):
    for shift, keys in enumerate(keychart):
        for row, row_keys in enumerate(keys):
            for column, key in enumerate(row_keys):
                yield key, (shift, row, column)


KEYMAP = dict(_invert(KEYCHART))
