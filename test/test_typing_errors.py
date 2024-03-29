from movee import constants
from movee.typing_errors import ErrorMaker
from unittest import TestCase


class ErrorAdderTest(TestCase):
    def test_empty(self):
        before = 'some long complicated string etc'
        after = ''.join(ErrorMaker(0, 0, 0)(before))
        assert before == after

    def test_complete(self):
        before = 'word'
        after = ''.join(ErrorMaker(1, 1, 1)(before))
        actual = after.split(constants.BACKSPACE)
        expected = ['D', 'w:', 'o#', 'rW', 'd']
        assert actual == expected

    def test_longer(self):
        before = 'a much longer sentence with errors'
        after = ErrorMaker(0.08, 0.09, 0.03)(before)
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

    def test_longer_2(self):
        before = 'a very very very much longer sentence with errors'
        after = []
        delete = False
        for ch in ErrorMaker(1, 1, 1)(before):
            if ch == constants.BACKSPACE:
                delete = True
            else:
                if delete:
                    delete = False
                else:
                    after.append(ch)

        assert len(before) == len(after)
        same = [i for i, j in zip(before, after) if i == j]
        assert len(same) == 9
