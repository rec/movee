"""
Takes a text and then adds a certain percentage of typing errors to it
using a crude model based on the layout of a standard keyboard.
"""
from . import constants
from .stable_hash import stable_hash
from dataclasses import dataclass
import random

KEYCHART = [
    ['`1234567890-=', ' qwertyuiop[]\\', ' asdfghjkl;\'', ' zxcvbnm,./'],
    ['~!@#$%^&*()_+', ' QWERTYUIOP{}|', ' ASDFGHJKL:"', ' ZXCVBNM<>?'],
]


@dataclass
class ErrorMaker:
    row: float = 0.03
    column: float = 0.03
    shift: float = 0.02

    def __call__(self, line):
        rstate = random.getstate()
        random.seed(stable_hash(line))

        try:
            for key in line:
                yield from self._error(key)
                yield key
        finally:
            random.setstate(rstate)

    def _error(self, key):
        try:
            shift, row, column = KEYMAP[key]

            if random.random() < self.shift:
                shift = 1 - shift
            if random.random() < self.row:
                row += -1 + 2 * (random.random() < 0.5)
            if random.random() < self.column:
                column += -1 + 2 * (random.random() < 0.5)

            new_key = KEYCHART[shift][row][column]
            if new_key != key and new_key != ' ':
                yield new_key
                yield constants.BACKSPACE
        except (IndexError, KeyError):
            pass


def _invert(keychart):
    for shift, keys in enumerate(keychart):
        for row, row_keys in enumerate(keys):
            for column, key in enumerate(row_keys):
                yield key, (shift, row, column)


KEYMAP = dict(_invert(KEYCHART))
