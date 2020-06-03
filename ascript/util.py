import hashlib


def stable_hash(s):
    return hashlib.blake2s(s.encode()).hexdigest()


def split_comments(lines):
    line_queue = []
    was_comment = False

    for line in lines:
        if line.strip():
            is_comment = line.strip().startswith('#')
        else:
            is_comment = was_comment

        if is_comment != was_comment:
            if line_queue:
                yield line_queue
                line_queue = []

        line_queue.append(line)
        was_comment = is_comment

    if line_queue:
        yield line_queue


def trailing_slash(lines):
    line_queue = []

    for line in lines:
        if line.strip().endswith('\\'):
            line_queue.append(line)
        elif line_queue:
            line_queue.append(line)
            yield line_queue
            line_queue = []
        else:
            yield [line]

    if line_queue:
        yield line_queue
