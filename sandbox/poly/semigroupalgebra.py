"""
semigroup algebra
"""

import operator
import nzmath.ring as _ring
import sandbox.poly.formalsum as formalsum

# operationtypes of semigroup
class _OpType (object):
    def __init__(self, code):
        """
        _OpType(code) makes an instance, but DO NOT CALL directly.
        It is strongly recommended to use pre-defined constants:
        ADDITIVE and MULTIPLICATIVE.

        opcode can be either 0 (additive) or 1 (multiplicative).
        """
        if code == 0:
            self.name = "ADDITIVE"
            self.op1 = operator.add
            self.op2 = operator.mul
        elif code == 1:
            self.name = "MULTIPLICATIVE"
            self.op1 = operator.mul
            self.op2 = operator.pow
        else:
            raise ValueError("You are too fool!")

    def __repr__(self):
        """
        'ADDITIVE' or 'MULTIPLICATIVE'
        """
        return self.name


ADDITIVE = _OpType(0)
MULTIPLICATIVE = _OpType(1)
_OPTYPES = (ADDITIVE, MULTIPLICATIVE)


class SemigroupAlgebraElement (object):
    def __init__(self, mapping, optype):
        """
        SemigroupAlgebraElement(mapping, optype)

        mapping: mapping from the semigroup to ring.
        optype: one of ADDITIVE(= 0) or MULTIPLICATIVE(= 1).
                (We assume additive semigroup is commutative.)

        The semigroup is not explicitly given.
        """
        self._data = formalsum.DictFormalSum(mapping)
        self.optype = optype

    def __add__(self, other):
        """
        self + other
        """
        assert self.optype == other.optype
        return self.__class__(self._data + other._data, self.optype)

    def __sub__(self, other):
        """
        self - other
        """
        assert self.optype == other.optype
        return self.__class__(self._data - other._data, self.optype)

    def __mul__(self, other):
        """
        self * other

        If type of other is SemigroupAlgebraElement, do multiplication
        induced from semigroup operation.  Otherwise, do scalar
        multiplication.
        """
        if isinstance(other, SemigroupAlgebraElement):
            return self.ring_mul(other)
        else:
            return self.scalar_mul(other)

    def __rmul__(self, other):
        """
        other * self

        Return the result of scalar multiplication with other, since
        other cannot be of SemigroupAlgebraElement.
        """
        return self.rscalar_mul(other)

    def ring_mul(self, other):
        """
        Return the result of multiplication induced from semigroup
        operation.
        """
        assert self.optype == other.optype
        assert self.optype in _OPTYPES
        mul_map = {}
        for ds, cs in self._data.iterterms():
            for do, co in other._data.iterterms():
                base = self.optype.op1(ds, do)
                if base in mul_map:
                    mul_map[base] += cs*co
                else:
                    mul_map[base] = cs*co
        return self.__class__([(d, c) for (d, c) in mul_map.iteritems() if c], self.optype)

    def scalar_mul(self, scale):
        """
        Return the result of scalar multiplication.
        """
        return self.__class__(self._data * scale, self.optype)

    def rscalar_mul(self, scale):
        """
        Return the result of r-scalar multiplication. (r- means as of
        r-methods of python special methods, where self is the right
        operand.)
        """
        return self.__class__(scale * self._data, self.optype)

    def __neg__(self):
        """
        -self
        """
        return self.__class__(-self._data, self.optype)

    def __pos__(self):
        """
        +self
        """
        return self.__class__(self._data, self.optype)

    def square(self):
        """
        Return the square of self.
        """
        assert self.optype in _OPTYPES
        # zero
        if not self:
            return self
        # else
        if self.optype == ADDITIVE:
            return self._square_additive()
        else:
            return self._square_multiplicative()

    def _square_additive(self):
        """
        Return the square of self, if self.optype == ADDITIVE.
        """
        data_length = len(self._data)
        # monomial
        if data_length == 1:
            return self.__class__([(b + b, c**2) for (b, c) in self._data.iterterms()], self.optype)
        # binomial
        if data_length == 2:
            (d1, c1), (d2, c2) = [(d, c) for (d, c) in self._data.iterterms()]
            sq_map = {d1 + d1: c1**2}
            b, c = d1 + d2, c1 * c2 * 2
            if b in sq_map:
                sq_map[b] += c
            else:
                sq_map[b] = c
            b, c = d2 + d2, c2**2
            if b in sq_map:
                sq_map[b] += c
            else:
                sq_map[b] = c
            return self.__class__(sq_map, self.optype)
        # general
        items = self._data.terms()
        fst, snd = {}, {}
        if data_length % 2 == 1:
            b, c = items.pop()
            fst[b] = c
        while items:
            b, c = items.pop()
            fst[b] = c
            b, c = items.pop()
            snd[b] = c
        fst = self.__class__(fst, self.optype)
        snd = self.__class__(snd, self.optype)
        mid = fst.ring_mul(snd.scalar_mul(2))
        return fst.square() + mid + snd.square()

    def _square_multiplicative(self):
        """
        Return the square of self, if self.optype == MULTIPLICATIVE.
        """
        data_length = len(self._data)
        # monomial
        if data_length == 1:
            return self.__class__([(b * b, c**2) for (b, c) in self._data.iterterms()], self.optype)
        # binomial
        sq_map = {}
        for d1, c1 in self._data.iterterms():
            for d2, c2 in self._data.iterterms():
                b, c = d1 * d2, c1 * c2
                if b in sq_map:
                    sq_map[b] += c
                else:
                    sq_map[b] = c
        return self.__class__(sq_map, self.optype)

    def __pow__(self, index):
        """
        self ** index
        """
        # special indeces
        if index < 0:
            raise ValueError("negative index is not allowed.")
        elif index == 0:
            zero, one = self.optype, 1
            for d, c in self._data.iterterms():
                zero = self.optype.op2(d, 0)
                if c:
                    one = _ring.getRing(c).one
                    break
            return self.__class__({zero: one})
        elif index == 1:
            return self
        elif index == 2:
            return self.square()
        # special polynomials
        if not self:
            return self
        elif len(self._data) == 1:
            d = self.optype.op2(self._data.bases()[0], index)
            c = self._data.coefficients()[0] ** index
            return self.__class__([(d, c)])
        # general
        power_product = self.__class__({0: 1})
        power_of_2 = self
        while index:
            if index & 1:
                power_product *= power_of_2
            index //= 2
            if index:
                power_of_2 = power_of_2.square()
        return power_product

    def __nonzero__(self):
        """
        if self is not zero, return True.
        """
        if self._data:
            return True
        return False

    def __eq__(self, other):
        """
        self == other
        """
        if self is other:
            return True
        if not isinstance(other, SemigroupAlgebraElement):
            return False
        if self._data == other._data:
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
        return sum([hash(c)*hash(d) for (d, c) in self._data.iterterms()]) & 0x7fff

    def __repr__(self): # for debug
        optype_str = "ADDITIVE"
        if self.optype == MULTIPLICATIVE:
            optype_str = "MULTIPLICATIVE"
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self._data), optype_str)


class SemigroupAlgebra (object):
    """
    Semigroup algebra.
    """
    def __init__(self, ring, semigroup):
        """
        SemigroupAlgebra(r, s)

        A semimgroup indexed direct sum of the given commutative ring
        r forms an r-algebra by defining multiplication from the
        operation of the semigroup s.

        If the semigroup s has an identity element, i.e. s is a
        monoid, the algebra is in fact a ring (with unity).
        """
        self.ring = ring
        # FIXME: there is no definition of semigroup
        self.semigroup = semigroup
