class Ring:
    """

    Ring is an abstract class which expresses that
    the derived classes are (in mathematical meaning) rings.

    Definition of ring is as follows:
      Ring is a structure with addition and multiplication.  It is an
      abelian group with addition, and a monoid with multiplication.
      The multiplication obeys the distributive law.

    """

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        raise NotImplementedError

    def createElement(self, seed):
        """createElement returns an element of the ring with seed."""
        raise NotImplementedError

    def issubring(self, other):
        """

        Report whether another ring contains the ring as a subring.

        """
        raise NotImplementedError

    def issuperring(self, other):
        """

        Report whether the ring is a superring of another ring.

        """
        raise NotImplementedError

class CommutativeRing (Ring):
    """CommutativeRing is an abstract subclass of Ring
    whose multiplication is commutative."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        self.properties = CommutativeRingProperties()
        raise NotImplementedError

    def getQuotientField(self):
        """getQuotientField returns the quotient field of the ring
        if available, otherwise raises exception."""
        raise NotImplementedError

    def isdomain(self):
        """isdomain returns True if the ring is actually a domain,
        False if not, or None if uncertain."""
        return self.properties.isdomain()

    def isnoetherian(self):
        """

        isnoetherian returns True if the ring is actually a Noetherian
        domain, False if not, or None if uncertain.

        """
        return self.properties.isnoetherian()

    def isufd(self):
        """

        isufd returns True if the ring is actually a unique
        factorization domain, False if not, or None if uncertain.

        """
        return self.properties.isufd()

    def ispid(self):
        """

        ispid returns True if the ring is actually a principal
        ideal domain, False if not, or None if uncertain.

        """
        return self.properties.ispid()

    def iseuclidean(self):
        """

        iseuclidean returns True if the ring is actually a Euclidean
        domain, False if not, or None if uncertain.

        """
        return self.properties.iseuclidean()

    def isfield(self):
        """isfield returns True if the ring is actually a field,
        False if not, or None if uncertain."""
        return self.properties.isfield()

class Field (CommutativeRing):
    """Field is an abstract class which expresses that
    the derived classes are (in mathematical meaning) fields."""

    def __init__(self, *args, **kwd):
        """This class is abstract and cannot be instanciated."""
        self.properties = CommutativeRingProperties()
        self.properties.setIsfield(True)
        raise NotImplementedError

    def createElement(self, *args):
        """createElement returns an element of the field."""
        raise NotImplementedError

    def isfield(self):
        """Field overrides isfield of CommutativeRing."""
        return True

    def gcd(self, a, b):
        """A field is trivially a ufd and shuold be provide gcd."""
        return self.createElement(1)

class QuotientField (Field):
    """QuotientField is a class of quotient field."""

    def __init__(self, domain):
        """creates quotient field from given domain."""
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

class Ideal:
    """

    Ideal class is an abstract class to represent the finitely
    generated ideals.  Because the finitely-generatedness is not a
    restriction for Noetherian rings and in the most cases only
    Noetherian rings are used, it is general enough.

    """
    def __init__(self, generators, ring):
        """

        Ideal(generators, ring) creates an ideal of the ring genarated
        by the generators.  generators must be an element of the ring
        or a list of elements of the ring.

        """
        raise NotImplementedError

    def __add__(self, other):
        """

        I + J <=> I.__add__(J)

        where I+J = {i+j | i in I and j in J}

        """
        raise NotImplementedError

    def __mul__(self, other):
        """

        I * J <=> I.__mul__(J)

        where I*J = {sum of i*j | i in I and j in J}

        """
        raise NotImplementedError

    def __eq__(self, other):
        """

        I == J <=> I.__eq__(J)

        """
        raise NotImplementedError

    def __ne__(self, other):
        """

        I != J <=> I.__ne__(J)

        """
        raise NotImplementedError

    def reduce(self, element):
        """

        Reduce an element with the ideal to simpler representative.

        """
        raise NotImplementedError

class ResidueClassRing (CommutativeRing):
    """

    A residue class ring R/I,
    where R is a commutative ring and I is its ideal.

    """
    def __init__(self, ring, ideal):
        """

        ResidueClassRing(ring, ideal) creates a resudue class ring.
        The ring should be an instance of CommutativeRing, and ideal
        must be an instance of Ideal, whose ring attribute points the
        same ring with the given ring.

        """
        self.ring = ring
        self.ideal = ideal
        self.properties = CommutativeRingProperties()
        if self.ring.isnoetherian():
            self.properties.setIsnoetherian(True)

    def __contains__(self, element):
        if isinstance(element, ResidueClass) and element.ideal == self.ideal:
            return True
        return False

    def __eq__(self, other):
        try:
            if self.ideal == other.ideal:
                return True
        except:
            pass
        return False

    def __ne__(self, other):
        return not (self == other)

class ResidueClass (CommutativeRingElement):
    """

    Element of residue class ring x+I, where I is the modulus ideal
    and x is a representative element.

    """
    def __init__(self, x, ideal):
        self.x = x
        self.ideal = ideal

    def __add__(self, other):
        assert self.ideal == other.ideal
        return self.__class__(self.ideal.reduce(self.x + other.x), self.ideal)

    def __sub__(self, other):
        assert self.ideal == other.ideal
        return self.__class__(self.ideal.reduce(self.x - other.x), self.ideal)

    def __mul__(self, other):
        assert self.ideal == other.ideal
        return self.__class__(self.ideal.reduce(self.x * other.x), self.ideal)

    def getRing(self):
        return ResidueClassRing(self.ideal.ring, self.ideal)

class CommutativeRingProperties:
    """

    boolean properties of ring.

    Each property can have one of three values; True, False, or None.
    Of cource True is true and False is false, and None means that the
    property is not set neither directly nor indirectly.

    """
    def __init__(self):
        self._isfield = None
        self._iseuclidean = None
        self._ispid = None
        self._isufd = None
        self._isnoetherian = None
        self._isdomain = None

    def isfield(self):
        return self._isfield

    def setIsfield(self, value):
        self._isfield = bool(value)
        if self._isfield:
            self.setIseuclidean(True)

    def iseuclidean(self):
        return self._iseuclidean

    def setIseuclidean(self, value):
        self._iseuclidean = bool(value)
        if self._iseuclidean:
            self.setIspid(True)
        else:
            self.setIsfield(False)

    def ispid(self):
        return self._ispid

    def setIspid(self, value):
        self._ispid = bool(value)
        if self._ispid:
            self.setIsufd(True)
            self.setIsnoetherian(True)
        else:
            self.setIseuclidean(False)

    def isufd(self):
        return self._isufd

    def setIsufd(self, value):
        self._isufd = bool(value)
        if self._isufd:
            self.setIsdomain(True)
        else:
            self.setIspid(False)

    def isnoetherian(self):
        return self._isnoetherian

    def setIsnoetherian(self, value):
        self._isnoetherian = bool(value)
        if self._isnoetherian:
            self.setIsdomain(True)
        else:
            self.setIspid(False)

    def isdomain(self):
        return self._isdomain

    def setIsdomain(self, value):
        self._isdomain = bool(value)
        if not self._isdomain:
            self.setIsufd(False)
            self.setIsnoetherian(False)
