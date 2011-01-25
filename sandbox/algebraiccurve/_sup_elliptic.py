""" support modules of elliptic curves. (private) 
"""
from __future__ import division

import nzmath.poly.uniutil as univar
import nzmath.poly.multiutil as multivar
import nzmath.poly.termorder as termorder

# sandbox(from future)
import sandbox.finitefield as finitefield

# symbol aliases
univar.special_ring_table[finitefield.FinitePrimeField] = univar.FinitePrimeFieldPolynomial
MultiVarPolynomial = multivar.MultiVariableSparsePolynomial

# polynomial wrapper
def UniVarPolynomial(dict,coeffring=None):
    return univar.OneVariableSparsePolynomial(dict,"x",coeffring)

# string format wrapper
def strUniPoly(poly, symbol="X", asc=True):
    """return format string of UniVarPolynomial"""
    return termorder.UnivarTermOrder(cmp).format(poly, symbol, asc)

def strMultiPoly(poly, symbol=["X","Y"], asc=True):
    """return format string of MultiVarPolynomial for EC"""
    return termorder.MultivarTermOrder(cmp).format(MultiVarPolynomial(poly,symbol), symbol, asc)

#def _isscalar(elem, field=None):
#    """
#    test whether 'elem' is scalar or not.
#    """
#    return isinstance(elem, (int, long))

def PolyMod(f, g):
    """
    return f (mod g)
    """
    return f % g

def GCD(f, g):
    # other cases
    return f.gcd(g)

def PolyPow(f, d, g):
    """
    this returns (f^d)%g
    """
    return g.mod_pow(f, d)

def PolyMulRed(multipliees, poly):
    """
    multipliees[*] is (OneSparsePoly,int,long)
    poly is OneSparsePoly
    """
    if poly.degree() < 1:
        return poly.getRing().zero
    product = multipliees.pop()
    for factor in multipliees:
        #print type(product)
        #if factor.degree() >= poly.degree():
        #factor = PolyMod(factor, poly)
        #if factor == 0:
        #    return 0
        product = product * factor
        if product.degree() >= poly.degree():
            product = PolyMod(product, poly)
            if not product:
                break
    return product


