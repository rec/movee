import argparse


def _parser():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('sources', nargs='+', help=_SOURCES_HELP)

    p.add_argument('--cast', '-c', help=_CAST_HELP)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_HELP)
    p.add_argument('--errors', '-e', help=_ERRORS_HELP)
    p.add_argument('--height', '-i', help=_HEIGHT_HELP)
    p.add_argument('--keys', '-k', help=_KEYS_HELP)
    p.add_argument('--prompt', '-p', help=_PROMPT_HELP)
    p.add_argument(
        '--quit_on_error', '-q', action='store_true', help=_QUIT_ON_ERROR_HELP
    )
    p.add_argument('--svg', '-s', default='', nargs='?', help=_SVG_HELP)
    p.add_argument('--theme', '-m', help=_THEME_HELP)
    p.add_argument('--times', '-t', help=_TIMES_HELP)
    p.add_argument('--upload', '-u', action='store_true', help=_UPLOAD_HELP)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_HELP)
    p.add_argument('--width', '-w', help=_WIDTH_HELP)

    return p


_DESCRIPTION = """Script bash and Python for asciinema"""

_SVG_HELP = """\
Render casts as SVG files if set.  If a value is given, it is the name of the
directory for SVG files."""

_WIDTH_HELP = """Width of the terminal in characters"""
_DRY_RUN_HELP = """Do not run, dump config file to stdout"""
_ERRORS_HELP = """Set error parameters"""
_KEYS_HELP = """A list of cast files from which to get key timing"""
_CAST_HELP = """Directory for cast files"""
_PROMPT_HELP = """Set the main bash prompt"""
_HEIGHT_HELP = """Height of the terminal in characters"""
_SOURCES_HELP = """Sources to run, either config files or scripts"""
_THEME_HELP = """Name of asciinema theme"""
_TIMES_HELP = """Set timing parameters"""
_QUIT_ON_ERROR_HELP = """Quit immediately if there is an error"""
_UPLOAD_HELP = """Upload the cast file to asciinema.com"""
_VERBOSE_HELP = """Print more stuff"""


PARSER = _parser()
parse = PARSER.parse_args
