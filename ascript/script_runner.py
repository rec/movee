from . import cast
from . import constants

# from . import keystrokes
from . import typing_errors
import sproc
import sys
import time


class ScriptRunner:
    def __init__(self):
        self.keystroke_times = []  # list(keystrokes.filtered_times())

    def run(self, script, timing):
        self.cast = cast.Cast()
        self.timing = timing
        self.start_time = time.time()
        self._add(constants.CONTROL_L)
        self._add(constants.PROMPT)
        self.lines = list(i for i in script.open() if i.strip())

        for i, line in enumerate(self.lines):
            self._run_one(i, line)

        self._wait(timing.TIME_AT_END)
        return self.cast

    def _run_one(self, i, line):
        self.index = hash(line)
        for k in typing_errors.with_errors(line):
            self._add_key(constants.RETURN if k == '\n' else k)

        lines = self.cast.lines
        before = len(lines)
        for ln in line.split('&&'):
            if not self._run(ln.strip()):
                break
        chars = sum(len(x[2]) for x in lines[before + 1 :])

        if not (
            i < len(self.lines) - 1
            and line.strip().startswith('#')
            and self.lines[i + 1].strip().startswith('#')
        ):
            self._add(constants.RETURN)
        self._add(constants.PROMPT)
        t = constants.TIME_TO_THINK + chars * constants.TIME_TO_READ_ONE_CHAR
        self._wait(t)

    def _run(self, cmd):
        try:
            sproc.sproc(cmd, self._add_line, shell=True)
            return True
        except Exception:
            return

    def _wait(self, delta):
        self.start_time -= delta
        self._add('')

    def _add(self, keys):
        self.cast.append(keys, time.time() - self.start_time)

    def _add_line(self, line):
        self._add(line)
        self._add(constants.RETURN)

    def _add_key(self, key):
        self.index %= len(self.keystroke_times)
        self.start_time -= self.keystroke_times[self.index]
        self.index += 1
        self._add(key)


run = ScriptRunner().run


if __name__ == '__main__':
    run('gitz_doc/cast/scripts/test.sh').write(sys.stdout)
