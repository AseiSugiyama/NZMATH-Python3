from __future__ import division
import cmath
import math
import gcd
import arith1
import random
import rational
import prime

def e2(x):
    a = x[0]
    b = x[1]
    c = x[2]
    if b**2 - 4*a*c >= 0:
        sqrtd = math.sqrt(b**2 - 4*a*c)
    else:
        sqrtd = cmath.sqrt(b**2 - 4*a*c)
    return ((-b + sqrtd)/(2*a), (-b - sqrtd)/(2*a))

def e2Fp(x,p): # p is prime
    a=x[0]%p    
    b=x[1]%p
    c=x[2]%p
    a=arith1.inverse(2*a,p)
    sqrtd = arith1.sqroot(b**2-4*a*c,p)
    return (((-b+sqrtd)*a)%p,((-b-sqrtd)*a)%p)

def e3(x):
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

def e3Fp(x,p): # p is prime
    a0=arith1.inverse(x[0],p)
    a=x[1]*a0%p
    b=x[2]*a0%p
    c=x[3]*a0%p
    p=(b-(a**2)*arith1.inverse(3,p))%p
    q=(2*(a**3)*arith1.inverse(27,p)-a*b*arith1.inverse(3,p)+c)%p
    raise NotImplementedError,"now making"

    w=(-1+cmath.sqrt(3)*1j)/2
    k=-q/2+math.sqrt((q**2)/4+(p**3)/27)
    l=-q/2-math.sqrt((q**2)/4+(p**3)/27)
    if k<0:
        m=-math.pow(abs(k),1/3)
    else:
        m=math.pow(k,1/3)
    n=-math.pow(abs(l),1/3)
    equ=[]

    i=0
    while i<=2:
        x=(w**i)*m +(w**(3-i))*n-a/3
        equ.append(x)
        i=i+1
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


def e(p,n):
    if prime.primeq(p):
        i=0
        while i<p:
            #print i
            if pow(i,3,p)==n:
                return i
            i=i+1
    return 0

