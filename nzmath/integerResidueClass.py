from gcd import extgcd
from ring import Integer
from rational import Rational

class IntegerResidueClass:
    def __init__(self, representative, modulus):
        if modulus == 0:
            raise ValueError, "modulus can not be zero"
        elif modulus < 0:
            modulus = -modulus
        self.m = modulus
        if isinstance(representative, Rational):
            t = extgcd(representative.denominator, self.m)
            if t[0] != 1:
                raise ValueError, "No inverse of %s." % representative
            self.n = (representative.numerator * t[1][0]) % self.m
        else:
            self.n = representative % self.m

    def __repr__(self):
        return "IntegerResidueClass(%d, %d)" % (self.n, self.m)

    def __mul__(self, other):
        if isinstance(other, IntegerResidueClass):
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

    def inverse(self):
        t = extgcd(self.n, self.m)
        if t[0] != 1:
            raise ValueError, "No inverse of %s." % self
        return IntegerResidueClass(t[1][0], self.m)

    def getModulus(self):
        return self.m

    def getResidue(self):
        return self.n

    def toInteger(self):
        return Integer(self.n % self.m)

    def getRing(self):
        return IntegerResidueClassRing.getInstance(self.m)

class IntegerResidueClassRing:
    """IntegerResidueClassRing is also known as Z/mZ."""

    _instances = {}

    def __init__(self, modulus):
        """The argument modulus m specifies an ideal mZ."""
        self.m = modulus

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
