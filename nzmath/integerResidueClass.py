from gcd import extgcd
from rational import Integer
from rational import Rational

class IntegerResidueClass:
    def __init__(self, representative, modulus):
        if modulus == 0:
            raise ValueError, "modulus can not be zero"
        elif modulus < 0:
            modulus = -modulus
        self.m = modulus
        if isinstance(representative, Rational):
            t = IntegerResidueClass(representative.denominator, self.m).inverse().getResidue()
            self.n = representative.numerator * t % self.m
        else:
            self.n = representative % self.m

    def __repr__(self):
        return "IntegerResidueClass(%d, %d)" % (self.n, self.m)

    def __mul__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n * other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n * other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n * other.n, self.m)
            else:
                raise ValueError, "incompatible modulus: %d and %d" % (self.m, other.m)
        try:
            return IntegerResidueClass(self.n * other, self.m)
        except:
            return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        try:
            return self * other.inverse()
        except AttributeError:
            pass
        try:
            return self * IntegerResidueClass(other, self.m).inverse()
        except ValueError:
            return NotImplemented

    __truediv__ = __div__

    def __add__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n + other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n + other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n + other.n, self.m)
            else:
                raise ValueError, "incompatible modulus: %d and %d" % (self.m, other.m)
        try:
            return IntegerResidueClass(self.n + other, self.m)
        except:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n - other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n - other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n - other.n, self.m)
            else:
                raise ValueError, "incompatible modulus: %d and %d" % (self.m, other.m)
        try:
            return IntegerResidueClass(self.n - other, self.m)
        except:
            return NotImplemented

    def __rsub__(self, other):
        try:
            return IntegerResidueClass(other - self.n, self.m)
        except:
            return NotImplemented

    def __pow__(self, other, mod=None):
        if other < 0:
            inverse = self.inverse()
            return self.__class__(pow(inverse.n, -other, self.m), self.m)
        elif other == 0:
            return self.__class__(1, self.m)
        else:
            return self.__class__(pow(self.n, other, self.m), self.m)

    def __neg__(self):
        return self.__class__(-self.n, self.m)

    def __pos__(self):
        return self.__class__(+self.n, self.m)

    def __eq__(self, other):
        if other == 0 and self.n == 0:
            return True
        try:
            if other.m == self.m and other.n == self.n:
                return True
        except:
            pass
        return False

    def __ne__(self, other):
        return not (self == other)

    def inverse(self):
        t = extgcd(self.n, self.m)
        if t[2] != 1:
            raise ValueError, "No inverse of %s." % self
        return self.__class__(t[0], self.m)

    def getModulus(self):
        return self.m

    def getResidue(self):
        return self.n

    def toInteger(self):
        return Integer(self.n % self.m)

    def getRing(self):
        return IntegerResidueClassRing.getInstance(self.m)

from ring import CommutativeRing, CommutativeRingProperties
from prime import primeq

class IntegerResidueClassRing (CommutativeRing):
    """IntegerResidueClassRing is also known as Z/mZ."""

    _instances = {}

    def __init__(self, modulus):
        """The argument modulus m specifies an ideal mZ."""
        self.m = modulus
        self.properties = CommutativeRingProperties()

    def __repr__(self):
        return "IntegerResidueClassRing(%d)" % self.m

    def __str__(self):
        return "Z/%dZ" % self.m

    def getInstance(self, modulus):
        """

        getInstance returns an instance of the class of specified
        modulus.

        """

        if modulus not in self._instances:
            anInstance = IntegerResidueClassRing(modulus)
            self._instances[modulus] = anInstance
        return self._instances[modulus]

    getInstance = classmethod(getInstance)

    def createElement(self, seed):
        if isinstance(seed, IntegerResidueClass) and seed.m % self.m == 0:
            return IntegerResidueClass(seed.n, self.m)
        try:
            return IntegerResidueClass(seed, self.m)
        except:
            raise ValueError, "%s can not be converted to an IntegerResidueClass object." % seed

    def __contains__(self, elem):
        if isinstance(elem, IntegerResidueClass) and \
           elem.getModulus() == self.m:
            return True
        return False

    def isfield(self):
        """

        isfield returns True if the modulus is prime, False if not.
        Since a finite domain is a field, other ring property tests
        are merely aliases of isfield.

        """
        if None == self.properties.isfield():
            if primeq(self.m):
                self.properties.setIsfield(True)
                return True
            else:
                self.properties.setIsdomain(False)
                return False
        else:
            return self.properties.isfield()

    isdomain = isfield
    isnoetherian = isfield
    isufd = isfield
    ispid = isfield
    iseuclidean = isfield

    def __eq__(self, other):
        if isinstance(other, IntegerResidueClassRing) and self.m == other.m:
            return True
        return False

    def issubring(self, other):
        if self == other:
            return True
        else:
            return False

    def issuperring(self, other):
        if self == other:
            return True
        else:
            return False
