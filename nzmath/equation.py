from __future__ import division
import cmath
import math
import gcd
import arith1

def e2(x):
    a=x[0]    
    b=x[1]
    c=x[2]
    return ((-b+cmath.sqrt(b**2-4*a*c))/(2*a),((-b-cmath.sqrt(b**2-4*a*c))/(2*a))

def e2Fp(x,p): # p is prime
    a=x[0]%p    
    b=x[1]%p
    c=x[2]%p
    a=arith1.inverse(2*a,p)
    c=arith1.sqroot(b**2-4*a*c,p)
    return (((-b+c)*a)%p,((-b-c)*a)%p)

def e3(x):
    a=x[1]/x[0]
    b=x[2]/x[0]
    c=x[3]/x[0]
    p=b-(a**2)/3
    q=2*(a**3)/27-a*b/3+c
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
