from asyncio.subprocess import PIPE
from dataclasses import dataclass
from .waiter import Waiter
import asyncio
import itertools
import shlex
import sys
import typing
import uuid

MARKER = str(uuid.uuid4()) + '.'

ERR, OUT, IN, PROMPT, KILL = 'EOIPK'


@dataclass
class Runner:
    execute: typing.Union[str, list, tuple]
    set_prompts: str
    exit: str

    async def __call__(self, callback, commands, shell=False, kill_after=None):
        pc = ProcCallback(self, callback, commands)
        await pc.run(shell, kill_after)


bash = Runner(
    '/bin/bash -i', f'PS1="{MARKER}1\\n" ; PS2="{MARKER}2\\n"', 'exit'
)
python = Runner(
    f'{sys.executable} -i',
    f'import sys; sys.ps1 = "{MARKER}1\\n"; sys.ps2 = "{MARKER}2\\n"',
    'quit()',
)


@dataclass
class ProcCallback:
    def __init__(self, runner, callback, commands):
        self.runner = runner
        self.callback = callback
        self.commands = commands
        self.ready = asyncio.Event()

    async def run(self, shell, kill_after):
        cmd = self.runner.execute
        if shell:
            create = asyncio.create_subprocess_shell
            if isinstance(cmd, str):
                cmd = [cmd]
            else:
                cmd = [shlex.join(cmd)]
        else:
            create = asyncio.create_subprocess_exec
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)

        self.proc = await create(*cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.killer = Waiter(kill_after and self._kill, kill_after)
        self.killer.start()

        await asyncio.gather(self._stdin(), self._stdout(), self._stderr())

    async def _stdin(self):
        cmds = itertools.chain(
            [self.runner.set_prompts], self.commands, [self.runner.exit]
        )
        self.ready.set()

        for command in cmds:
            await self.ready.wait()
            self.ready.clear()

            if command not in (self.runner.set_prompts, self.runner.exit):
                self.callback(IN, command)
            line = command.encode() + b'\n'
            self.proc.stdin.write(line)
            await self.proc.stdin.drain()

        self.killer.stop()
        self.proc.kill()

    async def _stdout(self):
        while line := await self.proc.stdout.readline():
            self.callback(OUT, line.decode().rstrip('\n'))

    async def _stderr(self):
        first_prompt = True

        while line := await self.proc.stderr.readline():
            before, *after = line.decode().split(MARKER, maxsplit=1)

            if after:
                if first_prompt:
                    first_prompt = False
                elif before:  # pragma: no cover
                    self.callback(ERR, before)
                self.callback(PROMPT, after[0].strip())
                self.ready.set()

            elif not first_prompt:  # pragma: no cover
                self.callback(ERR, before.rstrip('\n'))

    def _kill(self):
        self.callback(KILL, '')
        self.proc.kill()
