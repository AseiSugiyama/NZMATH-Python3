class Ring:
    """Ring is an abstract class which expresses that
    the derived classes are (in mathematical meaning) rings."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
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

    def getQuotientField(self):
        """getQuotientField returns the quotient field of the ring
        if available, otherwise raises exception."""
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

from rational import theIntegerRing, theRationalField
