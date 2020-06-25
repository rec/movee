from .travis import skip_if_travis
from scripta import run
import asyncio
import unittest


def bash(*commands, kill_after=1, use_strings=False, **kwds):
    results = []

    def callback(symbol, line):
        results.append([symbol, line])

    b = run.bash
    if not use_strings:
        b = run.Runner(b.execute.split(), b.set_prompts, b.exit)

    asyncio.run(b(callback, commands, kill_after=kill_after, **kwds))
    return results


@skip_if_travis
class TestRun(unittest.TestCase):
    def test_empty(self):
        # Doesn't work on Travis.  Had an intermittent failure but fixed

        for shell in False, True:
            actual = bash(shell=shell)
            expected = [['P', '1']]
            assert actual == expected

    def test_simple_run(self):
        for shell in False, True:
            for use_strings in False, True:
                args = '', '# cm', 'echo TEST', '# cm 2'
                actual = bash(*args, shell=shell, use_strings=use_strings)
                print(*actual)
                expected = [
                    ['P', '1'],
                    ['I', ''],
                    ['I', '# cm'],
                    ['I', 'echo TEST'],
                    ['O', 'TEST'],
                    ['P', '1'],
                    ['I', '# cm 2'],
                ]
                assert actual == expected

    def DONT_test_kill_after(self):
        # Freezes!
        for shell in False, True:
            actual = bash('sleep 0.5', 'echo NO', shell=shell, kill_after=0.2)
            expected = []
            assert actual == expected
