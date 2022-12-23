from . import movee
import asyncio
import sys
import traceback


def main(args=None):  # pragma: no cover
    try:
        asyncio.run(movee.movee(args))
        return 0
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        return -1


if __name__ == '__main__':
    sys.exit(main())
