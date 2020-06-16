import time
from .cast import Cast
from . import colors
from . import constants
from . import run

PROMPT = '▶ {BLUE}tom{RED}:{GREEN}/code/test{NONE}$ '
BASH_PS = PROMPT.format(**vars(colors)), '> '
PYTHON_PS = '>>> ', '... '


class CastRecorder:
    def __init__(self, errors, key_times):
        self.key_times = key_times
        self.errors = errors

    def record(self, script):
        if script.endswith('.py'):
            self.runner = run.python
            self.ps = PYTHON_PS
        else:
            self.runner = run.bash
            if not script.endswith('.sh'):
                raise ValueError('Do not understand script %s' % script)
            self.ps = BASH_PS

        self.cast = Cast()
        self.index = 0
        self.start_time = time.time()

        self._add(constants.CONTROL_L)
        self._add(self.prompt)
        self.runner(self._callback, open(script))

    def _callback(self, event, line):
        if event is run.IN:
            for k, t in self.key_times.to_type(line):
                self.start_time -= t
                self._add(k)

        elif event is run.PROMPT:
            self._add(self.ps['12'.index(line[0])])
            self._add(constants.RETURN)

        elif event in (run.OUT, run.ERR):
            self._add(line.rstrip('\n'))
            self._add(constants.RETURN)

    def _add(self, key):
        delta_time = (time.time() - self.start_time) - self.cast.duration
        self.cast.append(key, delta_time)
