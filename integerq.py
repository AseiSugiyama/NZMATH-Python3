#integerq.py
import primeq

def integer_q(a):
    if a < 0:
        a = - a
    if a == 1:
        return 1
    if a == 0:
        return 0
    elif primeq.primeQ(a) == 1:
        return 2
    else:
        return 6