from .cast_recorder import CastRecorder
from . import parse
import asyncio
import sys
import traceback


def main(args=None):  # pragma: no cover
    args = parse.parse(args)

    try:
        asyncio.run(CastRecorder().record_to(*args.scripts))
        return 0
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        return -1


if __name__ == '__main__':
    sys.exit(main())
