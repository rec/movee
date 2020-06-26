from . import parse
from pathlib import Path
import yaml

CONFIG_SUFFIXES = {'.yml', '.yaml', '.json'}
SCRIPT_SUFFIXES = {'.py', '.sh', '.bash'}
CONFIG_KEYS = {a.dest for a in parse.PARSER._actions}

# THEME = 'solarized_light'


def to_config(flags):
    if isinstance(flags, dict):
        sources = flags.pop('sources', [])
    else:
        sources, flags = list(flags), {}

    if not sources:
        raise ValueError('No source file given')

    scripts, dont_exist, unknown_suffix, exceptions = [], [], [], []

    def route_source(i, src):
        if isinstance(src, dict):
            return src

        if not isinstance(src, str):
            raise TypeError('Expected str or dict')

        route = None
        id = src
        if any(c in src for c in '[{:'):
            id = f'<argument {i}>'
            data = src

        elif not (p := Path(src)).exists():
            route = dont_exist

        elif p.suffix in SCRIPT_SUFFIXES:
            route = scripts

        elif p.suffix not in CONFIG_SUFFIXES:
            route = unknown_suffix

        else:
            data = p.read_text()

        if route is None:
            try:
                cfg = yaml.safe_load(data)
                if not isinstance(cfg, dict):
                    raise TypeError('Expected str or dict')
                return cfg
            except yaml.parser.ParserError as e:
                route = exceptions
                id = f'{id}: {e}'

        route.append(id)
        return {}

    configs = [route_source(i, c) for i, c in enumerate(sources)]

    errors = []
    if dont_exist:
        errors.append('Cannot find %s\n' % ' '.join(dont_exist))
    if unknown_suffix:
        errors.append('Suffix unknown: %s\n' % ' '.join(unknown_suffix))
    if exceptions:
        errors.append('Cannot load:\n%s\n' % '\n'.join(exceptions))

    if errors:
        raise ValueError(*errors)

    config = {'sources': scripts}
    for cfg in configs:
        scripts.extend(cfg.pop('sources', []))
        config.update(cfg)

    for k, v in flags.items():
        if v or (k not in config) or (k == 'svg' and v is None):
            config[k] = v

    if unknown_keys := set(config) - CONFIG_KEYS:
        raise ValueError('Invalid for config: %s\n' % ' ,'.join(unknown_keys))
    return config
