from ascript.typing_errors import ErrorAdder
from unittest import TestCase
from ascript import constants


class ErrorAdderTest(TestCase):
    def test_empty(self):
        before = 'some long complicated string etc'
        after = ''.join(ErrorAdder()(before))
        assert before == after

    def test_complete(self):
        before = 'word'
        ea = ErrorAdder(1, 1, 1)
        actual = ''.join(ea(before)).split(constants.BACKSPACE)
        expected = ['D', 'w:', 'o#', 'rW', 'd']
        assert actual == expected

    def test_tiny(self):
        before = 'a much longer sentence with errors'
        ea = ErrorAdder(0.03, 0.08, 0.09)
        actual = ''.join(ea(before)).split(constants.BACKSPACE)
        expected = [
            'a much longr',
            'et',
            'r sem',
            'ntence wir',
            'tH',
            'h errorS',
            's',
        ]
        assert actual == expected
