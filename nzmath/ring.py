### abstract classes
###
### There is no need to actually inherit these but only need to
### implement the methods of same names.

class Ring:
    """Ring is an abstract class which expresses that
    the derived classes are (in mathematical meaning) rings."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def getQuotientField(self):
        """getQuotientField returns the quotient field of the ring
        if available, otherwise raises exception."""
        raise NotImplementedError

    def createElement(self, seed):
        """createElement returns an element of the ring with seed."""
        raise NotImplementedError

class CommutativeRing (Ring):
    """CommutativeRing is an abstract subclass of Ring
    whose multiplication is commutative."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""  
        raise NotImplementedError

class Field (CommutativeRing):
    """Field is an abstract class which expresses that
    the derived classes are (in mathematical meaning) fields."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def createElement(self, numerator, denominator):
        """createElement returns an element of the field."""
        raise NotImplementedError

class PolynomialRing (CommutativeRing):
    """PolynomialRing is an abstract class which expresses that
    the derived classes are polynomial rings."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def getCoefficientRing(self):
        """getCoefficientRing returns the ring to which
        all coefficients of polynomials belong."""
        raise NotImplementedError

class RingElement:
    """RingElement is an abstract class for elements of rings."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def getRing(self):
        """getRing returns an object of a subclass of Ring,
        to which the element belongs."""
        raise NotImplementedError

###  concrete classes

class _IntegerRing:
    """_IntegerRing is a (private) class of ring of rational integers.
    The class has the single instance 'theIntegerRing'."""

    def __contains__(self, element):
        reduced = +element
        if isinstance(reduced, int) or isinstance(reduced, long):
            return 1
        else:
            return 0

    def getQuotientField(self):
        """getQuotientField returns the rational field."""
        return theRationalField

    def createElement(self, seed):
        """createElement returns an Integer object with seed,
        which must be an integer."""
        return Integer(seed)

theIntegerRing = _IntegerRing()

import rational

class _RationalField:
    """_RationalField is a (private) class of field of rationals.
    The class has the single instance 'theRationalField'."""

    def __contains__(self, element):
        reduced = +element
        if isinstance(reduced, rational.Rational) or reduced in theIntegerRing:
            return 1
        else:
            return 0

    def classNumber(self):
        """The class number of the rational field is one."""
        return 1

    def getQuotientField(self):
        """getQuotientField returns the rational field itself."""
        return self

    def createElement(self, numerator, denominator=1):
        """createElement
        returns a Rational object.
        If the number of arguments is one, it must be an integer or a rational.
        If the number of arguments is two, they must be integers."""
        return rational.Rational(numerator, denominator)

theRationalField = _RationalField()

class Integer(long):
    """Integer is a class of integer.  Since 'int' and 'long' do not
    return rational for division, it is needed to create a new class."""

    def __div__(self, other):
        if other in theIntegerRing:
            return +rational.Rational(self, +other)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        if other in theIntegerRing:
            return +rational.Rational(+other, self)
        else:
            return NotImplemented

    __truediv__ = __div__

    __rtruediv__ = __rdiv__

    def __floordiv__(self, other):
        return Integer(long(self)//other)

    def __rfloordiv__(self, other):
        return Integer(other//long(self))

    def __mod__(self, other):
        return Integer(long(self)%other)

    def __rmod__(self, other):
        return Integer(other%long(self))

    def __divmod__(self, other):
        return tuple(map(Integer, divmod(long(self), other)))

    def __rdivmod__(self, other):
        return tuple(map(Integer, divmod(other, long(self))))

    def __add__(self, other):
        return Integer(long(self)+other)

    __radd__ = __add__

    def __sub__(self, other):
        return Integer(long(self)-other)

    def __rsub__(self, other):
        return Integer(other-long(self))

    def __mul__(self, other):
        return Integer(long(self)*other)

    __rmul__ = __mul__

    def __pow__(self, other, modulo=None):
        return Integer(pow(long(self), other, modulo))

    def __rpow__(self, other, modulo=None):
        return Integer(pow(other, long(self), modulo))

    def __pos__(self):
        return Integer(self)

    def __neg__(self):
        return Integr(-long(self))

    def __abs__(self):
        return Integer(abs(long(self)))

    def getRing(self):
        return theIntegerRing
