import hashlib
from . import colors

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
PROMPT = PROMPT.format(**vars(colors))

BACKSPACE = '\x08\x1b[K'
RETURN = '\r\n'
CONTROL_L = '\x1b[H\x1b[2J'

MAX_KEYSTROKE_TIME = 0.7
KEYSTROKE_TIME_SCALE = 0.32
TIME_TO_THINK = 1
TIME_AT_END = 5
TIME_TO_READ_ONE_CHAR = 0.005
TYPING_ERROR_RATE = 0.06


def stable_hash(s):
    return hashlib.blake2s(s.encode()).hexdigest()
