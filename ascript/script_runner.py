from .cast_recorder import CastRecorder
from . import colors
from . import constants
from . import run

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
PROMPT = PROMPT.format(**vars(colors))


def run_script(script, timing, prompt, errors):
    is_python = script.endswith('.py')
    if not (is_python or script.endswith('.sh')):
        raise ValueError('Do not understand script %s' % script)

    rec = CastRecorder()
    rec.add(constants.CONTROL_L, prompt)

    def callback(event, line):
        if event is run.KILL:
            pass
        elif event is run.IN:
            rec.add_keys(line)
        elif event is run.PROMPT:
            if line.startswith('1'):
                rec.add_line('>>> ' if is_python else prompt)
            elif line.startwith('2'):
                rec.add_line('... ' if is_python else '> ')
            else:
                assert False, line
        else:
            assert event in run.OUT, run.err
            rec.add_line(line.rstrip('\n'))

    runner = run.python if is_python else run.bash
    runner(callback, open(script))

    return rec


if __name__ == '__main__':
    pass
