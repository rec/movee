"""
🎦 Script asciinema movies 🎦
====================================================================


USAGE
-------

.. code-block:: bash

    scripta my_file.py [castfile]

"""
import asyncio
import sys
from .cast_recorder import CastRecorder


if __name__ == '__main__':
    asyncio.run(CastRecorder().record_to(*sys.argv[1:]))
