from asyncio.subprocess import PIPE
from dataclasses import dataclass
from .waiter import Waiter
import asyncio
import itertools
import shlex
import sys
import uuid

MARKER = str(uuid.uuid4()) + '.'

ERR, OUT, IN, PROMPT, KILL = 'EOIPK'


@dataclass
class Runner:
    execute: str
    set_prompts: str
    exit: str

    async def __call__(self, callback, commands, kill_after=None, shell=False):
        self.callback = callback
        cmd = self.execute
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

        ready = asyncio.Event()
        ready.set()

        proc = await create(*cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def kill():
            callback(KILL, '')
            proc.kill()

        killer = Waiter(kill_after and kill, kill_after)
        killer.start()

        async def read_stdout():
            while line := await proc.stdout.readline():
                callback(OUT, line.decode('utf8').rstrip('\n'))

        async def read_stderr():
            first_prompt = True

            while line := await proc.stderr.readline():
                before, *after = line.decode('utf8').split(MARKER, maxsplit=1)

                if after:
                    if first_prompt:
                        first_prompt = False
                    elif before:
                        callback(ERR, before)
                    callback(PROMPT, after[0].strip())
                    ready.set()
                elif not first_prompt:
                    callback(ERR, before.rstrip('\n'))

        async def write_stdin():
            cmds = itertools.chain([self.set_prompts], commands, [self.exit])
            for command in cmds:
                await ready.wait()
                ready.clear()

                if command not in (self.set_prompts, self.exit):
                    callback(IN, command)
                line = command.encode('utf8') + b'\n'
                proc.stdin.write(line)
                await proc.stdin.drain()

            killer.stop()
            proc.kill()

        await asyncio.gather(read_stderr(), read_stdout(), write_stdin())


bash = Runner(
    '/bin/bash -i', f'PS1="{MARKER}1\\n" ; PS2="{MARKER}2\\n"', 'exit'
)
python = Runner(
    f'{sys.executable} -i',
    f'import sys; sys.ps1 = "{MARKER}1\\n"; sys.ps2 = "{MARKER}2\\n"',
    'quit()',
)
