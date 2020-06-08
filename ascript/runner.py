from asyncio.subprocess import PIPE
import asyncio
import itertools
import shlex
import uuid

MARKER = str(uuid.uuid4()) + '.'
BASH_PROMPT = f'PS1="{MARKER}1\\n" ; PS2="{MARKER}2\\n"'
PYTHON_PROMPT = ';'.join(
    ['import sys', f'sys.ps1 = "{MARKER}1\\n"', f'sys.ps2 = "{MARKER}2\\n"']
)

ERR, OUT, IN, PROMPT = 'EOIP'


async def run(execute, set_prompts, commands, callback, shell=False):
    cmd = execute
    if shell:
        create = asyncio.create_subprocess_shell
        if not isinstance(cmd, str):
            cmd = [shlex.join(cmd)]
    else:
        create = asyncio.create_subprocess_exec
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)

    ready = asyncio.Event()
    ready.set()

    proc = await create(*cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    async def read_out():
        while line := await proc.stdout.readline():
            callback(OUT, line.decode('utf8').rstrip('\n'))

    async def read_err():
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

    async def write():
        for command in itertools.chain((set_prompts,), commands):
            await ready.wait()
            ready.clear()

            if command is not set_prompts:
                callback(IN, command)
            line = command.encode('utf8') + b'\n'
            proc.stdin.write(line)
            await proc.stdin.drain()
        proc.kill()

    await asyncio.gather(read_err(), read_out(), write())


def yield_inputs(prompt):
    while True:
        s = input(prompt)
        if not s:
            break
        yield s


def main():
    commands = 'echo HELLO', 'ls', 'echo BYE'
    # commands = yield_inputs('$ ')

    asyncio.run(run('/bin/bash -i', BASH_PROMPT, commands, print))


if __name__ == '__main__':
    main()
