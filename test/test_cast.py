from ascript.cast import Cast
from unittest import TestCase
import io


def _round_trip(cast):
    s = io.StringIO()
    cast.write(s)

    s.seek(0)
    cast2 = Cast.read(s)
    assert cast.lines == cast2.lines
    assert cast.header == cast2.header


class TestCast(TestCase):
    def test_empty(self):
        cast = Cast()
        _round_trip(cast)

    def test_simple(self):
        cast = Cast()
        cast.append('ls -cail', 1)
        _round_trip(cast)

    def test_extend(self):
        cast = Cast()
        cast.append('ls -cail', 1)
        cast.extend(cast, 2)
        cast.extend(cast, 4)
        _round_trip(cast)
        expected = [
            [1, 'o', 'ls -cail'],
            [4, 'o', 'ls -cail'],
            [9, 'o', 'ls -cail'],
            [12, 'o', 'ls -cail'],
        ]
        assert cast.lines == expected
