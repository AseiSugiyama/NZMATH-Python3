"""
bigrange

Generators for range like sequences.
"""


def count(n=0):
    """
    Count up infinitely from 'n' (default to 0),

    see itertools.count
    """
    while True:
        yield n
        n += 1


def range(start, stop=None, step=None):
    """
    Generate range like finite integer sequence but can generate more
    than sys.maxint elements.
    """
    if step is None:
        step = 1
    elif not isinstance(step, (int, long)):
        raise ValueError("non-integer step for range()")
    if not isinstance(start, (int, long)):
        raise ValueError("non-integer arg 1 for range()")
    if stop is None:
        start, stop = 0, start
    elif not isinstance(stop, (int, long)):
        raise ValueError("non-integer stop for range()")

    if step > 0:
        n = start
        while n < stop:
            yield n
            n += step
    elif step < 0:
        n = start
        while n > stop:
            yield n
            n += step
    else:
        raise ValueError("zero step for range()")


def arithmetic_progression(init, difference):
    """
    Generate an arithmetic progression start form 'init' and
    'difference' step.
    """
    return _iterate(lambda x: x + difference, init)


def geometric_progression(init, ratio):
    """
    Generate a geometric progression start form 'init' and multiplying
    'ratio'.
    """
    return _iterate(lambda x: x * ratio, init)


def _iterate(func, init):
    """
    Generate (infinitely) a sequence (init, func(init), func(func(init)), ...)
    """
    val = init
    while True:
        yield val
        val = func(val)
