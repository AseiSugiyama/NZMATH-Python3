"""
Miscellaneous arithmetic functions
"""

import math
import random
import nzmath.gcd as gcd


def floorsqrt(a):
    """
    Return the floor of square root of the given integer.
    """
    if a < 2 ** 59:
        return int(math.sqrt(a))
    else:
        b_old = a
        b = pow(10, log(a, 10)//2 + 1)
        while b_old > b:
            b_old, b = b, (b+a//b)//2
        return b_old

def floorpowerroot(n, k):
    """
    Return the floor of k-th power root of the given integer n.
    """
    if k == 1:
        return n
    elif k == 2:
        return floorsqrt(n)
    if n < 0:
        if not (k & 1):
            raise ValueError("%d has no real %d-th root." % (n, k))
        else:
            sign = -1
            n = -n
    else:
        sign = 1

    a = floorsqrt(n)
    b = 0
    while a > b:
        c = (a + b) // 2
        if c**k > n:
            a = c
        else:
            if b == c:
                a = b
                break
            b = c
    while (a+1)**k <= n: # needed when floorsqrt(n) is already small.
        a += 1

    if sign < 0:
        a = -a
    return a

def legendre(a, m):
    """
    This function returns the Legendre symbol (a/m).
    If m is an odd composite then this is the Jacobi symbol.
    """
    a = a % m
    symbol = 1
    while a != 0:
        while a % 2 == 0:
            a = a//2
            if m % 8 == 3 or m % 8 == 5:
                symbol = -symbol
        a, m = m, a
        if a % 4 == 3 and m % 4 == 3:
            symbol = -symbol
        a = a % m
    if m == 1:
        return symbol
    return 0

def modsqrt(a, p):
    """
    This function returns one of the square roots of 'a' for mod 'p'.
    'p' must be an odd prime.
    """
    symbol = legendre(a, p)
    if symbol == 1:
        pmod8 = p % 8
        if pmod8 != 1:
            a = a % p
            if pmod8 == 3 or pmod8 == 7:
                x = pow(a, (p+1)//4, p)
            else: # p%8==5
                x = pow(a, (p+3)//8, p)
                c = pow(x, 2, p)
                if c != a:
                    x = (x * pow(2, (p-1)//4, p)) % p
        else: #p%8==1
            d = 2
            while legendre(d, p) != -1:
                d = random.randrange(3, p)
            s, t = vp(p-1, 2)
            A = pow(a, t, p)
            D = pow(d, t, p)
            m = 0
            for i in range(1, s):
                if pow(A*(D**m), 2**(s-1-i), p) == (p-1):
                    m += 2**i
            x = (a**((t+1)//2)) * (D**(m//2)) % p
        return x
    elif symbol == 0:
        return 0
    else:
        raise ValueError("There is no solution")

def expand(n, m):
    """
    This function returns m-adic expansion for n.
    n and m should satisfy n > m > 0.
    """
    k = []
    while n >= m:
        k.append(n % m)
        n //= m
    k.append(n)
    return k

def inverse(x, p):
    """
    This function returns inverse of x for modulo p.
    """
    x = x % p
    y = gcd.extgcd(p, x)
    if y[2] == 1:
        if y[1] < 0:
            r = p + y[1]
            return r
        else:
            return y[1]
    raise ZeroDivisionError("There is no inverse for %d modulo %d." % (x, p))

def CRT(nlist):
    """
    This function is Chinese Rmainder Theorem using Algorithm 2.1.7 
    of C.Pomerance and R.Crandall's book.

    For example:
    >>> CRT([(1,2),(2,3),(3,5)])
    23
    """
    r = len(nlist)
    product = []
    prodinv = []
    m = 1
    for i in range(1, r):
        m = m*nlist[i-1][1]
        c = inverse(m, nlist[i][1])
        product.append(m)
        prodinv.append(c)

    M = product[r-2]*nlist[r-1][1]
    n = nlist[0][0]
    for i in range(1, r):
        u = ((nlist[i][0]-n)*prodinv[i-1]) % nlist[i][1]
        n += u*product[i-1]
    return n % M

def AGM(a, b):
    """
    Arithmetic-Geometric Mean.
    """
    x = (a+b) * 0.5
    y = math.sqrt(a*b)
    while abs(x-y) > y*1e-15:
        x, y = (x+y) * 0.5, math.sqrt(x*y)
    return x

def _BhaskaraBrouncker(n):
    """

    _BhaskaraBrouncker returns the minimum tuple (p,q) such that:
        p ** 2 - n * q ** 2 = 1 or -1,
    for positive integer n, which is not a square.

    A good approximation for square root of n is given by the ratio
    p/q; the error is at most 1/2*q**2.

    """
    floorOfSqrt = floorsqrt(n)
    a = floorOfSqrt
    b0, b1 = 0, floorOfSqrt
    c0, c1 = 1, n - floorOfSqrt * floorOfSqrt
    p0, p1 = 1, floorOfSqrt
    q0, q1 = 0, 1
    while c1 != 1:
        a = (floorOfSqrt + b1)//c1
        b0, b1 = b1, a * c1 - b1
        c0, c1 = c1, c0 + a * (b0 - b1)
        p0, p1 = p1, p0 + a * p1
        q0, q1 = q1, q0 + a * q1
    return (p1, q1)

def vp(n, p, k=0):
    """
    Return p-adic valuation and indivisible part of given integer.

    For example:
    >>> vp(100, 2)
    (2, 25)

    That means, 100 is 2 times divisible by 2, and the factor 25 of
    100 is indivisible by 2.

    The optional argument k will be added to the valuation.
    """
    while not (n % p):
        k += 1
        n //= p
    return (k, n)

class _Issquare:
    """
    A class for testing whether a number is square or not.
    The function issquare is an instance of the class, indeed.
    """
    q11 = [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]
    q63 = [1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    q64 = [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    q65 = [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1]

    def __call__(self, c):
        """
        Test whether a given number is a square number or not.  If
        the number is a square number, the function returns its square
        root.  Otherwise zero is returned.
        """
        t = c % 64
        if not self.q64[t]:
            return 0
        r = c % 45045  # 45045 = 63 * 65 * 11
        if not self.q63[r % 63]:
            return 0
        if not self.q65[r % 65]:
            return 0
        if not self.q11[r % 11]:
            return 0
        t = floorsqrt(c)
        if t * t == c:
            return t
        else:
            return 0

# test whether a given number is a square number or not.
issquare = _Issquare()

def log(n, base=2):
    """
    Return the integer part of logarithm of the given natural number
    'n' to the 'base'.  The default value for 'base' is 2.
    """
    if n < base:
        return 0
    if base == 10:
        return _log10(n)
    fit = base
    result = 1
    stock = [(result, fit)]
    while fit < n:
        next = fit ** 2
        if next <= n:
            fit = next
            result += result
            stock.append((result, fit))
        else:
            break
    else: # just fit
        return result
    stock.reverse()
    for index, power in stock:
        prefit = fit * power
        if prefit == n:
            result += index
            break
        elif prefit < n:
            fit = prefit
            result += index
    return result

def _log10(n):
    return len(str(n))-1
