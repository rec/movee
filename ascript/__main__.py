"""
🎦 Script asciinema movies 🎦
====================================================================


USAGE
-------

.. code-block:: bash

    ascript my_file.py [README.rst]

"""
import sys
from .cast_recorder import CastRecorder

__all__ = ('main',)


def main(source, target=None):
    """Print documentation for a file or module

    ARGUMENTS
      path
        path to the Python file or module.

      target
        path to the output file or ``None``, in which case
        output is printed to stdout
    """
    cast = CastRecorder().record(source)

    if target:
        with open(target, 'w') as fp:
            cast.write(fp)
    else:
        cast.write(sys.stdout)


if __name__ == '__main__':
    main(*sys.argv[1:])
