from .waiter import Waiter
from asyncio.subprocess import PIPE
from dataclasses import dataclass
import asyncio
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
        await ProcessRunner(self, callback, commands).run(shell, kill_after)


bash = Runner(
    '/bin/bash -i', f'PS1="{MARKER}1\\n" ; PS2="{MARKER}2\\n"', 'exit'
)
python = Runner(
    f'{sys.executable} -i',
    f'import sys; sys.ps1 = "{MARKER}1\\n"; sys.ps2 = "{MARKER}2\\n"',
    'quit()',
)


@dataclass
class ProcessRunner:
    def __init__(self, runner, callback, commands):
        self.runner = runner
        self.callback = callback
        self.commands = commands
        self.ready = asyncio.Event()
        self.running = False

    async def run(self, shell, kill_after):
        self.running = True
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
        def write(command):
            self.proc.stdin.write(command.rstrip().encode() + b'\n')

        write(self.runner.set_prompts)
        for command in self.commands:
            await self.ready.wait()
            if command.split('#')[0].strip():
                # TODO: fails for multiline strings with blank lines/comments
                write(command)
                self.ready.clear()
            self.callback(IN, command)

        await self.ready.wait()

        self.running = False
        self.killer.stop()
        write(self.runner.exit)
        await self.proc.stdin.drain()

    async def _stdout(self):
        while (line := await self.proc.stdout.readline()) and self.running:
            self.callback(OUT, line.decode().rstrip('\n'))

    async def _stderr(self):
        first_prompt = True

        while (line := await self.proc.stderr.readline()) and self.running:
            before, *after = line.decode().split(MARKER, maxsplit=1)

            if after:
                if first_prompt:
                    first_prompt = False
                elif before:
                    self.callback(ERR, before)
                self.callback(PROMPT, after[0].strip())
                self.ready.set()

            elif not first_prompt:
                self.callback(ERR, before.rstrip('\n'))

    def _kill(self):
        self.callback(KILL, '')
        self.proc.kill()
        self.running = False


if __name__ == '__main__':
    import sys

    asyncio.run(bash(print, open(sys.argv[1])))
