"""
linrec -- Linearly Recurrent Sequence

Reference:
N.B. Atti, G.M. Diaz-Toca, H. Lombardi 'The Berlekamp-Massey Algorithm
revisited' AAECC (2006) 17:75-82.
"""

import nzmath.ring as ring
import nzmath.poly.uniutil as uniutil


def minpoly(firstterms):
    """
    Return the minimal polynomial having at most degree n of of the
    linearly recurrent sequence whose first 2n terms are given.
    """
    field = ring.getRing(firstterms[0])
    r_0 = uniutil.polynomial({len(firstterms):field.one}, field)
    r_1 = uniutil.polynomial(enumerate(reversed(firstterms)), field)
    poly_ring = r_0.getRing()
    v_0 = poly_ring.zero
    v_1 = poly_ring.one
    n = len(firstterms) // 2

    while n <= r_1.degree():
        q, r = divmod(r_0, r_1)
        v_0, v_1 = v_1, v_0 - q*v_1
        r_0, r_1 = r_1, r
    return v_1.scalar_mul(v_1.leading_coefficient().inverse())
