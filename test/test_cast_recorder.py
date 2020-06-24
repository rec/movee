from ascript.cast_recorder import CastRecorder, BASH_PS
from ascript.cast import Cast
from ascript import constants
from unittest import IsolatedAsyncioTestCase
from .travis import skip_if_travis
import os
import tdir


@skip_if_travis
class TestCastRecorder(IsolatedAsyncioTestCase):
    async def test_empty(self):
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
