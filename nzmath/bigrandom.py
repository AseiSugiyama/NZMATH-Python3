#bigrandom.py
def randrange(start,stop = 0,step = 1):
    import random
    if start > stop:
        v = stop
        stop = start
        start = v
    if step <= 0:
        return -1
    elif (stop - start) % step > 0:
        return long(random.random()*(long(stop - start)+1) / step)*step + start
    else:
        return long(random.random() * (stop - start) / step)*step + start
def random():
    import random
    return random.random()