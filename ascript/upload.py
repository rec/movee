from .stable_hash import stable_hash
from pathlib import Path
import json
import subprocess


def upload(cast_file, suffix='.cache'):
    f = Path(cast_file)

    id = stable_hash(f.read_bytes())
    cache_file = (f.parent / ('.' + f.stem)).with_suffix(f.suffix + suffix)

    if cache_file.exists():
        new_id, url = json.loads(cache_file.read_text())
        if new_id == id:
            return url, False

    lines = _call('asciinema', 'upload', str(cast_file))
    urls = {i.strip() for i in lines if 'https://' in i}
    if len(urls) != 1:
        raise ValueError('Failed to upload, error is \n%s' + '\n'.join(lines))
    cache_file.write_text(json.dumps([id, url := urls.pop()]))
    return url, True


def _call(*cmd):  # pragma: no cover
    with subprocess.Popen(cmd, encoding='utf8', stdout=subprocess.PIPE) as po:
        return po.communicate()[0].splitlines()
