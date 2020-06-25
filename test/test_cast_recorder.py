from scripta.cast_recorder import CastRecorder, BASH_PS
from scripta.cast import Cast
from scripta import constants
from unittest import IsolatedAsyncioTestCase
from .travis import skip_if_travis
import os
import tdir


@skip_if_travis
class TestCastRecorder(IsolatedAsyncioTestCase):
    async def test_bash(self):
        with tdir.tdir({'test.sh': 'echo HELLO\npwd\n'}):
            await CastRecorder().record_to('test.sh', 'test.cast')
            actual = [i.chars for i in Cast.read('test.cast').lines]
            expected = [
                constants.CONTROL_L,
                BASH_PS[0],
                '3',
                constants.BACKSPACE,
                'e',
                'c',
                'h',
                'o',
                ' ',
                'N',
                constants.BACKSPACE,
                'H',
                'E',
                'l',
                constants.BACKSPACE,
                'L',
                'L',
                'O',
                '\r\n',
                'HELLO\r\n',
                BASH_PS[0],
                'p',
                'w',
                'd',
                '\r\n',
                os.getcwd() + '\r\n',
                BASH_PS[0],
            ]
            if actual != expected:
                print(*actual, sep='\n')
            assert actual == expected

    async def test_record_python(self):
        with tdir.tdir({'test.py': TEST_PY}):
            await CastRecorder().record_to('test.py', 'test.cast')
            actual = [i.chars for i in Cast.read('test.cast').lines]
            expected = [
                '\x1b[H\x1b[2J',
                '>>> ',
                '\r\n',
                'p',
                'r',
                'i',
                'n',
                't',
                '9',
                constants.BACKSPACE,
                '(',
                "'",
                'h',
                'e',
                'l',
                'l',
                'o',
                "'",
                '0',
                constants.BACKSPACE,
                ')',
                '\r\n',
                'hello\r\n',
                '>>> ',
                'i',
                'm',
                'p',
                'o',
                'r',
                'T',
                constants.BACKSPACE,
                't',
                ' ',
                'o',
                's',
                '\r\n',
                '>>> ',
                'O',
                constants.BACKSPACE,
                'o',
                's',
                '.',
                'g',
                'e',
                't',
                'c',
                's',
                constants.BACKSPACE,
                'w',
                'd',
                '(',
                ')',
                '\r\n',
                "'%s'\r\n" % os.getcwd(),
                '>>> ',
            ]
            if actual != expected:
                print(*actual, sep='\n')
            assert actual == expected

    async def test_error(self):
        with self.assertRaises(ValueError) as m:
            await CastRecorder().record_to('test.xx', 'test.cast')
        assert m.exception.args[0] == 'Do not understand script test.xx'


TEST_PY = """
print('hello')
import os
os.getcwd()
"""
