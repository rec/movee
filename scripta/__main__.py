from . import config
from . import parse
from . import scripta
import sys
import traceback


def main(args=None):  # pragma: no cover
    flags = parse.parse(args)
    cfg = config.to_config(vars(flags))

    try:
        scripta.scripta(**cfg)
        return 0
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        return -1


if __name__ == '__main__':
    sys.exit(main())
