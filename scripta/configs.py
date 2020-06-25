from . import parse
from pathlib import Path
import yaml

CONFIG_SUFFIXES = {'.yml', '.yaml', '.json'}
SCRIPT_SUFFIXES = {'.py', '.sh', '.bash'}
CONFIG_KEYS = {a.dest for a in parse.PARSER._actions}

# THEME = 'solarized_light'


def to_config(args):
    if isinstance(args, list):
        sources, args = args, {}
    else:
        sources = args.pop('scripts')

    dont_exist, unknown_suffix = [], []
    scripts, configs = [], []

    for i, s in enumerate(sources):
        if isinstance(s, dict) or any(c in s for c in '[{:'):
            configs.append((f'<argument {i}: {s}>', s))

        elif not (p := Path(s)).exists():
            dont_exist.append(s)

        elif p.suffix in SCRIPT_SUFFIXES:
            scripts.append(s)

        elif p.suffix in CONFIG_SUFFIXES:
            configs.append((s, p.read_text()))

        else:
            unknown_suffix.append(s)

    if dont_exist:
        raise ValueError('Cannot find ' + ' '.join(dont_exist))
    if unknown_suffix:
        raise ValueError('Unknown suffixes: ' + ' '.join(unknown_suffix))

    exceptions = []
    config = {'scripts': scripts}
    for source, cfg in configs:
        if isinstance(cfg, str):
            try:
                cfg = yaml.safe_load(cfg)
            except Exception as e:
                exceptions.append(f'{source}: {e}')
                continue

        scripts += cfg.pop('scripts', [])
        config.update(cfg, scripts=scripts)

    if exceptions:
        raise ValueError('Cannot load:\n%s' % '\n'.join(exceptions))

    if unknown_keys := set(config) - CONFIG_KEYS:
        raise ValueError('Unknown config keys %s' % ''.join(unknown_keys))

    for k, v in args.items():
        if v or k not in config or k == 'svg' and v is None:
            config[k] = v

    return config
