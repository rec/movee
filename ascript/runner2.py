import asyncio

from subprocess import PIPE

BASH = '/bin/bash', '-il'
# BASH = '/bin/bash',
POPEN_ARGS = {
    'stdin': PIPE,
    'stdout': PIPE,
    'stderr': PIPE,
    'encoding': 'utf8',
    'shell': not True,
}

# https://dzone.com/articles/interacting-with-a-long-running-child-process-in-p


async def run(shell, commands, callback, echo):
    proc = await asyncio.create_subprocess_shell(
        ' '.join(shell), stdin=PIPE, stdout=PIPE, stderr=PIPE
    )

    async def read(stream):
        is_err = stream is proc.stderr
        print('read', is_err)
        while True:
            line = await stream.readline()
            if not line:
                break
            callback(is_err, line.decode('utf8'))

    async def write(stream):
        for command in commands:
            e = echo.format(command)
            for i in e, command:
                stream.write((i + '\n').encode('utf8'))
            stream.write((command + '\n').encode('utf8'))
            await stream.drain()

            # TODO: wait until I see a prompt in read.
            await asyncio.sleep(0.01)

        print('terminate')
        proc.terminate()

    await asyncio.gather(
        read(proc.stderr), read(proc.stdout), write(proc.stdin),
    )


def yield_inputs(prompt):
    while True:
        s = input(prompt)
        if not s:
            break
        yield s


def main():
    import os

    print(dict(os.environ))
    asyncio.run(run(BASH, yield_inputs('$ '), print, "echo '{}'"))


if __name__ == '__main__':
    main()
