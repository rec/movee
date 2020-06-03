from ascript import util
from unittest import TestCase


def split(lines):
    return list(util.split_comments(lines))


def trailing(lines):
    return list(util.trailing_slash(lines))


class SplitCommentsTest(TestCase):
    def test_empty(self):
        assert split([]) == []

    def test_single_split(self):
        assert split('a') == [['a']]
        assert split('#') == [['#']]

    def test_simple(self):
        lines = 'a#a'
        actual = split(lines)
        expected = [[i] for i in lines]
        assert actual == expected

    def test_complex(self):
        lines = ' ## # X XX#X'
        actual = split(lines)
        expected = [
            [' '],
            ['#', '#', ' ', '#', ' '],
            ['X', ' ', 'X', 'X'],
            ['#'],
            ['X'],
        ]
        assert actual == expected


class TrailingSlashTest(TestCase):
    def test_empty(self):
        assert trailing([]) == []

    def test_no_trailing(self):
        assert trailing('a') == [['a']]
        assert trailing('abc') == [['a'], ['b'], ['c']]

    def test_simple(self):
        lines = ['a', 'b\\', 'c\\', 'd', 'e']
        actual = trailing(lines)
        expected = [['a'], ['b\\', 'c\\', 'd'], ['e']]
        assert actual == expected

    def test_edge(self):
        lines = ['a', 'b\\', 'c\\']
        actual = trailing(lines)
        expected = [['a'], ['b\\', 'c\\']]
        assert actual == expected
