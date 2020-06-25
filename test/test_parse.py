from scripta import parse
from unittest import TestCase


class MainTest(TestCase):
    def test_main(self):
        actual = vars(parse.parse(['foo']))
        expected = {
            'columns': 100,
            'output': None,
            'prompt': None,
            'rows': 100,
            'scripts': ['foo'],
            'svg': '',
            'template': 'solarized_light',
            'upload': False,
            'verbose': False,
        }
        assert actual == expected
