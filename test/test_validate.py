from scripta import parse
from scripta import validate
from unittest import TestCase


class ValidateTest(TestCase):
    def test_empty(self):
        flags = vars(parse.parse('s.py'.split()))
        validate.validate(flags)
