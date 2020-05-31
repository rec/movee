"""
Represents a single asciinema file for reading or writing
"""

from . import constants
import json

EPSILON = 0.001


class Cast:
    def __init__(self, lines=None, header=None):
        self.lines = lines or []
        self.header = header or constants.HEADER

    @classmethod
    def read(cls, fp):
        lines = []

        first = True
        for line in fp:
            value = json.loads(line)
            if first:
                if not isinstance(value, dict):
                    raise TypeError('%s is not a dict' % value)
                header = value
                first = False
            else:
                if not isinstance(value, list):
                    raise TypeError('%s is not list dict' % value)
                lines.append(value)

        return cls(lines, header)

    def append(self, keys, delta_time):
        dt = 0 if delta_time < EPSILON else delta_time
        self.lines.append([dt, 'o', keys])

    def write(self, fp):
        for i in (self.header, *self.lines):
            print(json.dumps(i), file=fp)

    def scale_by(self, ratio):
        for line in self.lines:
            line[0] *= ratio

    def extend(self, other, offset=0):
        for c in 'width', 'height':
            s = self.header.get(c, 0)
            o = other.header.get(c, 0)
            m = max(s, o)
            if m > 0:
                self.header[c] = m

        if self.lines:
            offset += self.lines[-1][0]

        lines = other.lines[:] if other is self else other.lines
        self.lines.extend([t + offset, i, k] for t, i, k in lines)
