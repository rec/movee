from .cast import Cast
from .times import DEFAULT_TIMES
from .times import Times
from .typing_errors import ErrorMaker
from numbers import Number
from pathlib import Path
import functools
import termtosvg.config
import yaml

ASCIINEMA_DECIMALS = 6


def validate(cfg):
    errors = []
    for k, v in cfg.items():
        if f := VALIDATORS.get(k):
            try:
                v2 = f(k, v)
            except Exception as e:
                if not errors:
                    last_call = functools.partial(f, k, v)
                errors.append(f'{k}: {e}\n')
            else:
                cfg[k] = v if v2 is None else v2

    if len(errors) == 1:
        last_call()
    elif errors:
        raise ValueError(*errors)


def _to_data(Dataclass):
    def fn(k, v):
        if not v:
            return Dataclass()
        if isinstance(v, Dataclass):
            return v
        if isinstance(v, str):
            v = yaml.safe_load(v)
        if isinstance(v, dict):
            return Dataclass(**v)
        if isinstance(v, (list, tuple)):
            return Dataclass(*v)
        raise ValueError(f'Did not understand --{k}={v}')

    return fn


def _validate_path(k, v):
    if v:
        path = Path(v)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            raise ValueError(f'--cast: {k} exists but is not a directory')
        return path


def _validate_number(k, v):
    if not v:
        return 0
    try:
        v = int(v)
    except Exception:
        raise ValueError(f'--{k} takes a numeric argument')
    v = int(v or 0)
    if v < 0:
        raise ValueError(f'{k} must be non-negative')
    return v


def _validate_theme(k, v):
    if v and v not in termtosvg.config.default_templates():
        raise ValueError(f'Unknown asciinema theme "{v}"')


def _read_keys(k, v):
    v = v or DEFAULT_TIMES

    if isinstance(v, str):
        if set('-0123456789., ').issuperset(v):
            v = f'[{v}]'
        if '[' in v:
            v = yaml.safe_load(v)
        else:
            v = [i.strip() for i in v.split(',')]

    if not isinstance(v, (list, tuple)):
        raise ValueError(f'Do not understand --{k}={v}')

    if not all(isinstance(i, Number) for i in v):
        if not all(isinstance(i, str) for i in v):
            raise ValueError(f'Do not understand --{k}={v}')

        files = v
        v, errors = [], []

        for file in files:
            try:
                cast = Cast.read(file)
            except Exception:
                errors.append(file)
            else:
                v += cast.keystroke_times()

        if errors:
            raise ValueError('Cannot open file: ' + ', '.join(errors))

    if not all(t >= 0 for t in v):
        raise ValueError('Times must all be positive')

    return [round(i, ASCIINEMA_DECIMALS) for i in v]


VALIDATORS = {
    'cast': _validate_path,
    'svg': _validate_path,
    'errors': _to_data(ErrorMaker),
    'times': _to_data(Times),
    'height': _validate_number,
    'width': _validate_number,
    'theme': _validate_theme,
    'keys': _read_keys,
}
