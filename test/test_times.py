from scripta.times import KeyTimes
from unittest import TestCase


class TestTimes(TestCase):
    def test_read(self):
        assert KeyTimes().to_read(12) == 1.12

    def test_write(self):
        phrase = 'Sphinx'
        actual = [(c, round(t, 3)) for c, t in KeyTimes().to_type(phrase)]
        expected = [
            ('', 2),
            ('S', 0.024),
            ('p', 0.061),
            ('h', 0.035),
            ('i', 0.053),
            ('n', 0.075),
            ('x', 0.109),
            ('', 2),
        ]
        for a in actual:
            print('    %s,' % str(a))
        assert actual == expected
