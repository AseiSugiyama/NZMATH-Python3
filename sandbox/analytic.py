"""
Analytic number theory
"""

from __future__ import division
import cmath
import math
import sys
import nzmath.bigrange as bigrange
import nzmath.rational as rational
import nzmath.prime as prime


def zeta_real(s):
    """
    zeta function for a real positive value s.

    zeta(s) = \sum n^{-s} = \prod (1 - p^{-s})^{-1}
    """
    zeta_s = 1
    for p in prime.generator():
        euler_factor = 1 - 1/p**s
        if euler_factor == 1:
            break
        zeta_s /= euler_factor
    return zeta_s


def Li(x):
    """
    Compute Li(x) approximately.
    Roughly speaking, its value has error at most 2.

      Li(x)
    = \int_{2}^{x} dt / \log t
    = \log\log x + Sigma_{i=1}^{\infty} (\log^i x) / (i * i!) - c

    The constant c is small |c| < 1, and ignored here.
    """
    s = _convertToRational(math.log(math.log(x)))
    logx = _convertToRational(math.log(x))
    for t in _li_terms(logx):
        s += t
        if t < rational.Rational(1, 10):
            break
    return s

def _li_terms(x):
    """
    Generate terms of infinite part of Li(x):
      x^i / (i * i!)
    for each i.
    """
    d = rational.Integer(1)
    t = x
    for i in bigrange.count(2):
        yield t
        t = t * x * (i-1) / (i * i)

def _convertToRational(x):
    """
    Convert to rational from:
        * int,
        * long, or
        * float.
    A complex object cannot be converted and raise TypeError.
    """
    if isinstance(x, float):
        retval = +rational.Rational(long(math.frexp(x)[0] * 2 ** 53), 2 ** (53 - math.frexp(x)[1]))
    elif isinstance(x, (int, long)):
        retval = rational.Integer(x)
    elif isinstance(x, complex):
        raise TypeError, "The real module cannot handle %s. Please use imaginary module." % x
    else:
        # fall back
        retval = rational.Rational(x)
    return retval


def gauss_sum(m, chi):
    """
    Return Gauss sum of character chi of modulo m.
    """
    r = 0
    z_m = cmath.exp(2J * cmath.pi / m)
    for n in range(1, m):
        r += chi(n) * z_m ** n
    return r

def L1(m, chi):
    """
    Return the value of L(1, chi) for given character chi of modulo m.

    >>> chi2 = lambda n: (0, 1, -1)[n % 3]
    >>> L1(3, chi2).real
    0.60459978807807258
    >>> 2 * math.pi * 1 / (6 * math.sqrt(3))
    0.60459978807807258

    The example above shows that the class number of Q(sqrt(-3)) is 1.
    """
    r = 0
    if chi(-1) == 1:
        for n in range(1, m):
            r -= _conj(chi(n)) * math.log(math.sin(n * math.pi / m))
    else:
        for n in range(1, m):
            r += _conj(chi(n)) * n
        r *= 1J * cmath.pi / m
    return r / _conj(gauss_sum(m, chi))

def _conj(z):
    """
    Return complex conjugate of given number z.
    """
    if hasattr(z, "conjugate"):
        return z.conjugate()
    else:
        return z
