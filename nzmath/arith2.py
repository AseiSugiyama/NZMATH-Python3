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


def generator_fibonacci(n = None):
    """
    Generate Fibonacci number up to n
    """
    a = 0
    b = 1

    if None == n:
        while True:
            yield b
            a += b
            yield a
            b += a
    else:
        count = 0
        while True:
            yield b
            count += 1
            if n <= count:
                break
            a += b

            yield a
            count += 1
            if n <= count:
                break
            b += a


QLRST = {0:0, 1:1}
def fibonacci(n):
    """
    Fibonacci Sequence
    param positive integer n
    return the n-th term of the QLRS
    effect QLRST[n] = QLRS(n)
    """
    global PRECOMPUTED_FIBONACCI, QLRST

    if n < 0:
        raise ValueError, "fibonacci(n)  0 <= n  ?"

    if n in QLRST:
        return QLRST[n]

    m = n // 2
    if n & 1 == 0:
        f1 = fibonacci(m - 1)
        f2 = fibonacci(m)
        QLRST[n] = (f1 + f1 + f2) * f2
    else : # odd  n
        f1 = fibonacci(m)
        f2 = fibonacci(m + 1)
        QLRST[n] = f1 ** 2 + f2 ** 2

    return QLRST[n]
