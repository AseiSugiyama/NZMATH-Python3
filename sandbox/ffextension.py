"""
ffextension.py - Extention of FiniteExtendedField .
"""
from __future__ import division
import logging
import operator

import nzmath.arith1 as arith1
import nzmath.finitefield as finitefield
import nzmath.polynomial as polynomial
import nzmath.compatibility

_log = logging.getLogger('sandbox.fftools')

FiniteField = finitefield.FiniteExtendedField
FiniteFieldElement = finitefield.FiniteExtendedFieldElement

class FiniteFieldExtension (FiniteField):
    """
    FiniteFieldExtension is a class for finite field, whose cardinality
    q = (p**n)**e with a prime p and e, n>1. It is usually called F_q or GF(q).
    This class only deals with extension of finitefield.FiniteExtendedField .
    """
    def __init__(self, base_field, modulus):
        """
        FiniteFieldExtension(p, n_or_modulus) creates an extension field
        of a finite field.
        base_field must be finitefield.FiniteExtendedField or FiniteFieldExtension object.
        n_or_modulus can be:
          1) a polynomial in a polynomial ring of base_field with
             degree greater than 1.
          2) an ideal of the polynomial ring base_field[#1] with
             degree greater than 1.
        """
        if isinstance(base_field, finitefield.FinitePrimeField):
            raise TypeError("base field must be FiniteExtendedField.")
        finitefield.FiniteField.__init__(self, base_field.getCharacteristic())
        if isinstance(modulus, polynomial.OneVariablePolynomialCharNonZero):
            if isinstance(modulus.getCoefficientRing(), type(base_field)):
                if modulus.degree() > 1 and modulus.isIrreducible():
                    self.basefield = base_field
                    self.ext_degree = modulus.degree()
                    self.degree = self.ext_degree * base_field.degree
                    self.modulus = polynomial.OneVariablePolynomialIdeal(
                        modulus("#1"),
                        modulus("#1").getRing())
                else:
                    raise ValueError("modulus must be polynomial over base field.")
            else:
                raise TypeError("modulus must be F_p polynomial.")
        # FIXME: Undefined variable 'n_or_modulus'
        elif isinstance(n_or_modulus, polynomial.OneVariablePolynomialIdeal):
            if n_or_modulus.ring == polynomial.PolynomialRing(base_field, ["#1"]):
                if modulus.generators[0].degree() > 1:
                    self.basefield = base_field
                    self.modulus = modulus
                    self.ext_degree = self.modulus.generators[0].degree()
                    self.degree = self.ext_degree * base_field.degree
                else:
                    raise ValueError("modulus must be polynomial over base field.")
            else:
                raise TypeError("modulus must be in polynomial ring of base field with variable symbol '#1'.")
        else:
            raise TypeError("degree or modulus must be supplied.")

    def createElement(self, seed):
        """
        Create an element of the field.
        """
        # FIXME: Undefined variable 'FinitFieldExtensionElement'
        if isinstance(seed, (int, long)):
            expansion = arith1.expand(seed, card(self.basefield))
            return FinitFieldExtensionElement(
                polynomial.OneVariableDensePolynomial(
                expansion, "#1", self.basefield),
                self)
        elif isinstance(seed, polynomial.OneVariablePolynomial):
            return FiniteFieldExtensionElement(seed("#1"), self)
        else:
            try:
                # lastly check sequence
                return FiniteFieldExtensionElement(
                    polynomial.OneVariableDensePolynomial(
                    list(seed), "#1", self.basefield),
                    self)
            except TypeError:
                raise TypeError("seed %s is not an appropriate object." % str(seed))

    def __repr__(self):
        return "%s(%d, %s)" % (self.__class__.__name__, repr(self.basefield), repr(self.modulus))


    def issuperring(self, other):
        """
        Report whether the field is a superring of another ring.
        """
        if self is other:
            return True
        if isinstance(other, FiniteFieldExtension):
            if self.char == other.char and not (self.degree % other.degree):
                return True
            return False
        if isinstance(other, finitefield.FiniteExtendedField):
            if self.char == other.char and not (self.degree % other.degree):
                return True
            return False
        if isinstance(other, finitefield.FinitePrimeField):
            if self.char == other.getCharacteristic():
                return True
            return False
        try:
            return other.issubring(self)
        except:
            return False

    def issubring(self, other):
        """
        Report whether the field is a subring of another ring.
        """
        if self is other:
            return True
        if isinstance(other, (finitefield.FinitePrimeField, \
                              finitefield.FiniteExtendedField) ):
            return False
        if isinstance(other, FiniteFieldExtension):
            if self.char == other.char and not (other.degree % self.degree):
                return True
            return False
        try:
            return other.issuperring(self)
        except:
            return False

    def __contains__(self, elem):
        """
        Report whether elem is in field.
        """
        # FIXME: Undefined variable 'FiniteExtendedField'
        if isinstance(elem, FiniteFieldExtensionElement):
            elemgens = elem.getRing().modulus.generators
            if elemgens == self.modulus.generators:
                return True
            else:
                comparefield = self.basefield
                while not isinstance(comparefield, FiniteExtendedField):
                    if elemgens == comparefield.modulus.generators:
                        return True
                    comparefield = comparefield.basefield
                return False
        elif isinstance(elem, finitefield.FiniteExtendedFieldElement):
            elemring = elem.getRing().modulus.generators[0].getCoefficientRing()
            if elemring == self.basefield:
                return True
            else:
                comparefield = self.basefield
                while not isinstance(comparefield, FiniteExtendedField):
                    comparefield = comparefield.basefield
                if elemring == comparefield:
                    return True
                return False
        elif isinstance(elem, finitefield.FinitePrimeFieldElement) and \
                 elem.getRing().getCharacteristic() == self.getCharacteristic():
            return True
        return False

    def __eq__(self, other):
        """
        Equality test.
        """
        if isinstance(other, FiniteFieldExtension):
            return self.char == other.char and self.degree == other.degree
        return False

    def getBaseField(self):
        """ Return base field.
        """
        return self.basefield

    # properties
    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = FiniteFieldExtensionElement(
                polynomial.OneVariableDensePolynomial(
                [1], "#1", self.basefield),
                self)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = FiniteFieldExtensionElement(
                polynomial.OneVariableDensePolynomial(
                [], "#1", self.basefield),
                self)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


class FiniteFieldExtensionElement (FiniteFieldElement):
    """
    FiniteFieldExtensionElement is a class for an element of FiniteFieldExtension.
    """
    def __init__(self, representative, basefield):
        """
        FiniteFieldExtensionElement(representative, field) creates
        an element of the finite extended field.

        The argument representative must be an field.basefield polynomial.

        Another argument field mut be an instance of
        FiniteFieldExtension.
        """
        # FIXME: Undefined variable 'field'
        if isinstance(field, FiniteFieldExtension):
            self.field = field
        else:
            raise TypeError("wrong type argument for field.")
        if (isinstance(representative, polynomial.OneVariablePolynomial) and
            isinstance(representative.getCoefficientRing(), field.basefield)):
            self.rep = self.field.modulus.reduce(representative)
        else:
            raise TypeError("wrong type argument for representative.")

    def getRing(self):
        """
        Return the field to which the element belongs.
        """
        return self.field

    def __add__(self, other):
        # FIXME: Undefined variable 'FinitePrimeField'
        # FIXME: Instance of 'FiniteFieldExtensionElement' has no 'basefield' member
        if isinstance(other, (int, long)) and (not other):
            return self.__class__(self.rep, self.field)
        if other.getRing() == FinitePrimeField.getInstance(self.field.getCharacteristic()):
            seed = self.field.createElement(other.n)
            sum_ = self.field.modulus.reduce(self.rep + seed.rep)
        targetfield = self.basefield
        if other.getRing() == targetfield:
            seed = self.field.createElement([other])
            sum_ = self.field.modulus.reduce(self.rep + seed.rep)
        elif other.field == self.field:
            sum_ = self.field.modulus.reduce(self.rep + other.rep)
        else:
            if isinstance(targetfield, finitefield.FiniteExtendedField):
                raise TypeError("wrong type argument for computation.")

            # recursive field extension form other.basefield to self.field
            sum_base = targetfield.zero + other
            seed = self.field.createElement([sum_base])
            sum_ = self.field.modulus.reduce(self.rep + seed.rep)

            # follows are not recursive version.

            #targetfield = [self.basefield]
            #count = 0
            #while not isinstance(targetfield[count], finitefield.FiniteExtendedField):
            #    if other.getRing() == targetfield[count]:
            #        targetfield_base = targetfield.pop()
            #        seed = targetfield_base.createElement([other])
            #        for target in targetfield.reverse():
            #            seed = target.createElement([seed])
            #        seed = self.field.createElement([seed])
            #        sum_ = self.field.modulus.reduce(self.rep + seed.rep)
            #        return self.__class__(sum_, self.field)
            #    targetfield.append[targetfield.basefield]
            #    count += 1
            #raise TypeError("wrong type argument for computation.")
        return self.__class__(sum_, self.field)

    __radd__ = __add__

    def __sub__(self, other):
        # FIXME: Undefined variable 'FinitePrimeField'
        # FIXME: Instance of 'FiniteFieldExtensionElement' has no 'basefield' member
        if isinstance(other, (int, long)) and (not other):
            return self.__class__(self.rep, self.field)
        if other.getRing() == FinitePrimeField.getInstance(self.field.getCharacteristic()):
            seed = self.field.createElement(other.n)
            dif = self.field.modulus.reduce(self.rep - seed.rep)
        targetfield = self.basefield
        if other.getRing() == targetfield:
            seed = self.field.createElement([other])
            dif = self.field.modulus.reduce(self.rep - seed.rep)
        elif other.field == self.field:
            dif = self.field.modulus.reduce(self.rep - other.rep)
        else:
            if isinstance(targetfield, finitefield.FiniteExtendedField):
                raise TypeError("wrong type argument for computation.")
            dif_base = targetfield.zero + other # not subtract!
            seed = self.field.createElement([dif_base])
            dif = self.field.modulus.reduce(self.rep - seed.rep)
        return self.__class__(dif, self.field)

    def __mul__(self, other):
        # FIXME: Undefined variable 'FinitePrimeField'
        # FIXME: Instance of 'FiniteFieldExtensionElement' has no 'basefield' member
        if isinstance(other, (int, long)):
            seed = self.field.createElement(other % self.field.getCharacteristic())
            prod = self.field.modulus.reduce(self.rep * seed.rep)
        elif other.getRing() == FinitePrimeField.getInstance(self.field.getCharacteristic()):
            seed = self.field.createElement(other.n)
            prod = self.field.modulus.reduce(self.rep * seed.rep)
        targetfield = self.basefield
        if other.getRing() == targetfield:
            seed = self.field.createElement([other])
            prod = self.field.modulus.reduce(self.rep * seed.rep)
        elif other.field == self.field:
            prod = self.field.modulus.reduce(self.rep * other.rep)
        else:
            if isinstance(targetfield, finitefield.FiniteExtendedField):
                raise TypeError("wrong type argument for computation.")
            prod_base = targetfield.zero + other # ext. with mult. is nonsence
            seed = self.field.createElement([prod_base])
            prod = self.field.modulus.reduce(self.rep * seed.rep)
            raise NotImplementedError
        return self.__class__(prod, self.field)

    def __eq__(self, other):
        if self.field == other.field:
            if not self.field.modulus.reduce(self.rep - other.rep):
                return True
        return False

    def __nonzero__(self):
        return self.rep.__nonzero__()
