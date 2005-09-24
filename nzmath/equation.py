from __future__ import division
import arith1
import cmath
import finitefield
import gcd
import math
import polynomial
import rational
import imaginary

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
        return b//a
    
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
    a=x[2]%p    
    b=x[1]%p
    c=x[0]%p
    if arith1.legendre(a,p)!=1:
        return []
    else:
        sqrtd = arith1.modsqrt(b**2-4*a*c,p)
    a=arith1.inverse(2*a,p)
    return (((-b+sqrtd)*a)%p,((-b-sqrtd)*a)%p)

def e3(x):
    """
    0 = x[0] + x[1]*t + x[2]*t**2 + x[3]*t**3
    """
    a = x[2]/x[3]
    b = x[1]/x[3]
    c = x[0]/x[3]
    p = b - (a**2)/3
    q = 2*(a**3)/27 - a*b/3 + c
    w = ( -1 + cmath.sqrt(-3)) / 2
    k = -q/2 + cmath.sqrt((q**2)/4 + (p**3)/27)
    l = -q/2 - cmath.sqrt((q**2)/4 + (p**3)/27)
    m = k ** (1/3)
    n = -(abs(l) ** (1/3))

    equ = []
    for i in range(3):
        x = (w**i)*m +(w**(3-i))*n - a/3
        equ.append(x)
    return equ

def e3_Fp(x,p):
    """
    p is prime
    0 = x[0] + x[1]*t + x[2]*t**2 + x[3]*t**3
    """
    x.reverse()
    coeff=[]
    i=1
    while i<len(x):
        coeff.append(int(finitefield.FinitePrimeField(p).createElement(rational.Rational(x[i],x[0])).n))
        i=i+1
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
    X=e2_Fp([1,coeff[0]+equ[0],coeff[1]+coeff[0]*equ[0]+equ[0]**2],p)
    if len(X)!=0:
        equ.append(X[0])
        equ.append(X[1])
    return equ

"""
def solve_Fp(poly,p):
    if poly.degree()==1:
        return 0
    elif poly.degree()==2:
        return 0
    elif poly.degree()==3:
        return 0
    else:
        return 0
"""
    
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
    
def SimMethod(g,NewtonInitial=1,repeat=250):
    """
     g is list , m is the number of steps: ( = a_0*x^n + ... + a_(n-1)*x^1 + a_n*x^0 => [a_n, a_(n-1), ... , a_0] (a_0 != 0 and a_i is complex number))
    """
    f = polynomial.OneVariableDensePolynomial(g,'x')
    deg = f.degree()
    q=[]
    for i in range(0,deg):
        q.append(-abs(f[i]))
    q.append(abs(f[deg]))
    print q
    df = f.differentiate('x')
    r = Newton(q,NewtonInitial)
    print r
    b = -f[deg-1]/(deg*f[deg])
    z = []
    for i in range(deg):
        z.append(b+r*cmath.exp((1j)*(2*i*(math.pi)/deg+3/(2*deg))))
    
    for loop in range(repeat):
        sigma_list = []
        for i in range(len(z)):
            sigma = 0
            for j in range(len(z)):
                if j != i:
                    sigma = sigma + 1/(z[i] - z[j])
            sigma_list.append(sigma)

        k = []
        for i in range(len(z)):
            k.append(-f(z[i])/df(z[i])/(1-((-f(z[i])/df(z[i]))*sigma_list[i])))
        
        for i in range(len(z)):
            z[i] = k[i] + z[i]

    return z

