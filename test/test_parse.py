from .test_config import EMPTY
from movee import parse
from unittest import TestCase


class ParseTest(TestCase):
    def test_parse(self):
        actual = vars(parse.parse(['foo']))
        expected = dict(EMPTY, sources=['foo'], svg='')
        assert actual == expected
