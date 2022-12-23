from movee import cast_recorder
from movee import movee
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
import asyncio
import tdir


class CastRecorder(cast_recorder.CastRecorder):
    async def record_to(self, cast_file, cast):
        await asyncio.sleep(0)


class TestMovee(IsolatedAsyncioTestCase):
    @patch('movee.movee.CastRecorder', side_effect=CastRecorder)
    async def NO_test_movee(self):
        with tdir():
            await movee.movee()
