#bigrandom.py
def randrange(start,stop = 0,step = 1):
    import random
    if start > stop:
        v = stop
        stop = start
        start = v
    if step <= 0:
        return -1
    else:
        v = long(random.random() * (stop - start) / step)
        return v * step + start

def random():
    import random
    return random.random()