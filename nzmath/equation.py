from __future__ import division
import arith1
import cmath
import finitefield
import gcd
import math
import prime
import random
import rational


# x is (list,tuple) 
def e2(x):
    """
    f=x[0]*t**2+x[1]*t+x[2]
    """
    a = x[0]
    b = x[1]
    c = x[2]
    if b**2 - 4*a*c >= 0:
        sqrtd = math.sqrt(b**2 - 4*a*c)
    else:
        sqrtd = cmath.sqrt(b**2 - 4*a*c)
    return ((-b + sqrtd)/(2*a), (-b - sqrtd)/(2*a))

def e2_Fp(x,p):
    """
    p is prime
    f=x[0]*t**2+x[1]*t+x[2]
    """
    a=x[0]%p    
    b=x[1]%p
    c=x[2]%p
    sqrtd = arith1.sqroot(b**2-4*a*c,p)
    a=arith1.inverse(2*a,p)
    return (((-b+sqrtd)*a)%p,((-b-sqrtd)*a)%p)

def e3(x):
    """
    f=x[0]*t**3+x[1]*t**2+x[2]*t+x[3]
    """
    a = x[1]/x[0]
    b = x[2]/x[0]
    c = x[3]/x[0]
    p = b - (a**2)/3
    q = 2*(a**3)/27 - a*b/3 + c
    w = ( -1 + cmath.sqrt(-3)) / 2
    k = -q/2 + math.sqrt((q**2)/4 + (p**3)/27)
    l = -q/2 - math.sqrt((q**2)/4 + (p**3)/27)
    if k < 0:
        m = -math.pow(abs(k), 1/3)
    else:
        m = math.pow(k, 1/3)
    n = -math.pow(abs(l), 1/3)
    equ = []

    for i in range(3):
        x = (w**i)*m +(w**(3-i))*n - a/3
        equ.append(x)
    return equ

def e3_Fp(x,p): # p is prime
    """
    p is prime
    f=x[0]*t**3+x[1]*t**2+x[2]*t+x[3]
    """
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
        raise ValueError,"function is irred"
    X=e2_Fp([1,coeff[0]+equ[0],coeff[1]+coeff[0]*equ[0]+equ[0]**2],p)
    equ.append(X[0])
    equ.append(X[1])
    return equ

def EA(f,m): # f is list , m is the number of steps: ( = a_0*x^n + ... + a_(n-1)*x^1 + a_n => [a_0, a_1, ... , a_n] (a_0 != 0 and a_i is complex number))
    if f[0] == 0 :
        raise ValueError, "Delate 0 of first"
    
    n = len(f) # size of f

    i = -2
    df=[] # differential (of polynomial)
    while abs(i) <= n :
        df.append(f[i]*(abs(i)-1))
        i = i - 1
    df.reverse()
    
    i = 0
    x = 0 # the number of "a_i != 0"
    ai = []
    while i < n :
        if f[i] != 0 : 
            x = x + 1
            ai.append(i)
        i = i + 1
    
    i = 2
    r = math.pow(abs(ai[1]/f[0])*x, 1/ai[1]) 
    while i < len(ai) :
        r0 = math.pow(abs(ai[i]/f[0])*x, 1/ai[i])
        if r < r0 :
            r = r0
        i = i + 1

    b = -ai[1]/((n-1)*f[0])

    z = []
    i = 1
    while i < n :
        z.append(b+r*cmath.exp((1j)*(2*(math.pi)*(i-1)/(n-1)+3/(2*(n-1)))))
        i = i + 1

    loop = 0
    
    while loop < m :
        fz = 0
        fzi = []
        i = 1
        j = 0
        while j < len(z) :
            while i <= n :
                fz = fz + f[-i]*(z[j]**(i-1))
                i = i + 1
            fzi.append(fz)
            j = j + 1

        dfz = 0
        dfzi = []
        i = 1
        j = 0
        while j < len(z) :
            while i <= n - 1 :
                dfz = dfz + df[-i]*(z[j]**(i-1))
                i = i + 1
            dfzi.append(dfz)
            j = j + 1

        divz = []
        i = 0
        while i < len(z) :
            divz.append(fzi[i]/dfzi[i])
            i = i + 1
    
        sigma = 0
        sigmai = []
        i = 0
        j = 0
        while i < len(z) :
            while j < len(z) :
                if j != i :
                    sigma = sigma + 1/(z[i] - z[j])
                j = j + 1
            sigmai.append(sigma)
            i = i + 1

        i = 0
        div = []
        while i < len(z) :
            div.append(divz[i]/(1-(divz[i]*sigmai[i])))
            i = i + 1

        zi = []
        i = 0
        while i < len(z) :
            zi.append(z[i]+div[i])
            i = i + 1

        print z

        z = zi
        loop = loop + 1
        
    return z

def EAr(f,m): # f is list , m is the number of approximation steps: ( = a_0*x^n + ... + a_(n-1)*x^1 + a_n => [a_0, a_1, ... , a_n] (a_0 != 0 and a_i is complex number))
    if f[0] == 0 :
        raise ValueError, "Delate 0 of first "
    
    n = len(f) # size of f

    i = -2
    df=[] # differential (of polynomial)
    while abs(i) <= n :
        df.append(f[i]*(abs(i)-1))
        i = i - 1
    df.reverse()

    z = []
    i = 1
    while i < n :
        z.append(random.random())
        i = i + 1

    loop = 0
    
    while loop < m :
        fz = 0
        fzi = []
        i = 1
        j = 0
        while j < len(z) :
            while i <= n :
                fz = fz + f[-i]*(z[j]**(i-1))
                i = i + 1
            fzi.append(fz)
            j = j + 1

        dfz = 0
        dfzi = []
        i = 1
        j = 0
        while j < len(z) :
            while i <= n - 1 :
                dfz = dfz + df[-i]*(z[j]**(i-1))
                i = i + 1
            dfzi.append(dfz)
            j = j + 1

        divz = []
        i = 0
        while i < len(z) :
            divz.append(rational.Rational(fzi[i],dfzi[i]))
            i = i + 1
    
        sigma = 0
        sigmai = []
        i = 0
        j = 0
        while i < len(z) :
            while j < len(z) :
                if j != i :
                    sigma = sigma + 1/(z[i] - z[j])
                j = j + 1
            sigmai.append(sigma)
            i = i + 1

        i = 0
        div = []
        while i < len(z) :
            div.append(divz[i]/(1-(divz[i]*sigmai[i])))
            i = i + 1

        zi = []
        i = 0
        while i < len(z) :
            zi.append(z[i]+div[i])
            i = i + 1
            
        z = zi
        loop = loop + 1

    return z


