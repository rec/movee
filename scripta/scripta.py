from . import render
from . import upload
from .cast import Cast
from .cast_recorder import CastRecorder
from argparse import Namespace
from pathlib import Path
import asyncio
import sys
import traceback
import yaml


def scripta(*, dry_run=False, **config):
    if dry_run:
        yaml.safe_dump(config, sys.stdout)
        return

    return asyncio.run(_scripta(Namespace(config)))


async def _scripta(config):
    result = 0

    for source in config.sources:
        try:
            await _one_script(config, source)
        except Exception as e:
            if config.verbose:
                traceback.print_exc()
            print(f'ERROR: {e}', file=sys.stderr)
            result = -1
            if config.quit_on_error:
                break

    return result


async def _one_script(config, source):
    rec = CastRecorder(source, config.errors, config.keys, config.prompt)
    cast = Cast(width=config.width, height=config.height)

    cast_file = source.with_suffix(source.suffix + '.cast')
    if config.cast:
        cast_file = Path(config.cast) / cast_file.name

    await rec.record_to(cast_file, cast)

    if config.svg is not None:
        svg_file = cast_file.with_suffix(source.suffix + '.svg')
        if config.svg:
            svg_file = Path(config.svg) / svg_file.name
        render.render_file(cast_file, svg_file, config.theme)
    if config.upload:
        upload.upload(cast_file)
