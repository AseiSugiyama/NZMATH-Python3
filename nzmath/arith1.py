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
        if not (k & 1):
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
    This function returns Legendre symbol (a/m)
    If m is a odd composite then this is Jacobi symbol
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

import random
import gcd
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
        raise ValueError,"There is no solution"

def expand(n, m):
    """
    This function returns m-adic expansion for n.
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
    raise ZeroDivisionError("There is no inverse for %d." % x)

def CRT(nlist):
    """
    This function is Chinese Rmainder Theorem using Algorithm 2.1.7 
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
    while not (n % p):
        k += 1
        n //= p
    return (k, n)

class _Issquare:
    """
    A class for testing whether a number is square or not.
    The function issquare is an instance of the class, indeed.
    """
    q64 = [0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57]
    q63 = [0, 1, 4, 7, 9, 16, 18, 22, 25, 28, 36, 37, 43, 46, 49, 58]
    q65 = [0, 1, 4, 9, 10, 14, 16, 25, 26, 29, 30, 35, 36, 39, 40, 49, 51, 55, 56, 61, 64]
    q11 = [0, 1, 3, 4, 5, 9]
    def __call__(self, a):
        if a&63 in self.q64:
            r = a % 45045
            if r%63 in self.q63 and r%65 in self.q65 and r%11 in self.q11:
                q = arith1.floorsqrt(a)
                if q*q == a:
                    return q
        return 0

# test whether a given number is a square number or not.
issquare = _Issquare()
