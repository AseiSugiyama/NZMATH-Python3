### abstract classes
###
### There is no need to actually inherit these but only to implement
### the methods of same names.

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
        """This class is abstract and cannot be instanciated."""  raise
        NotImplementedError

class Field (CommutativeRing):
    """Field is an abstract class which expresses that
    the derived classes are (in mathematical meaning) fields."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
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
        """createElement returns an Integer object with seed."""
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

    def createElement(self, seed):
        """createElement returns a Rational object with seed."""
        return rational.Rational(seed)

theRationalField = _RationalField()

class Integer(long):
    """Integer is a class of integer.  Since 'int' and 'long' do not
    return rational for division, it is needed to create a new class."""

    def __div__(self, other):
        if other in theIntegerRing:
            return rational.Rational(self, other)
        else:
            return NotImplemented

    def getRing(self):
        return theIntegerRing
