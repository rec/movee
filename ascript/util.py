import hashlib


def stable_hash(s):
    return hashlib.blake2s(s.encode()).hexdigest()
