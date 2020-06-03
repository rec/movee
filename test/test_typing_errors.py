from ascript.typing_errors import ErrorMaker
from unittest import TestCase
from ascript import constants


class ErrorAdderTest(TestCase):
    def test_empty(self):
        before = 'some long complicated string etc'
        after = ''.join(ErrorMaker()(before))
        assert before == after

    def test_complete(self):
        before = 'word'
        after = ''.join(ErrorMaker(1, 1, 1)(before))
        actual = after.split(constants.BACKSPACE)
        expected = ['D', 'w:', 'o#', 'rW', 'd']
        assert actual == expected

    def test_tiny(self):
        before = 'a much longer sentence with errors'
        after = ErrorMaker(0.03, 0.08, 0.09)(before)
        actual = ''.join(after).split(constants.BACKSPACE)
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
