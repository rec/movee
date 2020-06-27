from scripta import parse
from unittest import TestCase


class ParseTest(TestCase):
    def test_parse(self):
        actual = vars(parse.parse(['foo']))
        expected = {
            'width': None,
            'errors': None,
            'keys': None,
            'output': None,
            'prompt': None,
            'height': None,
            'sources': ['foo'],
            'svg': '',
            'theme': None,
            'times': None,
            'upload': False,
            'verbose': False,
        }
        assert actual == expected
