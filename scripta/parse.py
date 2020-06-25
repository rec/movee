import argparse


def parse(args=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('scripts', nargs='+', help=_SCRIPTS_HELP)
    p.add_argument('--columns', '-c', default=100, help=_COLUMNS_HELP)
    p.add_argument('--output', '-o', help=_OUTPUT_HELP)
    p.add_argument('--prompt', '-p', help=_PROMPT_HELP)
    p.add_argument('--rows', '-r', default=100, help=_ROWS_HELP)
    p.add_argument('--svg', '-s', default='', nargs='?', help=_SVG_HELP)
    p.add_argument('--template', '-t', default=TEMPLATE, help=_TEMPLATE_HELP)
    p.add_argument('--upload', '-u', action='store_true', help=_UPLOAD_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    return p.parse_args(args)


_DESCRIPTION = """Script bash and Python for asciinema"""

_SVG_HELP = """\
Render casts as SVG files if set.  If a value is given, it is the name of the
directory for SVG files."""

_COLUMNS_HELP = """Columns of the terminal in characters"""
_OUTPUT_HELP = """Directory for output cast files"""
_ROWS_HELP = """Rows of the terminal in characters"""
_PROMPT_HELP = """Set the main bash prompt"""
_SCRIPTS_HELP = """Scripts to run"""
_TEMPLATE_HELP = """Name of asciinema template"""
_UPLOAD_HELP = """Upload the cast file to asciinema.com"""
_VERBOSE_HELP = """Print more stuff"""

TEMPLATE = 'solarized_light'
