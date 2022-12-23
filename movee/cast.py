"""
Represents a single asciinema file for reading or writing
"""

from . import constants
from .line import Line
import json
import safer

EPSILON = 0.001
HEADER = {'version': 2, 'width': 100, 'height': 40}
COMPOUND_KEYS = {constants.BACKSPACE, constants.RETURN}


class Cast:
    def __init__(self, lines=None, **kwargs):
        self.header = dict(HEADER, **kwargs)
        self.lines = lines or []

    @classmethod
    def read(cls, fp):
        if isinstance(fp, str):
            with open(fp) as fp2:
                return cls.read(fp2)

        header, *lines = (json.loads(i) for i in fp)
        return cls([Line(*i) for i in lines], **header)

    @property
    def duration(self):
        return self.lines[-1].time if self.lines else 0

    def append(self, chars, delta_time):
        if delta_time < 0:
            raise ValueError('delta_time < 0')
        if delta_time < EPSILON:
            delta_time = 0
        line = Line(self.duration + delta_time, 'o', chars)
        if self.lines and not self.lines[-1].chars:
            self.lines[-1] = line
        else:
            self.lines.append(line)

    def write(self, fp):
        if isinstance(fp, str):
            with safer.open(fp, 'w') as fp2:
                return self.write(fp2)
        print(json.dumps(self.header), file=fp)
        for line in self.lines:
            print(json.dumps(line.to_list()), file=fp)

    def scale_by(self, ratio):
        for line in self.lines:
            line.time *= ratio

    def extend(self, other, offset=0):
        if offset < 0:
            raise ValueError('offset < 0')
        for c in 'width', 'height':
            s = self.header.get(c, 0)
            o = other.header.get(c, 0)
            self.header[c] = max(s, o)

        if self.lines:
            offset += self.lines[-1].time

        lines = other.lines
        lines = lines[:] if lines is self.lines else lines
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
