#bigrandom.py
import random

def randrange(start,stop = 0,step = 1):
    if start > stop :
        v = stop
        stop = start
        start = v
    if step <= 0:
        return 0
    else:
        v = long(random.random() * (stop - start) / step)
        return v*step + start 

def random():
    return random.random()