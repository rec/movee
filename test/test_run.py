from ascript import run
import asyncio
import os
import unittest


def bash(*commands, kill_after=1):
    results = []

    def callback(symbol, line):
        results.append([symbol, line])

    asyncio.run(run.bash(callback, *commands, kill_after=kill_after))
    return results


@unittest.skipIf(
    os.getenv('TRAVIS', '').lower().startswith('t'),
    'Run tests do not work in travis :-(',
)
class TestRun(unittest.TestCase):
    def test_empty(self):
        actual = bash()
        expected = [['P', '1']]
        # TODO: oh, dear, this test failed ONCE intermittently and not
        # again in twenty tests.  The issue was that it once captured the
        # final ('I', 'exit') command, so there's a race condition in there.
        # Let's see what Travis says.

        assert actual == expected

    def test_simple_run(self):
        actual = bash('echo TEST')
        expected = [
            ['P', '1'],
            ['I', 'echo TEST'],
            ['O', 'TEST'],
            ['P', '1'],
        ]
        assert actual == expected
