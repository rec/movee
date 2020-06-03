from ascript import util
from unittest import TestCase


def split_by(lines):
    return list(util.split_by(lines))


def split_script(lines):
    return list(util.split_script(lines))


def trailing(lines):
    return list(util.trailing_slash(lines))


class SplitCommentsTest(TestCase):
    def test_empty(self):
        assert split_by([]) == []

    def test_single_split_by(self):
        assert split_by('a') == [['a']]
        assert split_by('#') == [['#']]

    def test_simple(self):
        lines = 'a#a'
        actual = split_by(lines)
        expected = [[i] for i in lines]
        assert actual == expected

    def test_complex(self):
        lines = ' ## # X XX#X'
        actual = split_by(lines)
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


class SplitScriptTest(TestCase):
    def test_empty(self):
        assert split_script([]) == []

    def test_lines(self):
        actual = split_script(LINES)
        expected = [
            [['']],
            [
                [
                    '# Hello, and welcome to my code. \\',
                    'This is part of the comment.',
                ],
                ['# This is another comment'],
                [''],
            ],
            [
                ['for i in range(10000000):  # This is code!'],
                ['    print(i)  \\', '# print statement'],
                [''],
            ],
            [['# a new comment']],
        ]
        assert actual == expected


LINES = """
# Hello, and welcome to my code. \\
This is part of the comment.
# This is another comment

for i in range(10000000):  # This is code!
    print(i)  \\
# print statement

# a new comment
""".splitlines()
