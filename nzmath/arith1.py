import math

def floorsqrt(a):
    """

    Return the floor of square root of the given integer.

    """
    if a < 2 ** 59:
        return long(math.sqrt(a))
    else:
        b_old = a
        b = pow(10,(len(str(long(a)))+1)//2)
        while b_old>b:
            b_old, b = b, (b+a//b)//2
        return b_old

import random
import gcd
import factor

def euler(n):                    
    """
    This program returns Eulernumber for n
    """
    f = factor.trialDivision(n)
    p = 1
    for f0, f1 in f:
        p *=pow(f0,f1-1)*(f0-1)
    return p

def moebius(n):
    """
    This program returns Moebius function for n
    """
    f = factor.trialDivision(n)
    i=0
    while i < len(f):
        g=f[i]
        if g[1]>1:
            return 0
        i=i+1
    return pow(-1,len(f))


def legendre(a,m): 
    """
    This program returns Legendre symbol (a/m)
    If m is a odd composite then this is Jacobi symbol
    """
    a=a%m
    t=1
    while a!=0:
        while a%2==0:
            a=a/2
            if m%8==3 or m%8==5:
                t=-t
        a,m=m,a
        if a%4==3 and m%4==3:
            t=-t
        a=a%m
    if m==1:
        return t
    return 0


def sqroot(a,p):
    """
    This program returns squareroot of 'a' for mod 'p'.
    'p' must be an odd prime.
    """
    if legendre(a,p) == 1:
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
            while q%2 == 0:
                q //= 2
                s += 1
            t = (p-1)/2**s
            A = pow(a,t,p)
            D = pow(d,t,p)
            m = 0
            for i in range(1,s):
                if pow((A*(D**m)),(2**(s-1-i)),p) == (p-1):
                    m = m + 2**i
            x = (a**((t+1)/2)) * (D**(m/2)) % p
            return x
    elif legendre(a,p)==0:
        return 0
    else:
        raise ValueError,"There is no solution"


def expand(n,m):
    """
    This program returns m-adic expansion for n.
    n and m should satisfy n > m > 0.
    """
    k = []
    while n//m:
        k.append(n % m)
        n //= m
    k.append(n%m)
    return k

def inverse(x,p):
    """
    This program returns inverse of x for modulo p.
    """
    if x<0:
        while x<0:
            x += p
    y = gcd.extgcd(p,x)
    if y[2]==1:
        if y[1]<0:
            r = p+y[1]
            return r
        else:
            return y[1]
    else:
        return False

def CRT(list):
    """
    This program is Chinese Rmainder Theorem using Algorithm 2.1.7 
    of C.Pomerance and R.Crandall's book.
    """
    r=len(list)
    product=[]
    prodinv=[]
    m=1
    i=1
    while i < r:
        m = m*list[i-1][1]
        c = inverse(m,list[i][1])
        product.append(m)
        prodinv.append(c)
        i = i+1

    M=product[r-2]*list[r-1][1]
    n=list[0][0]
    i=1
    while i < r:
        u = ((list[i][0]-n)*prodinv[i-1])%list[i][1]
        n = n + u*product[i-1]
        i = i+1
    n = n%M
    return n

def AGM(a,b):
    x=(a+b)/2.0
    y=math.sqrt(a*b)
    while abs(x-y)>y*1e-15:
        x=(x+y)/2.0
        y=math.sqrt(x*y)
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
