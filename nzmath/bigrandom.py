#bigrandom.py
import random


def random_range(min,max):

    return long(random.random() * (max-min)) + min

def random(z):
    return long(random.random() * z)