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

class FinitePrimeFieldElement(integerResidueClass.IntegerResidueClass):
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
