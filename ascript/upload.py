import hashlib
import json
import sproc
import webbrowser


def upload(cast_file, json_file):
    m = hashlib.sha256()
    m.update(cast_file.read_bytes())
    sha = m.hexdigest()

    if json_file.exists():
        new_sha, url = json.loads(json_file.read_text())
        if new_sha == sha:
            return url

    sproc.sproc('asciinema', 'upload', str(cast_file))

    lines = []
    url = next(i for i in lines if 'https://' in i).strip()
    json_file.write_text(json.dumps([sha, url]))
    webbrowser.open(url, new=0, autoraise=True)
    print(MESSAGE.format(url=url))
    return url


MESSAGE = """New upload {url}!"""
