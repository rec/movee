from .cast_recorder import CastRecorder
import asyncio


def scripta(
    scripts, columns, output, prompt, rows, svg, template, upload, verbose
):
    asyncio.run(CastRecorder().record_to(*scripts))
