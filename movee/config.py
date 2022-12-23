from . import parse
from pathlib import Path
import yaml

CONFIG_SUFFIXES = {'.yml', '.yaml', '.json'}
SCRIPT_SUFFIXES = {'.py', '.sh', '.bash'}
CONFIG_KEYS = {a.dest for a in parse.PARSER._actions}

# THEME = 'solarized_light'


def read_config(flags):
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

        if set('[{:').intersection(src):
            data = src
            src = f'<argument {i}>'

        elif any(src.endswith(s) for s in SCRIPT_SUFFIXES):
            scripts.append(src)
            return

        elif not any(src.endswith(s) for s in CONFIG_SUFFIXES):
            unknown_suffix.append(src)
            return

        else:
            data = Path(src).read_text()

        try:
            cfg = yaml.safe_load(data)
            if not isinstance(cfg, dict):
                raise TypeError('Expected str or dict')
            return cfg
        except yaml.parser.ParserError as e:
            exceptions.append(f'{src}: {e}')

    configs = [route_source(i, c) or {} for i, c in enumerate(sources)]

    config = {}
    for c in configs:
        p = c.pop('sources', [])
        scripts += p
        config.update(c)

    sources = [Path(s) for s in scripts]

    errors = []
    if dont_exist := [str(s) for s in sources if not s.exists()]:
        errors.append('Cannot find %s\n' % ' '.join(dont_exist))
    if unknown_suffix:
        errors.append('Suffix unknown: %s\n' % ' '.join(unknown_suffix))
    if exceptions:
        errors.append('Cannot load:\n%s\n' % '\n'.join(exceptions))

    if errors:
        raise ValueError(*errors)

    config['sources'] = sources

    for k, v in flags.items():
        if v or (k not in config) or (k == 'svg' and v is None):
            config[k] = v

    if unknown_keys := set(config) - CONFIG_KEYS:
        raise ValueError('Invalid for config: %s\n' % ' ,'.join(unknown_keys))
    return config
