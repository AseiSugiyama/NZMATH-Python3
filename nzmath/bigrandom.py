#bigrandom.py

import random as _random

def randrange(start,stop = "zero",step = 1):
    """Choose a random item from range([start,] stop[, step]).
(Return long integer.)"""
    positiveStep = 1
    if stop == "zero":
        stop = start
        start = 0
    if step == 0:
        raise ValueError, "zero step for randrange()"
    elif start != long(start):
        raise ValueError, "non-integer arg 1 for randrange()"
    elif stop != long(stop):
        raise ValueError, "non-integer stop for randrange()"
    elif step != long(step):
        raise ValueError, "non-integer step for randrange()"

    if step < 0:
        step = -step
        start = -start
        stop = -stop
        positiveStep = 0
    if start >= stop:
        raise ValueError, "empty range for randrange()"

    if (stop - start) % step != 0:
        v = (stop - start)//step + 1
    else:
        v = (stop - start)//step
    if positiveStep:
        return (long(random() * v) * step + start)
    return -(long(random() * v) * step + start)

random = _random.random

__all__ = ['random', 'randrange']
