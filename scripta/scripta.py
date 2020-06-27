from .cast_recorder import CastRecorder
import asyncio


def scripta(
    errors,
    height,
    key,
    output,
    prompt,
    sources,
    svg,
    theme,
    times,
    upload,
    verbose,
    width,
):
    source, target = sources
    asyncio.run(CastRecorder(source).record_to(target))
