from .cast import Cast
from .cast_recorder import CastRecorder
from argparse import Namespace
import asyncio
import sys
import traceback
import yaml

# from .typing_errors import ErrorMaker
# from pathlib import Path
# import termtosvg.config


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
    return result


async def _one_script(config, source):
    rec = CastRecorder(source, config.errors, config.keys, config.prompt)
    cast = Cast(width=config.width, height=config.height)
    if config.cast:
        cast_file = config.cast
    else:
        pass

    if config.svg:
        pass
    if config.upload:
        pass
    return rec, cast, cast_file
