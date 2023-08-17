from posixpath import dirname


__version__ = "0.2.3"


def lcp(a):
    """
    return longest common prefix of iterable of strings,
    or None when iterable is exhausted immediately
    """
    a = list(a)
    if len(a) == 0:
        return None
    first, last = min(a), max(a)
    stop = min(len(first), len(last))
    # find the common prefix between the first and last string
    i = 0
    while i < stop and first[i] == last[i]:
        i += 1
    return first[:i]


def human_bytes(n):
    """
    return size (in bytes) in more human readable form
    """
    if n < 1024:
        return '%d' % n
    k = float(n) / 1024
    if k < 1024:
        return '%dK' % round(k)
    m = k / 1024
    if m < 1024:
        return '%.1fM' % m
    g = m / 1024
    return '%.2fG' % g


def get_empty_missing_dirs(a):
    """
    given a list of tuples (name, isdir), return a tuple with
    two sets; the empty and the missing directories
    """
    dirs1 = set()  # input filtered for directories
    dirs2 = set()  # directories that contain files
    for name, isdir in a:
        if isdir:
            dirs1.add(name)
            continue
        # for each file path, add the directories leading to its path
        p = dirname(name)
        while p not in dirs2:
            dirs2.add(p)
            p = dirname(p)

    dirs1.discard('')
    dirs2.discard('')
    # set of empty dirs, set of missing dirs
    return dirs1 - dirs2, dirs2 - dirs1
