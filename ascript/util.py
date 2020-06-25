import hashlib


def stable_hash(s):
    if isinstance(s, str):
        s = s.encode()
    return hashlib.blake2s(s).hexdigest()
