from scripta.cast import Cast, EPSILON
from unittest import TestCase
import io
from pathlib import Path

TEST_CAST_FILE = Path(__file__).parents[1] / 'data/recorded/git-copy.cast'


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

    def test_error(self):
        cast = Cast()
        cast.append('ls -cail', 1)
        with self.assertRaises(ValueError):
            cast.extend(cast, -2)
        with self.assertRaises(ValueError):
            cast.append('hello', -2)

    def test_epsilon(self):
        cast = Cast()
        cast.append('ls -cail', EPSILON / 2)
        assert cast.lines[0].time == 0

    def test_extend(self):
        cast1 = Cast()
        cast1.append('ls -cail', 1)
        cast = Cast()
        cast.extend(cast)
        assert not cast.lines

    def test_append_time_zero(self):
        cast = Cast()
        cast.append('ls -cail', 1)
        cast.append('', 2.5)
        cast.append(' frog', 0.5)

        _round_trip(cast)
        expected = [
            [1, 'o', 'ls -cail'],
            [4, 'o', ' frog'],
        ]
        assert [i.to_list() for i in cast.lines] == expected

    def test_scale(self):
        cast = Cast()
        cast.append('ls -cail', 1)
        cast.extend(cast, 2)
        cast.extend(cast, 4)
        cast.scale_by(2)
        expected = [
            [2, 'o', 'ls -cail'],
            [8, 'o', 'ls -cail'],
            [18, 'o', 'ls -cail'],
            [24, 'o', 'ls -cail'],
        ]
        assert [i.to_list() for i in cast.lines] == expected

    def test_keystroke_times(self):
        cast = Cast.read(open(TEST_CAST_FILE))
        actual = list(cast.keystroke_times())
        for t in actual:
            print('%s,' % round(t, 3))
        expected = []
        assert len(actual) == 48
        expected = [0.279, 0.177, 0.104, 0.248, 0.103, 0.08, 0.186, 0.224]
        assert [round(i, 3) for i in actual[:8]] == expected
