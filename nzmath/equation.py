from __future__ import division
import math
import cmath
import logging

import nzmath.arith1 as arith1
import nzmath.polynomial as polynomial
import nzmath.finitefield as finitefield

_log = logging.getLogger('nzmath.equation')
_log.setLevel(logging.DEBUG)

# x is (list,tuple)
# t is variable
def e1(x):
    """
    0 = x[0] + x[1]*t
    """
    if x[1] == 0:
        raise ZeroDivisionError,"No Solution"
    else:
        return -x[0]/x[1]

def e1_Zn(x,n):
    """
    n is a element in Integer Sets.
    x = [a,b] <=> a*t = b (mod n)
    """
    (a,b,e,m) = (x[0],x[1],0,n)
    (c,d) = (m//a,m%a)
    while d :
        (m,a,e,b) = (a,d,b,e-c*b)
        (c,d) = (m//a,m%a)
    if x[1]%a != 0:
        raise ValueError, "No Solution"
    else:
        return (b//a)%n

def e2(x):
    """
    0 = x[0] + x[1]*t + x[2]*t**2
    """
    a = x[2]
    b = x[1]
    c = x[0]
    if b**2 - 4*a*c >= 0:
        sqrtd = math.sqrt(b**2 - 4*a*c)
    else:
        sqrtd = cmath.sqrt(b**2 - 4*a*c)
    return ((-b + sqrtd)/(2*a), (-b - sqrtd)/(2*a))

def e2_Fp(x,p):
    """
    p is prime
    f = x[0] + x[1]*t + x[2]*t**2
    """
    a = x[2]%p
    b = x[1]%p
    c = x[0]%p
    if a == 0:
        return [e1_Zn([c, b], p)]
    if p == 2:
        solutions = []
        if x[0] % 2 == 0:
            solutions.append(0)
        if (x[0] + x[1] + x[2]) % 2 == 0:
            solutions.append(1)
        if len(solutions) == 1:
            return solutions * 2
        return solutions
    d = b**2 - 4*a*c
    if arith1.legendre(d, p) == -1:
        return []
    sqrtd = arith1.modsqrt(d, p)
    a = arith1.inverse(2*a, p)
    return [((-b+sqrtd)*a)%p, ((-b-sqrtd)*a)%p]

def e3(x):
    """
    0 = x[0] + x[1]*t + x[2]*t**2 + x[3]*t**3
    """
    a = x[2]/x[3]
    b = x[1]/x[3]
    c = x[0]/x[3]
    p = b - (a**2)/3
    q = 2*(a**3)/27 - a*b/3 + c
    w = (-1 + cmath.sqrt(-3)) / 2
    W = (1, w, w.conjugate())
    k = -q/2 + cmath.sqrt((q**2)/4 + (p**3)/27)
    l = -q/2 - cmath.sqrt((q**2)/4 + (p**3)/27)
    m = k ** (1/3)
    n = l ** (1/3)

    # choose n*W[i] by which m*n*W[i] be the nearest to -p/3
    checker = [abs(3*m*n*z + p) for z in W]
    n = n * W[checker.index(min(checker))]

    equ = []
    for i in range(3):
        equ.append(W[i]*m + W[-i]*n - a/3)
    return equ

def e3_Fp(x,p):
    """
    p is prime
    0 = x[0] + x[1]*t + x[2]*t**2 + x[3]*t**3
    """
    x.reverse()
    lc_inv = finitefield.FinitePrimeFieldElement(x[0], p).inverse()
    coeff = []
    for c in x[1:]:
        coeff.append((c * lc_inv).n)
    equ=[]
    i=0
    while i<p:
        if (i**3+coeff[0]*i**2+coeff[1]*i+coeff[2])%p==0:
            equ.append(i)
            break
        else:
            i=i+1
    if len(equ)==0:
        return equ
    X=e2_Fp([coeff[1]+coeff[0]*equ[0]+equ[0]**2,coeff[0]+equ[0],1],p)
    if len(X)!=0:
        equ.append(X[0])
        equ.append(X[1])
    return equ

def Newton(f,initial=1,repeat=250):
    """
    f = a_n + a_(n-1) * x + ... + a_0 * x ** n
    """
    length = len(f)
    df = []
    i = 1
    j = 1
    while i != length:
        df.append(j*f[i])
        i = i + 1
        j = j + 1
    l = initial
    for k in range(repeat):
        i = 0
        j = 0
        coeff = 0
        dfcoeff = 0
        while i != length - 1:
            coeff = coeff + f[i]*(l**j)
            dfcoeff = dfcoeff + df[i]*(l**j)
            i = i + 1
            j = j + 1
        coeff = coeff + f[i]*(l**j)
        tangent = [coeff-l*dfcoeff,dfcoeff]
        if coeff == 0:
            return l
        elif coeff != 0 and dfcoeff == 0:
            raise ValueError,"There is not solution or Choose different initial"
        else:
            if l == e1(tangent):
                return l
            else:
                l = e1(tangent)
    return l

def SimMethod(g, initials=None, newtoninitial=1.0, repeat=250):
    """
    Return zeros of a polynomial given as a list.

    - g is the list of the polynomial coefficient in ascending order.
    - initial (optional) is a list of initial approximations of zeros.
    - newtoninitial (optional) is an initial value for Newton method to
      obtain an initial approximations of zeros if 'initial' is not given.
      default value is 1.0.
    - repeat (optional) is the number of iteration. default is 250.
    """
    if initials is None:
        z = _initialize(g, newtoninitial)
    else:
        z = initials

    f = polynomial.OneVariableDensePolynomial(g, 'x')
    deg = f.degree()
    df = f.differentiate('x')

    value_list = [f(z[i]) for i in range(deg)]
    for loop in range(repeat*deg):
        sigma_list = [0] * deg
        for i in range(deg):
            if not value_list[i]:
                continue
            sigma = 0
            for j in range(i):
                sigma += 1 / (z[i] - z[j])
            for j in range(i+1, deg):
                sigma += 1 / (z[i] - z[j])
            sigma_list[i] = sigma

        for i in range(deg):
            if not value_list[i]:
                continue
            ratio = value_list[i] / df(z[i])
            z[i] -= ratio / (1 - ratio*sigma_list[i])
            value_list[i] = f(z[i])

    return z

def _initialize(g, newtoninitial=1):
    """
    create initial values of equation given as a list g.
    """
    q = [-abs(c) for c in g[:-1]]
    q.append(abs(g[-1]))
    r = Newton(q, newtoninitial)

    deg = len(g) - 1
    center = -g[-2]/(deg*g[-1])
    about_two_pi = 6
    angular_step = cmath.exp(1j * about_two_pi / deg)
    angular_move = r
    z = []
    for i in range(deg):
        z.append(center + angular_move)
        angular_move *= angular_step

    return z
