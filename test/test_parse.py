from scripta import parse
from unittest import TestCase


class ParseTest(TestCase):
    def test_parse(self):
        actual = vars(parse.parse(['foo']))
        expected = {
            'dry_run': False,
            'errors': None,
            'height': None,
            'keys': None,
            'output': None,
            'prompt': None,
            'sources': ['foo'],
            'svg': '',
            'theme': None,
            'times': None,
            'upload': False,
            'verbose': False,
            'width': None,
        }
        assert actual == expected
