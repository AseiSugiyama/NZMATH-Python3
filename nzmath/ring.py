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

class RingElement:
    """RingElement is an abstract class for elements of rings."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def getRing(self):
        """getRing returns an object of a subclass of Ring,
        to which the element belongs."""
        raise NotImplementedError

class CommutativeRingElement (RingElement):
    pass

class FieldElement (CommutativeRingElement):
    pass

class QuotientFieldElement (FieldElement):
    """

    QuotientFieldElement class is an abstract class to be used as a
    super class of concrete quotient field element classes.

    """
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        if denominator == 0:
            raise ZeroDivisionError
        self.denominator = denominator

    def __add__(self, other):
        numerator = self.numerator*other.denominator + self.denominator*other.numerator
        denominator = self.denominator*other.denominator
        return self.__class__(numerator,denominator) 

    def __sub__(self, other):
        numerator = self.numerator*other.denominator - self.denominator*other.numerator
        denominator = self.denominator*other.denominator
        return self.__class__(numerator,denominator) 

    def __neg__(self):
        return self.__class__(-self.numerator, self.denominator)

    def __mul__(self, other):
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return self.__class__(numerator, denominator)

    def __pow__(self, index):
        return self.__class__(self.numerator ** index, self.denominator ** index)

    def __div__(self, other):
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return self.__class__(numerator, denominator)

    def inverse(self):
        return self.__class__(self.denominator, self.numerator)

    def __eq__(self,other):
        return self.numerator*other.denominator == self.denominator*other.numerator

from rational import theIntegerRing, theRationalField
