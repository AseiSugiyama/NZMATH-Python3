"""
Class definitions of multivariate polynomials.

The polynomials are immutable data types, under the public API.  If
one tries to manipulate its underlying data attributes, immutability
will be able to be broken.
"""

from __future__ import division
import logging
import warnings
import nzmath.ring as _ring
import nzmath.poly.formalsum as formalsum


_log = logging.getLogger('nzmath.sandbox.multivar')


class TermIndeces (object):
    """
    Indeces of terms of multivariate polynomials.
    """
    def __init__(self, indeces):
        """
        Termindeces(indeces)

        The constructor does not check the validity of indeces,
        such as integerness, nonnegativity, etc.
        """
        self._tuple = tuple(indeces)

    def __hash__(self):
        """
        hash(indeces)
        """
        return hash(self.__class__.__name__) ^ hash(self._tuple)

    def __len__(self):
        """
        len(indeces)
        """
        return len(self._tuple)

    def __iter__(self):
        """
        iter(indeces)

        Return iterator yielding successive elements.
        """
        return iter(self._tuple)

    def __repr__(self): # debug
        return repr(self._tuple)

    def __eq__(self, other):
        """
        self == other
        """
        if hash(self) != hash(other):
            return False
        return self._tuple == other._tuple

    def __ne__(self, other):
        """
        self != other
        """
        return not self.__eq__(other)

    def __le__(self, other):
        """
        self <= other
        """
        return self._tuple <= other._tuple

    def __lt__(self, other):
        """
        self < other
        """
        return self._tuple < other._tuple

    def __gt__(self, other):
        """
        self > other
        """
        return self._tuple > other._tuple

    def __ge__(self, other):
        """
        self >= other
        """
        return self._tuple >= other._tuple

    def __add__(self, other):
        """
        (i1, ..., in) + (j1, ..., jn) = (i1 + j1, ..., in + jn)
        """
        if len(self) != len(other):
            raise TypeError("different length indeces")
        return self.__class__([i + j for (i, j) in zip(self, other)])

    def __sub__(self, other):
        """
        (i1, ..., in) - (j1, ..., jn) = (i1 - j1, ..., in - jn)
        """
        if len(self) != len(other):
            raise TypeError("different length indeces")
        return self.__class__([i - j for (i, j) in zip(self, other)])

    def __mul__(self, scale):
        """
        (i1, ..., in) * s = (i1 * s, ..., in * s)
        """
        return self.__class__([i * scale for i in self])

    def __getitem__(self, index):
        """
        (i1, ..., in)[k] = ik
        """
        return self._tuple[index]

    def pop(self, pos):
        """
        Return the index at 'pos' and a new TermIndeces object as the
        omitting-the-'pos' indeces.
        """
        index = self.__class__(self._tuple[:pos] + self._tuple[pos + 1:])
        return self._tuple[pos], index

    def gcd(self, other):
        """
        Return the greatest common divisor.

        gcd((i1, ..., in), (j1, ..., jn)) = (min(i1, j1), ..., min(in, jn))
        """
        if len(self) != len(other):
            raise TypeError("different length indeces")
        return self.__class__([min(i, j) for (i, j) in zip(self, other)])

    def lcm(self, other):
        """
        Return the least common multiple.
        
        lcm((i1, ..., in), (j1, ..., jn)) = (max(i1, j1), ..., max(in, jn))
        """
        if len(self) != len(other):
            raise TypeError("different length indeces")
        return self.__class__([max(i, j) for (i, j) in zip(self, other)])


class PolynomialInterface (formalsum.FormalSumContainerInterface):
    """
    Base class for all multivariate polynomials.
    """
    def __eq__(self, other):
        """
        self == other
        """
        if not isinstance(other, PolynomialInterface):
            warnings.warn("comparison falls back to that of formal sum.")
        return formalsum.FormalSumContainerInterface.__eq__(self, other)


class BasicPolynomial (PolynomialInterface):
    """
    The class for basic multivariate polynomials.
    """

    def __init__(self, coefficients, **kwds):
        """
        BasicPolynomial(coefficients [, keyword_arguments...])

        coefficients can be any dict initial values.
        """
        PolynomialInterface.__init__(self)
        self._coefficients = dict([(TermIndeces(i), c) for (i, c) in dict(coefficients).iteritems()])
        if "number_of_variables" in kwds:
            self.number_of_variables = kwds.pop("number_of_variables")
        else:
            self.number_of_variables = 0
            for i in self.iterbases():
                if len(i) > self.number_of_variables:
                    self.number_of_variables = len(i)
        self._init_kwds = kwds

    def __eq__(self, other):
        """
        self == other
        """
        if self is other:
            return True
        return PolynomialInterface.__eq__(self, other)

    def __add__(self, other):
        """
        self + other

        Both self and other must have the same length tuples of
        indeces for every term.
        """
        sum_coeff = dict(iter(self))
        for term, coeff in other:
            if term in sum_coeff:
                sum_coeff[term] += coeff
            else:
                sum_coeff[term] = coeff
        return self.__class__([(d, c) for (d, c) in sum_coeff.iteritems() if c],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def __sub__(self, other):
        """
        self - other
        """
        return self + (-other)

    def __mul__(self, other):
        """
        self * other

        If type of other is Polynomial, do multiplication in ring.
        Otherwise, do scalar multiplication.
        """
        if isinstance(other, PolynomialInterface):
            return self.ring_mul(other)
        else:
            return self.scalar_mul(other)

    def __rmul__(self, other):
        """
        other * self
        """
        return self.scalar_mul(other)

    def ring_mul(self, other):
        """
        self * other

        Both self and other must have the same length tuples of
        indeces for every term.
        """
        mul_coeff = {}
        for ds, cs in self:
            if not cs:
                continue
            for do, co in other:
                if not co:
                    continue
                assert len(ds) == len(do)
                indeces = ds + do
                if indeces in mul_coeff:
                    mul_coeff[indeces] += cs*co
                else:
                    mul_coeff[indeces] = cs*co
        return self.__class__([(d, c) for (d, c) in mul_coeff.iteritems() if c],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def scalar_mul(self, scale):
        """
        Return the result of scalar multiplication.
        """
        return self.__class__([(i, c * scale) for (i, c) in self if c],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def term_mul(self, term):
        """
        Return the result of multiplication with the given term.
        The term can be given as a tuple (degree indeces, coeff)
        or as a Polynomial instance.
        """
        if isinstance(term, PolynomialInterface):
            degrees, coeff = iter(term).next()
        else:
            degrees, coeff = term
        return self.__class__([(d + degrees, c * coeff) for (d, c) in self],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def __pow__(self, index):
        """
        self ** index

        pow with three arguments is not supported by default.
        """
        if index < 0:
            raise ValueError("negative index is not allowed.")
        elif index == 0:
            indeces = (0,)
            for i, c in self:
                if c:
                    indeces = (0,) * len(i)
                    one = _ring.getRing(c).one
                    break
            else:
                one = 1
            return self.__class__({indeces: one}, **self._init_kwds)
        elif index == 1:
            return self
        elif index == 2:
            return self.square()
        # special polynomials
        if not self:
            return self
        elif len(self) == 1:
            return self.__class__([(d*index, c**index) for (d, c) in self],
                                  number_of_variables=self.number_of_variables,
                                  **self._init_kwds)
        # general
        for i, c in self:
            if c:
                zero = (0,) * len(i)
                one = _ring.getRing(c).one
                break
        power_product = self.__class__({zero: one}, **self._init_kwds)
        power_of_2 = self
        while index:
            if index & 1:
                power_product *= power_of_2
            index //= 2
            if index:
                power_of_2 = power_of_2.square()
        return power_product

    def square(self):
        """
        Return squared polynomial.
        """
        # zero
        if not self:
            return self

        polynomial = self.__class__
        data_length = len(self)
        # monomial
        if data_length == 1:
            for i, c in self:
                result = polynomial([(i * 2, c ** 2)], **self._init_kwds)
        # binomial
        elif data_length == 2:
            (i1, c1), (i2, c2) = [(i, c) for (i, c) in self]
            result = polynomial({i1 * 2: c1**2, i1 + i2: c1*c2*2, i2 * 2: c2**2}, **self._init_kwds)
        # general (recursive)
        else:
            half = data_length // 2
            coefficients = [(i, c) for (i, c) in self]
            left, right = polynomial(coefficients[:half], **self._init_kwds), polynomial(coefficients[half:], **self._init_kwds)
            result = left.square() + left * right * 2 + right.square()
        return result

    def __neg__(self):
        """
        -self
        """
        return self.__class__([(d, -c) for (d, c) in self],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def __pos__(self):
        """
        +self
        """
        return self.__class__(self._coefficients,
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def __nonzero__(self):
        """
        if self is not zero, return True.
        """
        for c in self.itercoefficients():
            if c:
                return True
        return False

    def __hash__(self):
        """
        hash(self)

        Return the hash satisfying hash(self) == hash(other)
        if self == other.
        """
        hashvalue = hash(self.__class__.__name__)
        for i, c in self:
            hashvalue = hashvalue ^ (hash(i) | hash(c))
        return hashvalue & 0x7fffffff

    def __call__(self, target, value):
        """
        Substitute 'value' to 'target' index variable.
        If 'target' is a tuple of indeces, it has to be sorted and
        'value' also has to be a tuple of the same length.

        Note that the result will not be a univar polynomial nor a
        scalar.
        """
        result = {}
        if isinstance(target, (int, long)):
            for i, c in self:
                deg, index = i[target], i[:target] + (0,) + i[target + 1:]
                if index in result:
                    result[index] += c * value ** deg
                else:
                    result[index] = c * value ** deg
        elif len(target) == len(value):
            substituted = self
            for var, val in zip(target[::-1], value[::-1]):
                substituted = substituted(var, val)
            return substituted
        else:
            raise TypeError("argument lengths mismatsch")
        return self.__class__([(i, c) for (i, c) in result.iteritems() if c], **self._init_kwds)

    def __len__(self):
        """
        Return the number of data entries.
        """
        return len(self._coefficients)

    def __getitem__(self, index):
        """
        Return the coefficient of specified index (tuple of degrees).
        If there is no term of index, return 0.
        """
        return self._coefficients.get(index, 0)

    def iterterms(self):
        """
        iterator for (degree, coefficient) pairs.
        """
        return self._coefficients.iteritems()

    def itercoefficients(self):
        """
        iterator for coefficients.
        """
        return self._coefficients.itervalues()

    def iterbases(self):
        """
        iterator for degrees.
        """
        return self._coefficients.iterkeys()

    def partial_differentiate(self, target):
        """
        Return the polynomial obtained by partial differentiation with
        the 'target' index variable.
        """
        partial = {}
        for i, c in self:
            index_diffed = list(i)
            target_degree = index_diffed[target]
            index_diffed[target] -= 1
            index_diffed = tuple(i)
            partial[index_diffed] = target_degree * c
        return self.__class__([(i, c) for (i, c) in partial.iteritems() if c],
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)

    def erase_variable(self, target=0):
        """
        Erase a variable from the polynomial.  The target variable is
        specified by the position in indeces.

        The method takes no care about resulting polynomial type, i.e.
        the result remains as the same type even if their indeces have
        length less than 2.
        """
        result = dict()
        for term, coeff in self:
            term = term[:target] + term[target + 1:]
            if term in result:
                result[term] += coeff
            else:
                result[term] = coeff

        return self.__class__([(d, c) for (d, c) in result.iteritems() if c],
                              number_of_variables=(self.number_of_variables - 1),
                              **self._init_kwds)

    def combine_similar_terms(self, target):
        """
        Combine similar terms and return the resulting univariate
        polynomial with polynomial coefficients in the form of list of
        (degree, coefficient) pairs.  The target variable is specified
        by the position in indeces.
        """
        zero = self.__class__((),
                              number_of_variables=self.number_of_variables,
                              **self._init_kwds)
        result = {}
        for i, c in self:
            result[i[target]] = result.get(i[target], zero) + self.__class__([(i, c)], **self._init_kwds)
        for i, c in result.iteritems():
            result[i] = c.erase_variable(target)
        return result.items()

    def __repr__(self): # debug use
        return "BasicPolynomial(%s)" % repr(self._coefficients)
