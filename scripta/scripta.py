from .cast_recorder import CastRecorder
import asyncio


def scripta(
    scripts,
    columns,
    errors,
    key,
    output,
    prompt,
    rows,
    svg,
    theme,
    times,
    upload,
    verbose,
):
    asyncio.run(CastRecorder().record_to(*scripts))
