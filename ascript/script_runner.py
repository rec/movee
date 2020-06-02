from .cast_recorder import CastRecorder
from . import colors
from . import constants
from . import typing_errors
import sproc
import sys

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
PROMPT = PROMPT.format(**vars(colors))


def run_script(script, timing, prompt):
    rec = CastRecorder()
    rec.start()
    rec.add(constants.CONTROL_L, constants.PROMPT)

    lines = list(script.open())

    for i, line in enumerate(lines):
        _run_one(i, line)

    rec.wait(timing.time_at_end)
    return rec.cast


def _run_one(self, i, line):
    self.rec.hash_line(line)
    for k in typing_errors.with_errors(line):
        self.rec.add_key(constants.RETURN if k == '\n' else k)

    lines = self.rec.cast.lines
    before = len(lines)
    for li in line.split('&&'):
        if not self._run(li.strip()):
            break
    chars = sum(len(x[2]) for x in lines[before + 1 :])

    if not (
        i < len(self.lines) - 1
        and line.strip().startswith('#')
        and self.lines[i + 1].strip().startswith('#')
    ):
        self.rec.add(constants.RETURN)
        self.rec.add(PROMPT)
        t = constants.TIME_TO_THINK + chars * constants.TIME_TO_READ_ONE_CHAR
        self.rec.wait(t)


def _run(self, cmd):
    try:
        sproc.sproc(cmd, self.rec.add_line, shell=True)
        return True
    except Exception:
        return


class ScriptRunner(CastRecorder):
    def start(self, script, timing):
        self.rec.start()
        self.rec.add(constants.CONTROL_L, constants.PROMPT)

        self.lines = list(i for i in script.open() if i.strip())

        for i, line in enumerate(self.lines):
            self._run_one(i, line)

        self.rec.wait(timing.time_at_end)
        return self.rec.cast

    def _run_one(self, i, line):
        self.rec.hash_line(line)
        for k in typing_errors.with_errors(line):
            self.rec.add_key(constants.RETURN if k == '\n' else k)

        lines = self.rec.cast.lines
        before = len(lines)
        for li in line.split('&&'):
            if not self._run(li.strip()):
                break
        chars = sum(len(x[2]) for x in lines[before + 1 :])

        if not (
            i < len(self.lines) - 1
            and line.strip().startswith('#')
            and self.lines[i + 1].strip().startswith('#')
        ):
            self.rec.add(constants.RETURN)
            self.rec.add(PROMPT)
            t = (
                constants.TIME_TO_THINK
                + chars * constants.TIME_TO_READ_ONE_CHAR
            )
            self.rec.wait(t)

    def _run(self, cmd):
        try:
            sproc.sproc(cmd, self.rec.add_line, shell=True)
            return True
        except Exception:
            return


run = ScriptRunner()._run


if __name__ == '__main__':
    run('gitz_doc/cast/scripts/test.sh').write(sys.stdout)
