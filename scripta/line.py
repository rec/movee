from dataclasses import dataclass


@dataclass
class Line:
    time: float = 0
    io: str = 'o'
    chars: str = ''

    def to_list(self):
        return [self.time, self.io, self.chars]

    def offset(self, dt):
        return Line(self.time + dt, self.io, self.chars)
