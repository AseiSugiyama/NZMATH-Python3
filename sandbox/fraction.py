"""
fraction  --  ring of fractions
"""

import nzmath.ring as ring


class RingOfFractions (ring.CommutativeRing):
    """
    A ring of fractions T = R x S / ~:
      R: a commutative ring
      S: a multiplicative subset of R
      ~: equivalence in a direct product R x S such that:
         (r, s) ~ (t, u) iff there exists v in R s.t. v(ru - st) == 0
    """
    def __init__(self, basering, multset):
        """
        RingOfFractions(basering, multset)

        basering: a ring instance
        multset: a multiplicative subset of the basering
        """
        ring.CommutativeRing.__init__(self)
        self.basering = basering
        self.properties.setIsdomain(self.basering.isdomain())
        self.multset = multset

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.basering, self.multset)

    def __str__(self):
        return "(%s %s**(-1))" % (self.basering, self.multset)

    def createElement(self, numerator, denominator):
        """
        Create an element of the ring of fractions with numerator in
        the base ring and denominator in the multiplicative set.
        """
        return RingOfFractionsElement(numerator, denominator, self)

    def _getOne(self):
        """
        getter for one.
        """
        if self._one is None:
            base_one = self.basering.one
            self._one = RingOfFractionsElement(base_one, base_one, self)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit")

    def _getZero(self):
        """
        getter for zero.
        """
        if self._zero is None:
            self._zero = RingOfFractionsElement(self.basering.zero,
                                               self.basering.one,
                                               self)
        return self._zero

    zero = property(_getZero, None, None, "additive unit")


class RingOfFractionsElement (ring.CommutativeRingElement):
    """
    A class for an element of a ring of fractions.
    """
    def __init__(self, numerator, denominator, fracring):
        """
        RingOfFractionsElement(numnerator, denominator ,fracring)

        numerator: an element of the base ring
        denominator: an element of the multiplicative set
        fracring: the ring of fractions to which the element belongs
        """
        self.numerator = numerator
        self.denominator = denominator
        self._ring = fracring

    def getRing(self):
        """
        Return the ring of fractions to which the element belongs.
        """
        return self._ring

    def __eq__(self, other):
        """
        (a, b) == (c, d)  <=> there exists an element t s.t.
                              t(ad - bc) = 0.
        """
        if self is other:
            return True
        diff = self.numerator*other.denominator - other.numerator*self.denominator
        if not diff:
            return True
        elif self._ring.isdomain():
            return False
        # FIXME
        raise NotImplementedError("how to find a zero divisor?")

    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__,
                                   self.numerator,
                                   self.denominator,
                                   self._ring)

    def __str__(self):
        return "%s/%s" % (self.numerator, self.denominator)

    def __nonzero__(self):
        return bool(self.numerator)

    def __pos__(self):
        return self.__class__(self.numerator, self.denominator, self._ring)

    def __neg__(self):
        return self.__class__(-self.numerator, self.denominator, self._ring)

    def __add__(self, other):
        numerator = self.numerator*other.denominator + self.denominator*other.numerator
        denominator = self.denominator*other.denominator
        return self.__class__(numerator, denominator, self._ring)

    def __sub__(self, other):
        numerator = self.numerator*other.denominator - self.denominator*other.numerator
        denominator = self.denominator*other.denominator
        return self.__class__(numerator, denominator, self._ring)

    def __mul__(self, other):
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return self.__class__(numerator, denominator, self._ring)

    def __pow__(self, index):
        return self.__class__(self.numerator ** index, self.denominator ** index, self._ring)
