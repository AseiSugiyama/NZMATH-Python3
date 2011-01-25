"""
p-adic numbers and their rings / fields
"""

from __future__ import division
import nzmath.arith1 as arith1
import nzmath.rational as rational
import nzmath.ring as ring


class BasePadicInteger (ring.CommutativeRingElement):
    """
    This is an abstract base class of p-adic integers.
    """
    def __init__(self, p):
        """
        Initialize.
        
        Actually, only set attribute p.
        """
        if type(self) == BasePadicInteger:
            raise NotImplementedError("class BasePadicInteger is abstract")
        ring.CommutativeRingElement.__init__(self)
        self.p = p

    def getRing(self):
        """
        Return the ring of p-adic integer.
        """
        return PadicIntegerRing.getInstance(self.p)


class FinitePrecisionPadicInteger (BasePadicInteger):
    """
    p-adic integer
    """
    # internal:
    # p-adic integer
    #   a0 + a1*p + ... + ar*p**r
    # is represented by p and (a0, ..., ar).
    #
    # It is immutable.

    def __init__(self, p, initial, power):
        """
        PadicInteger(p, initial, power)

        The second argument initial can be either integer or iterable.
        If initial is an integer, it will be expanded p-adically.
        In iterable case, it will be treated as a p-adic expansion.

        The third argument power is a power index of modulus, by which
        the representation is finite.
        """
        if isinstance(initial, (int, long)):
            cutoff = p ** power
            # taking modulo cutoff is useful for nagative integers.
            self.expansion = tuple(arith1.expand(initial % cutoff, p))
        else:
            # take only first 'power' elements of initial.
            self.expansion = tuple([e for i, e in zip(xrange(power), initial)])
        self.p = p

    def __nonzero__(self):
        """
        True for non-zero.
        """
        if filter(None, self.expansion):
            return True
        return False

    def __getitem__(self, index):
        """
        a[i] returns ai of a = a0 + a1*p + ... + ai*p**i + ...
        """
        # Though the exhaustion of self.expansion doesn't mean 0 thereafter,
        # this mothod returns 0.
        if index < 0 or index >= len(self.expansion):
            return 0
        return self.expansion[index]

    def __add__(self, other):
        """
        self + other
        """
        if self.p != other.p:
            raise TypeError("You can't add p-adic and q-adic numbers")
        result = []
        carry = 0
        for a, b in zip(self.expansion, other.expansion):
            carry, r = divmod(a + b + carry, self.p)
            result.append(r)
        return self.__class__(self.p, tuple(result), len(result))

    # FIXME: other operations should follow.

    def valuation(self):
        """
        Return the canonical p-adic valuation.
        If n = ak*p**k + ..., the value is p**(-k).
        If n is zero, the value is also zero.
        """
        if not self:
            return 0
        for i, e in enumerate(self.expansion):
            if e:
                return rational.Rational(1, p**i)


class PadicNumber (ring.FieldElement):
    """
    p-adic numbers
    """
    def __init__(self, integer, shift):
        """
        A p-adic number is a*p**(-m), where a is an p-adic integer.

        Give 'a' as integer and 'm' (>0) as shift.
        """
        self.integer = integer
        self.shift = shift
        self.p = self.integer.p

    def __add__(self, other):
        """
        n + m
        """
        if isinstance(other, PadicNumber):
            return self.add(other)
        # finally
        return NotImplemented

    def add(self, other):
        """
        Return sum of self and other, both of which are PadicNumber
        instance.
        """
        if self.shift > other.shift:
            addend = other.integer * p ** (self.shift - other.shift)
            return self.__class__(self.integer + addend, self.shift)
        elif self.shift < other.shift:
            addend = self.integer * p ** (other.shift - self.shift)
            return self.__class__(addend + other.integer, other.shift)
        else:
            return self.__class__(self.integer + other.integer, self.shift)

    def valuation(self):
        """
        Return the canonical p-adic valuation.
        If n = ak*p**k + ..., the value is p**(-k).
        If n is zero, the value is also zero.
        """
        self.integer.valuation() * (self.p ** self.shift)


class PadicIntegerRing (ring.CommutativeRing):
    """
    Rings of p-adic integers: Zp.
    """
    _instances = {}

    def __init__(self, p):
        """
        Initialize.
        """
        ring.CommutativeRing.__init__(self)
        self.p = p

    def getQuotientField(self):
        """
        Return quotient field Qp.
        """
        return PadicField.getInstance(self.p)

    @classmethod
    def getInstance(cls, p):
        """
        Return an instance of PadicIntegerRing with specified prime p.
        """
        if p not in cls._instances:
            cls._instances[p] = cls(p)
        return cls._instances[p]


class PadicField (ring.QuotientField):
    """
    Fields of p-adic numbers: Qp.
    """
    _instances = {}

    def __init__(self, p):
        """
        Initialize.
        """
        ring.QuotientField.__init__(self, PadicIntegerRing.getInstance(p))
        self.p = p

    @classmethod
    def getInstance(cls, p):
        """
        Return an instance of PadicIntegerRing with specified prime p.
        """
        if p not in cls._instances:
            cls._instances[p] = cls(p)
        return cls._instances[p]
