"""
Class definitions of polynomials.
"""

from __future__ import division
import re
import copy
import logging

import nzmath.bigrandom as bigrandom
import nzmath.rational as rational
import nzmath.ring as ring

try:
    # Python 2.4 has set type
    set
except NameError:
    # Python 2.3 has Set class in sets
    from sets import Set as set

_log = logging.getLogger('nzmath.polynomial')


class OneVariablePolynomial (ring.CommutativeRingElement):
    """
    The class is for polynomials with one variable.
    """

    def __init__(self, coefficient, variable, coeffring):
        """
        OneVariablePolynomial(coefficient, variable, coeffring)
        makes a one variable polynomial object.

        coefficient must be an instance of OneVariablePolynomialCoefficient.
        variable must be either one of string, list or tuple.
        coeffring must be a commutative ring object,
        which implements ring.CommutativeRing.
        """
        self.coefficient = coefficient
        self.variable = variable
        self.coefficientRing = coeffring
        self.ring = PolynomialRing(coeffring, variable)

    def __setitem__(self, index, value):
        """
        aOneVariablePolynomial[n] = val
        sets val to the coefficient at degree n.  val must be in the
        coefficient ring of aOneVariablePolynomial.

        TypeError will be raised if n is not an integer, or if val is
        not in the coefficient ring.
        ValueError will be raised if n is negative.
        """
        if value in self.getCoefficientRing():
            if index >= 0:
                self.coefficient[index] = value
            else:
                raise ValueError("degree must be a non-negative integer.")
        else:
            raise TypeError("value must be an element of the coefficient ring.")

    def __getitem__(self, index):
        """
        aOneVariablePolynomial[n]
        returns the coefficient at degree n.

        TypeError will be raised if n is not an integer.
        ValueError will be raised if n is negative.
        """
        if isinstance(index, (int, long)) and index >= 0:
            return self.coefficient[index]
        else:
            raise ValueError("degree must be a non-negative integer.")

    def __eq__(self, other):
        if not self and not other:
            return True
        if self is other:
            return True
        if isinstance(other, OneVariablePolynomial):
            if self.getVariable() == other.getVariable() and self.degree() == other.degree():
                for i in range(self.degree() + 1):
                    if self[i] != other[i]:
                        return False
                return True
            return False
        elif other in self.getCoefficientRing():
            if self.degree() < 1 and self[0] == other:
                return True
            return False
        return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __pos__(self):
        retval = self.copy()
        if retval.degree() == 0:
            retval = retval[0]
        elif retval.degree() < 0:
            retval = 0
        return retval

    def __neg__(self):
        reciprocal = {}
        for i, c in self.coefficient.iteritems():
            reciprocal[i] = -c
        return OneVariableSparsePolynomial(reciprocal, self.getVariableList(), self.getCoefficientRing())

    def __add__(self, other):
        if not other:
            return self.copy()
        if isinstance(other, OneVariablePolynomial):
            if self.getVariable() == other.getVariable():
                _sum = OneVariablePolynomialCoefficients()
                _sum.setDict(self.coefficient.getAsDict())
                for i, c in other.coefficient.iteritems():
                    _sum[i] = _sum[i] + c
                commonRing = self.ring.getCommonSuperring(other.getRing())
                return OneVariableSparsePolynomial(_sum.getAsDict(), self.getVariableList(), commonRing.getCoefficientRing())
            else:
                return self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() + other
        elif other in self.getCoefficientRing():
            _sum = OneVariablePolynomialCoefficients()
            _sum.setDict(self.coefficient.getAsDict())
            _sum[0] = _sum[0] + other
            return OneVariableSparsePolynomial(_sum.getAsDict(), self.getVariableList(), self.getCoefficientRing())
        else:
            commonSuperring = self.getRing().getCommonSuperring(ring.getRing(other))
            return commonSuperring.createElement(self) + commonSuperring.createElement(other)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        if isinstance(other, OneVariablePolynomial):
            if self.getVariable() == other.getVariable():
                product = OneVariablePolynomialCoefficients()
                for i, c in self.coefficient.iteritems():
                    for j, d in other.coefficient.iteritems():
                        product[i + j] = product[i + j] + c * d
                commonRing = self.getRing().getCommonSuperring(other.getRing())
                if not commonRing and self.getCoefficientRing():
                    return OneVariableSparsePolynomial(product.getAsDict(), self.getVariableList(), self.getCoefficientRing())
                return OneVariableSparsePolynomial(product.getAsDict(), self.getVariableList(), commonRing.getCoefficientRing())
            else:
                return self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() * other
        elif other in self.ring.getCoefficientRing():
            product = {}
            for i, c in self.coefficient.iteritems():
                product[i] = c * other
            return OneVariableSparsePolynomial(product, self.getVariableList(), self.getCoefficientRing())
        elif isinstance(other, (int, long)):
            return rational.Integer(other).actAdditive(self)
        else:
            commonSuperring = self.getRing().getCommonSuperring(ring.getRing(other))
            return commonSuperring.createElement(self) * commonSuperring.createElement(other)

    __rmul__ = __mul__

    def __divmod__(self, other):
        if not other:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        coeffring = self.getCoefficientRing()
        x = self.getVariable()
        if isinstance(other, OneVariablePolynomial):
            if other.degree() == 0:
                other = other[0]
                div_coeff, mod_coeff = {}, {}
                if coeffring.isfield() or isinstance(other, ring.FieldElement):
                    for i, c in self.coefficient.iteritems():
                        div_coeff[i] = c / other
                else:
                    for i, c in self.coefficient.iteritems():
                        div_coeff[i], mod_coeff[i] = divmod(c, other)
                return (OneVariableSparsePolynomial(div_coeff, x, coeffring),
                        OneVariableSparsePolynomial(mod_coeff, x , coeffring))
            elif x != other.getVariable() or self.degree() < other.degree():
                return  (OneVariableDensePolynomial([], x, coeffring),
                         self.copy())
            elif coeffring.isfield():
                div_poly = OneVariableDensePolynomial([], x, coeffring)
                mod_poly = self.coefficient.copy()
                deg, o_deg = mod_poly.degree(), other.degree()
                o_lc = other[o_deg]
                while deg >= o_deg:
                    deg_diff = deg - o_deg
                    div_poly[deg_diff] = coeffring.createElement(mod_poly[deg] / o_lc)
                    canceler = (div_poly[deg_diff] * other).coefficient
                    for i in range(deg_diff, deg):
                        mod_poly[i] = mod_poly[i] - canceler[i - deg_diff]
                    mod_poly[deg] = coeffring.zero
                    deg = mod_poly.degree()
                mod_poly = OneVariableSparsePolynomial(mod_poly.getAsDict(), x, coeffring)
                return div_poly, mod_poly
            else:
                div_poly = OneVariableDensePolynomial([], x, coeffring)
                mod_poly = self.coefficient.copy()
                deg, o_deg = mod_poly.degree(), other.degree()
                o_lc = other[o_deg]
                while deg >= o_deg:
                    deg_diff = deg - o_deg
                    div_poly[deg_diff] = coeffring.createElement(mod_poly[deg] // o_lc)
                    canceler = (div_poly[deg_diff] * other).coefficient
                    for i in range(deg_diff, deg+1):
                        mod_poly[i] = mod_poly[i] - canceler[i - deg_diff]
                    deg -= 1
                    while deg >= 0 and not mod_poly[deg]:
                        deg -= 1
                return (div_poly.copy(),
                        OneVariableSparsePolynomial(mod_poly.getAsDict(), x, coeffring))
        commonSuperring = self.getRing().getCommonSuperring(ring.getRing(other))
        return commonSuperring.createElement(self).__divmod__(commonSuperring.createElement(other))

    def __rdivmod__(self, other):
        if not self:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        if not other:
            return (OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing()),
                    OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing()))
        if other in self.getCoefficientRing():
            if self.degree() == 0:
                return divmod(other, self[0])
            else:
                return (OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing()), +other)

    def __truediv__(self, other):
        quot, rem = divmod(self, other)
        if not rem:
            return quot
        elif isinstance(other, (int, long)):
            return self * rational.Rational(1, other)
        else:
            import nzmath.rationalFunction as rationalFunction
            return rationalFunction.RationalFunction(self, other)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        quot, rem = divmod(other, self)
        if not rem:
            return quot
        else:
            import nzmath.rationalFunction as rationalFunction
            return rationalFunction.RationalFunction(other, self)

    __rdiv__ = __rtruediv__

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __rfloordiv__(self, other):
        if not self:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        if not other:
            return OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())
        if other in self.getCoefficientRing():
            if self.degree() == 0:
                return other // self[0]
            else:
                return OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __rmod__(self, other):
        if not self:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        if not other:
            return OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())
        if other in self.getCoefficientRing():
            if self.degree() == 0:
                return other % self[0]
            else:
                return +other

    def __pow__(self, index, mod = None):
        if not isinstance(index, (int, long)):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be a non-negative integer.")
        if mod == None:
            power_product = self.getRing().one
            power_of_2 = self.copy()
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                index = index // 2
                if index > 0:
                    power_of_2 = power_of_2 * power_of_2
            return power_product.copy()
        else:
            power_product = self.getRing().one
            power_of_2 = self.copy()
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                    power_product %= mod
                index = index // 2
                if index > 0:
                    power_of_2 = (power_of_2 * power_of_2) % mod
            return power_product.copy()

    def __nonzero__(self):
        if self.degree() >= 0:
            return True
        else:
            return False

    def __call__(self, other):
        if isinstance(other, str):
            return OneVariableSparsePolynomial(self.coefficient.getAsDict(), [other], self.getCoefficientRing())
        elif not other:
            return self.coefficient[0]
        elif not self:
            return self.getCoefficientRing().zero

        return_value = self.leadingCoefficient()
        for d in range(self.degree()-1, -1, -1):
            c_d = self[d]
            if c_d:
                return_value = return_value * other + c_d
            elif return_value:
                return_value = return_value * other
        return return_value

    def degree(self):
        return self.coefficient.degree()

    def differentiate(self, var):
        if isinstance(var, str):
            if self.degree() < 1 or var != self.getVariable():
                return self.getCoefficientRing().createElement(0)
            else:
                return_coefficient = {}
                for i, c in self.coefficient.iteritems():
                    if i:
                        return_coefficient[i - 1] = c * i
                return OneVariableSparsePolynomial(return_coefficient,
                                                   self.getVariableList(),
                                                   self.getCoefficientRing())
        else:
            raise ValueError("You must specify a variable.")

    def getRing(self):
        return self.ring

    def getCoefficientRing(self):
        return self.coefficientRing

    def content(self):
        """
        Return content of the polynomial.
        """
        coefring = self.getCoefficientRing()
        if coefring.isfield():
            if isinstance(coefring, ring.QuotientField):
                num, den = 0, 1
                for c in self.coefficient.itercoeffs():
                    num = c.numerator.getRing().gcd(num, c.numerator)
                    den = c.denominator.getRing().lcm(den, c.denominator)
                return coefring.createElement(num, den)
            else:
                raise NotImplementedError
        else:
            cont = 0
            for c in self.coefficient.itercoeffs():
                cont = coefring.gcd(cont, c)
            return cont

    def primitivePart(self):
        """
        Return the primitive part of the polynomial.
        """
        return self / self.content()

    def leadingCoefficient(self):
        """
        Return the leading coefficient of the polynomial.
        """
        try:
            return self[self.degree()]
        except ValueError:
            return self.getCoefficientRing().zero

    def toOneVariableDensePolynomial(self):
        return OneVariableDensePolynomial(self.coefficient.getAsList(), self.getVariable(), self.getCoefficientRing())

    def toOneVariableSparsePolynomial(self):
        return OneVariableSparsePolynomial(self.coefficient.getAsDict(), self.getVariableList(), self.getCoefficientRing())

    def toMultiVariableSparsePolynomial(self):
        return_coefficient = {}
        for i, c in self.coefficient.iteritems():
            return_coefficient[(i,)] = c
        return MultiVariableSparsePolynomial(return_coefficient, self.getVariableList())

    def __long__(self):
        if self.degree() < 1:
            if isinstance(self[0], (int, long)):
                return self[0]
            return long(self[0])
        raise ValueError("non-constant polynomial cannot be converted to long")

    def __repr__(self):
        return_str = '%s(%s, %s, %s)' % (self.__class__.__name__,
                                         repr(self.coefficient),
                                         repr(self.getVariable()),
                                         repr(self.getCoefficientRing()))
        return return_str

    def __str__(self):
        if self.degree() < 1:
            return str(self[0])
        termlist = []
        for i in range(self.degree() + 1):
            if self[i]:
                if i == 0:
                    termlist.append("%s" % (str(self[i]),))
                elif i == 1:
                    termlist.append("%s * %s" % (str(self[i]), str(self.getVariable()),))
                else:
                    termlist.append("%s * %s ** %d" % (str(self[i]), str(self.getVariable()), i))
        return_str = " + ".join(termlist)
        w_sign = re.compile(r"\+ -")
        return_str = w_sign.sub("- ", return_str)
        one_coeff = re.compile("(^| )1 \* ")
        return_str = one_coeff.sub(" ", return_str)
        while return_str.startswith(" "):
            return_str = return_str[1:]
        return return_str

    def getVariable(self):
        if isinstance(self.variable, list):
            return self.variable[0]
        return self.variable

    def getVariableList(self):
        if not isinstance(self.variable, list):
            return [self.variable]
        return self.variable[:]

    def copy(self):
        "Copy the structure"
        if self.coefficient._using == self.coefficient.USING_LIST:
            return OneVariableDensePolynomial(self.coefficient.getAsList(),
                                              self.getVariable(),
                                              self.getCoefficientRing())
        else:
            return OneVariableSparsePolynomial(self.coefficient.getAsDict(),
                                               self.getVariableList(),
                                               self.getCoefficientRing())

def initCoefficientRing(coefficient):
    myRing = None
    for c in coefficient.itercoeffs():
        cring = ring.getRing(c)
        if not myRing or myRing != cring and myRing.issubring(cring):
            myRing = cring
        elif not cring.issubring(myRing):
            myRing = myRing * cring
    return myRing

def OneVariableDensePolynomial(coefficient, variable, coeffring=None):
    """

    OneVariableDensePolynomial(coefficient, variable [,coeffring])

    coefficient must be a sequence of coefficients.
    variable must be a character string.
    coeffring must be, if specified, an object inheriting ring.Ring.

    """
    _coefficient = OneVariablePolynomialCoefficients()
    _variable = variable
    if not coeffring:
        _coefficient.setList(list(coefficient))
        _coefficientRing = initCoefficientRing(_coefficient)
    else:
        _coefficientRing = coeffring
        _coefficient.setList([coeffring.createElement(c) for c in coefficient])
    try:
        if _coefficientRing.getCharacteristic() > 0:
            return OneVariablePolynomialCharNonZero(_coefficient, _variable, _coefficientRing)
    except AttributeError:
        if _coefficientRing == rational.theRationalField:
            return RationalOneVariablePolynomial(_coefficient, _variable)
        elif _coefficientRing == rational.theIntegerRing:
            return OneVariablePolynomialChar0(_coefficient, _variable, rational.theIntegerRing)
    except:
        raise
    return OneVariablePolynomial(_coefficient, _variable, _coefficientRing)

def OneVariableSparsePolynomial(coefficient, variable, coeffring=None):
    "OneVariableSparsePolynomial(coefficient, variable)"
    _coefficient = OneVariablePolynomialCoefficients()
    if not coeffring:
        for i, c in coefficient.iteritems():
            if c:
                if isinstance(i, tuple):
                    key = i[0]
                else:
                    key = i
                _coefficient[key] = c
        _coefficientRing = initCoefficientRing(_coefficient)
    else:
        _coefficientRing = coeffring
        for i, c in coefficient.iteritems():
            _coefficient[i] = coeffring.createElement(c)
    try:
        if _coefficientRing.getCharacteristic() > 0:
            return OneVariablePolynomialCharNonZero(_coefficient, variable, _coefficientRing)
    except AttributeError:
        if _coefficientRing == rational.theRationalField:
            return RationalOneVariablePolynomial(_coefficient, variable)
        elif _coefficientRing == rational.theIntegerRing:
            return OneVariablePolynomialChar0(_coefficient, variable, rational.theIntegerRing)
    except:
        raise
    return OneVariablePolynomial(_coefficient, variable, _coefficientRing)


def OneVariableMonomial(variable, index=1, coefficient=1, coeffring=None):
    """
    Create a polynomial consists of one monomial.

    The variable name is required.
    Optional arguments are:
      index: power index of the monomial default to one.
      coefficient: coefficient of the monomial default to one.
      coeffring: ring of coefficients default to Z.
    """
    if not coeffring:
        coeffring = ring.getRing(coefficient)
    elif coefficient is 1:
        coefficient = coeffring.one
    _coefficient = OneVariablePolynomialCoefficients()
    _coefficient.setDict({index: coefficient})
    try:
        if coeffring.getCharacteristic() > 0:
            return OneVariablePolynomialCharNonZero(_coefficient, variable, coeffring)
    except AttributeError:
        pass
    return OneVariablePolynomial(_coefficient, variable, coeffring)


class MultiVariableSparsePolynomial:

    def __init__(self, coefficient, variable):
        "MultiVariableSparsePolynomial(coefficient, variable)."
        if isinstance(variable, list) and isinstance(coefficient, dict):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError("You must input MultiVariableSparsePolynomial(dict,list) but (%s, %s)." % (coefficient.__class__, variable.__class__))

    def __add__(self, other):
        if isinstance(other, OneVariablePolynomial):
            return self + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            if self.variable == other.variable:
                temp = self.coefficient.copy()
                return_coefficient = temp
                return_variable = self.variable[:]
                for i in other.coefficient:
                    if i in return_coefficient:
                        return_coefficient[i] = return_coefficient[i]+other.coefficient[i]
                    else:
                        return_coefficient[i] = other.coefficient[i]
                return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()
            else:
                self_adjust = self.adjust()
                if not isinstance(self_adjust, MultiVariableSparsePolynomial):
                    return self_adjust + other
                other_adjust = other.adjust()
                if not isinstance(other_adjust, MultiVariableSparsePolynomial):
                    return self_adjust + other_adjust
                if self_adjust.variable == other_adjust.variable:
                    return self_adjust + other_adjust
                sum_variable = list(set(self_adjust.variable).union(set(other_adjust.variable)))
                sum_variable.sort()
                return self_adjust.arrange_variable(sum_variable) + other_adjust.arrange_variable(sum_variable)
        elif other in self.getRing():
            return_coefficient = self.coefficient.copy()
            return_variable = self.variable[:]
            zero_key = (0,) * len(return_variable)
            if zero_key in return_coefficient:
                return_coefficient[zero_key] += other
            else:
                return_coefficient[zero_key] = other
            return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        return_coefficient = {}
        for i, c in self.coefficient.iteritems():
            if c != 0:
                return_coefficient[i] = -c
        return MultiVariableSparsePolynomial(return_coefficient, self.variable[:])

    def __mul__(self, other):
        if isinstance(other, OneVariablePolynomial):
            return self * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            if self.variable == other.variable:
                result_coefficient = {}
                result_variable = self.variable[:]
                for skey, sval in self.coefficient.iteritems():
                    for okey, oval in other.coefficient.iteritems():
                        index_list = []
                        for k in range(len(self.variable)):
                            index_list.append(skey[k] + okey[k])
                        mul_value = sval * oval
                        index_list = tuple(index_list)
                        if index_list in result_coefficient:
                            result_coefficient[index_list] += mul_value
                        else:
                            result_coefficient[index_list] = mul_value
                result_polynomial = MultiVariableSparsePolynomial(result_coefficient, result_variable)
                return result_polynomial.adjust()
            else:
                self_adjust = self.adjust()
                if not isinstance(self_adjust, MultiVariableSparsePolynomial):
                    return self_adjust * other
                other_adjust = other.adjust()
                if not isinstance(other_adjust, MultiVariableSparsePolynomial):
                    return self_adjust * other_adjust
                if self_adjust.variable == other_adjust.variable:
                    return self_adjust * other_adjust
                sum_variable = list(set(self_adjust.variable).union(set(other_adjust.variable)))
                sum_variable.sort()
                return self_adjust.arrange_variable(sum_variable) * other_adjust.arrange_variable(sum_variable)
        elif other in self.getRing():
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = other * self.coefficient[i]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()

    __rmul__ = __mul__

    def __pow__(self, other, mod = None):
        if isinstance(other, (int, long)):
            if mod == None:
                if other == 0:
                    return self.getRing().one
                elif other > 0:
                    index = other
                    power_product = self.getRing().one
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient, self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                        power_of_2 = power_of_2 * power_of_2
                        index = index // 2
                    return power_product.adjust()
            else:
                if other == 0:
                    return self.getRing().one
                elif other > 0:
                    index = other
                    power_product = self.getRing().one
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient, self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                            power_product %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return power_product.adjust()
        raise ValueError("You must input positive integer for index.")

    def __floordiv__(self, other):
        if isinstance(other, (int, long)) or isinstance(other, rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] // other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient, return_variable)
            return return_polynomial.adjust()
        elif isinstance(other, OneVariablePolynomial):
            return self // other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            if self.variable != other.variable:
                self_adjust = self.adjust()
                other_adjust = other.adjust()
                sum_variable = list(set(self_adjust.variable).union(set(other_adjust.variable)))
                sum_variable.sort()
                return self_adjust.arrange_variable(sum_variable) //  other_adjust.arrange_variable(sum_variable)
            else:
                typical_term_of_other = other.search_typical_term()
                div_test_flag = self.calc_quotioent_by_monomial(typical_term_of_other)
                if isinstance(div_test_flag, (int, long)) or isinstance(other, rational.Rational):
                    return div_test_flag // typical_term_of_other.coefficient.values()[0]
                else:
                    return_polynomial = 0
                    remainder_coefficient = self.coefficient.copy()
                    remainder_variable = self.variable[:]
                    remainder_polynomial = MultiVariableSparsePolynomial(remainder_coefficient, remainder_variable)
                    quotient_term = remainder_polynomial.calc_quotioent_by_monomial(typical_term_of_other).search_typical_term() // typical_term_of_other.coefficient.values()[0]
                    return_polynomial += quotient_term
                    remainder_polynomial -= quotient_term * other
                    if isinstance(quotient_term, MultiVariableSparsePolynomial):
                        typical_coefficient = quotient_term.coefficient.keys()[0]
                        if isinstance(remainder_polynomial, MultiVariableSparsePolynomial) and typical_coefficient in remainder_polynomial.coefficient:
                            remainder_coefficient = remainder_polynomial.coefficient.copy()
                            del(remainder_coefficient[typical_coefficient])
                            remainder_polynomial = MultiVariableSparsePolynomial(remainder_coefficient, remainder_polynomial.variable).adjust()
                    return_polynomial += remainder_polynomial // other
                    return return_polynomial
        else:
            raise NotImplementedError

    def search_typical_term(self):
        typical_coefficient = (0,) * len(self.variable)
        typical_coefficient_value = 0
        for i in self.coefficient:
            this_value = 0
            for j in i:
                this_value += j
            if this_value > typical_coefficient_value:
                typical_coefficient = i
                typical_coefficient_value = this_value
            elif this_value == typical_coefficient_value:
                for k in range(len(typical_coefficient)):
                    if i[k] < typical_coefficient[k]:
                        break
                    elif i[k] > typical_coefficient[k]:
                        typical_coefficient = i
                        typical_coefficient_value = this_value
        typical_term_value = self.coefficient[typical_coefficient]
        return_polynomial = MultiVariableSparsePolynomial({typical_coefficient:typical_term_value}, self.variable)
        return return_polynomial

    def calc_quotioent_by_monomial(self, other):
        if isinstance(other, MultiVariableSparsePolynomial):
            if self.variable == other.variable:
                if len(other.coefficient.keys()) == 1:
                    return_coefficient = {}
                    return_variable = self.variable[:]
                    for i in self.coefficient:
                        flag = 1
                        addition_term = []
                        for j in range(len(self.variable)):
                            if i[j] < other.coefficient.keys()[0][j]:
                                flag = 0
                                break
                            else:
                                addition_term += [(i[j] - other.coefficient.keys()[0][j])]
                        if flag == 1:
                            return_coefficient[tuple(addition_term)] = self.coefficient[i]
                    if len(return_coefficient.keys()) == 0:
                        return 0
                    else:
                        return_polynomial = MultiVariableSparsePolynomial(return_coefficient, return_variable)
                        return return_polynomial
                else:
                    raise ValueError("You must input a monomial for other.")
            else:
                raise ValueError("You must input two Polynomial that have common kind of variable.")
        else:
            raise ValueError("You must input two MultiVariableSparsePolynomial.")

    def __truediv__(self, other):
        if isinstance(other, (int, long)):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                if isinstance(self.coefficient[i], (int, long)):
                    return_coefficient[i] = rational.Rational(self.coefficient[i], other)
                else:
                    return_coefficient[i] = self.coefficient[i] / other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient, return_variable)
            return return_polynomial
        elif isinstance(other, rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] / other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient, return_variable)
            return return_polynomial
        elif isinstance(other, (OneVariablePolynomial, MultiVariableSparsePolynomial)) and (self % other == 0):
            return self // other
        else:
            return self.getRing().getQuotientField().createElement(self, other)

    __div__ = __truediv__

    def __rfloordiv__(self, other):
        if isinstance(other, (int, long)) or isinstance(other, rational.Rational):
            return 0
        elif isinstance(other, OneVariablePolynomial):
            return other.toMultiVariableSparsePolynomial() // self
        else:
            raise NotImplementedError

    def __rdiv__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        return self - (self // other) * other

    def __rmod__(self, other):
        return other - (other // self) * self

    def __divmod__(self, other):
        return (self // other, self % other)

    def __rdivmod__(self, other):
        return (other // self, other % self)

    def __eq__(self, other):
        sub_polynomial = self - other
        if not isinstance(sub_polynomial, MultiVariableSparsePolynomial) and sub_polynomial == 0:
            return True
        return False

    def __call__(self, **substitutions):
        adjust_polynomial = self.adjust()
        if not isinstance(adjust_polynomial, MultiVariableSparsePolynomial):
            return adjust_polynomial(**substitutions)
        basecoefficientring = self.getRing().getCoefficientRing(self.getRing().getVars())
        for var in adjust_polynomial.variable:
            if var in substitutions and not isinstance(substitutions[var], (str, OneVariablePolynomial, MultiVariableSparsePolynomial)):
                variable_position = adjust_polynomial.variable.index(var)
                new_coefficient = {}
                for j, new_value in adjust_polynomial.coefficient.items():
                    new_key = list(j)
                    new_key[variable_position] = 0
                    new_key = tuple(new_key)
                    new_value = new_value * substitutions[var]**j[variable_position]
                    if new_key in new_coefficient:
                        new_coefficient[new_key] += new_value
                    else:
                        new_coefficient[new_key] = new_value
                adjust_polynomial.coefficient = new_coefficient
        adjust_polynomial = adjust_polynomial.adjust()
        if adjust_polynomial in basecoefficientring:
            return adjust_polynomial
        elif not adjust_polynomial:
            return basecoefficientring.zero
        variable_to_variable_back_dict = {}
        variable_to_polynomial_back_dict = {}
        new_variable_parameter = 0
        new_variable_parameter_of_polynomial = 0
        new_variable = adjust_polynomial.variable[:]
        for i in adjust_polynomial.variable:
            variable_position = adjust_polynomial.variable.index(i)
            if i in substitutions and isinstance(substitutions[i], str):
                key = '__new_variable__' + str(new_variable_parameter)
                variable_to_variable_back_dict[key] = substitutions[i]
                new_variable[variable_position] = key
                new_variable_parameter += 1
            elif i in substitutions and isinstance(substitutions[i], (OneVariablePolynomial, MultiVariableSparsePolynomial)):
                key = '__new_polynomial__' + str(new_variable_parameter_of_polynomial)
                variable_to_polynomial_back_dict[key] = substitutions[i]
                new_variable[variable_position] = key
                new_variable_parameter_of_polynomial += 1
        adjust_polynomial.variable = new_variable
        test_key = 0
        for i in variable_to_variable_back_dict:
            if i in new_variable:
                test_key += 1
                variable_position = adjust_polynomial.variable.index(i)
                new_variable[variable_position] = variable_to_variable_back_dict[i]
        if test_key > 0:
            adjust_polynomial.variable = new_variable
            adjust_polynomial = adjust_polynomial.adjust()
        new_polynomial = 0
        test_key = 0
        for i in variable_to_polynomial_back_dict:
            if i in adjust_polynomial.variable:
                test_key += 1
                variable_position = adjust_polynomial.variable.index(i)
                for j in adjust_polynomial.coefficient:
                    if j[variable_position] >= 1:
                        add_polynomial_coefficient = {}
                        add_polynomial_variable = adjust_polynomial.variable[:]
                        new_key = list(j)
                        new_key[variable_position] = 0
                        new_key = tuple(new_key)
                        add_polynomial_coefficient[new_key] = adjust_polynomial.coefficient[j]
                        add_polynomial = MultiVariableSparsePolynomial(add_polynomial_coefficient, add_polynomial_variable) * (variable_to_polynomial_back_dict[i] ** j[variable_position])
                        new_polynomial += add_polynomial
                    else:
                        add_polynomial_coefficient = {}
                        add_polynomial_coefficient[j] = adjust_polynomial.coefficient[j]
                        add_polynomial_variable = adjust_polynomial.variable[:]
                        add_polynomial = MultiVariableSparsePolynomial(add_polynomial_coefficient, add_polynomial_variable)
                        new_polynomial += add_polynomial
        if test_key == 0:
            return adjust_polynomial
        else:
            return new_polynomial.adjust()

    def __pos__(self):
        return self.adjust()

    def __repr__(self):
        self_adjust = self.adjust()
        if not isinstance(self_adjust, MultiVariableSparsePolynomial):
            return repr(self_adjust)
        return_str = "MultiVariableSparsePolynomial(" + repr(self.coefficient) + ", "
        return_str += repr(self.variable) + ")"
        return return_str

    def __str__(self):
        disp_polynomial = self.adjust()
        if not isinstance(disp_polynomial, MultiVariableSparsePolynomial):
            return str(disp_polynomial)
        elif len(disp_polynomial.variable) == 1:
            max_index = 0
            for i in disp_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in disp_polynomial.coefficient:
                return_coefficient[i[0]] += disp_polynomial.coefficient[i]
            return str(OneVariableDensePolynomial(return_coefficient, disp_polynomial.variable[0]))
        else:
            old_variable = disp_polynomial.variable[:]
            reverse_coefficient = disp_polynomial.coefficient.copy()
            reverse_variable = old_variable[:]
            reverse_variable.reverse()
            reverse_polynomial = MultiVariableSparsePolynomial(reverse_coefficient, reverse_variable)
            reverse_polynomial = reverse_polynomial.sort_variable()
            result_coefficient = reverse_polynomial.coefficient.keys()
            result_coefficient.sort()
            test_key = (0,) * len(disp_polynomial.variable)
            return_str = ""
            for i in range(len(result_coefficient)):
                if reverse_polynomial.coefficient[result_coefficient[i]] > 0:
                    return_str += ' + '
                    if (reverse_polynomial.coefficient[result_coefficient[i]] != 1) or (result_coefficient[i] == test_key):
                        return_str += str(reverse_polynomial.coefficient[result_coefficient[i]])
                        if result_coefficient[i] != test_key:
                            return_str += ' * '
                else:
                    return_str += ' - '
                    if (reverse_polynomial.coefficient[result_coefficient[i]] != -1) or (result_coefficient[i] == test_key):
                        return_str += str(abs(reverse_polynomial.coefficient[result_coefficient[i]]))
                        if result_coefficient[i] != test_key:
                            return_str += ' * '
                index_total = 0
                for k in range(len(result_coefficient[i])):
                    index_total += result_coefficient[i][k]
                index_rest = index_total
                for j in range(len(result_coefficient[i])):
                    if result_coefficient[i][- 1 - j] == 1:
                        return_str += old_variable[j]
                    elif result_coefficient[i][- 1 - j] > 1:
                        if result_coefficient[i][- 1 - j] != index_total:
                            return_str += '('
                        return_str += old_variable[j]
                        return_str += ' ** '
                        return_str += str(result_coefficient[i][- 1 - j])
                        if result_coefficient[i][- 1 - j] != index_total:
                            return_str += ')'
                    index_rest -= result_coefficient[i][- 1 - j]
                    if index_rest and result_coefficient[i][- 1 - j]:
                        return_str += ' * '
            if return_str[1] != '+':
                return return_str[1:]
            else:
                return return_str[3:]

    def arrange_variable(self, other):
        if not isinstance(other, list):
            raise ValueError("You must input list for other.")
        else:
            result_polynomial = MultiVariableSparsePolynomial({}, other)
            index_list = self.coefficient.keys()[:]
            values_list = self.coefficient.values()[:]
            position_infomation = []
            for i in range(len(other)):
                if other[i] in self.variable:
                    position_infomation.append(i)
            for i in range(len(index_list)):
                key = [0]*len(other)
                for j in range(len(position_infomation)):
                    key[(position_infomation[j])] = index_list[i][j]
                result_polynomial.coefficient[tuple(key)] = values_list[i]
            return result_polynomial

    def adjust(self):
        if not self.variable or not self.coefficient:
            return self.getRing().zero
        result_polynomial = self.sort_variable()
        result_polynomial = result_polynomial.merge_variable()
        result_polynomial = result_polynomial.delete_zero_value()
        result_polynomial = result_polynomial.delete_zero_variable()
        result_coefficient = result_polynomial.coefficient
        if not result_coefficient:
            return result_polynomial.getRing().zero
        zero_test = (0,)*len(result_polynomial.variable)
        if (len(result_coefficient) == 1) and (zero_test in result_coefficient):
            return result_coefficient[zero_test]
        return result_polynomial

    copy = adjust

    def sort_variable(self):
        positions = {}
        for i, v in enumerate(self.variable):
            if v in positions:
                positions[v] = positions[v] + (i,)
            else:
                positions[v] = (i,)
        result_variable = self.variable[:]
        result_polynomial = MultiVariableSparsePolynomial({}, result_variable)
        result_polynomial.variable.sort()
        for i in self.coefficient:
            new_index_list = []
            old_positions = positions.copy()
            for j in range(len(i)):
                jth_variable = result_polynomial.variable[j]
                jth_position = positions[jth_variable]
                if len(jth_position) == 1:
                    new_index_list.append(i[jth_position[0]])
                else:
                    new_index_list.append(i[jth_position[0]])
                    positions[jth_variable] = jth_position[1:]
            new_index = tuple(new_index_list)
            if new_index in result_polynomial.coefficient:
                result_polynomial.coefficient[new_index] += self.coefficient[i]
            else:
                result_polynomial.coefficient[new_index] = self.coefficient[i]
            positions.update(old_positions)
        return result_polynomial

    def merge_variable(self):
        old_variable_list = self.variable
        merge_variable = [old_variable_list[0]]
        for i in range(len(old_variable_list) - 1):
            if old_variable_list[i+1] != old_variable_list[i]:
                merge_variable.append(old_variable_list[i+1])
        variable_position = {}
        for i, merging in enumerate(merge_variable):
            position_list = []
            for j, older in enumerate(old_variable_list):
                if older == merging:
                    position_list.append(j)
            variable_position[merging] = position_list
        result_coefficient = {}
        for key, coeff in self.coefficient.items():
            new_coefficient_key = []
            for j in merge_variable:
                new_value = sum([key[k] for k in variable_position[j]])
                new_coefficient_key.append(new_value)
            new_key_tuple = tuple(new_coefficient_key)
            if new_key_tuple in result_coefficient:
                result_coefficient[new_key_tuple] += coeff
            else:
                result_coefficient[new_key_tuple] = coeff
        return self.__class__(result_coefficient, merge_variable)

    def delete_zero_value(self):
        result_coefficient = {}
        for i in self.coefficient:
            if self.coefficient[i]:
                result_coefficient[i] = self.coefficient[i]
        return self.__class__(result_coefficient, self.variable)

    def delete_zero_variable(self):
        old_coefficient_keys = self.coefficient.keys()
        old_coefficient_values = self.coefficient.values()
        old_variable = self.variable
        exist_position_list = []
        for i in range(len(old_variable)):
            for k in old_coefficient_keys:
                if k[i]:
                    exist_position_list.append(i)
                    break
        new_variable = [old_variable[position] for position in exist_position_list]
        new_coefficient = {}
        for i in range(len(old_coefficient_keys)):
            new_coefficient_key = []
            for j in exist_position_list:
                new_coefficient_key += [old_coefficient_keys[i][j]]
            new_coefficient[tuple(new_coefficient_key)] = old_coefficient_values[i]
        return self.__class__(new_coefficient, new_variable)

    def differentiate(self, var):
        """
        Return partial differentiation with var.
        """
        if not isinstance(var, str):
            raise TypeError("var must be the name of a variable.")
        original = self.adjust()
        variables = original.variable
        if var not in variables: # trivial case
            return 0
        var_at = variables.index(var)
        coefficients = {}
        for degrees in original.coefficient:
            coefficient = original.coefficient[degrees]
            if degrees[var_at] == 0 or not coefficient:
                continue
            new_degrees = list(degrees)
            new_degrees[var_at] -= 1
            coefficients[tuple(new_degrees)] = coefficient * degrees[var_at]
        return MultiVariableSparsePolynomial(coefficients, variables).adjust()

    def integrate(self, var=None, mini=None, maxi=None):
        """
        Return definite or indefinite integration of the polynomial.
        """
        if not isinstance(var, str):
            raise TypeError("var must be the name of a variable.")
        if (mini is None and maxi is not None or
            mini is not None and maxi is None):
            raise ValueError("either one of mini or maxi is missing.")

        integrand = self.adjust()
        if var in integrand.variable:
            var_at = integrand.variable.index(var)
            coefficients = {}
            for degrees in integrand.coefficient:
                new_degrees = list(degrees)
                new_degrees[var_at] += 1
                new_coefficient = integrand.coefficient[degrees] * rational.Rational(1, new_degrees[var_at])
                new_degrees = tuple(new_degrees)
                coefficients[new_degrees] = new_coefficient
            integrated = MultiVariableSparsePolynomial(coefficients, integrand.variable).adjust()
            if mini is None and maxi is None:
                return integrated
            else:
                return integrated(**{var: maxi}) - integrated(**{var: mini})
        else:
            if mini is None and maxi is None:
                return integrand * OneVariableMonomial(var)
            else:
                return integrand * (maxi - mini)

    def toOneVariableDensePolynomial(self):
        origin_polynomial = self.adjust()
        if not isinstance(origin_polynomial, (MultiVariableSparsePolynomial, OneVariablePolynomial)):
            return origin_polynomial
        elif len(origin_polynomial.variable) == 1:
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                return_coefficient[i[0]] += origin_polynomial.coefficient[i]
            return OneVariableDensePolynomial(return_coefficient, origin_polynomial.variable[0])
        else:
            raise ValueError("You must input OneVariablePolynomial.")

    def toOneVariableSparsePolynomial(self):
        origin_polynomial = self.adjust()
        if not isinstance(origin_polynomial, (MultiVariableSparsePolynomial, OneVariablePolynomial)):
            return origin_polynomial
        elif len(origin_polynomial.variable) == 1:
            return_coefficient = {}
            return_variable = origin_polynomial.variable[:]
            return_coefficient.update(origin_polynomial.coefficient)
            return OneVariableSparsePolynomial(return_coefficient, return_variable)
        else:
            raise ValueError("You must input OneVariablePolynomial.")

    def getRing(self):
        myring = None
        for c in self.coefficient.values():
            cring = ring.getRing(c)
            if not myring or myring != cring and myring.issubring(cring):
                myring = cring
            elif not cring.issubring(myring):
                myring = myring.getCommonSuperring(cring)
        if not myring:
            return rational.theIntegerRing
        return PolynomialRing(myring, self.variable)


def construct(polynomial, kwd={}):
    """

    construct compiles a string to a polynomial.  The first argument
    should be a valid python code string representing a polynomial.
    The second optional argument is a dictionary which maps names to
    their values.

    """
    id_re = re.compile("[A-Za-z_][A-Za-z0-9_]*")
    start = 0
    while 1:
        m = id_re.search(polynomial[start:])
        if m:
            v = m.group()
            if v not in kwd:
                kwd[v] = OneVariableDensePolynomial([0, rational.Integer(1)], v)
            start += m.end()
        else:
            break
    r = eval(polynomial, kwd)
    return r

import nzmath.matrix as matrix

def resultant(f, g):
    """
    Return the resultant of 2 polynomials.
    """
    m = f.degree()
    n = g.degree()
    full_size = m + n

    f_row = f.coefficient.getAsList()[::-1] + [0] * (n - 1)
    upper = []
    for i in range(n):
        upper += f_row[-i:] + f_row[:-i]
    g_row = g.coefficient.getAsList()[::-1] + [0] * (m - 1)
    lower = []
    for i in range(m):
        lower += g_row[-i:] + g_row[:-i]

    assert len(upper) + len(lower) == full_size ** 2
    M = matrix.createMatrix(full_size, upper + lower)
    return M.determinant()

# Algorithm 3.1.2 of Cohen's book
def pseudoDivision(A, B):
    """

    pseudoDivision(A, B) -> (Q, R)

    Q, R are polynomials such that
    d**(deg(A)-deg(B)+1) * A == B * Q + R,
    where d is the leading coefficient of B.

    """
    if isinstance(A, OneVariablePolynomial):
        m = A.degree()
    else:
        m = 0
    if isinstance(B, OneVariablePolynomial):
        n = B.degree()
        d = B[n]
    else:
        n = 0
        d = B

    # step 1
    R = copy.deepcopy(A)
    Q = A.getRing().zero
    e = m-n+1
    while 1:
        # step 2
        if isinstance(R, OneVariablePolynomial):
            degR = R.degree()
        else:
            degR = 0
        if isinstance(B, OneVariablePolynomial):
            degB = B.degree()
        else:
            degB = 0

        if degR < degB:
            q = d ** e
            Q = q * Q
            R = q * R
            return (Q, R)
        # step 3
        if isinstance(R, OneVariablePolynomial):
            degR = R.degree()
        else:
            degR = 0

        if isinstance(B, OneVariablePolynomial):
            degB = B.degree()
        else:
            degB = 0

        if isinstance(R, OneVariablePolynomial):
            lR = R[degR]
        else:
            lR = R

        tmp = [0] * (degR - degB)
        tmp.append(1)
        S = lR * OneVariableDensePolynomial(tmp, A.variable)
        Q = d * Q + S
        R = d * R - S * B
        e -= 1

# Algorithm 3.3.1 of Cohen's book
def subResultantGCD(A, B):
    """

    returns a GCD of 2 polynomials whose coefficient ring is a UFD.

    """
    # step 1
    if B.degree() > A.degree():
        A, B = B, A
    if not B:
        return A
    a = A.content()
    b = B.content()
    d = a.getRing().gcd(a, b)
    A = A.primitivePart()
    B = B.primitivePart()
    g = rational.Integer(1)
    h = rational.Integer(1)

    while 1:
        # step 2
        if isinstance(A, OneVariablePolynomial):
            degA = A.degree()
        else:
            degA = 0
        if isinstance(B, OneVariablePolynomial):
            degB = B.degree()
        else:
            degB = 0
        delta = degA - degB
        R = pseudoDivision(A, B)[1]
        if not R:
            return d * B.primitivePart()
        if isinstance(R, OneVariablePolynomial):
            degR = R.degree()
        else:
            degR = 0
        if degR == 0:
            return d

        # step 3
        A = copy.deepcopy(B)
        B = R / (g * h**delta)
        g = A[A.degree()]
        if 1 - delta >= 0:
            h = h ** (1 - delta) * g ** delta
        else:
            h = h ** (delta - 1) * g ** delta

def discriminant(f):
    """
    Return discriminant of the given polynomial f.
    """
    deg = f.degree()
    variable = f.getVariable()
    df = f.differentiate(variable)
    return (-1)**(deg*(deg-1)/2)*resultant(f,df)/f[deg]


class OneVariablePolynomialChar0 (OneVariablePolynomial):
    """

    OneVariablePolynomialChar0 is a class for one variable polynomial
    whose coefficient ring is a field of characteristic 0.

    """
    def __init__(self, coefficient, variable, coeffring):
        if isinstance(coefficient, OneVariablePolynomialCoefficients):
            OneVariablePolynomial.__init__(self,
                                           coefficient,
                                           variable,
                                           coeffring)
        elif isinstance(coefficient, list):
            coeff = OneVariablePolynomialCoefficients()
            coeff.setList(coefficient)
            OneVariablePolynomial.__init__(self,
                                           coeff,
                                           variable,
                                           coeffring)

    def squareFreeDecomposition(self):
        """

        Return the square free decomposition of the polynomial.  The
        return value is a dict whose keys are integers and values are
        corresponding powered factors.  For example, if
        A = A1 * A2**2,
        the result is {1: A1, 2: A2}.

        """
        result = {}
        if self.degree() == 1:
            return {1: self.copy()}
        rx = self.getRing()
        b = rx.gcd(self, self.differentiate(self.getVariable()))
        a = self / b
        i = 1
        while b.degree() > 0:
            c = rx.gcd(a, b)
            b /= c
            if a != c:
                r = a / c
                if r.degree() > 0:
                    result[i] = r
                a = c
            i += 1
        result[i] = a
        return result

    def integrate(self, var=None, mini=None, maxi=None):
        if mini == None and maxi == None and var != None and isinstance(var, str):
            if self.degree() == 0:
                return OneVariableDensePolynomial([0, self[0]], var, self.getCoefficientRing())
            elif self.degree() < 0:
                return self(var)
            elif var != self.getVariable():
                return self * OneVariableDensePolynomial([0, 1], var, self.getCoefficientRing())
            else:
                integrate_coefficient = {}
                for i, c in self.coefficient.iteritems():
                    integrate_coefficient[i+1] = c / (i+1)
                return OneVariableSparsePolynomial(
                    integrate_coefficient,
                    var,
                    self.getCoefficientRing().getQuotientField())
        elif mini != None and maxi != None and var != None and isinstance(var, str):
            if var != self.getVariable():
                return self * (maxi - mini)
            primitive_function = self.integrate(var)
            return primitive_function(maxi) - primitive_function(mini)
        else:
            raise ValueError("You must call integrate with variable or with variable, min and max.")


class RationalOneVariablePolynomial (OneVariablePolynomialChar0):
    def __init__(self, coefficient, variable):
        if isinstance(coefficient, OneVariablePolynomialCoefficients):
            OneVariablePolynomialChar0.__init__(self,
                                                coefficient,
                                                variable,
                                                rational.theRationalField)
        elif isinstance(coefficient, list):
            coeff = OneVariablePolynomialCoefficients()
            coeff.setList(coefficient)
            OneVariablePolynomialChar0.__init__(self,
                                                coeff,
                                                variable,
                                                rational.theRationalField)

    def __divmod__(self, other):
        """
        About this division , we can treat only a map of
                     Q[x] --> Q[x]
        and only one variable polynomial.
        """
        if other == 0:
            raise ZeroDivisionError("division or modulo by zero.")
        elif isinstance(other, OneVariablePolynomial):
            if other.degree() == 0:
                coeff = other[0]
                new_coeff = OneVariablePolynomialCoefficients()
                for i, c in self.coefficient.iteritems():
                    new_coeff[i] = rational.Rational(c, coeff)
                return (OneVariableDensePolynomial(new_coeff.getAsList(),
                                                   self.variable,
                                                   rational.theRationalField),
                        0)
            if self.getVariable() != other.getVariable() or self.degree() < other.degree():
                return 0, self.copy()
            else:
                self_coeff = self.coefficient.getAsList()
                other_coeff = other.coefficient.getAsList()
                other_leading_coeff = other_coeff[-1]
                new_coeff = []
                i = self.degree()
                k = other.degree()
                while i >= k:
                    q = self_coeff[-1] / other_leading_coeff
                    m = 1
                    for j in other_coeff:
                        self_coeff[-(k+m)] = self_coeff[-(k+m)] - j * q
                        m -= 1
                    new_coeff.append(q)
                    self_coeff.pop()
                    i -= 1
                new_coeff.reverse()
                return (OneVariableDensePolynomial(new_coeff,
                                                   self.getVariable(),
                                                   rational.theRationalField),
                        OneVariableDensePolynomial(self_coeff,
                                                   self.getVariable(),
                                                   rational.theRationalField))
        elif isinstance(other, (rational.Rational, int, long)):
            new_coeff = OneVariablePolynomialCoefficients()
            for i, c in self.coefficient.iteritems():
                new_coeff[i] = rational.Rational(c) // other
            return (OneVariableDensePolynomial(new_coeff.getAsList(),
                                              self.getVariable(),
                                              rational.theRationalField),
                    0)
        else:
            commonSuperring = self.getRing().getCommonSuperring(ring.getRing(other))
            return commonSuperring.createElement(self).__divmod__(commonSuperring.createElement(other))


class OneVariablePolynomialCharNonZero (OneVariablePolynomial):
    """

    OneVariablePolynomialCharNonZero is a class for one variable polynomial
    whose coefficient ring is a field of characteristic p > 0.

    """
    def __init__(self, coefficient, variable, coeffring):
        if isinstance(coefficient, OneVariablePolynomialCoefficients):
            OneVariablePolynomial.__init__(self,
                                           coefficient,
                                           variable,
                                           coeffring)
        elif isinstance(coefficient, list):
            coeff = OneVariablePolynomialCoefficients()
            coeff.setList(coefficient)
            OneVariablePolynomial.__init__(self,
                                           coeff,
                                           variable,
                                           coeffring)
        self.ch = self.getCoefficientRing().getCharacteristic()

    def __divmod__(self, other):
        if not other:
            raise ZeroDivisionError("polynomial division or modulo by zero.")
        theField = self.getCoefficientRing()
        x = self.getVariable()
        if isinstance(other, OneVariablePolynomial):
            null = OneVariablePolynomialCoefficients()
            if other.degree() == 0:
                other = other[0]
                div_coeff = OneVariablePolynomialCoefficients()
                div_coeff.changeRepresentation(div_coeff.USING_DICT)
                for i, c in self.coefficient.iteritems():
                    div_coeff[i] = c / other
                return (self.__class__(div_coeff, x, theField),
                        self.__class__(null, x, theField))
            elif x != other.getVariable() or self.degree() < other.degree():
                return  (self.__class__(null, x, theField),
                         self.copy())
            else:
                div_poly = null
                mod_poly = self.coefficient.copy()
                deg, o_deg = mod_poly.degree(), other.degree()
                o_lc = other[o_deg]
                if o_deg > 0:
                    while deg >= o_deg:
                        deg_diff = deg - o_deg
                        div_poly[deg_diff] = theField.createElement(mod_poly[deg] / o_lc)
                        canceler = (div_poly[deg_diff] * other).coefficient
                        for i in range(deg_diff, deg):
                            mod_poly[i] = mod_poly[i] - canceler[i - deg_diff]
                        mod_poly[deg] = theField.zero
                        deg = mod_poly.degree()
                else:
                    while deg >= 0:
                        div_poly[deg] = theField.createElement(mod_poly[deg] / o_lc)
                        mod_poly[deg] = theField.zero
                        deg = mod_poly.degree()
                div_poly = self.__class__(div_poly, x, theField)
                mod_poly = self.__class__(mod_poly, x, theField)
                return (div_poly, mod_poly)
        commonSuperring = self.getRing().getCommonSuperring(ring.getRing(other))
        return commonSuperring.createElement(self).__divmod__(commonSuperring.createElement(other))

    def __pow__(self, index, mod = None):
        if not isinstance(index, (int, long)):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be a non-negative integer.")
        if index > 0:
            q = 1
            while index % self.ch == 0:
                q *= self.ch
                index //= self.ch
            if q > 1:
                poweredCoeff = OneVariablePolynomialCoefficients()
                for i, c in self.coefficient.iteritems():
                    poweredCoeff[i*q] = c
                powered = self.__class__(
                    poweredCoeff,
                    self.getVariable(),
                    self.getCoefficientRing())
            else:
                powered = self.copy()
        if index == 1:
            if mod == None:
                return powered
            else:
                return powered % mod
        power_product = self.getRing().one
        if index == 0:
            return power_product
        if mod == None:
            power_of_2 = powered.copy()
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                power_of_2 = power_of_2 * power_of_2
                index = index // 2
        else:
            power_of_2 = powered % mod
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                    power_product %= mod
                power_of_2 = (power_of_2 * power_of_2) % mod
                index = index // 2
        return power_product

    def squareFreeDecomposition(self):
        """

        Return the square free decomposition of the polynomial.  The
        return value is a dict whose keys are integers and values are
        corresponding powered factors.  For example, if
        A = A1 * A2**2,
        the result is {1: A1, 2: A2}.

        """
        f = self.copy()
        df = self.differentiate(self.getVariable())
        rx = self.getRing()
        result = {}
        if df:
            if f.degree() == 1:
                result = {1: f}
                f = self.getRing().one
            else:
                b = rx.gcd(f, df)
                a = f / b
                i = 1
                while a.degree() > 0:
                    c = rx.gcd(a, b)
                    b /= c
                    if a != c:
                        r = a / c
                        if r.degree() > 0:
                            result[i] = r
                        a = c
                    i += 1
                f = b
        if f.degree() > 0:
            f = f.pthroot(self.ch)
            subresult = f.squareFreeDecomposition()
            for i, g in subresult.iteritems():
                result[i*self.ch] = g
        return result

    def pthroot(self, ch=None):
        """
        If the polynomial is a characteristic ch-th power polynomial,
        then return its ch-th root.
        """
        if not ch:
            ch = self.getCoefficientRing().getCharacteristic()
        rootcoeff = OneVariablePolynomialCoefficients()
        for i in self.coefficient.iterdegrees():
            rootcoeff[i//ch] = self[i]
        return self.__class__(rootcoeff, self.getVariable(), self.getCoefficientRing())

    def distinctDegreeFactorization(self):
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
        Fq = self.getCoefficientRing()
        FqX = self.getRing()
        q = len(Fq)
        f = self.copy()
        x = f.__class__([0, 1], f.getVariable(), Fq)
        w = x.copy()
        i = 1
        result = {}
        while i*2 <= f.degree():
            w = pow(w, q, f)
            result[i] = FqX.gcd(f, w-x)
            if result[i].degree() > 0:
                f = f / result[i]
                w = w % f
            else:
                del result[i]
            i += 1
        if f.degree() != 0:
            result[f.degree()] = f
        return result

    def splitSameDegrees(self, degree):
        """

        Return the irreducible factors of the polynomial.  The
        polynomial must be a product of irreducible factors of the
        given degree.

        """
        r = self.degree() / degree
        Fq = self.getCoefficientRing()
        FqX = self.getRing()
        q = len(Fq)
        p = Fq.getCharacteristic()
        if degree == 1:
            result = []
            X = OneVariableDensePolynomial([0, 1],
                                           self.getVariable(),
                                           self.getCoefficientRing())
            f = self.copy()
            while not f[0]:
                f = f // X
                result.append(X)
            if f.degree() >= 1:
                result.append(f)
        else:
            result = [self.copy()]
        while len(result) < r:
            # g is a random polynomial
            randPolyCoeff = OneVariablePolynomialCoefficients()
            for i in range(2 * degree):
                randPolyCoeff[i] = Fq.createElement(bigrandom.randrange(q))
            randPoly = self.__class__(randPolyCoeff, self.getVariable(), Fq)
            if randPoly.degree() < 1:
                continue
            if p == 2:
                G = 0
                for j in range(degree*r):
                    G = G + pow(randPoly, 2**j, self)
            else:
                G = pow(randPoly, (q**degree - 1)//2, self) - FqX.one
            subresult = []
            while result:
                h = result.pop()
                if h.degree() == degree:
                    subresult.append(h)
                    continue
                z = FqX.gcd(h, G)
                if 0 < z.degree() < h.degree():
                    subresult.append(z)
                    subresult.append(h / z)
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
        if self[self.degree()] != self.getCoefficientRing().createElement(1):
            lc = self[self.degree()]
            self /= lc
            result.append((lc, 1))
        squareFreeFactors = self.squareFreeDecomposition()
        for m, f in squareFreeFactors.iteritems():
            distinctDegreeFactors = f.distinctDegreeFactorization()
            for d, g in distinctDegreeFactors.iteritems():
                if d == g.degree():
                    result.append((g, m))
                else:
                    for irred in g.splitSameDegrees(d):
                        result.append((irred, m))
        return result

    def isIrreducible(self):
        """

        f.isIrreducible() -> bool

        If f is irreducible return True, otherwise False.

        """
        result = []
        squareFreeFactors = self.squareFreeDecomposition()
        if len(squareFreeFactors) != 1:
            return False
        m, f = squareFreeFactors.popitem()
        if m != 1:
            return False
        distinctDegreeFactors = f.distinctDegreeFactorization()
        if len(distinctDegreeFactors) != 1:
            return False
        d, g = distinctDegreeFactors.popitem()
        if d != g.degree():
            return False
        return True


class OneVariablePolynomialCoefficients:
    """

    Polynomial coefficients data type for one variable polynomial.

    """

    USING_LIST = 0
    USING_DICT = 1

    def __init__(self):
        self._list = list()
        self._dict = dict()
        self._degree = -1
        self._using = self.USING_LIST

    def __getitem__(self, index):
        if not isinstance(index, (int, long)):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be a positive integer.")
        if self._using == self.USING_LIST:
            if len(self._list) > index:
                return self._list[index]
            else:
                return 0
        elif self._using == self.USING_DICT:
            return self._dict.get(index, 0)

    def __setitem__(self, index, value):
        if not isinstance(index, (int, long)):
            raise TypeError("index must be an integer.")
        if index < 0:
            raise ValueError("index must be a positive integer.")
        if self._using == self.USING_LIST:
            if len(self._list) > index:
                self._list[index] = value
            elif value or not isinstance(value, (int, long, float, complex)):
                zero = ring.getRing(value).zero
                self._list += [zero]*(index - len(self._list)) + [value]
        elif self._using == self.USING_DICT:
            self._dict[index] = value

    def degree(self):
        if self._using == self.USING_LIST:
            deg = len(self._list) - 1
            while deg >= 0:
                if not self._list[deg]:
                    deg -= 1
                else:
                    break
            return deg
        elif self._using == self.USING_DICT:
            if not self._dict:
                return -1
            deg = -1
            for index in self._dict:
                if index > deg and self._dict[index]:
                    deg = index
            return deg

    def getAsList(self):
        return [+self[i] for i in range(self.degree()+1)]

    def getAsDict(self):
        if self._using == self.USING_LIST:
            retval = dict()
            for i in range(self.degree()+1):
                if self[i]:
                    retval[i] = +self[i]
            return retval
        else:
            return self._dict.copy()

    def setList(self, aList):
        self._using = self.USING_LIST
        self._list = aList

    def setDict(self, aDict):
        self._using = self.USING_DICT
        self._dict = aDict

    def changeRepresentation(self, rep):
        """

        Change inner representaion.
        This method is destructive.

        """
        if self._using == rep:
            pass
        elif rep == self.USING_LIST:
            self._list = self.getAsList()
            self._using = rep
        elif rep == self.USING_DICT:
            self._dict = self.getAsDict()
            self._using = rep
        return

    def __iter__(self):
        if self._using == self.USING_LIST:
            return iter(self._list)
        elif self._using == self.USING_DICT:
            return iter(self._dict)

    def __len__(self):
        return self.degree() + 1

    def iteritems(self):
        if self._using == self.USING_LIST:
            return iter([(i, c) for i, c in enumerate(self._list) if c])
        elif self._using == self.USING_DICT:
            return iter([(i, c) for i, c in self._dict.iteritems() if c])

    def itercoeffs(self):
        if self._using == self.USING_LIST:
            for c in self._list:
                if c:
                    yield c
        elif self._using == self.USING_DICT:
            for c in self._dict.itervalues():
                yield c

    def iterdegrees(self):
        if self._using == self.USING_LIST:
            for i, c in zip(range(len(self._list)), self._list):
                if c:
                    yield i
        elif self._using == self.USING_DICT:
            for i in self._dict.iterkeys():
                yield i

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.getAsList())

    def copy(self):
        retval = OneVariablePolynomialCoefficients()
        retval.setDict(self.getAsDict())
        return retval

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, OneVariablePolynomialCoefficients):
            return NotImplemented
        if self._using == other._using:
            if self._using == self.USING_LIST:
                return self._list == other._list
            else:
                return self._dict == other._dict
        else:
            if self._using == self.USING_LIST:
                return self._list == other.getAsList()
            else:
                return self._dict == other.getAsDict()

    def __ne__(self, other):
        if not isinstance(other, OneVariablePolynomialCoefficients):
            return NotImplemented
        return not (self == other)


class PolynomialRing (ring.CommutativeRing):
    """
    The class of polynomial ring.
    """

    def __init__(self, aRing, var):
        if not isinstance(aRing, ring.Ring):
            raise TypeError("%s should not be passed as ring" % aRing.__class__)
        ring.CommutativeRing.__init__(self)
        self.coefficientRing = aRing
        if isinstance(var, str):
            self.vars = set((var,))
        else:
            self.vars = set(var)
        if self.coefficientRing.isfield() and len(self.vars) == 1:
            self.properties.setIseuclidean(True)
        else:
            if self.coefficientRing.isufd():
                self.properties.setIsufd(True)
            if self.coefficientRing.isnoetherian():
                self.properties.setIsnoetherian(True)
            elif self.coefficientRing.isdomain():
                self.properties.setIsdomain(True)
            elif False == self.coefficientRing.isdomain():
                self.properties.setIsdomain(False)

    def getVars(self):
        return self.vars.copy()

    def getCoefficientRing(self, var = None):
        """

        returns coefficient ring corresponding to given variable(s).
        If variable is not given or irrelevant, only univariate
        polynomial ring can return the answer.  In other cases,
        TypeError will be raised.

        """
        if not var:
            _vars = set()
        elif isinstance(var, str):
            _vars = set((var,))
        else:
            _vars = set(var)
        _vars &= self.vars
        varsInRing = self.vars - _vars
        if _vars and varsInRing:
            return PolynomialRing(self.coefficientRing, varsInRing)
        elif _vars:
            return self.coefficientRing
        elif varsInRing:
            if len(varsInRing) == 1:
                return self.coefficientRing
            raise TypeError("The meaning of `coefficient ring' is ambiguous.")
        else:
            # never happen
            pass

    def getQuotientField(self):
        """

        getQuotientField returns the quotient field of the ring
        if coefficient ring has its quotient field.  Otherwise,
        an exception will be raised.

        """
        try:
            coefficientField = self.coefficientRing.getQuotientField()
            import nzmath.rationalFunction as rationalFunction
            return rationalFunction.RationalFunctionField(coefficientField, self.vars)
        except:
            raise

    def __eq__(self, other):
        if not isinstance(other, PolynomialRing):
            return False
        if self.coefficientRing == other.coefficientRing and self.vars == other.vars:
            return True
        elif isinstance(self.coefficientRing, PolynomialRing):
            return self.unnest() == other
        elif isinstance(other.coefficientRing, PolynomialRing):
            return self == other.unnest()
        return False

    def __repr__(self):
        return "PolynomialRing(" + repr(self.coefficientRing) + ", " + repr(self.vars) + ")"

    def __str__(self):
        retval = str(self.coefficientRing)
        retval += "["
        retval += ", ".join(list(self.vars))
        retval += "]"
        return retval

    def __hash__(self):
        return hash(self.coefficientRing) ^ hash(repr(self.vars))

    def __contains__(self, element):
        """
        `in' operator is provided for checking the element be in the
        ring.
        """
        if element in self.coefficientRing:
            return True
        elem_ring = ring.getRing(element)
        if elem_ring.issubring(self):
            return True
        return False

    def issubring(self, other):
        """

        reports whether another ring contains this polynomial ring.

        """
        import nzmath.rationalFunction as rationalFunction
        if isinstance(other, PolynomialRing):
            if self.coefficientRing.issubring(other.getCoefficientRing(other.getVars())) and \
                   self.vars.issubset(other.getVars()):
                return True
            else:
                return False
        elif isinstance(other, rationalFunction.RationalFunctionField):
            return other.issuperring(self)
        else:
            return False

    def issuperring(self, other):
        """

        reports whether this polynomial ring contains another ring.

        """
        if self.coefficientRing.issuperring(other):
            return True
        if isinstance(other, PolynomialRing):
            if self.coefficientRing.issuperring(other.getCoefficientRing(other.getVars())) and \
                   self.vars.issuperset(other.getVars()):
                return True
            else:
                return False
        return False

    def unnest(self):
        """

        if self is a nested PolynomialRing i.e. its coefficientRing is
        also a PolynomialRing, then the function returns one level
        unnested PolynomialRing.

        For example:
        PolynomialRing(PolynomialRing(Q, "x"), "y").unnest()
        returns
        PolynomialRing(Q, set(["x","y"])).

        """
        return PolynomialRing(self.coefficientRing.coefficientRing, self.coefficientRing.vars | self.vars)

    def getCommonSuperring(self, other):
        if self.issuperring(other):
            return self
        elif other.issuperring(self):
            return other
        elif not isinstance(other, PolynomialRing) and other.issuperring(self.coefficientRing):
            return PolynomialRing(other, self.getVars())
        elif isinstance(other, PolynomialRing):
            sCoef = self.getCoefficientRing(self.getVars())
            oCoef = other.getCoefficientRing(other.getVars())
            sVars = self.getVars()
            oVars = other.getVars()
            if sCoef.issuperring(oCoef):
                return PolynomialRing(sCoef, sVars | oVars)
            elif oCoef.issuperring(sCoef):
                return PolynomialRing(oCoef, sVars | oVars)

    def createElement(self, seed):
        if ring.getRing(seed) == self:
            return seed.copy()
        if len(self.vars) == 1:
            variable = [v for v in self.vars][0]
            if seed in self.coefficientRing:
                return OneVariableDensePolynomial([seed], variable, self.coefficientRing)
            if isinstance(seed, OneVariablePolynomial):
                return OneVariableDensePolynomial(seed.coefficient.getAsList(), variable, self.coefficientRing)
            # container classes
            if isinstance(seed, list):
                return OneVariableDensePolynomial(seed, variable, self.coefficientRing)
            if isinstance(seed, dict):
                return OneVariableSparsePolynomial(seed, variable, self.coefficientRing)
            if isinstance(seed, OneVariablePolynomialCoefficients):
                return OneVariablePolynomial(seed, variable, self.coefficientRing)
            # final judgement
            raise TypeError("larger ring element cannot be a seed.")
        else:
            if seed in self.coefficientRing:
                return MultiVariableSparsePolynomial({(0,)*len(self.vars):self.coefficientRing.createElement(seed)}, list(self.vars))
            listvars = list(self.vars)
            if isinstance(seed, OneVariablePolynomial):
                position = listvars.index(seed.getVariable())
                new_coef = {}
                for i, c in seed.coefficient.iteritems():
                    index = [0]*len(listvars)
                    index[position] = i
                    new_coef[tuple(index)] = self.coefficientRing.createElement(c)
                return MultiVariableSparsePolynomial(new_coef, listvars)
            elif isinstance(seed, str) and seed in self.vars:
                position = listvars.index(seed)
                new_coef = {}
                index = [0]*len(listvars)
                index[position] = 1
                new_coef[tuple(index)] = self.coefficientRing.one
                return MultiVariableSparsePolynomial(new_coef, listvars)
        # seed cannot be a multi-variable polynomial now
        raise NotImplementedError

    def __getattr__(self, attr):
        """
        __getattr__

        Return a polynomial corresponding to a specified variable.
        """
        if attr in self.vars:
            if len(self.vars) == 1:
                return self.createElement({1:1})
            else:
                return self.createElement(attr)
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr))

    def _getOne(self):
        "getter for one"
        if not self._one:
            if len(self.vars) == 1:
                variable = [v for v in self.vars][0]
                self._one = OneVariableDensePolynomial([1], variable, self.coefficientRing)
            else:
                self._one = MultiVariableSparsePolynomial({(0,)*len(self.vars): self.coefficientRing.createElement(1)}, list(self.vars))
        return self._one

    one = property(_getOne, None, None, "multiplicative unit")

    def _getZero(self):
        "getter for zero"
        if len(self.vars) == 1:
            variable = [v for v in self.vars][0]
            return OneVariableDensePolynomial([], variable, self.coefficientRing)
        else:
            return MultiVariableSparsePolynomial({}, list(self.vars))

    zero = property(_getZero, None, None, "additive unit")

    def gcd(self, a, b):
        if self.coefficientRing.isfield():
            A = self.createElement(a)
            B = self.createElement(b)
            while B:
                A, B = B, A % B
            if A in self.coefficientRing:
                return 1
            else:
                return A / A[A.degree()]
        elif self.coefficientRing.isufd():
            return subResultantGCD(a, b)
        else:
            raise NotImplementedError


class OneVariablePolynomialIdeal (ring.Ideal):
    """
    OneVariablePolynomialIdeal is a class to represent an ideal of one
    variable polynomial ring.
    """
    def __init__(self, generators, aRing):
        """
        OneVariablePolynomialIdeal(generators, ring) creates an ideal
        in the ring, which must be a polynomial ring with one
        variable, with the given generators.
        """
        if generators in aRing:
            self.generators = [generators]
        elif isinstance(generators, list) and len(generators) > 0:
            if aRing.ispid():
                g = generators[0]
                for t in generators:
                    g = aRing.gcd(t, g)
                if aRing.getCoefficientRing().isfield():
                    if g.leadingCoefficient() != aRing.getCoefficientRing().one:
                        g = g * g.leadingCoefficient().inverse()
                self.generators = [g]
            else:
                self.generators = generators[:]
        else:
            raise TypeError("generators of ideal must be elements of the ring.")
        self.ring = aRing
        self._cache = {}

    def __eq__(self, other):
        """
        I == J  <=>  I.__eq__(J)
        """
        assert self.__class__ == other.__class__
        if self is other:
            return True
        for i in self.generators:
            if i not in other:
                return False
        for j in other.generators:
            if j not in other:
                return False
        return True

    def __ne__(self, other):
        """
        I != J  <=>  I.__ne__(J)
        """
        return not (self == other)

    def __contains__(self, element):
        """
        e in I  <=>  I.__contains__(e)

        for e in the ring, to which the ideal I belongs.
        """
        assert self.ring == element.getRing()
        for g in self.generators:
            if not element % g:
                return True
        if len(self.generators) == 1:
            return False
        else:
            raise NotImplementedError

    def reduce(self, element):
        """
        Reduce the given element by the ideal.  The result is an
        element of the class which represents the equivalent class.
        """
        reduced = element.copy()
        if self.ring.iseuclidean() and isinstance(self.generators[0], OneVariablePolynomial):
            g = self.generators[0]
            coeffring = self.ring.getCoefficientRing()
            zero = coeffring.zero
            g_degree = g.degree()
            r_degree = reduced.degree()
            while r_degree >= g_degree:
                if r_degree not in self._cache:
                    self._expand_cache(r_degree)
                reduced = reduced + reduced[r_degree]*self._cache[r_degree]
                reduced[r_degree] = zero
                r_degree = reduced.degree()
        else:
            for g in self.generators:
                reduced = reduced % g
        return reduced

    def _expand_cache(self, degree):
        """
        Expand cache to given degree.
        """
        g = self.generators[0]
        g_degree = g.degree()
        R = self.ring.getCoefficientRing()
        x = self.ring.getVars().pop()
        if not self._cache:
            f = -g
            f[g_degree] = R.zero
            self._cache[g_degree] = f
            for d in range(g_degree + 1, 2*g_degree + 1):
                clist = self._cache[d - 1].coefficient.getAsList()
                if self._cache[d - 1][g_degree - 1]:
                    lc = clist[-1]
                    clist = [R.zero] + clist[:-1]
                    f = OneVariableDensePolynomial(clist, x, R)
                    self._cache[d] = f + lc * self._cache[g_degree]
                else:
                    clist = [R.zero] + clist
                    self._cache[d] = OneVariableDensePolynomial(clist, x, R)
        d = degree
        d_list = []
        while d >= g_degree:
            d_list.append(d)
            d = d // 2
        while d_list:
            d = d_list.pop() # LIFO
            if d in self._cache:
                continue
            double = self._cache[d//2] ** 2
            clist = double.coefficient.getAsList()
            while len(clist) - 1 >= g_degree:
                lc = clist.pop()
                if not lc:
                    continue
                reducer = self._cache[len(clist)].coefficient.getAsList()
                for i, r in enumerate(reducer):
                    clist[i] = clist[i] + r * lc
            if d % 2:
                clist = [R.zero] + clist
                if len(clist) - 1 == g_degree:
                    lc = clist.pop()
                    reducer = self._cache[g_degree].coefficient.getAsList()
                    for i, r in enumerate(reducer):
                        clist[i] = clist[i] + r * lc
            self._cache[d] = OneVariableDensePolynomial(clist, x, R)


class MultiVariablePolynomialIdeal (ring.Ideal):
    """

    MultiVariablePolynomialIdeal is a class to represent an ideal of
    multi variable polynomial ring.

    """
    def __init__(self, generators, ring):
        if isinstance(generators, list):
            self.generators = generators[:]
        elif generators in ring:
            self.generators = [generators]
        self.ring = ring

    def reduce(self, element):
        "reduction have not been provided yet."
        raise NotImplementedError

class PolynomialResidueRing (ring.ResidueClassRing):
    """

    PolynomialResidueRing is a ring of polynomial residues by an
    ideal.

    """
    def __init__(self, aRing, ideal):
        """

        PolynomialResidueRing(ring, ideal) creates a resudue class
        ring.  The ring should be a polynomial ring, and ideal must be
        an instance of OneVariablePolynomialIdeal or
        MultiVariablePolynomialIdeal according to the number of
        variables of the ring.

        """
        ring.ResidueClassRing.__init__(self, aRing, ideal)
        if self.ring.isnoetherian():
            self.properties.setIsnoetherian(True)
        if self.ring.isfield():
            self.properties.setIspid(True)

    def createElement(self, seed):
        """

        Create an element of the ring with seed.

        """
        if seed in self.ring:
            return ring.ResidueClass(seed, self.ideal)
        raise ValueError("seed is not valid.")


    
