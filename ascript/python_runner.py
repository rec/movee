import getopt

NON_REPL_FLAGS = {'-h', '-? ', '--help', '-m', '-V', '--version'}

SHORTOPTS = 'BdEhim:OORQ:sStuvVW:x3?c:'
LONGOPTS = ['version']


def enters_repl(sys_args):
    options, args = getopt.getopt(sys_args, SHORTOPTS, LONGOPTS)
    options = {o for o, v in options}
    if not (NON_REPL_FLAGS & options):
        return '-i' in options or not args or args[0] == '-'


"""
    python [ -B ] [ -d ] [ -E ] [ -h ] [ -i ] [ -m module-name ]
              [ -O ] [ -OO ] [ -R ] [ -Q argument ] [ -s ] [ -S ] [ -t ] [ -u ]
              [ -v ] [ -V ] [ -W argument ] [ -x ] [ -3 ] [ -?  ]
              [ -c command | script | - ] [ arguments ]
"""
