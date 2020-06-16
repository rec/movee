from ascript.cast_recorder import CastRecorder
from ascript.typing_errors import ErrorMaker
from unittest import TestCase

# from ascript.keystrokes import DEFAULT_K

ERRORS = ErrorMaker(0.1, 0.1, 0.1)
# RECORDER = CastRecorder()


class TestCastReorder(TestCase):
    def test_empty(self):
        assert CastRecorder
