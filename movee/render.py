from termtosvg import anim
from termtosvg import asciicast
from termtosvg import config
from termtosvg import term

DEFAULT_THEME = 'solarized_light'


def render_file(cast_file, svg_file, theme=None):
    asciicast_records = asciicast.read_records(str(cast_file))
    geometry, frames = term.timed_frames(asciicast_records)

    tmpl = config.default_templates()[theme or DEFAULT_THEME]
    anim.render_animation(frames, geometry, str(svg_file), tmpl)
