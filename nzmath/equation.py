from __future__ import division
import cmath
import math
import gcd

def e2(x):
    a = x[0]    
    b = x[1]
    c = x[2]

    return (((-1)*b+cmath.sqrt(b**2-4*a*c))/(2*a),((-1)*b-cmath.sqrt(b**2-4*a*c))/(2*a))

def e3(x):
    a = x[1] / x[0]
    b = x[2] / x[0]
    c = x[3] / x[0]

    p = b - (a**2)/3
    q = 2*(a**3)/27 - a*b/3 + c
    w = ( -1 + cmath.sqrt(3) * 1j ) / 2

    k = -q/2 + math.sqrt( (q**2)/4 + (p**3)/27)
    l = -q/2 - math.sqrt( (q**2)/4 + (p**3)/27)
    
    if k < 0:
       m = -math.pow(abs(k), 1/3)
      
    else:
	m = math.pow(k, 1/3)
   
    n = -math.pow(abs(l), 1/3)
    
    equ = []

    i=0

    while i<=2:
	x = (w**i) * m + (w**(3-i)) * n - a/3
	equ.append(x)
	i = i + 1

    return equ


  
