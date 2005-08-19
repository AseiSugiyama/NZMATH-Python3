import math

def floorsqrt(a):
    """

    Return the floor of square root of the given integer.

    """
    if a < 2 ** 59:
        return long(math.sqrt(a))
    else:
        b_old = a
        b = pow(10, (len(str(long(a)))+1)//2)
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
        if k&1 == 0:
            raise ValueError, "%d has no real %d-th root." % (n, k)
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
    This program returns Legendre symbol (a/m)
    If m is a odd composite then this is Jacobi symbol
    """
    a = a % m
    t = 1
    while a != 0:
        while a % 2 == 0:
            a = a//2
            if m % 8 == 3 or m % 8 == 5:
                t = -t
        a, m = m, a
        if a % 4 == 3 and m % 4 == 3:
            t = -t
        a = a % m
    if m == 1:
        return t
    return 0

import random
import gcd
def sqroot(a, p):
    """
    This program returns squareroot of 'a' for mod 'p'.
    'p' must be an odd prime.
    """
    if legendre(a, p) == 1:
        pmod8 = p % 8
        if pmod8 != 1:
            a = a % p
            if pmod8 == 3 or pmod8 == 7:
                x = pow(a, ((p+1)/4), p)
                return x
            else: # p%8==5
                x = pow(a, ((p+3)/8), p)
                c = (x**2) % p
                if c != a:
                    x = x*(2**((p-1)/4)) % p
                return x
        else: #p%8==1
            d = random.randint(2, p-1)
            while legendre(d, p) != -1:
                d = random.randint(2, p-1)
            s = 0
            q = p-1
            while q % 2 == 0:
                q //= 2
                s += 1
            t = (p-1)/2**s
            A = pow(a, t, p)
            D = pow(d, t, p)
            m = 0
            for i in range(1, s):
                if pow(A*(D**m), 2**(s-1-i), p) == (p-1):
                    m = m + 2**i
            x = (a**((t+1)/2)) * (D**(m/2)) % p
            return x
    elif legendre(a, p) == 0:
        return 0
    else:
        raise ValueError,"There is no solution"


def expand(n, m):
    """
    This program returns m-adic expansion for n.
    n and m should satisfy n > m > 0.
    """
    k = []
    while n // m:
        k.append(n % m)
        n //= m
    k.append(n%m)
    return k

def inverse(x, p):
    """
    This program returns inverse of x for modulo p.
    """
    if x < 0:
        while x < 0:
            x += p
    y = gcd.extgcd(p, x)
    if y[2] == 1:
        if y[1] < 0:
            r = p + y[1]
            return r
        else:
            return y[1]
    else:
        return False

def CRT(nlist):
    """
    This program is Chinese Rmainder Theorem using Algorithm 2.1.7 
    of C.Pomerance and R.Crandall's book.
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
    x = (a+b) / 2.0
    y = math.sqrt(a*b)
    while abs(x-y) > y*1e-15:
        x = (x+y) / 2.0
        y = math.sqrt(x*y)
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
    while n % p == 0:
        n, k = n//p, k+1
    return (k, n)
