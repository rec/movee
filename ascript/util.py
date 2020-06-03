import contextlib
import hashlib
import traceback


@contextlib.contextmanager
def print_exception():
    try:
        yield
    except Exception:
        traceback.print_exc()


def stable_hash(s):
    return hashlib.blake2s(s.encode()).hexdigest()


def is_comment(line, was_comment):
    if line.strip():
        return line.strip().startswith('#')
    return was_comment


def is_comment_lines(lines, was_comment):
    return is_comment(lines[0], was_comment)


def split_by(items, condition=is_comment, initial_state=False):
    """Like groupby, but with a state"""
    queue = []
    state = initial_state

    for i in items:
        new_state = condition(i, state)
        if new_state != state:
            if queue:
                yield queue
                queue = []

        queue.append(i)
        state = new_state

    if queue:
        yield queue


def trailing_slash(lines):
    """
    Groups lines with trailing slashes and yields lists of strings.
    Within each list, every string except the last one ends in a backslash.
    Each list corresponds to one executable command.
    """
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


def split_script(lines):
    return split_by(trailing_slash(lines), is_comment_lines)
