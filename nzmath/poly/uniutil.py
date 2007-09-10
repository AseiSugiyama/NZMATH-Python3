"""
Utilities for univar.

The module provides higher level interfaces to univar classes and
functions.
"""

from __future__ import division
import nzmath.bigrandom as bigrandom
import nzmath.polynomial as old_polynomial
import nzmath.rational as rational
import nzmath.rationalFunction as rationalFunction
import nzmath.ring as ring
import nzmath.poly.univar as univar
import nzmath.poly.termorder as termorder


_MIXIN_MSG = "%s is mix-in"


class OrderProvider (object):
    """
    OrderProvider provides order and related operations.
    """
    def __init__(self, order=termorder.ascending_order):
        """
        Do not instanciate OrderProvider.
        This initializer should be called from descendant:
          OrderProvider.__init__(self, order)
        where order is default to termorder.ascending_order.
        """
        if type(self) is OrderProvider:
            raise NotImplementedError(_MIXIN_MSG % self.__class__.__name__)
        self.order = order

    def shift_degree_to(self, degree):
        """
        Return polynomial whose degree is the given degree.

        More precisely, let f(X) = a_0 + ... + a_n * X**n, then
        order.shift_degree_to(f, m) returns:
        - zero polynomial, if f is zero polynomial
        - a_(n-m) + ... + a_n * X**m, if 0 <= m < n
        - a_0 * X**(m-n) + ... + a_n * X**m, if m >= n
        """
        original_degree = self.order.degree(self)
        difference = degree - original_degree
        if difference == 0:
            return self
        elif difference < 0:
            return self.__class__([(d + difference, c) for (d, c) in self if d + difference >= 0], **self._init_kwds)
        else:
            return self.upshift_degree(difference)

    def split_at(self, degree):
        """
        Return tuple of two polynomials, which are splitted at the
        given degree.  The term of the given degree, if exists,
        belongs to the lower degree polynomial.
        """
        lower, upper = [], []
        for d, c in self:
            if self.order.cmp(d, degree) <= 0:
                lower.append((d, c))
            else:
                upper.append((d, c))
        return (self.__class__(lower, **self._init_kwds),
                self.__class__(upper, **self._init_kwds))


class DivisionProvider (object):
    """
    DivisionProvider provides all kind of divisions for univariate
    polynomials.  It is assumed that the coefficient ring of the
    polynomials is a field.

    The class should be used as a mix-in.

    REQUIRE: OrderProvider
    """
    def __init__(self):
        """
        Do not instanciate DivisionProvider.
        This initializer should be called from descendant.
        """
        if type(self) is DivisionProvider:
            raise NotImplementedError(_MIXIN_MSG % self.__class__.__name__)
        self._reduced = None

    def __divmod__(self, other):
        """
        divmod(self, other)

        The method does, as the built-in divmod, return a tuple of
        (self // other, self % other).
        """
        degree, lc = self.order.leading_term(other)
        quotient, remainder = [], self
        while self.order.degree(remainder) >= degree:
            rdegree, rlc = self.order.leading_term(remainder)
            q = rdegree - degree, rlc / lc
            remainder = remainder - other.term_mul(q)
            quotient.append(q)
        quotient = self.__class__(quotient, **self._init_kwds)
        return quotient, remainder

    def __floordiv__(self, other):
        """
        self // other
        """
        degree, lc = self.order.leading_term(other)
        quotient, remainder = [], self
        while self.order.degree(remainder) >= degree:
            rdegree, rlc = self.order.leading_term(remainder)
            q = rdegree - degree, rlc / lc
            remainder = remainder - other.term_mul(q)
            quotient.append(q)
        return self.__class__(quotient, **self._init_kwds)

    def __mod__(self, other):
        """
        self % other
        """
        degree, lc = self.order.leading_term(other)
        remainder = self
        rdegree, rlc = self.order.leading_term(remainder)
        if rdegree <= degree * 2:
            return other.mod(remainder)
        while rdegree >= degree:
            q = rdegree - degree, rlc / lc
            remainder = remainder - other.term_mul(q)
            rdegree, rlc = self.order.leading_term(remainder)
        return remainder

    def mod(self, dividend):
        """
        Return dividend % self.

        self should have attribute _reduced to cache reduced monomials.
        """
        degree, lc = self.order.leading_term(self)
        if not self._reduced:
            self._reduced = {}
            one = ring.getRing(self.itercoefficients().next()).one
            redux = self.__class__([(degree, one)], **self._init_kwds)
            moniced = self.scalar_mul(one / lc)
            for i in range(degree, degree * 2 + 1):
                if self.order.degree(redux) == degree:
                    redux -= moniced.scalar_mul(self.order.leading_coefficient(redux))
                self._reduced[i] = redux
                redux = redux.term_mul((1, 1))
        div_deg = self.order.degree(dividend)
        if div_deg > degree * 2:
            dividend %= self.square()
        assert self.order.degree(dividend) <= degree * 2
        accum = self.__class__((), **self._init_kwds)
        lowers = []
        for d, c in dividend:
            if c:
                if d < degree:
                    lowers.append((d, c))
                else:
                    accum += self._reduced[d].scalar_mul(c)
        return accum + self.__class__(lowers, **self._init_kwds)

    def __truediv__(self, other):
        """
        self / other

        The result is a rational function.
        """
        return rationalFunction.RationalFunction(self, other)

    def scalar_exact_division(self, scale):
        """
        Return quotient by a scalar which can divide each coefficient
        exactly.
        """
        return self.coefficients_map(lambda c: c.exact_division(scale))

    def gcd(self, other):
        """
        Return a greatest common divisor of self and other.
        Returned polynomial is always monic.
        """
        divident = self
        divisor = other
        while divisor:
            divident, divisor = divisor, divident % divisor
        lc = self.order.leading_coefficient(divident)
        if lc and lc != 1:
            divident = divident.scalar_exact_division(lc)
        return divident

    def extgcd(self, other):
        """
        Return a tuple (u, v, d); they are the greatest common divisor
        d of two polynomials self and other and u, v such that
        d = self * u + other * v.

        see nzmath.gcd.extgcd
        """
        order = termorder.ascending_order
        polynomial_ring = self.getRing()
        zero, one = polynomial_ring.zero, polynomial_ring.one
        a, b, g, u, v, w = one, zero, self, zero, one, other
        while w:
            q = g // w
            a, b, g, u, v, w = u, v, w, a - q*u, b - q*v, g - q*w
        lc = self.order.leading_coefficient(g)
        if lc and lc != 1:
            linv = lc.inverse()
            a, b, g = linv * a, linv * b, linv * g
        return (a, b, g)


class PseudoDivisionProvider (object):
    """
    PseudoDivisionProvider provides pseudo divisions for univariate
    polynomials.  It is assumed that the coefficient ring of the
    polynomials is a domain.

    The class should be used as a mix-in.
    """
    def pseudo_divmod(self, other):
        """
        self.pseudo_divmod(other) -> (Q, R)

        Q, R are polynomials such that
        d**(deg(self) - deg(other) + 1) * self == other * Q + R,
        where d is the leading coefficient of other.
        """
        order = termorder.ascending_order
        if hasattr(self, 'order'):
            assert self.order is order
        degree, lc = order.leading_term(other)
        # step 1
        quotient, remainder = self.__class__((), **self._init_kwds), self
        rdegree, rlc = order.leading_term(remainder)
        e = order.degree(remainder) - degree + 1
        if e <= 0:
            return quotient, remainder
        while rdegree >= degree:
            # step 3
            canceller = self.__class__([(rdegree - degree, rlc)], **self._init_kwds)
            quotient = quotient.scalar_mul(lc) + canceller
            remainder = remainder.scalar_mul(lc) - canceller * other
            e -= 1
            rdegree, rlc = order.leading_term(remainder)
        # step 2
        q = lc ** e
        quotient = quotient.scalar_mul(q)
        remainder = remainder.scalar_mul(q)
        return quotient, remainder

    def pseudo_floordiv(self, other):
        """
        self.pseudo_floordiv(other) -> Q

        Q is a polynomial such that
        d**(deg(self) - deg(other) + 1) * self == other * Q + R,
        where d is the leading coefficient of other and R is a
        polynomial.
        """
        order = termorder.ascending_order
        if hasattr(self, 'order'):
            assert self.order is order
        degree, lc = order.leading_term(other)
        # step 1
        quotient, remainder = self.__class__((), **self._init_kwds), self
        rdegree, rlc = order.leading_term(remainder)
        e = order.degree(remainder) - degree + 1
        if e <= 0:
            return quotient
        while rdegree >= degree:
            # step 3
            canceller = self.__class__([(rdegree - degree, rlc)], **self._init_kwds)
            quotient = quotient.scalar_mul(lc) + canceller
            remainder = remainder.scalar_mul(lc) - canceller * other
            e -= 1
            rdegree, rlc = order.leading_term(remainder)
        # step 2
        return quotient.scalar_mul(lc ** e)

    def pseudo_mod(self, other):
        """
        self.pseudo_mod(other) -> R

        R is a polynomial such that
        d**(deg(self) - deg(other) + 1) * self == other * Q + R,
        where d is the leading coefficient of other and Q a
        polynomial.
        """
        order = termorder.ascending_order
        if hasattr(self, 'order'):
            assert self.order is order
        degree, lc = order.leading_term(other)
        # step 1
        remainder = self
        rdegree, rlc = order.leading_term(remainder)
        e = order.degree(remainder) - degree + 1
        if e <= 0:
            return remainder
        while rdegree >= degree:
            # step 3
            canceller = self.__class__([(rdegree - degree, rlc)], **self._init_kwds)
            remainder = remainder.scalar_mul(lc) - canceller * other
            e -= 1
            rdegree, rlc = order.leading_term(remainder)
        # step 2
        return remainder.scalar_mul(lc ** e)

    def __truediv__(self, other):
        """
        self / other

        Return the result as a rational function.
        """
        order = termorder.ascending_order
        return rationalFunction.RationalFunction(self, other)

    def exact_division(self, other):
        """
        Return quotient of exact division.
        """
        order = termorder.ascending_order
        if hasattr(self, 'order'):
            assert self.order is order
        quotient, remainder = self.pseudo_divmod(other)
        if not remainder:
            deg_other, lc = order.leading_term(other)
            deg_self = order.degree(self)
            extra_factor = lc ** (deg_self - deg_other + 1)
            return quotient.scalar_exact_division(extra_factor)
        raise ValueError("division is not exact")

    def scalar_exact_division(self, scale):
        """
        Return quotient by a scalar which can divide each coefficient
        exactly.
        """
        return self.coefficients_map(lambda c: c.exact_division(scale))


class ContentProvider (object):
    """
    ContentProvider provides content and primitive part.

    The coefficient ring must be a unique factorization domain.
    """
    def content(self):
        """
        Return content of the polynomial.
        """
        coeffring = None
        isquotfield = None
        cont = 0
        num, den = 0, 1
        for c in self.itercoefficients():
            if isquotfield is None:
                coeffring = c.getRing()
                if coeffring.isfield() and isinstance(coeffring, ring.QuotientField):
                    isquotfield = True
                    basedomain = coeffring.basedomain
                else:
                    isquotfield = False
            if isquotfield:
                num = basedomain.gcd(num, c.numerator)
                den = basedomain.lcm(den, c.denominator)
            else:
                if not cont:
                    cont = c
                else:
                    cont = coeffring.gcd(cont, c)
        if isquotfield:
            cont = coeffring.createElement(num, den)
        return cont

    def primitive_part(self):
        """
        Return the primitive part of the polynomial.
        """
        return self.scalar_exact_division(self.content())


class SubresultantGcdProvider (object):
    """
    SubresultantGcdProvider provides gcd method using subresultant
    algorithm.

    REQUIRE: PseudoDivisionProvider, ContentProvider
    """
    def subresultant_gcd(self, other):
        """
        Return the greatest common divisor of given polynomials.  They
        must be in the polynomial ring and its coefficient ring must
        be a UFD.

        Reference: Algorithm 3.3.1 of Cohen's book
        """
        order = termorder.ascending_order
        divident = self
        divisor = other
        polynomial_ring = self.getRing()
        one = polynomial_ring.getCoefficientRing().one
        # step 1
        if order.degree(divisor) > order.degree(divident):
            divident, divisor = divisor, divident
        if not divisor:
            return divident
        content_gcd = polynomial_ring.gcd(divident.content(), divisor.content())
        divident = divident.primitive_part()
        divisor = divisor.primitive_part()
        g = h = one

        while 1:
            # step 2
            delta = order.degree(divident) - order.degree(divisor)
            quotient, remainder = divident.pseudo_divmod(divisor)
            if not remainder:
                return divisor.primitive_part().scalar_mul(content_gcd)
            if order.degree(remainder) == 0:
                return polynomial_ring.createElement(content_gcd)

            # step 3
            divident, divisor = divisor, quotient
            if delta == 0 and g != one:
                divisor = divisor.exact_division(g)
            elif delta == 1 and (g != one or h != one):
                divisor = divisor.exact_division(g * h)
            elif delta > 1 and (g != one or h != one):
                divisor = quotient.exact_division(g * h**delta)
            g = divident.leading_coefficient()
            if delta == 1 and h != g:
                h = g
            elif delta > 1 and (g != one or h != one):
                h = g * (h * g) ** (delta - 1)


class PrimeCharacteristicFunctionsProvider (object):
    """
    PrimeCharacteristicFunctionsProvider provides efficient powering
    and factorization for polynomials whose coefficient ring has prime
    characteristic.

    - A client of this mix-in class should use DivisionProvider also.
    - A client of this mix-in class must have attribute ch, which
      stores the prime characteristic of the coefficient ring.
    """
    def __init__(self, ch):
        """
        Do not instanciate PrimeCharacteristicFunctionsProvider.
        This initializer should be called from descendant.
        """
        if type(self) is PrimeCharacteristicFunctionsProvider:
            raise NotImplementedError(_MIXIN_MSG % self.__class__.__name__)
        self.ch = ch

    def __pow__(self, index, mod=None):
        """
        self ** index

        A client of the mix-in class should write the name in front of
        the main class so that the __pow__ defined here would be
        preceded in method resolution order.  For example:

        class Client (PrimeCharacteristicFunctionsProvider
                      DivisionProvider,
                      Polynomial):
        """
        if not isinstance(index, (int, long)):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be a non-negative integer.")
        if mod is not None:
            return mod.mod_pow(self, index)
        if index > 0:
            if not self:
                return self
            q = 1
            while index % self.ch == 0:
                q *= self.ch
                index //= self.ch
            if q > 1:
                powered = self.__class__([(d * q, c ** q) for (d, c) in self], **self._init_kwds)
            else:
                powered = self
        if index == 1:
            return powered
        acoefficient = self.itercoefficients().next()
        one = ring.getRing(acoefficient).one
        power_product = self.__class__({0: one}, **self._init_kwds)
        if index:
            power_of_2 = powered
            while index:
                if index % 2 == 1:
                    power_product *= power_of_2
                power_of_2 = power_of_2 * power_of_2
                index //= 2
        return power_product

    def mod_pow(self, polynom, index):
        """
        Return polynom ** index % self.
        """
        if not self:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        polynom %= self
        if index == 1:
            return polynom
        acoefficient = polynom.itercoefficients().next()
        one = ring.getRing(acoefficient).one
        power_product = self.__class__({0: one}, **self._init_kwds)
        if index:
            power_of_2 = polynom
            while index:
                if index % 2 == 1:
                    power_product = self.mod(power_product * power_of_2)
                power_of_2 = self.mod(power_of_2.square())
                index //= 2
        return power_product

    def squarefree_decomposition(self):
        """
        Return the square free decomposition of the polynomial.  The
        return value is a dict whose keys are integers and values are
        corresponding powered factors.  For example, if
        A = A1 * A2**2,
        the result is {1: A1, 2: A2}.

        gcd method is required.
        """
        result = {}
        if self.order.degree(self) == 1:
            return {1: self}
        f = self
        df = f.differentiate()
        if df:
            b = f.gcd(df)
            a = f.exact_division(b)
            i = 1
            while self.order.degree(a) > 0:
                c = a.gcd(b)
                b = b.exact_division(c)
                if a != c:
                    r = a.exact_division(c)
                    if self.order.degree(r) > 0:
                        result[i] = r
                    a = c
                i += 1
            f = b
        if self.order.degree(f) > 0:
            f = f.pthroot()
            subresult = f.squarefree_decomposition()
            for i, g in subresult.iteritems():
                result[i*self.ch] = g
        return result

    def pthroot(self):
        """
        Return a polynomial obtained by sending X**p to X, where p is
        the characteristic.  If the polynomial does not consist of
        p-th powered terms only, result is nonsense.
        """
        return self.__class__([(d // self.ch, c) for (d, c) in self], **self._init_kwds)

    def distinct_degree_factorization(self):
        """
        Return the distinct degree factorization of the polynomial.
        The return value is a dict whose keys are integers and values
        are corresponding product of factors of the degree.  For
        example, if A = A1 * A2, and all irreducible factors of A1
        having degree 1 and all irreducible factors of A2 having
        degree 2, then the result is:
          {1: A1, 2: A2}.

        The given polynomial must be square free, and its coefficient
        ring must be a finite field.
        """
        Fq = ring.getRing(self.itercoefficients().next())
        q = len(Fq)
        f = self
        x = f.__class__([(1, Fq.one)], **self._init_kwds)
        w = x
        i = 1
        result = {}
        while i*2 <= self.order.degree(f):
            w = pow(w, q, f)
            result[i] = f.gcd(w - x)
            if self.order.degree(result[i]) > 0:
                f = f.exact_division(result[i])
                w = w % f
            else:
                del result[i]
            i += 1
        if self.order.degree(f) != 0:
            result[self.order.degree(f)] = f
        return result

    def split_same_degrees(self, degree):
        """
        Return the irreducible factors of the polynomial.  The
        polynomial must be a product of irreducible factors of the
        given degree.
        """
        r = self.order.degree(self) // degree
        Fq = ring.getRing(self.itercoefficients().next())
        q = len(Fq)
        p = Fq.getCharacteristic()
        if degree == 1:
            result = []
            X = self.__class__([(1, Fq.one)], **self._init_kwds)
            f = self
            while not f[0]:
                f = f // X
                result.append(X)
            if self.order.degree(f) >= 1:
                result.append(f)
        else:
            result = [self]
        while len(result) < r:
            # g is a random polynomial
            rand_coeff = {}
            for i in range(2 * degree):
                rand_coeff[i] = Fq.createElement(bigrandom.randrange(q))
            if not rand_coeff[2 * degree - 1]:
                rand_coeff[2 * degree - 1] = Fq.one
            randpoly = self.__class__(rand_coeff, **self._init_kwds)
            if p == 2:
                G = self.__class__((), **self._init_kwds)
                for i in range(degree * r):
                    G = G + randpoly
                    randpoly = self.mod(randpoly.square())
            else:
                one = self.__class__([(0, Fq.one)], **self._init_kwds)
                G = pow(randpoly, (q**degree - 1)//2, self) - one
            subresult = []
            while result:
                h = result.pop()
                if self.order.degree(h) == degree:
                    subresult.append(h)
                    continue
                z = h.gcd(G)
                if 0 < self.order.degree(z) < self.order.degree(h):
                    subresult.append(z)
                    subresult.append(h.exact_division(z))
                else:
                    subresult.append(h)
            result = subresult
        return result

    def factor(self):
        """
        Factor the polynomial.

        The returned value is a list of tuples whose first component
        is a factor and second component is its multiplicity.
        """
        result = []
        lc = self.order.leading_coefficient(self)
        if lc != ring.getRing(lc).one:
            self = self.scalar_exact_division(lc)
            result.append((lc, 1))
        squarefreefactors = self.squarefree_decomposition()
        for m, f in squarefreefactors.iteritems():
            distinct_degree_factors = f.distinct_degree_factorization()
            for d, g in distinct_degree_factors.iteritems():
                if d == self.order.degree(g):
                    result.append((g, m))
                else:
                    for irred in g.split_same_degrees(d):
                        result.append((irred, m))
        return result

    def isirreducible(self):
        """
        f.isirreducible() -> bool

        If f is irreducible return True, otherwise False.
        """
        if not self[0]:
            return False
        squareFreeFactors = self.squarefree_decomposition()
        if len(squareFreeFactors) != 1:
            return False
        m, f = squareFreeFactors.popitem()
        if m != 1:
            return False
        distinctDegreeFactors = f.distinct_degree_factorization()
        if len(distinctDegreeFactors) != 1:
            return False
        d, g = distinctDegreeFactors.popitem()
        if d != self.order.degree(g):
            return False
        return True


class KaratsubaProvider (object):
    """
    define Karatsuba method multiplication and squaring.

    REQUIRE: OrderProvider
    """
    def ring_mul_karatsuba(self, other):
        """
        Multiplication of two polynomials in the same ring.

        Computation is carried out by Karatsuba method.
        """
        polynomial = self.__class__
        # zero
        if not self or not other:
            return polynomial((), **self._init_kwds)
        # monomial
        if len(self) == 1:
            return other.term_mul(self)
        if len(other) == 1:
            return self.term_mul(other)
        # binomial
        if len(self) == 2:
            p, q = [other.term_mul(term) for term in self]
            return p + q
        if len(other) == 2:
            p, q = [self.term_mul(term) for term in other]
            return p + q
        # suppose self is black and other is red.
        black_least_degree = self.order.tail_degree(self)
        black_most_degree = self.order.degree(self)
        red_least_degree = self.order.tail_degree(other)
        red_most_degree = self.order.degree(other)
        least_degree = min(black_least_degree, red_least_degree)
        most_degree = max(black_most_degree, red_most_degree)
        assert least_degree < most_degree
        half_degree = (least_degree + most_degree) // 2

        if black_least_degree > half_degree:
            return self.downshift_degree(black_least_degree).ring_mul_karatsuba(other).upshift_degree(black_least_degree)
        if red_least_degree > half_degree:
            return self.ring_mul_karatsuba(other.downshift_degree(red_least_degree)).upshift_degree(red_least_degree)

        black = self.downshift_degree(least_degree)
        red = other.downshift_degree(least_degree)
        club, spade = black.split_at(half_degree - least_degree)
        dia, heart = red.split_at(half_degree - least_degree)
        weaker = club.ring_mul_karatsuba(dia)
        stronger = spade.ring_mul_karatsuba(heart)
        karatsuba = (club + spade).ring_mul_karatsuba(dia + heart) - weaker - stronger
        return (weaker.upshift_degree(least_degree * 2) +
                karatsuba.upshift_degree(least_degree + half_degree) +
                stronger.upshift_degree(half_degree * 2))

    def square_karatsuba(self):
        """
        Return the square of self.
        """
        # zero
        if not self:
            return self

        polynomial = self.__class__
        data_length = len(self)
        # monomial
        if data_length == 1:
            d, c = iter(self).next()
            if d:
                return polynomial([(d*2, c**2)], _sorted=True, **self._init_kwds)
            else:
                return polynomial([(0, c**2)], _sorted=True, **self._init_kwds)
        # binomial
        if data_length == 2:
            (d1, c1), (d2, c2) = [(d, c) for (d, c) in self]
            if "_sorted" in self._init_kwds:
                del self._init_kwds["_sorted"]
            return polynomial({d1*2:c1**2, d1+d2:c1*c2*2, d2*2:c2**2}, _sorted=False, **self._init_kwds)
        # general (Karatsuba)
        least_degree = self.order.tail_degree(self)
        if least_degree:
            chopped = self.downshift_degree(least_degree)
        else:
            chopped = self
        half_degree = self.order.degree(self) // 2
        fst, snd = chopped.split_at(half_degree)
        fst_squared = fst.square()
        snd_squared = snd.square()
        karatsuba = (fst + snd).square() - fst_squared - snd_squared
        result = (fst_squared +
                  karatsuba.upshift_degree(half_degree) +
                  snd_squared.upshift_degree(half_degree * 2))
        if least_degree:
            return result.upshift_degree(least_degree)
        else:
            return result


class VariableProvider (object):
    """
    VariableProvider provides the variable name and other cariable
    related methods.
    """
    def __init__(self, varname):
        """
        Do not instanciate VariableProvider.
        This initializer should be called from descendant.
        """
        if type(self) is VariableProvider:
            raise NotImplementedError(_MIXIN_MSG % self.__class__.__name__)
        self.variable = varname

    def getVariable(self):
        """
        Get variable name
        """
        return self.variable

    def getVariableList(self):
        """
        Get variable name as list.
        """
        return [self.variable]


class RingElementProvider (ring.CommutativeRingElement):
    """
    Provides interfaces for ring.CommutativeRingElement.
    """
    def __init__(self):
        """
        Do not instanciate RingElementProvider.
        This initializer should be called from descendant:
          RingElementProvider.__init__(self)
        """
        if type(self) is RingElementProvider:
            raise NotImplementedError(_MIXIN_MSG % self.__class__.__name__)
        ring.CommutativeRingElement.__init__(self)
        self._coefficient_ring = None
        self._ring = None

    def getRing(self):
        """
        Return an object of a subclass of Ring, to which the element
        belongs.
        """
        if self._coefficient_ring is None or self._ring is None:
            myring = None
            for c in self.itercoefficients():
                cring = ring.getRing(c)
                if not myring or myring != cring and myring.issubring(cring):
                    myring = cring
                elif not cring.issubring(myring):
                    myring = myring.getCommonSuperring(cring)
            if not myring:
                myring = rational.theIntegerRing
            self.set_coefficient_ring(myring)
        return self._ring

    def set_coefficient_ring(self, coeffring):
        if self._coefficient_ring is None:
            self._coefficient_ring = coeffring
            if isinstance(self, VariableProvider):
                self._ring = old_polynomial.PolynomialRing(self._coefficient_ring, self.getVariable())
            else:
                self._ring = PolynomialRingAnonymousVariable.getInstance(self._coefficient_ring)


class PolynomialRingAnonymousVariable (ring.CommutativeRing):
    """
    The class of univariate polynomial ring.
    There's no need to specify the variable name.
    """

    _instances = {}

    def __init__(self, aRing):
        if not isinstance(aRing, ring.Ring):
            raise TypeError("%s should not be passed as ring" % aRing.__class__)
        ring.CommutativeRing.__init__(self)
        self._coefficient_ring = aRing
        if self._coefficient_ring.isfield():
            self.properties.setIseuclidean(True)
        else:
            if self._coefficient_ring.isufd():
                self.properties.setIsufd(True)
            if self._coefficient_ring.isnoetherian():
                self.properties.setIsnoetherian(True)
            elif self._coefficient_ring.isdomain():
                self.properties.setIsdomain(True)
            elif self._coefficient_ring.isdomain() is False:
                self.properties.setIsdomain(False)

    def getCoefficientRing(self):
        """
        Return the coefficient ring.
        """
        return self._coefficient_ring

    def getQuotientField(self):
        """
        getQuotientField returns the quotient field of the ring
        if coefficient ring has its quotient field.  Otherwise,
        an exception will be raised.
        """
        try:
            coefficientField = self._coefficient_ring.getQuotientField()
            import nzmath.rationalFunction as rationalfunction
            # use always "x" as the variable name
            return rationalfunction.RationalFunctionField(coefficientField, "x")
        except:
            raise

    def __eq__(self, other):
        """
        Report whether this ring and that ring are equal ring.
        """
        if self is other:
            return True
        if not isinstance(other, PolynomialRingAnonymousVariable):
            return False
        if self._coefficient_ring == other._coefficient_ring:
            return True
        return False

    def __repr__(self):
        """
        Return 'PolynomialRingAnonymousVariable(Ring)'
        """
        return "%s(%s)" % (self.__class__.__name__, repr(self._coefficient_ring))

    def __str__(self):
        """
        Return R[]
        """
        return str(self._coefficient_ring) + "[]"

    def __hash__(self):
        """
        hash(self)
        """
        return hash(self._coefficient_ring) ^ hash(self.__class__.__name__)

    def __contains__(self, element):
        """
        `in' operator is provided for checking the element be in the
        ring.
        """
        if element in self._coefficient_ring:
            return True
        elem_ring = ring.getRing(element)
        if elem_ring is not None and elem_ring.issubring(self):
            return True
        return False

    def issubring(self, other):
        """
        Report whether another ring contains this polynomial ring.
        """
        if isinstance(other, PolynomialRingAnonymousVariable):
            return self._coefficient_ring.issubring(other.getCoefficientRing())
        elif self._coefficient_ring.issuperring(other):
            return False
        try:
            return other.issuperring(self)
        except RuntimeError:
            # reach max recursion by calling each other
            return False

    def issuperring(self, other):
        """
        reports whether this polynomial ring contains another ring.
        """
        if self._coefficient_ring.issuperring(other):
            return True
        if isinstance(other, PolynomialRingAnonymousVariable):
            return self._coefficient_ring.issuperring(other.getCoefficientRing())
        return False

    def getCommonSuperring(self, other):
        """
        Return common superring of two rings.
        """
        if self.issuperring(other):
            return self
        elif other.issuperring(self):
            return other
        elif (not isinstance(other, PolynomialRingAnonymousVariable) and
              other.issuperring(self._coefficient_ring)):
            return self.__class__(other)
        try:
            if hasattr(other, "getCommonSuperring"):
                return other.getCommonSuperring(self)
        except RuntimeError:
            # reached recursion limit by calling on each other
            pass
        raise TypeError("no common super ring")

    def createElement(self, seed):
        """
        Return an element of the polynomial ring made from seed
        overriding ring.createElement.
        """
        if ring.getRing(seed) == self:
            return seed
        if seed in self._coefficient_ring:
            return polynomial([(0, seed)], self._coefficient_ring)
        else:
            return polynomial(seed, self._coefficient_ring)

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = self.createElement(self._coefficient_ring.one)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = self.createElement(self._coefficient_ring.zero)
        return self._zero

    zero = property(_getZero, None, None, "additive unit")

    def gcd(self, a, b):
        """
        Return the greatest common divisor of given polynomials.
        The polynomials must be in the polynomial ring.
        If the coefficient ring is a field, the result is monic.
        """
        if hasattr(a, "gcd"):
            return a.gcd(b)
        elif hasattr(a, "subresultant_gcd"):
            return a.subresultant_gcd(b)
        raise NotImplementedError

    def extgcd(self, a, b):
        """
        Return the tuple (u, v, d): d is the greatest common divisor
        of given polynomials, and they satisfy d = u*a + v*b. The
        polynomials must be in the polynomial ring.  If the
        coefficient ring is a field, the result is monic.
        """
        if hasattr(a, "extgcd"):
            return a.extgcd(b)
        raise NotImplementedError

    # class method
    def getInstance(cls, coeffring):
        """
        Return an instance of the class with specified coefficient ring.
        """
        if coeffring not in cls._instances:
            cls._instances[coeffring] = cls(coeffring)
        return cls._instances[coeffring]

    getInstance = classmethod(getInstance)


class PolynomialIdeal (ring.Ideal):
    """
    A class to represent an ideal of univariate polynomial ring.
    """
    def __init__(self, generators, polyring):
        """
        Initialize an ideal in the given polyring (polynomial ring).

        generators: a generator polynomial or a list of polynomials
        """
        if type(polyring) is not PolynomialRingAnonymousVariable:
            raise TypeError("polyring has to be an instance of PolynomialRingAnonymousVariable")
        ring.Ideal.__init__(self, generators, polyring)
        self._normalize_generators()

    def __contains__(self, elem):
        """
        Return whether elem is in the ideal or not.
        """
        if elem.getRing() != self.ring:
            return False
        return not self.reduce(elem)

    def __nonzero__(self):
        """
        Report whether the ideal is null ideal or not.  Of course,
        False is for null ideal.
        """
        return bool(self.generators)

    def issubset(self, other):
        """
        Report whether another ideal contains this ideal.
        """
        if self is other:
            return True
        for g in self.generators:
            if g not in other:
                return False
        return True

    def issuperset(self, other):
        """
        Report whether this ideal contains another ideal.
        """
        if self is other:
            return True
        for g in other.generators:
            if g not in self:
                return False
        return True

    def reduce(self, element):
        """
        Reduce the given element by the ideal.  The result is an
        element of the class which represents the equivalent class.
        """
        order = termorder.ascending_order
        if isinstance(element, univar.PolynomialInterface):
            reduced = element
        else:
            reduced = self.ring.createElement(element)
        if not self:
            if not reduced:
                reduced = self.ring.zero
        elif len(self.generators) == 1:
            g = self.generators[0]
            if self.ring.iseuclidean():
                if isinstance(g, univar.PolynomialInterface):
                    reduced %= g
                else: # g is element of a field
                    reduced = self.ring.zero
            elif self.ring.getCoefficientRing().iseuclidean():
                # higher degree to lower degree
                # subtract euclid quotient of lc * generator
                if isinstance(g, univar.PolynomialInterface):
                    g_degree, lc = order.leading_term(g)
                    degree = order.degree(reduced)
                    for d in range(degree, g_degree - 1, -1):
                        q = reduced[d] // lc
                        reduced -= g.term_mul((d - g_degree, q))
                else:
                    reduced = reduced.coefficients_map(lambda c: c % g)
        elif self.ring.getCoefficientRing().iseuclidean():
            # assert that the generators are sorted descending order
            # of degrees.
            for g in self.generators:
                reduced = self._euclidean_reduce(reduced, g)
        else:
            raise NotImplementedError("should be implemented")
        return reduced

    def _euclidean_reduce(self, element, g):
        """
        Reduce an element of the ring by a polynomial g.
        The coefficient ring has to be a Euclidean domain.
        """
        order = termorder.ascending_order
        coeffring = self.ring.getCoefficientRing()
        reduced = element
        g_degree, g_lc = order.leading_term(g)
        degree, lc = order.leading_term(reduced)
        while degree >= g_degree:
            if not (lc % g_lc):
                reduced -= g.term_mul((degree - g_degree, lc // g_lc))
            else:
                u, v, common_divisor = coeffring.extgcd(lc, g_lc)
                reduced = reduced.scalar_mul(u) + g.term_mul((degree - g_degree, v))
                break
            degree, lc = order.leading_term(reduced)
        return reduced

    def _normalize_generators(self):
        """
        Normalize generators
        """
        order = termorder.ascending_order
        if len(self.generators) > 1 and self.ring.ispid():
            g = self.generators[0]
            for t in self.generators:
                g = self.ring.gcd(g, t)
            self.generators = [g]
        elif self.ring.getCoefficientRing().iseuclidean():
            coeffring = self.ring.getCoefficientRing()
            degree = order.degree
            lc = order.leading_coefficient
            cand_stack = list(self.generators)
            tentative = []
            while cand_stack:
                next = cand_stack.pop()
                if not tentative:
                    tentative.append(next)
                    continue
                next_degree = degree(next)
                while tentative:
                    last = tentative.pop()
                    last_degree = degree(last)
                    if last_degree > next_degree:
                        cand_stack.append(last)
                        continue
                    next_lc, last_lc = lc(next), lc(last)
                    if last_degree == next_degree:
                        u, v, d = coeffring.extgcd(next_lc, last_lc)
                        # make new polynomial whose lc = d
                        head = next.scalar_mul(u) + last.scalar_mul(v)
                        next -= head.scalar_mul(next_lc // d)
                        last -= head.scalar_mul(last_lc // d)
                        assert degree(next) < next_degree
                        assert degree(last) < last_degree
                        cand_stack.append(head)
                        if next:
                            cand_stack.append(next)
                        if last:
                            cand_stack.append(last)
                        break
                    elif not (next_lc % last_lc):
                        next -= last.scalar_mul(next_lc // last_lc)
                        cand_stack.append(next)
                        break
                    elif last_lc % next_lc:
                        u, v, d = coeffring.extgcd(next_lc, last_lc)
                        next = next.scalar_mul(u) + last.term_mul((next_degree - last_degree, v))
                    tentative.append(last)
                    tentative.append(next)
                    break
                else:
                    tentative.append(next)
            self.generators = tentative
        else:
            degree = order.degree
            # sort in descending order
            self.generators.sort(cmp=lambda a, b: cmp(degree(b), degree(a)))


class RingPolynomial (OrderProvider,
                      univar.SortedPolynomial,
                      RingElementProvider):
    """
    General polynomial with commutative ring coefficients.
    """
    def __init__(self, coefficients, coeffring=None, _sorted=False, **kwds):
        """
        Initialize the polynomial.

        - coefficients: initializer for polynomial coefficients
        - coeffring: commutative ring
        """
        if coeffring is None:
            raise TypeError("argument `coeffring' is required")
        coefficients = dict(coefficients)
        if coefficients and coefficients.itervalues().next() not in coeffring:
            coefficients = [(d, coeffring.createElement(c)) for (d, c) in coefficients.iteritems()]
            _sorted = False
        kwds["coeffring"] = coeffring
        univar.SortedPolynomial.__init__(self, coefficients, _sorted, **kwds)
        OrderProvider.__init__(self, termorder.ascending_order)
        RingElementProvider.__init__(self)
        self.set_coefficient_ring(coeffring)

    def getRing(self):
        """
        Return an object of a subclass of Ring, to which the element
        belongs.
        """
        # short-cut self._ring is None case
        return self._ring

    def getCoefficientRing(self):
        """
        Return an object of a subclass of Ring, to which the all
        coefficients belong.
        """
        # short-cut self._coefficient_ring is None case
        return self._coefficient_ring

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.terms()), repr(self._coefficient_ring))


class DomainPolynomial(PseudoDivisionProvider,
                       RingPolynomial):
    """
    Polynomial with domain coefficients.
    """
    def __init__(self, coefficients, coeffring=None, _sorted=False, **kwds):
        """
        Initialize the polynomial.

        - coefficients: initializer for polynomial coefficients
        - coeffring: domain
        """
        if coeffring is None:
            raise TypeError("argument `coeffring' is required")
        elif not coeffring.isdomain():
            raise TypeError("coefficient ring has to be a domain")
        RingPolynomial.__init__(self, coefficients, coeffring, _sorted, **kwds)
        PseudoDivisionProvider.__init__(self)


class UniqueFactorizationDomainPolynomial(SubresultantGcdProvider,
                                          ContentProvider,
                                          DomainPolynomial):
    """
    Polynomial with unique factorization domain coefficients.
    """
    def __init__(self, coefficients, coeffring=None, _sorted=False, **kwds):
        """
        Initialize the polynomial.

        - coefficients: initializer for polynomial coefficients
        - coeffring: unique factorization domain
        """
        if coeffring is None:
            raise TypeError("argument `coeffring' is required")
        elif not coeffring.isufd():
            raise TypeError("coefficient ring has to be a UFD")
        DomainPolynomial.__init__(self, coefficients, coeffring, _sorted, **kwds)
        ContentProvider.__init__(self)
        SubresultantGcdProvider.__init__(self)


class FieldPolynomial(DivisionProvider,
                      ContentProvider,
                      RingPolynomial):
    """
    Polynomial with field coefficients.
    """
    def __init__(self, coefficients, coeffring=None, _sorted=False, **kwds):
        """
        Initialize the polynomial.

        - coefficients: initializer for polynomial coefficients
        - coeffring: field
        """
        if coeffring is None:
            raise TypeError("argument `coeffring' is required")
        elif not coeffring.isfield():
            raise TypeError("coefficient ring has to be a field")
        RingPolynomial.__init__(self, coefficients, coeffring, _sorted, **kwds)
        DivisionProvider.__init__(self)
        ContentProvider.__init__(self)


class FinitePrimeFieldPolynomial (PrimeCharacteristicFunctionsProvider,
                                  FieldPolynomial):
    """
    Fp polynomial
    """
    def __init__(self, coefficients, coeffring=None, _sorted=False, **kwds):
        """
        Initialize the polynomial.

        - coefficients: initializer for polynomial coefficients
        - coeffring: finite prime field
        """
        if coeffring is None:
            raise TypeError("argument `coeffring' is required")
        FieldPolynomial.__init__(self, coefficients, coeffring, _sorted, **kwds)
        PrimeCharacteristicFunctionsProvider.__init__(self, coeffring.getCharacteristic())


def inject_variable(polynom, variable):
    """
    Inject variable into polynom temporarily.  The variable name will
    be lost after any arithmetic operations on polynom, though the
    class name of polynom will remain prefixed with 'Var'.  If one need
    variable name permanently, he/she should define a class inheriting
    VariableProvider.
    """
    baseclasses = polynom.__class__.__bases__
    if VariableProvider not in baseclasses:
        polynom.__class__ = type("Var" + polynom.__class__.__name__,
                                 (polynom.__class__, VariableProvider,),
                                 {})
    polynom.variable = variable


special_ring_table = {}


def polynomial(coefficients, coeffring):
    """
    Return a polynomial.
    - coefficients has to be a initializer for dict, whose keys are
      degrees and values are coefficients at degrees.
    - coeffring has to be an object inheriting ring.Ring.

    One can override the way to choose a polynomial type from a
    coefficient ring, by setting:
    special_ring_table[coeffring_type] = polynomial_type
    before the function call.
    """
    if type(coeffring) in special_ring_table:
        poly_type = special_ring_table[type(coeffring)]
    elif coeffring.isfield():
        poly_type = FieldPolynomial
    elif coeffring.isufd():
        poly_type = UniqueFactorizationDomainPolynomial
    elif coeffring.isdomain():
        poly_type = DomainPolynomial
    else:
        poly_type = RingPolynomial
    return poly_type(coefficients, coeffring)


def OneVariableDensePolynomial(coefficient, variable, coeffring=None):
    """
    OneVariableDensePolynomial(coefficient, variable [,coeffring])

    - coefficient has to be a sequence of coefficients in ascending order
    of degree.
    - variable has to be a character string.
    - coeffring has to be, if specified, an object inheriting ring.Ring.

    This function is provided for backward compatible way of defining
    univariate polynomial.  The argument variable is ignored.
    """
    _coefficients = dict(enumerate(coefficient))
    if not coeffring:
        coeffring = init_coefficient_ring(_coefficients)
    return polynomial(_coefficients, coeffring)

def OneVariableSparsePolynomial(coefficient, variable, coeffring=None):
    """
    OneVariableSparsePolynomial(coefficient, variable [,coeffring])

    - coefficient has to be a dictionary of degree-coefficient pairs.
    - variable has to be a character string.
    - coeffring has to be, if specified, an object inheriting ring.Ring.

    This function is provided for backward compatible way of defining
    univariate polynomial.  The argument variable is ignored.
    """
    _coefficients = dict(coefficient)
    if not coeffring:
        coeffring = init_coefficient_ring(_coefficients)
    return polynomial(_coefficients, coeffring)

def init_coefficient_ring(coefficients):
    """
    Return a ring to which all coefficients belong.  The argument
    coefficients is a dictionary whose values are the coefficients.
    """
    myRing = None
    for c in coefficients.itervalues():
        cring = ring.getRing(c)
        if not myRing or myRing != cring and myRing.issubring(cring):
            myRing = cring
        elif not cring.issubring(myRing):
            myRing = myRing.getCommonSuperring(cring)
    return myRing