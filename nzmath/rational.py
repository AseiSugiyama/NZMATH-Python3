"""

rational module provides Rational, Integer, RationalField, and IntegerRing.

"""
import ring

class Rational (ring.QuotientFieldElement):
    """

    Rational is the class of rational numbers.

    """

    def __init__(self, numerator, denominator=1):
        if denominator < 0:
            self.numerator = Integer(-numerator)
            self.denominator = Integer(-denominator)
        elif denominator == 1 and isinstance(numerator, Rational):
            self.numerator = numerator.numerator
            self.denominator = numerator.denominator
        else :
            self.numerator = Integer(numerator)
            self.denominator = Integer(denominator)

    def __add__(self,other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator + self.denominator*other.numerator
            denominator = self.denominator*other.denominator
            return  +Rational(numerator,denominator)
        elif isIntegerObject(other):
            numerator = self.numerator + self.denominator*other
            denominator = self.denominator
            return  +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __sub__(self,other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator - self.denominator*other.numerator
            denominator = self.denominator*other.denominator
            return +Rational(numerator,denominator) 
        elif isIntegerObject(other):
            numerator = self.numerator - self.denominator*other
            denominator = self.denominator            
            return +Rational(numerator,denominator) 
        else:
            return NotImplemented

    def __mul__(self,other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.numerator
            denominator = self.denominator*other.denominator
            return +Rational(numerator,denominator)
        elif isIntegerObject(other):
            numerator = self.numerator*other
            denominator = self.denominator
            return +Rational(numerator,denominator) 
        else:
            return NotImplemented

    def __truediv__(self,other):
        if isinstance(other, Rational):
            numerator = self.numerator*other.denominator
            denominator = self.denominator*other.numerator
            return +Rational(numerator,denominator)
        elif isIntegerObject(other):
            numerator = self.numerator
            denominator = self.denominator*other
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    __div__ = __truediv__
    __floordiv__ = __truediv__

    def __radd__(self,other):
        if isIntegerObject(other):
            numerator = self.numerator + self.denominator*other
            denominator = self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rsub__(self,other):
        if isIntegerObject(other):
            numerator = self.denominator*other - self.numerator
            denominator = self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rmul__(self,other):
        if isIntegerObject(other):
            numerator = self.numerator*other
            denominator = self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rtruediv__(self,other):
        if isIntegerObject(other):
            numerator = self.denominator*other
            denominator = self.numerator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    __rdiv__ = __rtruediv__
    __rfloordiv__ = __rtruediv__

    def __pow__(self, index):
        return +Rational(self.numerator ** index, self.denominator ** index)

    def __lt__(self,other):
        return self.compare(other) < 0

    def __le__(self,other):
        return self.compare(other) <= 0

    def __eq__(self,other):
        return self.compare(other) == 0

    def __ne__(self,other):
        return self.compare(other) != 0

    def __gt__(self,other):
        return self.compare(other) > 0

    def __ge__(self,other):
        return self.compare(other) >= 0

    def __pos__(self):
        commonDivisor = theIntegerRing.gcd(self.numerator,self.denominator)
        if commonDivisor != 1:
            self.numerator //= commonDivisor
            self.denominator //= commonDivisor
        if self.denominator == 1:
            return Integer(self.numerator)
        else:
            return Rational(self.numerator, self.denominator)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __abs__(self):
        return +Rational(abs(self.numerator), self.denominator)

    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)

    def __repr__(self):
        return "Rational(" + str(self.numerator) + ", " + str(self.denominator) + ")"

    def compare(self, other):
        if isIntegerObject(other):
            return self.numerator - self.denominator * other
        return self.numerator*other.denominator - self.denominator*other.numerator
    def getRing(self):
        return theRationalField

class RationalField (ring.QuotientField):
    """

    RationalField is a class of field of rationals.
    The class has the single instance 'theRationalField'.

    """

    def __init__(self):
        self.basedomain = theIntegerRing
        self.properties = ring.CommutativeRingProperties()
        self.properties.setIsfield(True)

    def __contains__(self, element):
        reduced = +element
        return (isinstance(reduced, Rational) or isIntegerObject(reduced))

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

    def issubring(self, other):
        """

        reports whether another ring contains the rational field as
        subring.

        If other is also the rational field, the output is True.  If
        other is the integer ring, the output is False.  In other
        cases it depends on the implementation of another ring's
        issuperring method.

        """
        if other == self:
            return True
        elif other == theIntegerRing:
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
        if other == self or other == theIntegerRing:
            return True
        return other.issubring(self)

class Integer(long, ring.CommutativeRingElement):
    """

    Integer is a class of integer.  Since 'int' and 'long' do not
    return rational for division, it is needed to create a new class.

    """

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
        return Integer(long(self)%other)

    def __rmod__(self, other):
        try:
            return Integer(other%long(self))
        except:
            return NotImplemented

    def __divmod__(self, other):
        return tuple(map(Integer, divmod(long(self), other)))

    def __rdivmod__(self, other):
        return tuple(map(Integer, divmod(other, long(self))))

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
        if isinstance(other, list) or isinstance(other, tuple):
            return long(self) * other
        try:
            return Integer(long(self)*other)
        except:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, list) or isinstance(other, tuple):
            return other * long(self)
        try:
            return Integer(other*long(self))
        except:
            return NotImplemented

    def __pow__(self, other, modulo=None):
        return Integer(pow(long(self), other, modulo))

    def __pos__(self):
        return Integer(self)

    def __neg__(self):
        return Integer(-long(self))

    def __abs__(self):
        return Integer(abs(long(self)))

    def getRing(self):
        return theIntegerRing

class IntegerRing (ring.CommutativeRing):
    """

    IntegerRing is a class of ring of rational integers.
    The class has the single instance 'theIntegerRing'.

    """

    def __init__(self):
        self.properties = ring.CommutativeRingProperties()
        self.properties.setIseuclidean(True)
        self.properties.setIsfield(False)

    def __contains__(self, element):
        """

        `in' operator is provided for checking an object be in the
        rational integer ring mathematically.  To check an object be
        an integer object in Python, please use isIntegerObject.

        """
        return isIntegerObject(+element)

    def getQuotientField(self):
        """getQuotientField returns the rational field."""
        return theRationalField

    def createElement(self, seed):
        """createElement returns an Integer object with seed,
        which must be an integer."""
        return Integer(seed)

    def __str__(self):
        return "Z"

    def issubring(self, other):
        """

        reports whether another ring contains the integer ring as
        subring.

        If other is also the integer ring, the output is True.  In
        other cases it depends on the implementation of another ring's
        issuperring method.

        """
        if other == self:
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
        if other == self:
            return True
        return other.issubring(self)

    def gcd(self, n, m):
        """

        gcd returns the greatest common divisor of given 2 integers.

        """
        a, b = abs(n), abs(m)
        while b:
            a, b = b, a%b
        return Integer(a)

    def lcm(self, a, b):
        """

        lcm returns the lowest common multiple of given 2 integers.
        If both are zero, it raises an exception.

        """
        return a // self.gcd(a, b) * b 

theIntegerRing = IntegerRing()
theRationalField = RationalField()

def isIntegerObject(anObject):
    return isinstance(anObject, (int, long))
