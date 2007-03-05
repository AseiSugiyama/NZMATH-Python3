import nzmath.ring as ring


class BasicPolynomial:
    """
    Basic polynomial data type ignoring a variable name and the ring.
    """
    def __init__(self, coefficients):
        """
        BasicPolynomial(coefficients)

        coefficients can be any dict initial values.
        """
        self.coefficients = dict(coefficients)

    def __add__(self, other):
        """
        self + other
        """
        sum_coeff = other.coefficients.copy()
        for term, coeff in self.coefficients.iteritems():
            if term in sum_coeff:
                sum_coeff[term] += coeff
            else:
                sum_coeff[term] = coeff
        return self.__class__(sum_coeff)

    def __sub__(self, other):
        """
        self - other
        """
        dif_coeff = self.coefficients.copy()
        for term, coeff in other.coefficients.iteritems():
            if term in dif_coeff:
                dif_coeff[term] -= coeff
            else:
                dif_coeff[term] = -coeff
        return self.__class__(dif_coeff)

    def __mul__(self, other):
        """
        self * other
        """
        mul_coeff = {}
        for ds, cs in self.coefficients.iteritems():
            for do, co in other.coefficients.iteritems():
                if ds + do in mul_coeff:
                    mul_coeff[ds + do] += cs*co
                else:
                    mul_coeff[ds + do] = cs*co
        return self.__class__([(d, c) for (d, c) in mul_coeff.iteritems() if c])

    def __neg__(self):
        """
        -self
        """
        neg_coeff = dict([(d, -c) for (d, c) in self.coefficients.iteritems()])
        return self.__class__(neg_coeff)

    def __pos__(self):
        """
        +self
        """
        return self.__class__(self.coefficients)

    def _square(self):
        """
        Return the square of self.
        """
        # zero
        if not self:
            return self
        # monomial
        if len(self.coefficients) == 1:
            return self.__class__([(d*2, c**2) for (d, c) in self.coefficients.iteritems()])
        # binomial
        if len(self.coefficients) == 2:
            (d1, c1), (d2, c2) = [(d, c) for (d, c) in self.coefficients.iteritems()]
            return self.__class__({d1*2:c1**2, d1+d2:c1*c2*2, d2*2:c2**2})
        # general (inefficient)
        items = self.coefficients.items()
        mono = self.__class__(items.pop())
        rest = self.__class__(items)
        mid = mono*rest
        return mono**2 + mid + mid + rest**2

    def __pow__(self, index):
        """
        self ** index
        """
        # special indeces
        if index < 0:
            raise ValueError("negative index is not allowed.")
        elif index == 0:
            for c in self.coefficients.itervalues():
                if c:
                    one = ring.getRing(c).one
            else:
                one = 1
            return self.__class__({0: 1})
        elif index == 1:
            return self
        elif index == 2:
            return self._square()
        # special polynomials
        if not self:
            return self
        elif len(self.coefficients) == 1:
            return self.__class__([(d*index, c**index) for (d, c) in self.coefficients.iteritems()])
        # general
        power_product = self.__class__({0: 1})
        power_of_2 = self
        while index:
            if index & 1:
                power_product *= power_of_2
            index //= 2
            if index:
                power_of_2 = power_of_2._square()
        return power_product

    def __nonzero__(self):
        """
        if self is not zero, return True.
        """
        for c in self.coefficients.itervalues():
            if c:
                return True
        return False

    def __eq__(self, other):
        """
        self == other
        """
        if self is other:
            return True
        if not isinstance(other, BasicPolynomial):
            return False
        if self.coefficients == other.coefficients:
            return True
        return False

    def __ne__(self, other):
        """
        self != other
        """
        return not (self == other)

    def __hash__(self):
        """
        hash(self)
        """
        return sum([hash(c)*d for (d, c) in self.coefficients.iteritems()]) & 0x7fff

    def __repr__(self): # for debug
        return repr(self.coefficients)

    def differentiate(self):
        """
        Return the formal differentiation of self.
        """
        return self.__class__([(d - 1, d*c) for (d,c) in self.coefficients.iteritems() if d > 0])
