from pathlib import Path
from termtosvg import anim
from termtosvg import asciicast
from termtosvg import config
from termtosvg import term
import tempfile

TEMPLATE = 'solarized_light'


def render(cast, svg_file, template=TEMPLATE):
    with tempfile.TemporaryDirectory() as td:
        cast_file = Path(td) / 'file.cast'
        cast.write(cast_file)
        _render_file(cast_file, svg_file, template)


def _render_file(cast_file, svg_file, template):
    asciicast_records = asciicast.read_records(str(cast_file))
    geometry, frames = term.timed_frames(asciicast_records)

    tmpl = config.default_templates()[template]
    anim.render_animation(frames, geometry, str(svg_file), tmpl)
