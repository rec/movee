from .cast import Cast
from .times import Times
from .typing_errors import ErrorMaker
from numbers import Number
from pathlib import Path
import termtosvg.config
import yaml


def validate(cfg):
    errors = []
    for k, v in cfg.items():
        if f := VALIDATORS.get(k):
            try:
                v2 = f(k, v)
            except Exception as e:
                errors.append(f'{k}: {e}\n')
            else:
                cfg[k] = v if v2 is None else v2

    if errors:
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


def _validate_number(k, v):
    v = int(v or 0)
    if v < 0:
        raise ValueError(f'{k} must be non-negative')
    return v


def _validate_theme(k, v):
    if v and v not in termtosvg.config.default_templates():
        raise ValueError(f'Unknown asciinema theme {v}')


def _read_keys(k, v):
    if v:
        if isinstance(v, str):
            if set('0123456789., ').issuperset(v):
                return [float(s) for s in v.split()]
        elif isinstance(v, (list, tuple)):
            if all(isinstance(i, Number) for i in v):
                return v
            if not all(isinstance(i, str) for i in v):
                raise ValueError(f'Do not understand --{k}={v}')
        else:
            raise ValueError(f'Do not understand --{k}={v}')

        keys, errors = [], [], []

        for file in v:
            try:
                cast = Cast.read(file)
            except Exception:
                errors.append(file)
            else:
                keys += cast.keystroke_times()

        if not errors:
            return keys

        raise ValueError('Cannot open', ', '.join(errors))


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
