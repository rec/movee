from . import config
from . import parse
from . import scripta
from . import validate
import sys
import traceback


def main(args=None):  # pragma: no cover
    flags = vars(parse.parse(args))
    cfg = config.read_config(flags)
    validate.validate(cfg)

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
