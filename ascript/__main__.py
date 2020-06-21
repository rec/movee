"""
🎦 Script asciinema movies 🎦
====================================================================


USAGE
-------

.. code-block:: bash

    ascript my_file.py [castfile]

"""
import sys
from .cast_recorder import CastRecorder


if __name__ == '__main__':
    CastRecorder().record_to(*sys.argv[1:])
