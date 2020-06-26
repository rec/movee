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
    source, target = scripts
    asyncio.run(CastRecorder(source).record_to(target))
