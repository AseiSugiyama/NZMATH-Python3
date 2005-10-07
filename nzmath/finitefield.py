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
    def __init__(self, representative, modulus, modulus_is_prime = True):
        if modulus < 0:
            modulus = -modulus
        if modulus_is_prime or prime.primeq(modulus):
            self.m = modulus
        else:
            raise ValueError, "modulus must be a prime."
        if isinstance(representative, rational.Rational):
            t = gcd.extgcd(representative.denominator, self.m)
            if t[2] != 1:
                raise ValueError, "No inverse of %s." % representative.denominator
            self.n = (representative.numerator * t[0]) % self.m
        elif isinstance(representative, (int, long)):
            self.n = representative % self.m
        elif isinstance(representative, integerResidueClass.IntegerResidueClass):
            assert representative.m == modulus
            self.n = representative.n
        else:
            raise NotImplementedError, "FinitePrimeFieldElement is not made from %s." % (repr(representative),)
        # ring
        self.ring = None

    def __repr__(self):
        return "FinitePrimeFieldElement(%d, %d)" % (self.n, self.m)

    def __str__(self):
        return "%d in F_%d" % (self.n, self.m)

    def getRing(self):
        if not self.ring:
            self.ring = FinitePrimeField.getInstance(self.m)
        return self.ring

    def __eq__(self, other):
        if not other and self.n == 0:
            return True
        if isinstance(other, integerResidueClass.IntegerResidueClass):
            if other.m == self.m and other.n == self.n:
                return True
            else:
                return False
        return NotImplemented


class FinitePrimeField (FiniteField):
    """

    FinitePrimeField is also known as F_p or GF(p).

    """

    # class variable
    _instances = {}

    def __init__(self, characteristic):
        self.char = characteristic
        self.properties = ring.CommutativeRingProperties()
        self.properties.setIsfield(True)
        self._one = self._zero = None

    def getCharacteristic(self):
        """

        Return the characteristic of the field.

        """
        return self.char

    def __eq__(self, other):
        if isinstance(other, FinitePrimeField):
            return self.char == other.char
        return False

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "F_%d" % self.char

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.char)

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

    # properties
    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = FinitePrimeFieldElement(1, self.char)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = FinitePrimeFieldElement(0, self.char)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")

    # class method
    def getInstance(cls, characteristic):
        """
        Return an instance of the class with specified characteristic.
        """
        if characteristic not in cls._instances:
            cls._instances[characteristic] = cls(characteristic)
        return cls._instances[characteristic]

    getInstance = classmethod(getInstance)


import arith1
import bigrandom
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
          3) an ideal of the polynomial ring F_p[#1] with degree
             greater than 1.

        """
        if prime.primeq(characteristic):
            self.char = characteristic
        else:
            raise ValueError, "characteristic must be a prime."
        if isinstance(n_or_modulus, (int, long)):
            if n_or_modulus <= 1:
                raise ValueError, "degree of extension must be > 1."
            self.degree = n_or_modulus
            # randomly chosen irreducible polynomial
            seed = bigrandom.randrange(self.char ** self.degree)
            cand = polynomial.OneVariableDensePolynomial(arith1.expand(seed, self.char)+[1], "#1", FinitePrimeField(self.char))
            while cand.degree() < self.degree and not cand.isIrreducible():
                seed = bigrandom.randrange(self.char ** self.degree)
                cand = polynomial.OneVariableDensePolynomial(arith1.expand(seed, self.char)+[1], "#1", FinitePrimeField(self.char))
            self.modulus = polynomial.OneVariablePolynomialIdeal(cand, cand.getRing())
        elif isinstance(n_or_modulus, polynomial.OneVariablePolynomial):
            if isinstance(n_or_modulus.getCoefficientRing(), FinitePrimeField):
                if n_or_modulus.degree() > 1 and n_or_modulus.isIrreducible():
                    self.degree = n_or_modulus.degree()
                    self.modulus = polynomial.OneVariablePolynomialIdeal(
                        n_or_modulus("#1"),
                        n_or_modulus("#1").getRing())
                else:
                    raise ValueError, "modulus must be of degree greater than 1."
            else:
                raise TypeError, "modulus must be F_p polynomial."
        elif isinstance(n_or_modulus, polynomial.OneVariablePolynomialIdeal):
            if n_or_modulus.ring == polynomial.PolynomialRing(FinitePrimeField(self.char), ["#1"]):
                if n_or_modulus.generators[0].degree() > 1:
                    self.modulus = n_or_modulus
                    self.degree = self.modulus.generators[0].degree()
                else:
                    raise ValueError, "modulus must be of degree greater than 1."
            else:
                raise TypeError, "modulus must be in F_p[#1]"
        else:
            raise TypeError, "degree or modulus must be supplied."
        self._one = self._zero = None

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
        if isinstance(seed, (int, long)):
            expansion = arith1.expand(seed, self.char)
            return FiniteExtendedFieldElement(
                polynomial.OneVariableDensePolynomial(
                expansion, "#1", FinitePrimeField(self.char)),
                self)
        elif isinstance(seed, polynomial.OneVariablePolynomial):
            return FiniteExtendedFieldElement(seed("#1"), self)

    def __repr__(self):
        return "%s(%d, %s)" % (self.__class__.__name__, self.char, repr(self.modulus))

    def __str__(self):
        return "F_%d @(%s)" % (len(self), str(self.modulus.generators[0]))

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = FiniteExtendedFieldElement(
                polynomial.OneVariableDensePolynomial(
                [1], "#1", FinitePrimeField(self.char)),
                self)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = FiniteExtendedFieldElement(
                polynomial.OneVariableDensePolynomial(
                [], "#1", FinitePrimeField(self.char)),
                self)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


class FiniteExtendedFieldElement (FiniteFieldElement):
    """

    FiniteExtendedFieldElement is a class for an element of F_q.

    """
    def __init__(self, representative, field):
        """

        FiniteExtendedFieldElement(representative, field) creates
        an element of the finite extended field.

        The argument representative must be an F_p polynomial.

        Another argument field mut be an instance of
        FiniteExtendedField.

        """
        if isinstance(field, FiniteExtendedField):
            self.field = field
        else:
            raise TypeError, "wrong type argument for field."
        if (isinstance(representative, polynomial.OneVariablePolynomial) and
            isinstance(representative.getCoefficientRing(), FinitePrimeField)):
            self.rep = self.field.modulus.reduce(representative)
        else:
            raise TypeError, "wrong type argument for representative."

    def getRing(self):
        return self.field

    def __add__(self, other):
        assert self.field == other.field
        sum = self.field.modulus.reduce(self.rep + other.rep)
        return self.__class__(sum, self.field)

    def __sub__(self, other):
        assert self.field == other.field
        dif = self.field.modulus.reduce(self.rep - other.rep)
        return self.__class__(dif, self.field)

    def __mul__(self, other):
        assert self.field == other.field
        prod = self.field.modulus.reduce(self.rep * other.rep)
        return self.__class__(prod, self.field)

    def __truediv__(self, other):
        return self * other.inverse()

    __div__ = __truediv__

    def inverse(self):
        if not self:
            raise ZeroDivisionError, "There is no inverse of zero."
        return self ** (len(self.field)-2)

    def __pow__(self, index):
        while index < 0:
            index += self.field.getCharacteristic()
        power = self.field.modulus.reduce(self.rep ** index) # slow
        return self.__class__(power, self.field)

    def __eq__(self, other):
        if self.field == other.field:
            if not self.field.modulus.reduce(self.rep - other.rep):
                return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return self.rep.__nonzero__()

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.rep), repr(self.field))

