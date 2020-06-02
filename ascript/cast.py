"""
Represents a single asciinema file for reading or writing
"""

from .line import Line
from . import constants
import json

EPSILON = 0.001
HEADER = {'version': 2, 'width': 100, 'height': 40}
COMPOUND_KEYS = {constants.BACKSPACE, constants.RETURN}


class Cast:
    def __init__(self, lines=None, header=None):
        self.lines = lines or []
        self.header = header or HEADER

    @classmethod
    def read(cls, fp):
        header, *lines = (json.loads(i) for i in fp)
        if not isinstance(header, dict):
            raise TypeError('%s is not a dict' % header)

        if not all(isinstance(i, list) for i in lines):
            raise TypeError('%s contains non-list' % lines)

        return cls([Line(*i) for i in lines], header)

    @property
    def length(self):
        return self.lines[-1].time if self.lines else 0

    def append(self, chars, delta_time):
        if delta_time < 0:
            raise ValueError('delta_time < 0')
        if delta_time < EPSILON:
            delta_time = 0
        self.lines.append(Line(self.length + delta_time, 'o', chars))

    def write(self, fp):
        print(json.dumps(self.header), file=fp)
        for line in self.lines:
            print(json.dumps(line.to_list()), file=fp)

    def scale_by(self, ratio):
        for line in self.lines:
            line.time *= ratio

    def extend(self, other, offset=0):
        for c in 'width', 'height':
            s = self.header.get(c, 0)
            o = other.header.get(c, 0)
            m = max(s, o)
            if m > 0:
                self.header[c] = m

        if self.lines:
            offset += self.lines[-1].time

        # A little more code to avoid doom if other.lines is self.lines
        lines = (other.lines[i] for i in range(len(other.lines)))
        self.lines.extend(i.offset(offset) for i in lines)

    def keystroke_times(self):
        time = None
        for line in self.lines:
            if len(line.chars) == 1 or line.chars in COMPOUND_KEYS:
                if time is not None:
                    yield line.time - time
                time = line.time
            else:
                time = None
