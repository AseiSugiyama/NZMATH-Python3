#integerq.py
import primeq

def integer_q(a):
    """Judge the integer which you input.
return 0 if the integer is 0.
return 1 if the integer is 1.
return 2 if the integer belongs prime numbers.
return 6 in the case of others."""
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