"""
Represents a single asciinema file for reading or writing
"""

from dataclasses import dataclass
import json

EPSILON = 0.001
HEADER = {'version': 2, 'width': 100, 'height': 40}


@dataclass
class Line:
    time: float = 0
    io: str = 'o'
    chars: str = ''

    def to_list(self):
        return [self.time, self.io, self.chars]

    def to_json(self):
        return

    def offset(self, dt):
        return Line(self.time + dt, self.io, self.chars)


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
            raise TypeError('%s has non-list' % lines)

        return cls([Line(*i) for i in lines], header)

    def append(self, keys, delta_time):
        time = self.lines[-1].time if self.lines else 0
        if delta_time < EPSILON:
            delta_time = 0
        self.lines.append(Line(time + delta_time, 'o', keys))

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

        lines = other.lines
        if other is self:
            lines = lines[:]
        for line in lines:
            self.lines.append(line.offset(offset))
