#bigrandom.py
import random


def big_random(min,max):

    return long(random.random() * (max-min)) + min
