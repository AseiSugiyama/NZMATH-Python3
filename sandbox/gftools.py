"""
gftools.py - efficiently interpreter tools for Galois fields.
function symbols starting with ``u_'' means ``unstable'', use sandbox version
of finitefield (module sandbox.finitefield).
"""
from __future__ import division
import logging
import operator

import nzmath.polynomial
import nzmath.finitefield
import sandbox.finitefield as u_finitefield

_log = logging.getLogger('sandbox.fftools')

polynomial = nzmath.polynomial
finitefield = nzmath.finitefield


def PolynomialoverGF(fieldrepr, coeffs, symbol="#1"):
    """ Create OneVariablePolynomial from coeffs with mapping
     FinitePrimeField(char).createElement.
    """
    if isinstance(fieldrepr, (int, long)):
        field = finitefield.FinitePrimeField(fieldrepr)
    elif isinstance(fieldrepr, (finitefield.FinitePrimeField,
                                finitefield.FiniteExtendedField)):
        field = fieldrepr

    if type(coeffs) is dict:
        return polynomial.OneVariableSparsePolynomial(coeffs, symbol, field)
    elif type(coeffs) is list:
        coefficients=map(field.createElement, coeffs)
        return polynomial.OneVariableDensePolynomial(coefficients, symbol)

def GaloisField(char, modulus=None):
    """ Create FiniteField from modulus.
    modulus must be a form of PolynomialoverGF or PolynomialoverGF.

    GaloisField is aliased as GF or FiniteField .
    """
    if isinstance(modulus, list):
        polyGF = PolynomialoverGF(char, modulus)
        return finitefield.FiniteExtendedField(char, polyGF)
    if type(modulus) is polynomial.OneVariablePolynomialCharNonZero:
        return finitefield.FiniteExtendedField(char, modulus)
    if type(char) is polynomial.OneVariablePolynomialCharNonZero:
        character = char.getCoefficientRing().getCharacteristic()
        return finitefield.FiniteExtendedField(character, char)
    elif not modulus:
        return finitefield.FinitePrimeField(char)
    raise ValueError("modulus must be sequence or OneVariablePolynomialCharNonZero")

def GFPolynomialRing(field, symbol="#1"):
    """ return polynomial ring of Galois Field.

     GFPolynomialRing is aliased as GFPolyRing .
    """
    if type(field) is finitefield.FiniteExtendedField or \
           finitefield.FinitePrimeField:
        return polynomial.PolynomialRing(field, symbol)
    raise ValueError("field must be GaloisField.")

def GeneratorofGFPolyRing(field, symbol="#1"):
    """ return set of generator of polynomial ring of Galois Field.
     set is as symbol, (1/GF, root/GF(if extended)) .

     GeneratorofGFPolyRing is aliased as GenofGFPolyRing .
    """
    ring = GFPolynomialRing(field, symbol)
    if type(field) is finitefield.FiniteExtendedField:
        return ring.createElement([0,1]), (field.one, \
               field.createElement(field.char))
    elif type(field) is finitefield.FinitePrimeField:
        return ring.createElement([0,1]), (field.one)
    raise ValueError("field must be GaloisField.")

def strFieldRepresent(field, symbol='x'):
    """ return a mathematical string of galois field.
    """
    if type(field) is finitefield.FiniteExtendedField:
        char = field.getCharacteristic()
        ideals = field.modulus.generators
        ideal = ideals.pop()
        idealstr = str(ideal(symbol))
        for i in ideals:
            idealstr += ","+str(i(symbol))
        return 'F_'+str(char)+'['+symbol+'] / ('+str(idealstr)+')'
    elif type(field) is finitefield.FinitePrimeField:
        char = field.getCharacteristic()
        return 'F_'+str(char)
    raise ValueError("field must be GaloisField.")

# follows are for unstable(sandbox) version.
def u_FpPolynomial(char, coeffs):
    """ Create FinitePrimeFieldPolynomial from coeffs with mapping
     FinitePrimeField(char).createElement.
    """
    field = u_finitefield.FinitePrimeField(char)
    if type(coeffs) is dict:
        return u_finitefield.FinitePrimeFieldPolynomial(coeffs, field)
    if isinstance(coeffs, list):
        coefficients = []
        for index in range(len(coeffs)):
            coefficients.append([index, coeffs[index]])
        return u_finitefield.FinitePrimeFieldPolynomial(coefficients, field)

def u_FiniteField(char, modulus=None):
    """ Create FiniteField from modulus.
    modulus must be a form of PolynomialoverFp.
    """
    if type(modulus) is list:
        # FIXME: Undefined variable 'FpPolynomial'
        poly_Fp = FpPolynomial(char, modulus)
        return u_finitefield.FiniteExtendedField(char, poly_Fp)
    if type(modulus) is u_finitefield.FinitePrimeFieldPolynomial:
        return u_finitefield.FiniteExtendedField(char, modulus)
    elif not modulus:
        return u_finitefield.FinitePrimeField(char)

# this is alias name.
GFPoly = PolynomialoverGF
FiniteField = GaloisField
GF = GaloisField
GFPolyRing = GFPolynomialRing
GenGFPolyRing = GeneratorofGFPolyRing


u_FpPoly = u_FpPolynomial
