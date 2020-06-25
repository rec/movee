from scripta import __main__
from unittest import TestCase


class MainTest(TestCase):
    def test_main(self):
        actual = vars(__main__.parse(['foo']))
        expected = {
            'columns': 100,
            'output': None,
            'rows': 100,
            'scripts': ['foo'],
            'svg': '',
            'template': 'solarized_light',
            'upload': False,
            'verbose': False,
        }
        assert actual == expected
