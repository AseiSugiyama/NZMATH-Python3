"""
rational module provides Rational, Integer, RationalField, and IntegerRing.
"""

import math
import nzmath.ring as ring


class Rational (ring.QuotientFieldElement):
    """
    Rational is the class of rational numbers.
    """

    def __init__(self, numerator, denominator=1):
        """
        Create a rational from:
          * integers,
          * float, or
          * Rational.
        Other objects can be converted if they have toRational
        methods.  Otherwise raise TypeError.
        """
        if not denominator:
            raise ZeroDivisionError
        # numerator
        integer = (int, long)
        initDispatcher = {
            (Rational, Rational): Rational._init_by_Rational_Rational,
            (float, Rational): Rational._init_by_float_Rational,
            (integer, Rational): Rational._init_by_int_Rational,
            (Rational, float): Rational._init_by_Rational_float,
            (float, float): Rational._init_by_float_float,
            (integer, float): Rational._init_by_int_float,
            (Rational, integer): Rational._init_by_Rational_int,
            (float, integer): Rational._init_by_float_int,
            (integer, integer): Rational._init_by_int_int,
            }
        if not isinstance(numerator, (Rational, float, int, long)):
            if hasattr(numerator, "toRational"):
                numerator = numerator.toRational()
            elif hasattr(numerator, "__pos__"):
                numerator = +numerator
        if not isinstance(denominator, (Rational, float, int, long)):
            if hasattr(denominator, "toRational"):
                denominator = denominator.toRational()
            elif hasattr(numerator, "__pos__"):
                denominator = +denominator
        for (t1, t2) in initDispatcher:
            if isinstance(numerator, t1) and isinstance(denominator, t2):
                initDispatcher[(t1, t2)](self, numerator, denominator)
                break
        else:
            raise TypeError("Rational cannot be created with %s(%s) and %s(%s)." % (numerator, numerator.__class__, denominator, denominator.__class__))
        self._reduce()

    def __add__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator + self.denominator*other.numerator
            denominator = self.denominator*other.denominator
            return  +Rational(numerator, denominator)
        elif isIntegerObject(other):
            numerator = self.numerator + self.denominator*other
            denominator = self.denominator
            return  +Rational(numerator, denominator)
        elif isinstance(other, float):
            return self + Rational(other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator - self.denominator*other.numerator
            denominator = self.denominator*other.denominator
            return +Rational(numerator, denominator)
        elif isIntegerObject(other):
            numerator = self.numerator - self.denominator*other
            denominator = self.denominator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return self - Rational(other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.numerator
            denominator = self.denominator*other.denominator
            return +Rational(numerator, denominator)
        elif isIntegerObject(other):
            numerator = self.numerator*other
            denominator = self.denominator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return self * Rational(other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator
            denominator = self.denominator*other.numerator
            return +Rational(numerator, denominator)
        elif isIntegerObject(other):
            q, r = divmod(self.numerator, other)
            if r == 0:
                return Rational(q, self.denominator)
            numerator = self.numerator
            denominator = self.denominator*other
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return self / Rational(other)
        else:
            return NotImplemented

    __div__ = __truediv__
    __floordiv__ = __truediv__

    def __radd__(self, other):
        if isIntegerObject(other):
            numerator = self.numerator + self.denominator*other
            denominator = self.denominator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return Rational(other) + self
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isIntegerObject(other):
            numerator = self.denominator*other - self.numerator
            denominator = self.denominator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return Rational(other) - self
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isIntegerObject(other):
            numerator = self.numerator*other
            denominator = self.denominator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return Rational(other) * self
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isIntegerObject(other):
            if other == 1:
                return Rational(self.denominator, self.numerator)
            numerator = self.denominator*other
            denominator = self.numerator
            return +Rational(numerator, denominator)
        elif isinstance(other, float):
            return Rational(other) / self
        else:
            return NotImplemented

    __rdiv__ = __rtruediv__
    __rfloordiv__ = __rtruediv__

    def __pow__(self, index):
        assert isIntegerObject(index)
        if index > 0:
            return +Rational(self.numerator ** index, self.denominator ** index)
        elif index < 0:
            if index == -1:
                return Rational(self.denominator, self.numerator)
            return +Rational(self.denominator ** (-index), self.numerator ** (-index))
        else:
            return Integer(1)

    def __lt__(self, other):
        return self.compare(other) < 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __eq__(self, other):
        if isIntegerObject(other):
            if self.denominator == 1:
                return self.numerator == other
            elif self.numerator % self.denominator == 0:
                return self.numerator // self.denominator == other
            else:
                return False
        elif hasattr(other, "denominator") and hasattr(other, "numerator"):
            return self.compare(other) == 0
        else:
            return NotImplemented

    def __ne__(self, other):
        return self.compare(other) != 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __pos__(self):
        common_divisor = theIntegerRing.gcd(self.numerator, self.denominator)
        if common_divisor != 1:
            self.numerator //= common_divisor
            self.denominator //= common_divisor
        return Rational(self.numerator, self.denominator)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __abs__(self):
        return +Rational(abs(self.numerator), self.denominator)

    def __long__(self):
        return self.numerator // self.denominator

    __int__ = __long__

    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)

    def __repr__(self):
        return "%s(%d, %d)" % (self.__class__.__name__, self.numerator, self.denominator)

    def __nonzero__(self):
        if self.numerator:
            return True
        else:
            return False

    def __hash__(self):
        """
        a==b => hash(a)==hash(b)
        """
        hashed = hash(self.__class__.__name__)
        if self.numerator % self.denominator == 0:
            hashed ^= hash(self.numerator // self.denominator)
        else:
            hashed ^= hash(self.numerator)
            hashed ^= hash(self.denominator)
        return hashed

    def expand(self, base, limit):
        """
        r.expand(k, limit) returns the nearest rational number whose
        denominator is a power of k and at most limit, if k > 0.  if
        k==0, it returns the nearest rational number whose denominator
        is at most limit, i.e. r.expand(0, limit) == r.trim(limit).
        """
        if base == 0:
            return self.trim(limit)
        assert isIntegerObject(base) and base > 0
        if self < 0:
            return -(-self).expand(base, limit)
        numerator, rest = divmod(self.numerator, self.denominator)
        i = 0
        if base == 2:
            while numerator*2 <= limit and rest:
                numerator <<= 1
                rest <<= 1
                i += 1
                if rest >= self.denominator:
                    numerator += 1
                    rest -= self.denominator
            if rest*2 > self.denominator:
                numerator += 1
        else:
            while numerator*base <= limit and rest:
                numerator *= base
                rest *= base
                i += 1
                while rest >= self.denominator:
                    numerator += 1
                    rest -= self.denominator
            if rest*2 > self.denominator:
                numerator += 1
        return Rational(numerator, base ** i)

    def trim(self, max_denominator):
        quotient, remainder = divmod(self.numerator, self.denominator)
        approximant0 = Rational(quotient, 1)
        if remainder == 0:
            return approximant0
        rest = Rational(remainder, self.denominator)
        quotient, remainder = divmod(rest.denominator, rest.numerator)
        if quotient > max_denominator:
            return approximant0
        approximant1 = Rational(quotient * approximant0.numerator + 1, quotient)
        if remainder == 0:
            return approximant1
        rest = Rational(remainder, rest.numerator)
        while remainder:
            if rest.numerator > 1:
                quotient, remainder = divmod(rest.denominator, rest.numerator)
            elif rest.denominator > 1:
                quotient, remainder = (rest.denominator-1, 1)
            else:
                quotient, remainder = (1, 0)
            approximant = Rational(quotient * approximant1.numerator + approximant0.numerator, quotient * approximant1.denominator + approximant0.denominator)
            if approximant.denominator > max_denominator:
                break
            approximant0, approximant1 = approximant1, approximant
            rest = Rational(remainder, rest.numerator)
        return approximant1

    def compare(self, other):
        if isIntegerObject(other):
            return self.numerator - self.denominator * other
        if isinstance(other, float):
            return self.compare(Rational(other))
        return self.numerator*other.denominator - self.denominator*other.numerator

    def getRing(self):
        return theRationalField

    def _reduce(self):
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        common_divisor = theIntegerRing.gcd(self.numerator, self.denominator)
        if common_divisor != 1:
            self.numerator //= common_divisor
            self.denominator //= common_divisor

    def __iadd__(self, other):
        if isinstance(other, Rational):
            self.numerator = self.numerator*other.denominator + self.denominator*other.numerator
            self.denominator = self.denominator*other.denominator
        elif isIntegerObject(other):
            self.numerator += self.denominator*other
        else:
            return NotImplemented
        self._reduce()
        return self

    def __isub__(self, other):
        if isinstance(other, Rational):
            self.numerator = self.numerator*other.denominator - self.denominator*other.numerator
            self.denominator = self.denominator*other.denominator
        elif isIntegerObject(other):
            self.numerator -= self.denominator*other
        else:
            return NotImplemented
        self._reduce()
        return self

    def __imul__(self, other):
        if isinstance(other, Rational):
            self.numerator *= other.numerator
            self.denominator *= other.denominator
        elif isIntegerObject(other):
            self.numerator *= other
        else:
            return NotImplemented
        self._reduce()
        return self

    def __itruediv__(self, other):
        if isinstance(other, Rational):
            self.numerator *= other.denominator
            self.denominator *= other.numerator
        elif isIntegerObject(other):
            self.denominator *= other
        else:
            return NotImplemented
        self._reduce()
        return self

    __idiv__ = __itruediv__
    __ifloordiv__ = __itruediv__

    def __ipow__(self, index):
        assert isIntegerObject(index)
        if index > 0:
            self.numerator **= index
            self.denominator **= index
        elif index < 0:
            self.numerator, self.denominator = self.denominator ** (-index), self.numerator ** (-index)
        else:
            self = Integer(1)
        return self

    def __float__(self):
        return float(self.decimalString(17))

    def decimalString(self, N):
        """
        Return a string of the number to N decimal places.
        """
        n = self.numerator
        d = self.denominator
        L = []
        if n < 0:
            L.append('-')
            n = -n
        i = 1
        L.append(str(n//d))
        L.append('.')
        while i <= N:
            n = n % d * 10
            L.append(str(n//d))
            i += 1
        return ''.join(L)

    def _init_by_Rational_Rational(self, numerator, denominator):
        """
        Initialize by a rational numbers.
        """
        self.numerator = numerator.numerator * denominator.denominator
        self.denominator = numerator.denominator * denominator.numerator

    def _init_by_float_Rational(self, numerator, denominator):
        """
        Initialize by a float number and a rational number.
        """
        dp = 53
        frexp = math.frexp(numerator)
        self.numerator = denominator.denominator * (frexp[0] * 2 ** dp)
        self.denominator = denominator.numerator * (2 ** (dp - frexp[1]))

    def _init_by_int_Rational(self, numerator, denominator):
        """
        Initailize by an integer and a rational number.
        """
        self.numerator = denominator.denominator * numerator
        self.denominator = denominator.numerator

    def _init_by_Rational_float(self, numerator, denominator):
        """
        Initialize by a rational number and a float.
        """
        dp = 53
        frexp = math.frexp(denominator)
        self.numerator = numerator.numerator * (2 ** (dp - frexp[1]))
        self.denominator = numerator.denominator * (frexp[0] * 2 ** dp)

    def _init_by_float_float(self, numerator, denominator):
        """
        Initialize by a float numbers.
        """
        dp = 53
        frexp_num = math.frexp(numerator)
        frexp_den = math.frexp(denominator)
        self.numerator = Integer(frexp_num[0] * 2 ** (2 * dp - frexp_den[1]))
        self.denominator = Integer(frexp_den[0] * 2 ** (2 * dp - frexp_num[1]))

    def _init_by_int_float(self, numerator, denominator):
        """
        Initailize by an integer and a float
        """
        dp = 53
        frexp_den = math.frexp(denominator)
        self.numerator = Integer(numerator * (2 ** (dp - frexp_den[1])))
        self.denominator = Integer(frexp_den[0] * 2 ** dp)

    def _init_by_Rational_int(self, numerator, denominator):
        """
        Initialize by a rational number and integer.
        """
        self.numerator = numerator.numerator
        self.denominator = numerator.denominator * denominator

    def _init_by_float_int(self, numerator, denominator):
        """
        Initialize by a float number and an integer.
        """
        dp = 53
        frexp = math.frexp(numerator)
        self.numerator = Integer(frexp[0] * 2 ** dp)
        self.denominator = Integer(2 ** (dp - frexp[1]) * denominator)

    def _init_by_int_int(self, numerator, denominator):
        """
        Initailize by an integers.
        """
        self.numerator = Integer(numerator)
        self.denominator = Integer(denominator)


class RationalField (ring.QuotientField):
    """
    RationalField is a class of field of rationals.
    The class has the single instance 'theRationalField'.
    """

    def __init__(self):
        ring.QuotientField.__init__(self, theIntegerRing)

    def __contains__(self, element):
        try:
            reduced = +element
            return (isinstance(reduced, Rational) or isIntegerObject(reduced))
        except (TypeError, AttributeError):
            return False

    def __eq__(self, other):
        """
        Equality test.
        """
        return isinstance(other, RationalField)

    def classNumber(self):
        """The class number of the rational field is one."""
        return 1

    def getQuotientField(self):
        """getQuotientField returns the rational field itself."""
        return self

    def createElement(self, numerator, denominator=1):
        """
        createElement returns a Rational object.
        If the number of arguments is one, it must be an integer or a rational.
        If the number of arguments is two, they must be integers.
        """
        return Rational(numerator, denominator)

    def __str__(self):
        return "Q"

    def __repr__(self):
        return "RationalField()"

    def __hash__(self):
        """
        Return a hash number (always 1).
        """
        return 1

    def issubring(self, other):
        """
        reports whether another ring contains the rational field as
        subring.

        If other is also the rational field, the output is True.  If
        other is the integer ring, the output is False.  In other
        cases it depends on the implementation of another ring's
        issuperring method.
        """
        if isinstance(other, RationalField):
            return True
        elif isinstance(other, IntegerRing):
            return False
        return other.issuperring(self)

    def issuperring(self, other):
        """
        reports whether the rational number field contains another
        ring as subring.

        If other is also the rational number field or the ring of
        integer, the output is True.  In other cases it depends on the
        implementation of another ring's issubring method.
        """
        if isinstance(other, (RationalField, IntegerRing)):
            return True
        return other.issubring(self)

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = Rational(1, 1)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = Rational(0, 1)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


class Integer(long, ring.CommutativeRingElement):
    """
    Integer is a class of integer.  Since 'int' and 'long' do not
    return rational for division, it is needed to create a new class.
    """
    def __init__(self, value):
        ring.CommutativeRingElement.__init__(self)

    def __div__(self, other):
        if other in theIntegerRing:
            return +Rational(self, +other)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        if other in theIntegerRing:
            return +Rational(+other, self)
        else:
            return NotImplemented

    __truediv__ = __div__

    __rtruediv__ = __rdiv__

    def __floordiv__(self, other):
        return Integer(long(self)//other)

    def __rfloordiv__(self, other):
        try:
            return Integer(other//long(self))
        except:
            return NotImplemented

    def __mod__(self, other):
        if isinstance(other, (int, long)):
            return Integer(long(self)%long(other))
        return NotImplemented

    def __rmod__(self, other):
        return Integer(other%long(self))

    def __divmod__(self, other):
        return tuple([Integer(x) for x in divmod(long(self), other)])

    def __rdivmod__(self, other):
        return tuple([Integer(x) for x in divmod(other, long(self))])

    def __add__(self, other):
        if isIntegerObject(other):
            return Integer(long(self)+other)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isIntegerObject(other):
            return Integer(long(self)-other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        return Integer(other-long(self))

    def __mul__(self, other):
        if isinstance(other, (int, long)):
            return self.__class__(long(self) * other)
        try:
            retval = other.__rmul__(self)
            if retval and retval is not NotImplemented:
                return retval
        except Exception:
            pass
        return self.actAdditive(other)

    def __rmul__(self, other):
        if isinstance(other, (int, long)):
            return self.__class__(other * long(self))
        elif other.__class__ in __builtins__.values():
            return other.__mul__(long(self))
        return self.actAdditive(other)

    def __pow__(self, other, modulo=None):
        return Integer(pow(long(self), other, modulo))

    def __pos__(self):
        return Integer(self)

    def __neg__(self):
        return Integer(-long(self))

    def __abs__(self):
        return Integer(abs(long(self)))

    def __eq__(self, other):
        return long(self) == long(other)

    def getRing(self):
        return theIntegerRing

    def actAdditive(self, other):
        """
        Act on other additively, i.e. n is expanded to n time
        additions of other.  Naively, it is:
          return sum([+other for _ in xrange(self)])
        but, here we use a binary addition chain.
        """
        nonneg, absVal = (self >= 0), abs(self)
        result = 0
        doubling = +other
        while absVal:
            if absVal & 1:
                result += doubling
            doubling += doubling
            absVal >>= 1
        if not nonneg:
            result = -result
        return result

    def actMultiplicative(self, other):
        """
        Act on other multiplicatively, i.e. n is expanded to n time
        multiplications of other.  Naively, it is:
          return reduce(lambda x,y:x*y, [+other for _ in xrange(self)])
        but, here we use a binary addition chain.
        """
        nonneg, absVal = (self >= 0), abs(self)
        result = 1
        doubling = +other
        while absVal:
            if absVal& 1:
                result *= doubling
            doubling *= doubling
            absVal >>= 1
        if not nonneg:
            result = result.inverse()
        return result


class IntegerRing (ring.CommutativeRing):
    """
    IntegerRing is a class of ring of rational integers.
    The class has the single instance 'theIntegerRing'.
    """

    def __init__(self):
        ring.CommutativeRing.__init__(self)
        self.properties.setIseuclidean(True)
        self.properties.setIsfield(False)

    def __contains__(self, element):
        """
        `in' operator is provided for checking an object be in the
        rational integer ring mathematically.  To check an object be
        an integer object in Python, please use isIntegerObject.
        """
        try:
            return isIntegerObject(+element)
        except (TypeError, AttributeError):
            return False

    def __eq__(self, other):
        """
        Equality test.
        """
        return isinstance(other, IntegerRing)

    def getQuotientField(self):
        """
        getQuotientField returns the rational field.
        """
        return theRationalField

    def createElement(self, seed):
        """
        createElement returns an Integer object with seed,
        which must be an integer.
        """
        return Integer(seed)

    def __str__(self):
        return "Z"

    def __repr__(self):
        return "IntegerRing()"

    def __hash__(self):
        """
        Return a hash number (always 0).
        """
        return 0

    def issubring(self, other):
        """
        reports whether another ring contains the integer ring as
        subring.

        If other is also the integer ring, the output is True.  In
        other cases it depends on the implementation of another ring's
        issuperring method.
        """
        if isinstance(other, IntegerRing):
            return True
        return other.issuperring(self)

    def issuperring(self, other):
        """
        reports whether the integer ring contains another ring as
        subring.

        If other is also the integer ring, the output is True.  In
        other cases it depends on the implementation of another ring's
        issubring method.
        """
        if isinstance(other, IntegerRing):
            return True
        return other.issubring(self)

    def gcd(self, n, m):
        """
        gcd returns the greatest common divisor of given 2 integers.
        """
        import nzmath.gcd as gcd
        a, b = abs(n), abs(m)
        return Integer(gcd.gcd(a, b))

    def lcm(self, a, b):
        """
        lcm returns the lowest common multiple of given 2 integers.
        If both are zero, it raises an exception.
        """
        return a // self.gcd(a, b) * b

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = Integer(1)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = Integer(0)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


theIntegerRing = IntegerRing()
theRationalField = RationalField()


def isIntegerObject(anObject):
    """
    True if the given object is instance of int or long,
    False otherwise.
    """
    return isinstance(anObject, (int, long))

def IntegerIfIntOrLong(anObject):
    """
    Cast int or long objects to Integer.
    The objects in list or tuple can be casted also.
    """
    objectClass = anObject.__class__
    if objectClass == int or objectClass == long:
        return Integer(anObject)
    elif isinstance(anObject, (list,tuple)):
        return objectClass([IntegerIfIntOrLong(i) for i in anObject])
    return anObject
