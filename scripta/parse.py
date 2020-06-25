import argparse


def _parser():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('scripts', nargs='+', help=_SCRIPTS_HELP)
    p.add_argument('--columns', '-c', help=_COLUMNS_HELP)
    p.add_argument('--errors', '-e', help=_ERRORS_HELP)
    p.add_argument('--keys', '-k', help=_KEYS_HELP)
    p.add_argument('--output', '-o', help=_OUTPUT_HELP)
    p.add_argument('--prompt', '-p', help=_PROMPT_HELP)
    p.add_argument('--rows', '-r', help=_ROWS_HELP)
    p.add_argument('--svg', '-s', default='', nargs='?', help=_SVG_HELP)
    p.add_argument('--theme', '-m', help=_THEME_HELP)
    p.add_argument('--times', '-t', help=_TIMES_HELP)
    p.add_argument('--upload', '-u', action='store_true', help=_UPLOAD_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    return p


_DESCRIPTION = """Script bash and Python for asciinema"""

_SVG_HELP = """\
Render casts as SVG files if set.  If a value is given, it is the name of the
directory for SVG files."""

_COLUMNS_HELP = """Columns of the terminal in characters"""
_ERRORS_HELP = """Set error parameters"""
_KEYS_HELP = """A list of cast files from which to get key timing"""
_OUTPUT_HELP = """Directory for output cast files"""
_PROMPT_HELP = """Set the main bash prompt"""
_ROWS_HELP = """Rows of the terminal in characters"""
_SCRIPTS_HELP = """Scripts to run"""
_THEME_HELP = """Name of asciinema theme"""
_TIMES_HELP = """Set timing parameters"""
_UPLOAD_HELP = """Upload the cast file to asciinema.com"""
_VERBOSE_HELP = """Print more stuff"""


PARSER = _parser()
parse = PARSER.parse_args
