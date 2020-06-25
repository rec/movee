import os

COLORS = {
    'black': '\x1b[0;30m',
    'red': '\x1b[0;31m',
    'green': '\x1b[0;32m',
    'brown': '\x1b[0;33m',
    'blue': '\x1b[0;34m',
    'purple': '\x1b[0;35m',
    'cyan': '\x1b[0;36m',
    'light_gray': '\x1b[0;37m',
    'dark_gray': '\x1b[1;30m',
    'light_red': '\x1b[1;31m',
    'light_green': '\x1b[1;32m',
    'yellow': '\x1b[1;33m',
    'light_blue': '\x1b[1;34m',
    'light_purple': '\x1b[1;35m',
    'light_cyan': '\x1b[1;36m',
    'white': '\x1b[1;37m',
    'no_color': '\x1b[0m',
}

DEFAULT_PROMPT = '▶ {blue}{USER}{red}:{green}{CWD}{no_color}$ '


def expand(prompt=DEFAULT_PROMPT, **kwds):
    env = dict(COLORS, CWD=os.getcwd(), **os.environ)
    env.update(**kwds)
    return prompt.format(**env)
