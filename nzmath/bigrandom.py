#bigrandom.py
def randrange(start,stop = "zero",step = 1):
    """Choose a random item from range([start,] stop[, step]).
(Return long integer.)"""
    import random
    t = 1
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
    else:
        if step < 0:
            step = -step
            start = -start
            stop = -stop
            t = -t
        if start > stop:
            raise ValueError, "empty range for randrange()"
        else:
            if (stop - start) % step != 0:
                v = long((stop - start)/step) + 1
            else:
                v = long((stop - start)/step) 
            return (long(random.random() * v) * step + start) * t   
def random():
    """Get the next random number in the range [0.0, 1.0)."""
    import random
    return random.random()