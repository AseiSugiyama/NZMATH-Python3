"""
Multiplicative number theoretic functions.
"""

import nzmath.factor.methods as factor_methods
import prime

def euler(n):                    
    """
    Euler totient function.
    It returns the number of relatively prime numbers to n smaller than n.
    """
    if n == 1:
        return 1
    if prime.primeq(n):
        return n-1
    f = factor_methods.factor(n)
    t = 1
    for p, e in f:
        if e > 1:
            t *= pow(p, e-1) * (p-1)
        else:
            t *= p-1
    return t

def moebius(n):
    """
    Moebius function.
    It returns:
      -1  if n has odd distinct prime factors,
       1  if n has even distinct prime factors, or
       0  if n has a squared prime factor. 
    """
    if n == 1:
        return 1
    if prime.primeq(n):
        return -1
    f = factor_methods.factor(n)
    m = 1
    for p, e in f:
        if e > 1:
            return 0
        m = -m
    return m

def sigma(m, n):
    """
    Return the sum of m-th powers of the factors of n.
    """
    if n == 1:
        return 1
    if prime.primeq(n):
        return 1 + n**m
    f = factor_methods.factor(n)
    s = 1
    for p, e in f:
        t = 1
        for i in range(1,e+1):
            t += (p**i)**m
        s *= t
    return s

