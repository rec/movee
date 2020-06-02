import hashlib
from . import colors

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
PROMPT = PROMPT.format(**vars(colors))

BACKSPACE = '\x08\x1b[K'
RETURN = '\r\n'
CONTROL_L = '\x1b[H\x1b[2J'


def stable_hash(s):
    return hashlib.blake2s(s.encode()).hexdigest()
