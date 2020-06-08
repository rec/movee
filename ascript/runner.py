from queue import Queue
from subprocess import Popen, PIPE
from threading import Thread
from .util import print_exception
import contextlib
import sys

BASH = '/bin/bash', '-i'
MARKER = 'xyzzyxyzzy'
STDOUT, STDERR, STDIN = range(3)
NAMES = 'stdout', 'stderr', 'stdin'
POPEN_ARGS = {
    'stdin': PIPE,
    'stdout': PIPE,
    'stderr': PIPE,
    'encoding': 'utf8',
    'shell': not True,
}

# https://dzone.com/articles/interacting-with-a-long-running-child-process-in-p


@contextlib.contextmanager
def run(cmd, marker, callback, timeout=0.2):
    proc = Popen(cmd, **POPEN_ARGS)

    def printline(*parts):
        print(*parts, file=proc.stdin)
        proc.stdin.flush()

    proc.printline = printline

    def read(stream):
        name = STDERR if stream is proc.stderr else STDOUT
        line = True
        while line or proc.poll() is None:
            line = stream.readline()
            line and callback(name, line.rstrip('\n'))

        callback(name, None)

    for stream in proc.stderr, proc.stdout:
        Thread(target=read, args=(stream,), daemon=True).start()

    try:
        yield proc

    finally:
        with print_exception():
            proc.stdin.close()

        with print_exception():
            proc.terminate()
            proc.wait(timeout=timeout)


def shell_commands(commands, callback, shell=BASH, marker='echo {}'):
    marker = marker.format(MARKER)
    finished = 0
    queue = Queue()

    with run(shell, marker, lambda *a: queue.put(a)) as proc:
        for i, command in enumerate(commands):
            callback(STDIN, command)
            proc.printline(command)
            proc.printline(marker)

            line = ''
            while finished < 2:
                name, line = queue.get()
                if line and marker in line.strip():
                    break

                callback(name, line)
                finished += line is None
            else:
                raise ValueError('End without marker')

        callback(STDIN, None)


def printer(name, line):
    print('%7s:' % NAMES[name], line)


def print_shell_commands(filename, shell=BASH, marker='echo {}'):
    shell_commands(
        open(filename), callback=printer, shell=shell, marker=marker
    )


def print_python_commands(filename):
    print_shell_commands(filename, ('python3', '-i'), "print('{}')")


def run_python_commands():
    def commands():
        while True:
            s = input('>>> ')
            if not s:
                break
            yield s

    shell_commands(commands(), printer, ('python3', '-i'), "print('{}')")


if __name__ == '__main__':
    # print_shell_commands(sys.argv[1])
    print_python_commands(sys.argv[1])
    # run_python_commands()
