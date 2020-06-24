"""
🎦 Script asciinema movies 🎦
====================================================================


USAGE
-------

.. code-block:: bash

    ascript my_file.py [castfile]

"""
import asyncio
import sys
from .cast_recorder import CastRecorder


async def record_and_compare(count=4):
    lines = []
    for i in range(count):
        cr = CastRecorder()

        await cr.record_to(*sys.argv[1:])
        lines.append([i.chars for i in cr.cast.lines])

    for i in range(1, count):
        print(lines[0] == lines[i], i)

    for j in range(max(len(i) for i in lines)):
        items = []
        for i in range(count):
            try:
                items.append(lines[i][j])
            except IndexError:
                items.append('')

        symbol = ' ' if len(set(items)) == 1 else '*'

        print(symbol, '%2d: ' % j, end='')
        for i in items:
            print('%16s' % i[:12].rstrip(), end='')
        print()

    for i in range(count):
        print(i, lines[i][36])
    print()


if __name__ == '__main__':
    if not False:
        asyncio.run(CastRecorder().record_to(*sys.argv[1:]))
    else:
        asyncio.run(record_and_compare())
