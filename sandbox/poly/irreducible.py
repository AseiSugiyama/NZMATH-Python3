"""
irreducible -- tests for irreducibility of integer coefficient polynomials.

REFERENCE:
V.V.Prasolov. 'Polynomials',
Algorithms and Computation in Mathematics Volume 11, Springer-Verlag (2004).
"""

import nzmath.arith1 as arith1
import nzmath.combinatorial as combinatorial
import nzmath.gcd as gcd
import nzmath.prime as prime


def trivial(target):
    """
    Return True if target is irreducible, False if reducible
    or None if undecidable.

    This trivial function checks the followings:
    (1) if the constant term is zero, the polynomial is reducible.
    (2) if not (1) and the degree is <= 1, the polynomial is irreducible.
    """
    if not target[0]:
        return False
    elif target.degree() <= 1:
        return True
    else:
        return None


def dumas(target, p):
    """
    Return True if target is irreducible, False if reducible
    or None if undecidable.

    Dumas's criterion is the following.  Let f = \sum a_i X^i be a
    integer coefficient polynomial with degree n, and p be a prime
    number.  f is irreducible if
    (I) gcd(n, v(a_n) - v(a_0)) == 1
        (where v(m) denotes the number e that p**e divide m but
        p**(e+1) doesn't)
    (II) for any i (0 < i < n), (i, v(a_i)) is above the line connecting
        (0, v(a_0)) and (n, v(a_n)).
    This criterion includes Eisenstein's case.
    """
    segments = dict((d, arith1.vp(c, p=p)[0]) for (d, c) in target)
    # (I)
    degree = target.degree()
    if abs(gcd.gcd(degree, segments[degree] - segments[0])) != 1:
        return None
    # (II)
    #(segments[degree] - segments[0]) / degree * x + segment[0] < segments[x]
    slope = segments[degree] - segments[0]
    if all(slope * x <= degree * (v - segments[0]) for x, v in segments.iteritems()):
        return True
    # the criterion doesn't work
    return None


def perron(target):
    """
    Return True if target is irreducible, False if reducible
    or None if undecidable.

    Perron's criterion is the following.  Let f = \sum a_i X^i be a
    monic integer coefficient polynomial.  Then, if one of the
    following conditions holds, f is irreducible.
    (1) |a{n-1}| > 1 + \sum_{i=0}^{n-2} |ai|,
    (2) |a{n-1}| >= 1 + \sum_{i=0}^{n-2} |ai| and f(1) nor f(-1) isn't zero.
    """
    # precondition
    if target.leading_coefficient() != 1:
        return None

    # the criterion
    degree = target.degree()
    rhs = 1 + sum(abs(c) for (d, c) in target if d < degree - 1)
    # (1)
    if abs(target[degree - 1]) > rhs:
        return True
    # (2)
    elif abs(target[degree - 1]) >= rhs and target(1) != 0 and target(-1) != 0:
        return True

    # undecided
    return None


def osada(target):
    """
    Return True if target is irreducible, False if reducible
    or None if undecidable.

    Osada's criterion is the following.  Let f = \sum a_i X^i be a
    monic integer coefficient polynomial whose constant term is a
    prime number p or -p.  Then, if one of the following conditions
    holds, f is irreducible.
    (1) p > 1 + \sum_{i=1}^{n-1} |ai|,
    (2) p >= 1 + \sum_{i=1}^{n-1} |ai| and f has no root with
        absolute value 1.

    Note that the second case is not implemented.
    """
    # precondition
    if target.leading_coefficient() != 1:
        return None
    if not prime.primeq(abs(target[0])):
        return None

    # the criterion
    degree = target.degree()
    rhs = 1 + sum(abs(c) for (d, c) in target if 0 < d < degree - 1)
    # (1)
    if abs(target[0]) > rhs:
        return True

    # undecided
    return None


def polya(target):
    """
    Return True if target is irreducible, False if reducible
    or None if undecidable.

    P\'olya's criterion is the following.  Let f = \sum a_i X^i be a
    integer coefficient polynomial with degree n, and let m be the
    floor of (n+1)/2.  If there exists a set of distinct integers
    {b1,...,bn} such that 0 < |f(bi)| < 2**(-m)*m!, then f is
    irreducible.
    """
    degree = target.degree()
    m = (degree + 1) // 2
    #ubound = combinatorial.factorial(m) // 2**m
    mfact = combinatorial.factorial(m)
    mpow = 2**m

    satisfy = 0
    # We don't know how to search bi's, so here we just check in range
    # [-degree, degree).
    for i in range(-degree, degree):
        val = abs(target(i))
        if not val:
            return False
        #elif val < ubound:
        elif val * mpow < mfact:
            satisfy += 1
        if satisfy == degree:
            return True

    return None
