"""

finite fields.

"""
import gcd
import prime
import rational
import ring

class FiniteField (ring.Field):
    def __len__(self):
        "Cardinality of the field"
        raise NotImplementedError

    def __nonzero__(self):
        return True

class FiniteFieldElement (ring.FieldElement):
    pass

import integerResidueClass

class FinitePrimeFieldElement (integerResidueClass.IntegerResidueClass, FiniteFieldElement):
    def __init__(self, representative, modulus):
        if modulus < 0:
            modulus = -modulus
        if prime.primeq(modulus):
            self.m = modulus
        else:
            raise ValueError, "modulus must be a prime."
        if isinstance(representative, rational.Rational):
            t = gcd.extgcd(representative.denominator, self.m)
            if t[2] != 1:
                raise ValueError, "No inverse of %s." % representative
            self.n = (representative.numerator * t[0]) % self.m
        elif isinstance(representative, (int, long)):
            self.n = representative % self.m
        elif isinstance(representative, integerResidueClass.IntegerResidueClass):
            assert representative.m == modulus
            self.n = representative.n
        else:
            raise NotImplementedError, repr(representative)

    def __repr__(self):
        return "FinitePrimeFieldElement(%d, %d)" % (self.n, self.m)

    def __str__(self):
        return "%d in F_%d" % (self.n, self.m)

    def getRing(self):
        return FinitePrimeField(self.m)

class FinitePrimeField (FiniteField):
    """

    FinitePrimeField is also known as F_p or GF(p).

    """
    def __init__(self, characteristic):
        self.char = characteristic
        self.properties = ring.CommutativeRingProperties()
        self.properties.setIsfield(True)

    def getCharacteristic(self):
        """

        Return the characteristic of the field.

        """
        return self.char

    def __eq__(self, other):
        if isinstance(other, FinitePrimeField) and self.char == other.char:
            return True
        return False

    def issubring(self, other):
        """

        Report whether another ring contains the field as a subring.

        """
        if self == other:
            return True
        elif isinstance(other, FiniteField) and other.getCharacteristic() == self.char:
            return True
        return False

    def issuperring(self, other):
        """

        Report whether the field is a superring of another ring.
        Since the field is a prime field, it can be a superring of
        itself only.

        """
        if self == other:
            return True
        return False

    def __contains__(self, elem):
        if isinstance(elem, FinitePrimeFieldElement) and elem.getModulus() == self.char:
            return True
        return False

    def createElement(self, seed):
        return FinitePrimeFieldElement(seed, self.char)

    def __len__(self):
        "Cardinality of the field"
        return self.char

    def __nonzero__(self):
        return True

import arith1
import polynomial

class FiniteExtendedField (FiniteField):
    """

    FiniteExtendedField is a class for finite field, whose cardinality
    q = p**n with a prime p and n>1. It is usually called F_q or GF(q).

    """
    def __init__(self, characteristic, n_or_modulus):
        """

        FiniteExtendedField(p, n_or_modulus) creates a finite field.
        characteristic must be prime. n_or_modulus can be:
          1) an integer greater than 1, or
          2) a polynomial in a polynomial ring of F_p with degree
             greater than 1.

        """
        if prime.primeq(characteristic):
            self.char = characteristic
        else:
            raise ValueError, "characteristic must be a prime."
        if isinstance(n_or_modulus, (int,long)):
            if n_or_modulus <= 1:
                raise ValueError, "degree of extension must be > 1."
            self.degree = n_or_modulus
            self.modulus = spam # use a randomly chosen polynomial as modulus
        elif not isinstance(n_or_modulus, polynomial.OneVariablePolynomial):
            raise TypeError, "n_or_modulus must be integer or polynomial"
        elif not isinstance(n_or_modulus.getCoefficientRing(), FinitePrimeField):
            raise TypeError, "n_or_modulus must be F_p polynomial."
        elif n_or_modulus.degree() > 1 and n_or_modulus.isIrreducible():
            self.modulus = n_or_modulus("#1")
            self.degree = n_or_modulus.degree()

    def getCharacteristic(self):
        """

        Return the characteristic of the field.

        """
        return self.char

    def __len__(self):
        """

        Return the cardinality of the field

        """
        return self.char ** self.degree

    def createElement(self, seed):
        expansion = arith1.expand(seed, self.char)
        return FiniteExtendedFieldElement(
            polynomial.OneVariableDensePolynomial(
            expansion, "#1", FinitePrimeField(self.char)),
            self.modulus)

class FiniteExtendedFieldElement (FiniteFieldElement):
    """

    FiniteExtendedFieldElement is a class for an element of F_q.

    """
    def __init__(self, representative, modulus=None):
        if modulus == None:
            if not isinstance(representative, ring.ResidueClass) or
            not isinstance(representative.getRing().ring,
                           polynomial.PolynomialRing) or
            not isinstance(representative.getRing().ring.getCoefficientRing(),
                           FinitePrimeField):
                raise TypeError, "wrong type argument for representative."
            self.rep = representative
            self.field = FiniteExtendedField(
                representative.getRing().ring.getCoefficientRing().getCharacteristic(),
                representative.ideal.generators[0])
        else:
            if not isinstance(representative,
                              polynomial.OneVariablePolynomial) or
            not isinstance(representative.getCoefficientRing(),
                           FinitePrimeField):
                raise TypeError, "wrong type argument for representative."
            if not isinstance(modulus, polynomial.OneVariablePolynomial) or
            not isinstance(modulus.getCoefficientRing(), FinitePrimeField) or
            modulus.degree() <= 1:
                raise TypeError, "wrong type argument for modulus."
            self.rep = ring.ResidueClass(
                representative,
                polynomial.OneVariablePolynomialIdeal(
                modulus, modulus.getRing()))
            self.field = FiniteExtendedField(
                modulus.getCoefficientRing().getCharacteristic(),
                modulus)

    def getRing(self):
        return self.field

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    __div__ = __truediv__

    def inverse(self):
        pass

    def __pow__(self, index):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

