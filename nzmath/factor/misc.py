"""
misc functions using factorization.
"""

import nzmath.gcd as gcd
import nzmath.arith1 as arith1
import nzmath.prime as prime
import nzmath.factor.methods as methods


def primePowerTest(n):
    """
    This program using Algo. 1.7.5 in Cohen's book judges whether
    n is of the form p**k with prime p or not.
    If it is True, then (p,k) will be returned,
    otherwise (n,0).
    """
    if n % 2 == 1:
        q = n
        while True:
            if not prime.primeq(q):
                a = 2
                while prime.spsp(n, a):
                    a += 1
                d = gcd.gcd(pow(a,q,q) - a, q)
                if d == 1 or d == q:
                    return (n, 0)
                else:
                    q = d
            else:
                p = q
                break
    else:
        p = 2

    k, q = arith1.vp(n, p)
    if q == 1:
        return (p, k)
    else:
        return (n, 0)

def allDivisors(n):
    """
    Return all factors divide n.
    """
    divisors = [1]
    for p, e in methods.factor(n):
        p_part = [p**j for j in range(1, e+1)]
        divisors += [n*q for n in divisors for q in p_part]
    divisors.sort()
    return divisors

def primeDivisors(n):
    """
    primeDivisors(n) returns the list of primes that divides n.
    """
    result = []
    for d, e in methods.factor(n):
        result.append(d)
    return result

def squarePart(n):
    """
    squarePart(n) returns the largest integer whose
    square divides n.
    """
    result = 1
    for d, e in methods.factor(n):
        if e >= 2:
            result *= d ** (e//2)
    return result
