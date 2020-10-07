from scripta import cast_recorder
from scripta import scripta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
import asyncio
import tdir


class CastRecorder(cast_recorder.CastRecorder):
    async def record_to(self, cast_file, cast):
        await asyncio.sleep(0)


class TestScripta(IsolatedAsyncioTestCase):
    @patch('scripta.scripta.CastRecorder', side_effect=CastRecorder)
    async def NO_test_scripta(self):
        with tdir():
            await scripta.scripta()
