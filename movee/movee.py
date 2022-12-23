from . import config
from . import parse
from . import render
from . import upload
from . import validate
from .cast import Cast
from .cast_recorder import CastRecorder
from pathlib import Path
import sys
import traceback
import yaml


async def movee(args=None):
    await _movee(**validated_config(args))


def validated_config(args=None, **kwargs):
    flags = vars(parse.parse(args))
    flags.update(kwargs)
    cfg = config.read_config(flags)
    validate.validate(cfg)
    return cfg


async def _movee(*, sources, dry_run, verbose, **config):
    if dry_run:
        yaml.safe_dump(config, sys.stdout)
        return 0

    result = 0
    for source in sources:
        try:
            await _once(source, **config)
        except Exception as e:
            if verbose:
                traceback.print_exc()
            print(f'ERROR: {e}', file=sys.stderr)
            result = -1
            if config['quit_on_error']:
                break

    return result


async def _once(
    source, *, errors, keys, prompts, width, height, cast, svg, theme, prompt
):
    rec = CastRecorder(source, errors, keys, prompt)
    cast_file = source.with_suffix(source.suffix + '.cast')
    if config.cast:
        cast_file = Path(cast) / cast_file.name

    await rec.record_to(cast_file, Cast(width=width, height=height))

    if svg is not None:
        svg_file = cast_file.with_suffix(source.suffix + '.svg')
        if svg:
            svg_file = Path(svg) / svg_file.name
        render.render_file(cast_file, svg_file, theme)

    if upload:
        upload.upload(cast_file)
