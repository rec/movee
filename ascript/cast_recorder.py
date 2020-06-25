import time
from .cast import Cast
from . import colors
from . import constants
from . import run
from . import times
from . import typing_errors
import safer

_PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
BASH_PS = _PROMPT.format(**vars(colors)), '> '
PYTHON_PS = '>>> ', '... '


class CastRecorder:
    def __init__(self, errors=None, key_times=None):
        self.errors = errors or typing_errors.ErrorMaker(0.08, 0.08, 0.08)
        self.key_times = key_times or times.KeyTimes()

    async def record(self, script):
        if script.endswith('.py'):
            self.runner = run.python
            self.ps = PYTHON_PS
        else:
            self.runner = run.bash
            if not script.endswith('.sh'):
                raise ValueError('Do not understand script %s' % script)
            self.ps = BASH_PS

        self.cast = Cast()
        self.start_time = time.time()
        self.chars = 0

        self._add(constants.CONTROL_L)
        await self.runner(self._callback, open(script))
        return self.cast

    async def record_to(self, script, target=None):
        await self.record(script)
        with safer.writer(target) as fp:
            self.cast.write(fp)

    def _callback(self, event, line):
        if event in (run.OUT, run.ERR):
            self.chars += len(line)
            line = line.rstrip('\n') + constants.RETURN
            self._add(line, self.key_times.times.to_print_one_line)
            return

        if self.chars:
            self._add('', self.key_times.to_read(self.chars))
            self.chars = 0

        if event is run.IN:
            with_errors = self.errors(line)
            for k, t in self.key_times.to_type(with_errors, line):
                if k == '\n':
                    k = constants.RETURN
                self._add(k, t)
        elif event is run.PROMPT:
            self._add(self.ps['12'.index(line[0])])

        else:  # pragma: no cover
            pass

    def _add(self, key, delta_time=0):
        delta_time = (time.time() - self.start_time) - self.cast.duration
        self.cast.append(key, delta_time)
        self.start_time -= delta_time
