from nzmath.arith1 import *
from nzmath.prime import generator_eratosthenes as generator_eratosthenes

def powerDetection(n, largest_exp = False):
    """
    param positive integer n
    param boolean largest_exp
    return integer x, k s.t. n == x ** k
           (2 <= k if exist else x, k == n, 1)
           if largest_exp is true then return largest k
    """
    ge = generator_eratosthenes(log(n, 2))
    for exp in ge:
        power_root, power = floorpowerroot(n, exp, True)
        if power == n:
            if largest_exp:
                x, k = powerDetection(power_root, True)
                return x, k * exp
            else:
                return power_root, exp

    return n, 1
