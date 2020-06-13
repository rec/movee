from .travis import skip_if_travis
from ascript import run
import asyncio
import unittest


def bash(*commands, kill_after=1, **kwds):
    results = []

    def callback(symbol, line):
        results.append([symbol, line])

    asyncio.run(run.bash(callback, commands, kill_after=kill_after, **kwds))
    return results


@skip_if_travis
class TestRun(unittest.TestCase):
    def test_empty(self):
        for shell in False, True:
            actual = bash(shell=shell)
            expected = [['P', '1']]
            # TODO: oh, dear, this test failed ONCE intermittently and not
            # again in twenty tests.  The issue was that it once captured the
            # final ('I', 'exit') command, so there's a race condition.
            # Let's see what Travis says.  UPDATE: doesn't work on Travis

            assert actual == expected

    def test_simple_run(self):
        for shell in False, True:
            actual = bash('echo TEST', shell=shell)
            expected = [
                ['P', '1'],
                ['I', 'echo TEST'],
                ['O', 'TEST'],
                ['P', '1'],
            ]
            assert actual == expected
