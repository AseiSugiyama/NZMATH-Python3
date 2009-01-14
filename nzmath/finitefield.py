"""
finite fields.
"""

from __future__ import division
import logging
import nzmath.gcd as gcd
import nzmath.bigrandom as bigrandom
import nzmath.bigrange as bigrange
import nzmath.arith1 as arith1
import nzmath.prime as prime
import nzmath.ring as ring
import nzmath.rational as rational
import nzmath.factor.misc as factor_misc
import nzmath.intresidue as intresidue
import nzmath.poly.univar as univar
import nzmath.poly.uniutil as uniutil
import nzmath.compatibility

_log = logging.getLogger('nzmath.finitefield')


class FiniteFieldElement(ring.FieldElement):
    """
    The base class for all finite field element.
    """
    def __init__(self):
        # This class is abstract and can not be instanciated.
        if type(self) is FiniteFieldElement:
            raise NotImplementedError("the class FiniteFieldElement is abstract")
        ring.FieldElement.__init__(self)


class FiniteField(ring.Field):
    """
    The base class for all finite fields.
    """
    def __init__(self, characteristic):
        # This class is abstract and can not be instanciated.
        if type(self) is FiniteField:
            raise NotImplementedError("the class FiniteField is abstract")
        ring.Field.__init__(self)
        self.char = characteristic
        self._orderfactor = None  # postpone the initialization

    def card(self):
        "Cardinality of the field"
        raise NotImplementedError("card have to be overridden")

    def getCharacteristic(self):
        """
        Return the characteristic of the field.
        """
        return self.char

    def order(self, elem):
        """
        Find and return the order of the element in the multiplicative
        group of the field.
        """
        if not elem:
            raise ValueError("zero is not in the multiplicative group.")
        if self._orderfactor is None:
            self._orderfactor = factor_misc.FactoredInteger(card(self) - 1)
        o = 1
        for p, e in self._orderfactor:
            b = elem ** (int(self._orderfactor) // (p**e))
            while b != self.one:
                o = o * p
                b = b ** p
        return o

    def random_element(self, *args):
        """
        Return a randomly chosen element og the field.
        """
        return self.createElement(bigrandom.randrange(*args))

    def primitive_element(self):
        """
        Return a primitive element of the field, i.e., a generator of
        the multiplicative group.
        """
        raise NotImplementedError("primitive_element should be overridden")

    def Legendre(self, element):
        """ Return generalize Legendre Symbol for FiniteField.
        """
        if not element:
            return 0

        if element == self.one or self.char == 2:
            return 1 # element of cyclic group order 2**n-1 also always 1

        # generic method:successive squaring
        # generalized Legendre symbol definition:
        #    (self/_ring) := self ** ((card(_ring)-1)/2)
        x = element ** ((card(self)-1) // 2)
        if x == self.one:
            return 1
        elif x == -self.one:
            return -1
        raise ValueError("element must be not in field")

    def TonelliShanks(self, element):
        """ Return square root of element if exist.
        assume that characteristic have to be more than three.
        """
        if  self.char == 2:
            return self.sqrt(element) # should be error

        if self.Legendre(element) == -1:
            raise ValueError("There is no solution")

        # symbol and code reference from Cohen, CCANT 1.5.1
        (e, q) = arith1.vp(card(self)-1, 2)

        a = element
        n = self.createElement(self.char+1)
        while self.Legendre(n) != -1:
            n = self.random_element(2, card(self)) # field maybe large
        y = z = n ** q
        r = e
        x = a ** ((q-1) // 2)
        b = a * (x ** 2)
        x = a * x
        while True:
            if b == self.one:
                return x
            m = 1
            while m < r:
                if b ** (2 ** m) == self.one:
                    break
                m = m+1
            if m == r:
                break
            t = y ** (2 ** (r-m-1))
            y = t ** 2
            r = m
            x = x * t
            b = b * y
        raise ValueError("There is no solution")

    def sqrt(self, element):
        """ Return square root if exist.
        """
        if not element or element == self.one:
            return element # trivial case

        # element of characteristic 2 always exist square root
        if  self.char == 2:
            return element ** ((card(self)) // 2)

        # otherwise,
        return self.TonelliShanks(element)


class FinitePrimeFieldElement(intresidue.IntegerResidueClass, FiniteFieldElement):
    """
    The class for finite prime field element.
    """
    def __init__(self, representative, modulus, modulus_is_prime=True):
        if not modulus_is_prime and not prime.primeq(abs(modulus)):
            raise ValueError("modulus must be a prime.")

        FiniteFieldElement.__init__(self)
        intresidue.IntegerResidueClass.__init__(self, representative, modulus)

        # ring
        self.ring = None

    def __repr__(self):
        return "FinitePrimeFieldElement(%d, %d)" % (self.n, self.m)

    def __str__(self):
        return "%d in F_%d" % (self.n, self.m)

    def getRing(self):
        """
        Return the finite prime field to which the element belongs.
        """
        if self.ring is None:
            self.ring = FinitePrimeField.getInstance(self.m)
        return self.ring

    def order(self):
        """
        Find and return the order of the element in the multiplicative
        group of F_p.
        """
        if self.n == 0:
            raise ValueError("zero is not in the group.")
        if not hasattr(self, "orderfactor"):
            self.orderfactor = factor_misc.FactoredInteger(self.m - 1)
        o = 1
        for p, e in self.orderfactor:
            b = self ** (int(self.orderfactor) // (p**e))
            while b.n != 1:
                o = o*p
                b = b**p
        return o


class FinitePrimeField(FiniteField):
    """
    FinitePrimeField is also known as F_p or GF(p).
    """

    # class variable
    _instances = {}

    def __init__(self, characteristic):
        FiniteField.__init__(self, characteristic)
        self.registerModuleAction(rational.theIntegerRing, self._int_times)
        # mathematically Q_p = Q \ {r/s; gcd(r, s) == 1, gcd(s, p) > 1}
        # is more appropriate.
        self.registerModuleAction(rational.theRationalField, self._rat_times)

    @staticmethod
    def _int_times(integer, fpelem):
        """
        Return k * FinitePrimeFieldElement(n, p)
        """
        return FinitePrimeFieldElement(integer * fpelem.n, fpelem.m)

    @staticmethod
    def _rat_times(rat, fpelem):
        """
        Return Rational(a, b) * FinitePrimeFieldElement(n, p)
        """
        return FinitePrimeFieldElement(rat * fpelem.n, fpelem.m)

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, FinitePrimeField):
            return self.char == other.char
        return False

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "F_%d" % self.char

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.char)

    def __hash__(self):
        return self.char & 0xFFFFFFFF

    def issubring(self, other):
        """
        Report whether another ring contains the field as a subring.
        """
        if self == other:
            return True
        if isinstance(other, FiniteField) and other.getCharacteristic() == self.char:
            return True
        try:
            return other.issuperring(self)
        except:
            return False

    def issuperring(self, other):
        """
        Report whether the field is a superring of another ring.
        Since the field is a prime field, it can be a superring of
        itself only.
        """
        return self == other

    def __contains__(self, elem):
        if isinstance(elem, FinitePrimeFieldElement) and elem.getModulus() == self.char:
            return True
        return False

    def createElement(self, seed):
        """
        Create an element of the field.

        'seed' should be an integer.
        """
        return FinitePrimeFieldElement(seed, self.char, modulus_is_prime=True)

    def primitive_element(self):
        """
        Return a primitive element of the field, i.e., a generator of
        the multiplicative group.
        """
        if self.char == 2:
            return self.one
        fullorder = card(self) - 1
        if self._orderfactor is None:
            self._orderfactor = factor_misc.FactoredInteger(fullorder)
        for i in bigrange.range(2, self.char):
            g = self.createElement(i)
            for p in self._orderfactor.prime_divisors():
                if g ** (fullorder // p) == self.one:
                    break
            else:
                return g

    def Legendre(self, element):
        """ Return generalize Legendre Symbol for FinitePrimeField.
        """
        if not element:
            return 0
        if element.n == 1 or element.m == 2:
            return 1 # trivial

        return arith1.legendre(element.n, element.m)

    def SquareRoot(self, element):
        """ Return square root if exist.
        """
        if not element or element.n == 1:
            return element # trivial case
        if element.m == 2:
            return element.getRing().one
        return arith1.modsqrt(element.n, element.m)

    def card(self):
        "Cardinality of the field"
        return self.char

    # properties
    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = FinitePrimeFieldElement(1, self.char)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = FinitePrimeFieldElement(0, self.char)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")

    @classmethod
    def getInstance(cls, characteristic):
        """
        Return an instance of the class with specified characteristic.
        """
        if characteristic not in cls._instances:
            cls._instances[characteristic] = cls(characteristic)
        return cls._instances[characteristic]


FinitePrimeFieldPolynomial = uniutil.FinitePrimeFieldPolynomial
uniutil.special_ring_table[FinitePrimeField] = FinitePrimeFieldPolynomial


class FiniteExtendedFieldElement(FiniteFieldElement):
    """
    FiniteExtendedFieldElement is a class for an element of F_q.
    """
    def __init__(self, representative, field):
        """
        FiniteExtendedFieldElement(representative, field) creates
        an element of the finite extended field.

        The argument representative must be an F_p polynomial
        (an instance of FinitePrimeFieldPolynomial).

        Another argument field mut be an instance of
        FiniteExtendedField.
        """
        if isinstance(field, FiniteExtendedField):
            self.field = field
        else:
            raise TypeError("wrong type argument for field.")
        if (isinstance(representative, FinitePrimeFieldPolynomial) and
            isinstance(representative.getCoefficientRing(), FinitePrimeField)):
            self.rep = self.field.modulus.mod(representative)
        else:
            _log.debug(representative.__class__.__name__)
            raise TypeError("wrong type argument for representative.")

    def getRing(self):
        """
        Return the field to which the element belongs.
        """
        return self.field

    def _op(self, other, op):
        """
        Do `self (op) other'.
        op must be a name of the special method for binary operation.
        """
        if isinstance(other, FiniteExtendedFieldElement):
            if other.field is self.field:
                result = self.field.modulus.mod(getattr(self.rep, op)(other.rep))
                return self.__class__(result, self.field)
            else:
                fq1, fq2 = self.field, other.field
                emb1, emb2 = double_embeddings(fq1, fq2)
                return getattr(emb1(self), op)(emb2(other))
        if self.field.hasaction(ring.getRing(other)):
            # cases for action ring elements
            embedded = self.field.getaction(ring.getRing(other))(other, self.field.one)
            result = self.field.modulus.mod(getattr(self.rep, op)(embedded.rep))
            return self.__class__(result, self.field)
        else:
            return NotImplemented

    def __add__(self, other):
        """
        self + other

        other can be an element of either F_q, F_p or Z.
        """
        if other is 0 or other is self.field.zero:
            return self
        return self._op(other, "__add__")

    __radd__ = __add__

    def __sub__(self, other):
        """
        self - other

        other can be an element of either F_q, F_p or Z.
        """
        if other is 0 or other is self.field.zero:
            return self
        return self._op(other, "__sub__")

    def __rsub__(self, other):
        """
        other - self

        other can be an element of either F_q, F_p or Z.
        """
        return self._op(other, "__rsub__")

    def __mul__(self, other):
        """
        self * other

        other can be an element of either F_q, F_p or Z.
        """
        if other is 1 or other is self.field.one:
            return self
        return self._op(other, "__mul__")

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * other.inverse()

    __div__ = __truediv__

    def inverse(self):
        """
        Return the inverse of the element.
        """
        if not self:
            raise ZeroDivisionError("There is no inverse of zero.")
        return self.__class__(self.rep.extgcd(self.field.modulus)[0], self.field)

    def __pow__(self, index):
        """
        self ** index

        pow() with three arguments is not supported.
        """
        if not self:
            return self # trivial
        if index < 0:
            index %= self.field.getCharacteristic()
        power = pow(self.rep, index, self.field.modulus)
        return self.__class__(power, self.field)

    def __neg__(self):
        return self.field.zero - self

    def __pos__(self):
        return self

    def __eq__(self, other):
        try:
            if self.field == other.field:
                if self.rep == other.rep:
                    return True
        except AttributeError:
            pass
        return False

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return self.rep.__nonzero__()

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.rep), repr(self.field))

    def trace(self):
        """
        Return the absolute trace.
        """
        p = self.field.char
        q = p
        alpha = self
        tr = alpha.rep[0]
        while q < card(self.field):
            q *= p
            alpha **= p
            tr += alpha.rep[0]
        if tr not in FinitePrimeField.getInstance(p):
            tr = FinitePrimeField.getInstance(p).createElement(tr)
        return tr

    def norm(self):
        """
        Return the absolute norm.
        """
        p = self.field.char
        nrm = (self ** ((card(self.field) - 1) // (p - 1))).rep[0]
        if nrm not in FinitePrimeField.getInstance(p):
            nrm = FinitePrimeField.getInstance(p).createElement(nrm)
        return nrm


class FiniteExtendedField(FiniteField):
    """
    FiniteExtendedField is a class for finite field, whose cardinality
    q = p**n with a prime p and n>1. It is usually called F_q or GF(q).
    """
    def __init__(self, characteristic, n_or_modulus):
        """
        FiniteExtendedField(p, n_or_modulus) creates a finite field.
        characteristic must be prime. n_or_modulus can be:
          1) an integer greater than 1, or
          2) a polynomial in a polynomial ring of F_p with degree
             greater than 1.
        """
        FiniteField.__init__(self, characteristic)
        self.basefield = FinitePrimeField.getInstance(self.char)
        if isinstance(n_or_modulus, (int, long)):
            if n_or_modulus <= 1:
                raise ValueError("degree of extension must be > 1.")
            self.degree = n_or_modulus
            # choose a method among three variants:
            #self.modulus = self._random_irriducible()
            #self.modulus = self._small_irriducible()
            self.modulus = self._primitive_polynomial()
        elif isinstance(n_or_modulus, FinitePrimeFieldPolynomial):
            if isinstance(n_or_modulus.getCoefficientRing(), FinitePrimeField):
                if n_or_modulus.degree() > 1 and n_or_modulus.isirreducible():
                    self.degree = n_or_modulus.degree()
                    self.modulus = n_or_modulus
                else:
                    raise ValueError("modulus must be of degree greater than 1.")
            else:
                raise TypeError("modulus must be F_p polynomial.")
        else:
            raise TypeError("degree or modulus must be supplied.")
        self.registerModuleAction(rational.theIntegerRing, self._int_mul)
        self.registerModuleAction(FinitePrimeField.getInstance(self.char), self._fp_mul)

    def _random_irriducible(self):
        """
        Return randomly chosen irreducible polynomial of self.degree.
        """
        cardinality = self.char ** self.degree
        seed = bigrandom.randrange(1, self.char) + cardinality
        cand = uniutil.polynomial(enumerate(arith1.expand(seed, self.char)), coeffring=self.basefield)
        while cand.degree() < self.degree or not cand.isirreducible():
            seed = bigrandom.randrange(1, cardinality) + cardinality
            cand = uniutil.polynomial(enumerate(arith1.expand(seed, self.char)), coeffring=self.basefield)
        _log.debug(cand.order.format(cand))
        return cand

    def _small_irriducible(self):
        """
        Return an irreducible polynomial of self.degree with a small
        number of non-zero coefficients.
        """
        cardinality = self.char ** self.degree
        top = uniutil.polynomial({self.degree: 1}, coeffring=self.basefield)
        for seed in range(self.degree - 1):
            for const in range(1, self.char):
                coeffs = [const] + arith1.expand(seed, 2)
                cand = uniutil.polynomial(enumerate(coeffs), coeffring=self.basefield) + top
                if cand.isirreducible():
                    _log.debug(cand.order.format(cand))
                    return cand
        for subdeg in range(self.degree):
            subseedbound = self.char ** subdeg
            for subseed in range(subseedbound + 1, self.char * subseedbound):
                if not subseed % self.char:
                    continue
                seed = subseed + cardinality
                cand = uniutil.polynomial(enumerate(arith1.expand(seed, self.char)), coeffring=self.basefield)
                if cand.isirreducible():
                    return cand

    def _primitive_polynomial(self):
        """
        Return a primitive polynomial of self.degree.

        REF: Lidl & Niederreiter, Introduction to finite fields and
             their applications.
        """
        cardinality = self.char ** self.degree
        const = self.basefield.primitive_element()
        if self.degree % 2:
            const = -const
        cand = uniutil.polynomial({0:const, self.degree:self.basefield.one}, self.basefield)
        maxorder = factor_misc.FactoredInteger((card(self) - 1) // (self.char - 1))
        var = uniutil.polynomial({1:self.basefield.one}, self.basefield)
        while not (cand.isirreducible() and
                   all(pow(var, int(maxorder) // p, cand).degree() > 0 for p in maxorder.prime_divisors())):
            # randomly modify the polynomial
            deg = bigrandom.randrange(1, self.degree)
            coeff = self.basefield.random_element(1, self.char)
            cand += uniutil.polynomial({deg:coeff}, self.basefield)
        _log.debug(cand.order.format(cand))
        return cand

    @staticmethod
    def _int_mul(integer, fqelem):
        """
        Return integer * (Fq element).
        """
        return fqelem.__class__(fqelem.rep * integer, fqelem.field)

    @staticmethod
    def _fp_mul(fpelem, fqelem):
        """
        Return (Fp element) * (Fq element).
        """
        newrep = fqelem.rep * fpelem
        return fqelem.__class__(newrep, fqelem.field)

    def card(self):
        """
        Return the cardinality of the field
        """
        return self.char ** self.degree

    def createElement(self, seed):
        """
        Create an element of the field.
        """
        if isinstance(seed, (int, long)):
            expansion = arith1.expand(seed, self.char)
            return FiniteExtendedFieldElement(
                FinitePrimeFieldPolynomial(enumerate(expansion), self.basefield),
                self)
        elif isinstance(seed, FinitePrimeFieldPolynomial):
            return FiniteExtendedFieldElement(seed, self)
        elif isinstance(seed, FinitePrimeFieldElement) and seed.m == self.getCharacteristic():
            return FiniteExtendedFieldElement(
                FinitePrimeFieldPolynomial([(0, seed)], self.basefield),
                self)
        elif seed in self:
            # seed is in self, return only embedding
            return self.zero + seed
        else:
            try:
                # lastly check sequence
                return FiniteExtendedFieldElement(
                    FinitePrimeFieldPolynomial(enumerate(seed), self.basefield),
                    self)
            except TypeError:
                raise TypeError("seed %s is not an appropriate object." % str(seed))

    def __repr__(self):
        return "%s(%d, %d)" % (self.__class__.__name__, self.char, self.degree)

    def __str__(self):
        return "F_%d @(%s)" % (card(self), str(self.modulus))

    def __hash__(self):
        return (self.char ** self.degree) & 0xFFFFFFFF

    def issuperring(self, other):
        """
        Report whether the field is a superring of another ring.
        """
        if self is other:
            return True
        if isinstance(other, FiniteExtendedField):
            if self.char == other.char and not (self.degree % other.degree):
                return True
            return False
        if isinstance(other, FinitePrimeField):
            if self.char == other.getCharacteristic():
                return True
            return False
        try:
            return other.issubring(self)
        except:
            return False

    def issubring(self, other):
        """
        Report whether the field is a subring of another ring.
        """
        if self is other:
            return True
        if isinstance(other, FinitePrimeField):
            return False
        if isinstance(other, FiniteExtendedField):
            if self.char == other.char and not (other.degree % self.degree):
                return True
            return False
        try:
            return other.issuperring(self)
        except:
            return False

    def __contains__(self, elem):
        """
        Report whether elem is in field.
        """
        if isinstance(elem, FiniteExtendedFieldElement) and \
               elem.getRing().modulus == self.modulus:
            return True
        elif isinstance(elem, FinitePrimeFieldElement) and \
                 elem.getRing().getCharacteristic() == self.getCharacteristic():
            return True
        return False

    def __eq__(self, other):
        """
        Equality test.
        """
        if isinstance(other, FiniteExtendedField):
            return self.char == other.char and self.degree == other.degree
        return False

    def primitive_element(self):
        """
        Return a primitive element of the field, i.e., a generator of
        the multiplicative group.
        """
        fullorder = card(self) - 1
        if self._orderfactor is None:
            self._orderfactor = factor_misc.FactoredInteger(fullorder)
        for i in bigrange.range(self.char, card(self)):
            g = self.createElement(i)
            for p in self._orderfactor.prime_divisors():
                if g ** (fullorder // p) == self.one:
                    break
            else:
                return g

    # properties
    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = FiniteExtendedFieldElement(
                FinitePrimeFieldPolynomial(
                [(0, 1)], self.basefield),
                self)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = FiniteExtendedFieldElement(
                FinitePrimeFieldPolynomial(
                [], self.basefield),
                self)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


def fqiso(f_q, gfq):
    """
    Return isomorphism function of extended finite fields from f_q to gfq.
    """
    if f_q is gfq:
        return lambda x: x
    if card(f_q) != card(gfq):
        raise TypeError("both fields must have the same cardinality.")

    # find a root of f_q's defining polynomial in gfq.
    p = f_q.getCharacteristic()
    q = card(f_q)
    for i in bigrange.range(p, q):
        root = gfq.createElement(i)
        if not f_q.modulus(root):
            break

    # finally, define a function
    def f_q_to_gfq_iso(f_q_elem):
        """
        Return the image of the isomorphism of the given element.
        """
        if not f_q_elem:
            return gfq.zero
        if f_q_elem.rep.degree() == 0:
            # F_p elements
            return gfq.createElement(f_q_elem.rep)
        return f_q_elem.rep(root)

    return f_q_to_gfq_iso


def embedding(f_q1, f_q2):
    """
    Return embedding homomorphism function from f_q1 to f_q2,
    where q1 = p ** k1, q2 = p ** k2 and k1 divides k2.
    """
    if card(f_q1) == card(f_q2):
        return fqiso(f_q1, f_q2)
    # search multiplicative generators of both fields and relate them.
    # 0. initialize basic variables
    p = f_q2.getCharacteristic()
    q1, q2 = card(f_q1), card(f_q2)

    # 1. find a multiplicative generator of f_q2
    f_q2_gen = f_q2.primitive_element()
    f_q2_subgen = f_q2_gen ** ((q2 - 1) // (q1 - 1))

    # 2. find a root of defining polynomial of f_q1 in f_q2
    image_of_x_1 = _findroot(f_q2_subgen, f_q1)

    # 3. finally, define a function
    def f_q1_to_f_q2_homo(f_q1_elem):
        """
        Return the image of the isomorphism of the given element.
        """
        if not f_q1_elem:
            return f_q2.zero
        if f_q1_elem.rep.degree() == 0:
            # F_p elements
            return f_q2.createElement(f_q1_elem.rep)
        return f_q1_elem.rep(image_of_x_1)

    return f_q1_to_f_q2_homo

def _findroot(f_q2_subgen, f_q1):
    """
    Find root of the defining polynomial of f_q1 in f_q2
    """
    root = f_q2_subgen
    for i in range(1, card(f_q1)):
        if not f_q1.modulus(root):
            image_of_x_1 = root
            break
        root *= f_q2_subgen
    return image_of_x_1

def double_embeddings(f_q1, f_q2):
    """
    Return embedding homomorphism functions from f_q1 and f_q2
    to the composite field.
    """
    identity = lambda x: x
    if f_q1 is f_q2:
        return (identity, identity)
    p = f_q2.getCharacteristic()
    k1, k2 = f_q1.degree, f_q2.degree
    if not k2 % k1:
        return (embedding(f_q1, f_q2), identity)
    if not k1 % k2:
        return (identity, embedding(f_q2, f_q1))
    composite = FiniteExtendedField(p, gcd.lcm(k1, k2))
    return (embedding(f_q1, composite), embedding(f_q2, composite))
