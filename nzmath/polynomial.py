"""

Class definitions of polynomials.

"""
import math
import sets
import re

import rational
import ring
from rationalFunction import RationalFunctionField

class OneVariableDensePolynomial:

    def __init__(self, coefficient, variable, coeffring=None):
        """
        
        OneVariableDensePolynomial(coefficient, variable [,coeffring])

        coefficient must be a sequence of coefficients.
        variable must be a character string.
        coeffring must be, if specified, an object inheriting ring.Ring.
        """
        self.coefficient = OneVariablePolynomialCoefficients()
        self.variable = variable
        if not coeffring:
            self.coefficient.setList(list(coefficient))
            self.coeffcientRing, self.ring = self.initRing()
        else:
            self.coeffcientRing = coeffring
            self.ring = PolynomialRing(coeffring, self.variable)
            self.coefficient.setList([coeffring.createElement(c) for c in coefficient])

    def __setitem__(self, index, value):
        """

        aOneVariableDensePolynomial[n] = val
        sets val to the coefficient at degree n.  val must be in the
        coefficient ring of aOneVariableDensePolynomial.

        TypeError will be raised if n is not an integer, or if val is
        not in the coefficient ring.
        ValueError will be raised if n is negative.

        """
        if value in self.getCoefficientRing():
            self.coefficient[index] = value
        else:
            raise TypeError, "You must input an element of the coefficient ring for value."

    def __getitem__(self, index):
        """

        aOneVariableDensePolynomial[n]
        returns the coefficient at degree n.

        TypeError will be raised if n is not an integer.
        ValueError will be raised if n is negative.

        """
        return self.coefficient[index]

    def __add__(self, other):
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial)):
            if self.getVariable() == other.getVariable():
                sum = OneVariablePolynomialCoefficients()
                for i in range(max(self.degree(), other.degree()) + 1):
                    sum[i] = self[i] + other[i]
                commonRing = self.ring.getCommonSuperring(other.getRing())
                return OneVariableDensePolynomial(sum.getAsList(), self.getVariable(), commonRing.getCoefficientRing())
            else:
                return (self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()).toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableDensePolynomial() + other
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() + other
        elif other in self.getCoefficientRing():
            sum = OneVariableDensePolynomial(self.coefficient.getAsList(), self.getVariable())
            sum.coefficient[0] += other
            return sum.adjust()
        elif other == 0:
            return +self
        else:
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self) + commonSuperring.createElement(other)

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        reciprocal = [-c for c in self.coefficient]
        return OneVariableSparsePolynomial(reciprocal, self.getVariable(), self.getCoefficientRing())

    def __mul__(self, other):
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial)):
            if self.getVariable() == other.getVariable():
                product = OneVariablePolynomialCoefficients()
                for l in range(len(self.coefficient)):
                    if self[l]:
                        for r in range(len(other.coefficient)):
                            product[l + r] = product[l + r] + self[l] * other[r]
                commonRing = self.getRing().getCommonSuperring(other.getRing())
                if not commonRing and self.getCoefficientRing():
                    return OneVariableDensePolynomial(product.getAsList(), self.getVariable(), self.getCoefficientRing())
                return OneVariableDensePolynomial(product.getAsList(), self.getVariable(), commonRing.getCoefficientRing())
            else:
                return (self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()\
                        ).toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableDensePolynomial() * other
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() * other
        elif other in self.getCoefficientRing():
            product = [c * other for c in self.coefficient]
            commonRing = self.getCoefficientRing()
            return OneVariableDensePolynomial(product, self.getVariable(), commonRing).adjust()
        elif isinstance(other, (int,long)):
            return rational.Integer(other).actAdditive(self)
        else:
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self) * commonSuperring.createElement(other)

    __rmul__ = __mul__

    def __pow__(self, other, mod = None):
        if not isinstance(other, (int,long)):
            raise TypeError, "You must input an integer for index."
        if other == 0:
            return 1
        if other < 0:
            raise NotImplementedError
        if mod == None:
            index = other
            power_product = OneVariableDensePolynomial([1], self.getVariable(), self.getCoefficientRing())
            power_of_2 = OneVariableDensePolynomial(self.coefficient.getAsList(), self.getVariable(), self.getCoefficientRing())
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                power_of_2 = power_of_2 * power_of_2
                index = index // 2
            return power_product.adjust()
        else:
            index = other
            power_product = OneVariableDensePolynomial([1], self.getVariable(), self.getCoefficientRing())
            power_of_2 = OneVariableDensePolynomial(self.coefficient.getAsList(), self.getVariable(), self.getCoefficientRing())
            while index > 0:
                if index % 2 == 1:
                    power_product *= power_of_2
                    power_product %= mod
                power_of_2 = (power_of_2 * power_of_2) % mod
                index = index // 2
            return power_product.adjust()

    def __divmod__(self, other):
        if other == 0:
            raise ZeroDivisionError, "division or modulo by zero."
        if isinstance(other, OneVariableDensePolynomial):
            if other.degree() < 0:
                raise ZeroDivisionError, "division or modulo by zero."
            if other.degree() == 0:
                other = other[0]
                if self.getCoefficientRing().isfield() or isinstance(other, ring.FieldElement):
                    div_coeff = [c / other for c in self.coefficient]
                    return OneVariableDensePolynomial(div_coeff, self.getVariable(), self.getCoefficientRing()), OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())
                else:
                    div_coeff = [c // other for c in self.coefficient]
                    mod_coeff = [c %  other for c in self.coefficient]
                    return OneVariableDensePolynomial(div_coeff, self.getVariable(), self.getCoefficientRing()), OneVariableDensePolynomial(mod_coeff, self.getVariable(), self.getCoefficientRing())
            elif self.getVariable() != other.getVariable() or self.degree() < other.degree():
                return  OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing()), self.adjust()
            elif isinstance(self.getCoefficientRing(), ring.Field):
                div_poly = OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())
                mod_poly = self
                deg, o_deg = mod_poly.degree(), other.degree()
                o_lc = other[o_deg]
                while deg >= o_deg:
                    div_poly[deg - o_deg] = mod_poly[deg] / o_lc
                    mod_poly = mod_poly - OneVariableDensePolynomial([0] * (deg - o_deg) + ((mod_poly[deg] / o_lc) * other).coefficient.getAsList(), self.getVariable(), self.getCoefficientRing())
                    deg = mod_poly.degree()
                return div_poly.adjust(), mod_poly
            else:
                div_poly = OneVariableDensePolynomial([], self.getVariable(), self.getCoefficientRing())
                mod_poly = self
                deg, o_deg = mod_poly.degree(), other.degree()
                o_lc = other[o_deg]
                x = OneVariableDensePolynomial([0, 1], self.getVariable(), self.getCoefficientRing())
                while deg >= o_deg:
                    div_poly[deg - o_deg] = mod_poly[deg] // o_lc
                    mod_poly = mod_poly - (mod_poly[deg] // o_lc) * other * x**(deg - o_deg)
                    deg -= 1
                    while deg >= 0 and not mod_poly[deg]:
                        deg -= 1
                return div_poly.adjust(), mod_poly
        elif isinstance(other, OneVariableSparsePolynomial):
            return divmod(self, other.toOneVariableDensePolynomial())
        elif isinstance(other, (int,long)):
            other = rational.Integer(other)
        commonSuperring = self.getRing().getCommonSuperring(other.getRing())
        return commonSuperring.createElement(self).__divmod__(commonSuperring.createElement(other))

    def __floordiv__(self,other):
        return self.__divmod__(other)[0]
    
    def __rfloordiv__(self, other):
        if isinstance(other, MultiVariableDensePolynomial):
            return other.toMultiVariableSparsePolynomial() // self.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return other // self.toMultiVariableSparsePolynomial()
        elif other in self.getCoefficientRing() or other.degree() < self.degree():
            return 0
        else:
            self,other = other,self
            return self//other

    def __truediv__(self,other):
        quot, rem = divmod(self, other)
        if not rem:
            return quot
        elif isinstance(other, (int,long)):
            return self * rational.Rational(1, other)
        else:
            raise NotImplementedError

    __div__=__truediv__

    def __mod__(self, other):
        return self.__divmod__(other)[1]

    __rmod__=__mod__

    def __eq__(self, other):
        if not self and not other:
            True
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial)):
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
        else:
            return NotImplemented

    def __call__(self,other):
        if isinstance(other,str):
            result_coefficient = self.coefficient.getAsList()
            return OneVariableDensePolynomial(result_coefficient, other)
        elif isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial, MultiVariableSparsePolynomial)):
            return_polynomial = 0
            for i in range(len(self.coefficient)):
                return_polynomial += self.coefficient[i] * (other**i)
            return return_polynomial.adjust()
        else:
            return_value = 0
            for i in range(self.degree() + 1):
                return_value = return_value * other + self.coefficient[self.degree()-i]
            return return_value

    def __pos__(self):
        retval = self.adjust()
        if retval.degree() == 0:
            retval = retval[0]
        elif retval.degree() < 0:
            retval = 0
        return retval

    def __nonzero__(self):
        if self.degree() >= 0:
            return True
        else:
            return False

    def __repr__(self):
        self_adjust = self.adjust()
        if not isinstance(self_adjust, OneVariableDensePolynomial):
            return repr(self_adjust)
        return_str = 'OneVariableDensePolynomial(' + repr(self.coefficient) + ', "'
        return_str += repr(self.getVariable()) + '", '
        return_str += repr(self.getCoefficientRing()) + ','
        return_str += ')'
        return return_str

    def __str__(self):
        if self.degree() < 1:
            return str(self[0])
        coeffs = self.coefficient.getAsList()
        termlist = []
        for i in range(self.degree() + 1):
            if self[i]:
                if i == 0:
                    termlist.append("%s" % (str(self[i]), self.getVariable(),))
                elif i == 1:
                    termlist.append("%s * %s" % (str(self[i]), self.getVariable(),))
                else:
                    termlist.append("%s * %s ** %d" % (str(self[i]), self.getVariable(), i))
        return_str = " + ".join(termlist)
        w_sign = re.compile(r"\+ -")
        return_str = w_sign.sub("- ", return_str)
        one_coeff = re.compile("(^| )1 \* ")
        return_str = one_coeff.sub(" ", return_str)
        return return_str

    def adjust(self):
        "Use this method in case of leading term of coefffidcient = 0"
        return OneVariableDensePolynomial(self.coefficient.getAsList(), self.getVariable(), self.getCoefficientRing())

    def differentiate(self, other):
        if isinstance(other, str):
            if self.getVariable() == other:
                if len(self.coefficient) == 1:
                    return 0
                diff = OneVariablePolynomialCoefficients()
                for i in range(self.degree()):
                    diff[i] = (self.coefficient[i+1]) * (i+1)
                return OneVariableDensePolynomial(diff.getAsList(), self.getVariable(), self.getCoefficientRing())
            else:
                return 0
        else:
            raise ValueError, "You must input differentiate(polynomial,string)."

    def integrate(self, other = None, min = None, max = None):
        if min == None and max == None and other != None and isinstance(other, str):
             integrate_coefficient = [0] * ( len(self.coefficient) + 1)
             integrate_variable = other
             if integrate_variable != self.getVariable():
                 return MultiVariableDensePolynomial([0,self],integrate_variable).adjust()
             else:
                 for i in range(len(self.coefficient)):
                     integrate_coefficient[i+1] = self.coefficient[i] * rational.Rational(1,i+1)
                 return OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust()
        elif min != None and max != None and other != None and isinstance(other, str):
             integrate_coefficient = [0] *(  len(self.coefficient) + 1)
             integrate_variable = other
             if integrate_variable != self.getVariable():
                 return self * (max - min)
             else:
                 for i in range(len(self.coefficient)):
                     integrate_coefficient[i+1] = self.coefficient[i] * rational.Rational(1, i+1)
                 return OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust().__call__(max) - OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust().__call__(min)
        else:
            raise ValueErroe, "You must imput integrate(polynomial, variable) or integrate(polynomial, variable, min, max)."

    def toOneVariableDensePolynomial(self):
        return self.adjust()

    def toOneVariableSparsePolynomial(self):
        return OneVariableSparsePolynomial(self.coefficient.getAsDict(), self.getVariableList(), self.getCoefficientRing())

    def toMultiVariableDensePolynomial(self):
        return MultiVariableDensePolynomial(self.coefficient, self.getVariable()).adjust()

    def toMultiVariableSparsePolynomial(self):
        if self.degree() < 1:
            return self[0]
        else:
            return_coefficient = {}
            for i in range(len(self.coefficient)):
                if self.coefficient[i] != 0:
                    return_coefficient[(i,)] = self.coefficient[i]
            return MultiVariableSparsePolynomial(return_coefficient, self.getVariableList())

    def getRing(self):
        return self.ring

    def getCoefficientRing(self):
        return self.coeffcientRing

    def initRing(self):
        myRing = None
        for c in self.coefficient:
            if isinstance(c, (int,long)):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not myRing or myRing != cring and myRing.issubring(cring):
                myRing = cring
            elif not cring.issubring(myRing):
                myRing = myRing * cring
        return myRing, PolynomialRing(myRing, self.getVariable())

    def degree(self):
        for i in range(len(self.coefficient)-1, -1, -1):
            if self[i] != 0:
                return i
        return -1

    def content(self):
        """

        Return content of the polynomial.

        """
        coefring = self.getCoefficientRing()
        if coefring.isfield():
            if isinstance(coefring, ring.QuotientField):
                num, den = 0, 1
                for c in self.coefficient:
                    num = c.numerator.getRing().gcd(num, c.numerator)
                    den = c.denominator.getRing().lcm(den, c.denominator)
                return coefring.createElement(num,den)
            else:
                raise NotImplementedError
        else:
            cont = 0
            for c in self.coefficient:
                cont = coefring.gcd(cont, c)
            return cont

    def primitivePart(self):
        """

        Return the primitive part of the polynomial.

        """
        return self / self.content()

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
            return {1: OneVariableDensePolynomial(self.coefficient, self.getVariable())}
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
        # except char > 0 case, result is the answer.
        return result

    def getVariable(self):
        return self.variable

    def getVariableList(self):
        return [self.variable]

class OneVariableSparsePolynomial:

    def __init__(self, coefficient, variable, coeffring=None):
        "OneVariableSparsePolynomial(coefficient, variable)"
        self.coefficient = OneVariablePolynomialCoefficients()
        if not coeffring:
            for i,c in coefficient.iteritems():
                if c:
                    if isinstance(i, tuple):
                        key = i[0]
                    else:
                        key = i
                    self.coefficient[key] = c
            self.variable = variable
            self.ring, self.coefficientRing = self.initRing()
        else:
            self.variable = variable
            self.coefficientRing = coeffring
            self.ring = PolynomialRing(coeffring, self.variable)
            for i, c in coefficient.iteritems():
                self.coefficient[i] = coeffring.createElement(c)

    def __setitem__(self, index, value):
        """

        aOneVariableSparsePolynomial[n] = val
        sets val to the coefficient at degree n.  val must be in the
        coefficient ring of aOneVariableSparsePolynomial.

        TypeError will be raised if n is not an integer, or if val is
        not in the coefficient ring.
        ValueError will be raised if n is negative.

        """
        if value in self.ring.getCoefficientRing():
            if index >= 0:
                self.coefficient[index] = value
            else:
                raise ValueError, "You must input non-negative integer for index."
        else:
            raise TypeError, "You must input an element of the coefficient ring for value."

    def __getitem__(self, index):
        """

        aOneVariableSparsePolynomial[n]
        returns the coefficient at degree n.

        TypeError will be raised if n is not an integer.
        ValueError will be raised if n is negative.

        """
        if isinstance(index, (int,long)) and index >= 0:
            return self.coefficient[index]
        else:
            raise ValueError, "You must input non-negative integer for index."

    def __add__(self, other):
        if isinstance(other, OneVariableDensePolynomial):
            return self + other.toOneVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() + other
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.getVariable() == other.getVariable():
                return_coefficient = OneVariablePolynomialCoefficients()
                for i,c in self.coefficient.iteritems():
                    return_coefficient[i] = c
                for i,c in other.coefficient.iteritems():
                    return_coefficient[i] = return_coefficient[i] + c
                return OneVariableSparsePolynomial(return_coefficient.getAsDict(), self.getVariableList(), self.getCoefficientRing())
            else:
                return self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
        elif other:
            #in self.getCoefficientRing():
            return_coefficient = OneVariablePolynomialCoefficients()
            return_variable = self.getVariableList()
            for i,c in self.coefficient.iteritems():
                return_coefficient[i] = c
            return_coefficient[0] = return_coefficient[0] + other
            return OneVariableSparsePolynomial(return_coefficient.getAsDict(), return_variable, self.getCoefficientRing())
        else:
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self) + commonSuperring.createElement(other)

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        reciprocal = {}
        for i, c in self.coefficient.iteritems():
            reciprocal[i] = -c
        return OneVariableSparsePolynomial(reciprocal, self.getVariableList(), self.getCoefficientRing())

    def __mul__(self, other):
        if isinstance(other, OneVariableDensePolynomial):
            return self * other.toOneVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() * other
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.getVariable() != other.getVariable():
                return self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
            else:
                return_coefficient = OneVariablePolynomialCoefficients()
                return_variable = self.getVariableList()
                for i,c in self.coefficient.iteritems():
                    for j,d in other.coefficient.iteritems():
                        return_coefficient[i + j] = return_coefficient[i + j] + c * d
                return OneVariableSparsePolynomial(return_coefficient.getAsDict(), return_variable)
        elif other in self.ring.getCoefficientRing():
            return_coefficient = {}
            return_variable = self.getVariableList()
            for i,c in self.coefficient.iteritems():
                return_coefficient[i] = c * other
            if isinstance(other, (int,long)):
                other_ring = rational.theIntegerRing
            else:
                other_ring = other.getRing()
            commonRing = self.getRing().getCommonSuperring(other_ring)
            if not commonRing and self.getCoefficientRing():
                return OneVariableSparsePolynomial(product.getAsList(), self.getVariable(), self.getCoefficientRing())
            return OneVariableSparsePolynomial(return_coefficient, return_variable, commonRing.getCoefficientRing())
        else:
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self) * commonSuperring.createElement(other)

    __rmul__=__mul__

    def __pow__(self, index, mod = None):
        if isinstance(index, (int,long)):
            if mod == None:
                if index == 0:
                    return 1
                elif index > 0:
                    index_2 = index
                    return_polynomial = OneVariableSparsePolynomial({(0,):1}, self.getVariableList())
                    power_of_2 = OneVariableSparsePolynomial(self.coefficient.getAsDict(), self.getVariableList())
                    while index_2 > 0:
                        if index_2 % 2 == 1:
                            return_polynomial *= power_of_2
                        power_of_2 = power_of_2 * power_of_2
                        index_2 = index_2 // 2
                    return return_polynomial.adjust()
            else:
                if index == 0:
                    return 1 % mod
                elif index > 0:
                    index_2 = index
                    return_polynomial = OneVariableSparsePolynomial({(0,):1}, self.getVariableList())
                    power_of_2 = OneVariableSparsePolynomial(self.coefficient.getAsDict(), self.getVariableList())
                    while index_2 > 0:
                        if index_2 % 2 == 1:
                            return_polynomial *= power_of_2
                            return_polynomial %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return return_polynomial.adjust()
        raise ValueError, "You must input non-negative integer for index."

    def __floordiv__(self, other):
        if not other:
            raise ZeroDivisionError, "integer division or modulo by zero."
        elif isinstance(other, OneVariableDensePolynomial):
            if self.getVariable() == other.getVariable():
                return self.toOneVariableDensePolynomial() // other
            else:
                return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.getVariable() == other.getVariable():
                return self.toOneVariableDensePolynomial() // other.toOneVariableDensePolynomial()
            else:
                return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        elif other in self.getCoefficientRing():
            return_coefficient = {}
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] // other
            return OneVariableSparsePolynomial(return_coefficient, self.getVariableList(), self.getCoefficientRing()).adjust()
        else:
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self) // commonSuperring.createElement(other)

    def __rfloordiv__(self, other):
        if isinstance(other, MultiVariableDensePolynomial):
            return other.toMultiVariableSparsePolynomial() // self.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return other.toMultiVariableSparsePolynomial() // self.toMultiVariableSparsePolynomial()
        elif other in self.getRing().getCoefficientRing() or other.degree() < self.degree():
            return 0
        elif self.degree() < 1:
            return other // self[0]
        else:
            raise NotImplementedError

    def __truediv__(self, other):
        return self.toOneVariableDensePolynomial() / other

    __div__ = __truediv__

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
        if isinstance(sub_polynomial, (int,long)) and sub_polynomial == 0:
            return True
        return False

    def __call__(self, other):
        if isinstance(other, str):
            return_coefficient = self.coefficient[:]
            return OneVariableSparsePolynomial(return_coefficient, [other]).adjust()
        elif isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial, MultiVariableSparsePolynomial)):
            return_polynomial = 0
            for i in self.coefficient:
                return_polynomial += self.coefficient[i] * (other**i[0])
            return return_polynomial.adjust()
        else:
            return_value = 0
            for i in self.coefficient:
                return_value += (other**i[0]) * self.coefficient[i]
            return return_value

    def __pos__(self):
        return self.adjust()

    def __nonzero__(self):
        if self.degree() >= 0:
            return True
        else:
            return False

    def __repr__(self):
        if self.degree() < 1:
            return repr(self[0])
        adjust_polynomial = self.adjust()
        return_str = "OneVariableSparsePolynomial(" + repr(adjust_polynomial.coefficient) + ", "
        return_str += repr(adjust_polynomial.variable) + ")"
        return return_str

    def __str__(self):
        return str(self.toOneVariableDensePolynomial())

    def adjust(self):
        return OneVariableSparsePolynomial(self.coefficient.getAsDict(), self.getVariableList(), self.getCoefficientRing())

    def differentiate(self, var):
        if isinstance(var, str):
            if self.degree() < 1 or var not in self.getVariableList():
                return 0
            else:
                origin_polynomial = self.adjust()
                return_variable = self.getVariableList()
                return_coefficient = {}
                for i in origin_polynomial.coefficient:
                    if i[0] != 0:
                        return_coefficient[(i[0] - 1,)] = origin_polynomial.coefficient[i] * i[0]
                return OneVariableSparsePolynomial(return_coefficient, return_variable)
        else:
            raise ValueError, "You must input variable for var."

    def integrate(self, other=None, min=None, max=None):
        if min == None and max == None and other != None and isinstance(other, str):
            if self.degree() < 1:
                return OneVariableSparsePolynomial({(1,):self[0]}, [other])
            adjust_polynomial = self.adjust()
            if adjust_polynomial.getVariable() == other:
                return_coefficient = {}
                return_variable = adjust_polynomial.getVariableList()
                for i in adjust_polynomial.coefficient:
                    return_coefficient[(i[0]+1,)] = adjust_polynomial.coefficient[i] * rational.Rational(1,i[0]+1)
                return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
            else:
                other_polynomial = OneVariableSparsePolynomial({(1,):1}, [other])
                return self * other_polynomial
        elif min != None and max != None and isinstance(other, str):
            if self.degree() < 1:
                other_polynomial = OneVariableSparsePolynomial({(1,):self[0]}, [other])
                return other_polynomial(max) - other_polynomial(min)
            adjust_polynomial = self.adjust()
            if adjust_polynomial.getVariable() == other:
                return_coefficient = {}
                return_variable = adjust_polynomial.getVariableList()
                for i in adjust_polynomial.coefficient:
                    return_coefficient[(i[0]+1,)] = adjust_polynomial.coefficient[i] * rational.Rational(1, i[0]+1)
                return_polynomial = OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
                return return_polynomial(max) - return_polynomial(min)
            else:
                other_polynomial = OneVariableSparsePolynomial({(1,):1}, [other])
                return self * (other_polynomial(max) - other_polynomial(min))
        else:
            raise ValueError, "You must input integrate(polynomial, variable (, min, max))."

    def toOneVariableDensePolynomial(self):
        retval = OneVariablePolynomialCoefficients()
        for i,c in self.coefficient.iteritems():
            if c:
                retval[i] = c
        return OneVariableDensePolynomial(retval.getAsList(), self.getVariable(), self.getRing().getCoefficientRing())

    def toOneVariableSparsePolynomial(self):
        return +self

    def toMultiVariableDensePolynomial(self):
        if self.degree() < 1:
            return self[0]
        else:
            origin_polynomial = self.adjust()
            return_variable = self.getVariable()
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                return_coefficient[i[0]] += origin_polynomial.coefficient[i]
            return MultiVariableDensePolynomial(return_coefficient, return_variable)

    def toMultiVariableSparsePolynomial(self):
        if self.degree() < 1:
            return self[0]
        else:
            return_coefficient = {}
            for i,c in self.coefficient.iteritems():
                if c:
                    return_coefficient[(i,)] = c
            return_variable = self.getVariableList()
            return MultiVariableSparsePolynomial(return_coefficient, return_variable)

    def getRing(self):
        return self.ring

    def getCoefficientRing(self):
        return self.coefficientRing

    def initRing(self):
        ring = None
        for c in self.coefficient.itercoeffs():
            if isinstance(c, (int,long)):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        return PolynomialRing(ring, self.getVariable()), ring

    def content(self):
        """

        Return content of the polynomial.

        """
        coefring = self.getRing().getCoefficientRing()
        if coefring.isfield():
            if isinstance(coefring, ring.QuotientField):
                num, den = 0, 1
                for c in self.coefficient.values():
                    num = c.numerator.getRing().gcd(num, c.numerator)
                    den = c.denominator.getRing().lcm(den, c.denominator)
                return coefring.createElement(num,den)
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

    def degree(self):
        degreelist = [d for d in self.coefficient.iterdegrees()]
        degreelist.sort()
        for d in degreelist[::-1]:
            if self[d] != 0:
                return d
        return -1

    def getVariable(self):
        return self.variable[0]

    def getVariableList(self):
        return self.variable[:]

class MultiVariableDensePolynomial:

    def __init__(self, coefficient, variable):
        "MultiVariableDensePolynomial(coefficient, variable)."
        if isinstance(variable, str) and isinstance(coefficient, list):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError, "You must input (list, string)."

    def __add__(self, other):
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial)):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other
        elif other in self.getRing().getCoefficientRing(self.variable):
            return_coefficient = self.coefficient[:]
            return_coefficient[0] += other
            return_variable = self.variable
            return_polynomial = MultiVariableDensePolynomial(return_coefficient, return_variable)
        else:
            if isinstance(other, (int, long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return_polynomial = commonSuperring.createElement(self) + commonSuperring.createElement(other)
        if isinstance(return_polynomial, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableSparsePolynomial)):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        reciprocal = [-c for c in self.coefficient]
        return MultiVariableDensePolynomial(reciprocal, self.variable)

    def __mul__(self, other):
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial)):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other
        elif other in self.getRing().getCoefficientRing(self.variable):
            return_coefficient = [c * other for c in self.coefficient]
            return_polynomial = MultiVariableDensePolynomial(return_coefficient, self.variable).adjust()
        else:
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return_polynomial = commonSuperring.createElement(self) * commonSuperring.createElement(other)
        if isinstance(return_polynomial, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableSparsePolynomial)):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    __rmul__=__mul__

    def __pow__(self, other, mod = None):
        if other == 0:
            return 1
        if isinstance(other, (int,long)):
            if mod == None:
                if other > 0:
                    index = other
                    power_product = MultiVariableDensePolynomial([1],self.variable)
                    power_of_2 = MultiVariableDensePolynomial(self.coefficient[:],self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                        power_of_2 = power_of_2 * power_of_2
                        index = index // 2
                    return power_product.adjust()
            else:
                if other > 0:
                    index = other
                    power_product = MultiVariableDensePolynomial([1],self.variable)
                    power_of_2 = MultiVariableDensePolynomial(self.coefficient[:],self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                            power_product %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return power_product.adjust()
        raise ValueError, "You must input non-negative integer for index."

    def __floordiv__(self, other):
        return_polynomial = self.toMultiVariableSparsePolynomial() // other
        if isinstance(return_polynomial, (int,long)) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial 
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def __rfloordiv__(self, other):
        return_polynomial = other // self.toMultiVariableSparsePolynomial()
        if isinstance(return_polynomial, (int,long)) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def __truediv__(self, other):
        return_polynomial = self.toMultiVariableSparsePolynomial() / other
        if isinstance(return_polynomial, (int,long)) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    __div__ = __truediv__

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
        if not isinstance(sub_polynomial, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial)) and sub_polynomial == 0:
            return True
        else:
            return False

    def __call__(self, **other):
        return_polynomial = self.toMultiVariableSparsePolynomial().__call__(**other)
        if isinstance(return_polynomial, (OneVariableSparsePolynomial, OneVariableDensePolynomial, MultiVariableSparsePolynomial)):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    def __pos__(self):
        return self.adjust()

    def __repr__(self):
        self_adjust = self.adjust()
        if not isinstance(self_adjust, MultiVariableDensePolynomial):
            return repr(self_adjust)
        return_str = 'MultiVariableDensePolynomial(' + repr(self.coefficient) + ', "'
        return_str += self.variable + '")'
        return return_str

    def __str__(self):
        self_adjust = self.adjust()
        if not isinstance(self_adjust, MultiVariableDensePolynomial):
            return str(self)
        else:
            return str(self.toMultiVariableSparsePolynomial())

    def adjust(self):
        return_polynomial = self.toMultiVariableSparsePolynomial().adjust()
        if isinstance(return_polynomial, MultiVariableSparsePolynomial):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    def differentiate(self, other):
        return_polynomial = self.toMultiVariableSparsePolynomial().differentiate(other)
        if isinstance(return_polynomial, MultiVariableSparsePolynomial):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    def integrate(self, other = None, min = None, max = None):
        return_polynomial = self.toMultiVariableSparsePolynomial().integrate(other, min, max)
        if isinstance(return_polynomial, MultiVariableSparsePolynomial):
            return return_polynomial.toMultiVariableDensePolynomial()
        else:
            return return_polynomial

    def toOneVariableDensePolynomial(self):
        adjust_polynomial = self.adjust()
        if not isinstance(adjust_polynomial, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
            return adjust_polynomial
        else:
            for i in adjust_polynomial.coefficient:
                if isinstance(i, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
                    raise ValueError, "You must input one variable polynomial."
            return_coefficient = adjust_polynomial.coefficient[:]
            return_variable = adjust_polynomial.variable
            return OneVariableDensePolynomial(return_coefficient, return_variable)

    def toOneVariableSparsePolynomial(self):
        return self.toOneVariableDensePolynomial().toOneVariableSparsePolynomial()

    def toMultiVariableSparsePolynomial(self):
        length = len(self.coefficient)
        if length == 0:
            return 0
        while (length != 1) and (self.coefficient[length-1] == 0):
            length -= 1
        if length == 1:
            return self.coefficient[0]
        self_adjust = self.coefficient[:length]
        for c in self_adjust:
            if isinstance(c, (MultiVariableDensePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
                result_polynomial = MultiVariableSparsePolynomial({}, [self.variable])
                for i, coeff in enumerate(self_adjust):
                    if coeff != 0:
                        try:
                            result_polynomial += coeff.toMultiVariableSparsePolynomial() * OneVariableSparsePolynomial({(i,):1}, [self.variable])
                        except AttributeError:
                            result_polynomial += OneVariableSparsePolynomial({(i,):coeff}, [self.variable])
                return result_polynomial.adjust()
        else:
            baseCoefficientRing = self.getRing().getCoefficientRing(self.getRing().getVars())
            for coeff in self_adjust:
                if coeff not in baseCoefficientRing:
                    raise ValueError, "You must input rightly nested MultiVariableDensePolynomial."
            result_coefficient = {}
            for i in range(len(self_adjust)):
                result_coefficient[(i,)] = self_adjust[i]
            result_polynomial = MultiVariableSparsePolynomial(result_coefficient, [self.variable])
            return result_polynomial.adjust()

    def getRing(self):
        ring = None
        for c in self.coefficient:
            if isinstance(c, (int,long)):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        return PolynomialRing(ring, self.variable)

class MultiVariableSparsePolynomial:

    def __init__(self, coefficient, variable):
        "MultiVariableSparsePolynomial(coefficient, variable)."
        if isinstance(variable, list) and isinstance(coefficient, dict):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError, "You must input MultiVariableSparsePolynomial(dict,list)."

    def __add__(self, other):
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial)):
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
                sum_variable = list(sets.Set(self_adjust.variable).union(sets.Set(other_adjust.variable)))
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

    __radd__=__add__

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
        if isinstance(other, (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial)):
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
                sum_variable = list(sets.Set(self_adjust.variable).union(sets.Set(other_adjust.variable)))
                sum_variable.sort()
                return self_adjust.arrange_variable(sum_variable) * other_adjust.arrange_variable(sum_variable)
        elif other in self.getRing():
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = other * self.coefficient[i]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()

    __rmul__=__mul__

    def __pow__(self, other, mod = None):
        if isinstance(other, (int,long)):
            if mod == None:
                if other == 0:
                    return 1
                elif other > 0:
                    index = other
                    zero_tuple = (0,) * len(self.variable)
                    power_product = MultiVariableSparsePolynomial({zero_tuple:1},self.variable)
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient,self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                        power_of_2 = power_of_2 * power_of_2
                        index = index // 2
                    return power_product.adjust()
            else:
                if other == 0:
                    return 1
                elif other > 0:
                    index = other
                    zero_tuple = (0,) * len(self.variable)
                    power_product = MultiVariableSparsePolynomial({zero_tuple:1},self.variable)
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient,self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                            power_product %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return power_product.adjust()
        raise ValueError, "You must input positive integer for index."

    def __floordiv__(self, other):
        if isinstance(other, (int,long)) or isinstance(other,rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] // other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient, return_variable)
            return return_polynomial.adjust()
        elif isinstance(other,(OneVariableDensePolynomial,OneVariableSparsePolynomial,MultiVariableDensePolynomial)):
            return self // other.toMultiVariableSparsePolynomial()
        elif isinstance(other,MultiVariableSparsePolynomial):
            if self.variable != other.variable:
                self_adjust = self.adjust()
                other_adjust = other.adjust()
                sum_variable = list(sets.Set(self_adjust.variable).union(sets.Set(other_adjust.variable)))
                sum_variable.sort()
                return self_adjust.arrange_variable(sum_variable) //  other_adjust.arrange_variable(sum_variable)
            else:
                typical_term_of_other = other.search_typical_term()
                div_test_flag = self.calc_quotioent_by_monomial(typical_term_of_other)
                if isinstance(div_test_flag, (int,long)) or isinstance(other,rational.Rational):
                    return div_test_flag // typical_term_of_other.coefficient.values()[0]
                else:
                    return_polynomial = 0
                    remainder_coefficient = self.coefficient.copy()
                    remainder_variable = self.variable[:]
                    remainder_polynomial = MultiVariableSparsePolynomial(remainder_coefficient, remainder_variable)
                    quotient_term = remainder_polynomial.calc_quotioent_by_monomial(typical_term_of_other).search_typical_term() // typical_term_of_other.coefficient.values()[0]
                    return_polynomial += quotient_term
                    remainder_polynomial -= quotient_term * other
                    if isinstance(quotient_term,MultiVariableSparsePolynomial):
                        typical_coefficient = quotient_term.coefficient.keys()[0]
                        if isinstance(remainder_polynomial,MultiVariableSparsePolynomial) and typical_coefficient in remainder_polynomial.coefficient:
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
        return_polynomial = MultiVariableSparsePolynomial({typical_coefficient:typical_term_value},self.variable)
        return return_polynomial

    def calc_quotioent_by_monomial(self,other):
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
                    raise ValueError, "You must input a monomial for other."
            else:
                raise ValueError, "You must input two Polynomial that have common kind of variable."
        else:
            raise ValueError, "You must input two MultiVariableSparsePolynomial."

    def __truediv__(self, other):
        if isinstance(other, (int,long)):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                if isinstance(self.coefficient[i], (int,long)):
                    return_coefficient[i] = rational.Rational(self.coefficient[i],other)
                else:
                    return_coefficient[i] = self.coefficient[i] / other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient,return_variable)
            return return_polynomial
        elif isinstance(other,rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] / other
            return_polynomial = MultiVariableSparsePolynomial(return_coefficient,return_variable)
            return return_polynomial
        elif isinstance(other,(OneVariableDensePolynomial,OneVariableSparsePolynomial,MultiVariableDensePolynomial,MultiVariableSparsePolynomial)) and (self % other == 0):
            return self // other
        else:
            return self.getRing().getQuotientField().createElement(self, other)

    __div__=__truediv__

    def __rfloordiv__(self, other):
        if isinstance(other, (int,long)) or isinstance(other,rational.Rational):
            return 0
        elif isinstance(other,(OneVariableDensePolynomial,OneVariableSparsePolynomial,MultiVariableDensePolynomial)):
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
        if not isinstance(sub_polynomial, (MultiVariableSparsePolynomial, MultiVariableDensePolynomial)) and sub_polynomial == 0:
            return True
        return False

    def __call__(self, **other):
        adjust_polynomial = self.adjust()
        if not isinstance(adjust_polynomial, MultiVariableSparsePolynomial):
            return adjust_polynomial(**other)
        substitutions = other
        basecoefficientring = self.getRing().getCoefficientRing(self.getRing().getVars())
        for i in adjust_polynomial.variable:
            if i in substitutions and not isinstance(substitutions[i], str) and substitutions[i] in basecoefficientring:
                variable_position = adjust_polynomial.variable.index(i)
                new_coefficient = {}
                for j in adjust_polynomial.coefficient:
                    new_value = adjust_polynomial.coefficient[j]
                    new_key = list(j)
                    new_key[variable_position] = 0
                    new_value *= substitutions[i]**j[variable_position]
                    new_key = tuple(new_key)
                    if new_key in new_coefficient:
                        new_coefficient[new_key] += new_value
                    else:
                        new_coefficient[new_key] = new_value
                adjust_polynomial.coefficient = new_coefficient
        adjust_polynomial = adjust_polynomial.adjust()
        if adjust_polynomial in basecoefficientring:
            return adjust_polynomial
        variable_to_variable_back_dict = {}
        variable_to_polynomial_back_dict = {}
        new_variable_parameter = 0
        new_variable_parameter_of_polynomial = 0
        new_variable = adjust_polynomial.variable[:]
        for i in adjust_polynomial.variable:
            variable_position = adjust_polynomial.variable.index(i)
            if i in substitutions and isinstance(substitutions[i],str):
                key = '__new_variable__' + str(new_variable_parameter)
                variable_to_variable_back_dict[key] = substitutions[i]
                new_variable[variable_position] = key
                new_variable_parameter += 1
            elif i in substitutions and isinstance(substitutions[i], (OneVariableDensePolynomial, OneVariableSparsePolynomial, MultiVariableDensePolynomial ,MultiVariableSparsePolynomial)):
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
            return repr(self)
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
                else:
                    return_str += ' - '
                    if (reverse_polynomial.coefficient[result_coefficient[i]] != -1) or (result_coefficient[i] == test_key):
                        return_str += str(abs(reverse_polynomial.coefficient[result_coefficient[i]]))
                index_total = 0
                for k in range(len(result_coefficient[i])):
                    index_total += result_coefficient[i][k]
                for j in range(len(result_coefficient[i])):
                    if result_coefficient[i][- 1 - j] == 1:
                        return_str += old_variable[j]
                    elif result_coefficient[i][- 1 - j] > 1:
                        if result_coefficient[i][- 1 - j] != index_total:
                            return_str += '('
                        return_str += old_variable[j]
                        return_str += '**'
                        return_str += str(result_coefficient[i][- 1 - j])
                        if result_coefficient[i][- 1 - j] != index_total:
                            return_str += ')'
            if return_str[1] != '+':
                return return_str[1:]
            else:
                return return_str[3:]

    def arrange_variable(self, other):
        if not isinstance(other, list):
            raise ValueError, "You must input list for other."
        else:
            result_polynomial = MultiVariableSparsePolynomial({},other)
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
        if (len(self.variable) == 0) or (len(self.coefficient.keys()) == 0):
            return 0
        result_polynomial = self.sort_variable()
        result_polynomial = result_polynomial.merge_variable()
        result_polynomial = result_polynomial.delete_zero_value()
        result_polynomial = result_polynomial.delete_zero_variable()
        result_coefficient = result_polynomial.coefficient
        if len(result_coefficient) == 0:
            return 0
        zero_test = (0,)*len(result_polynomial.variable)
        if (len(result_coefficient) == 1) and (zero_test in result_coefficient):
            return result_coefficient[zero_test]
        return result_polynomial

    def sort_variable(self):
        positions = {}
        for i in range(len(self.variable)):
            if self.variable[i] in positions:
                positions[self.variable[i]] = tuple(list(positions[self.variable[i]]) + [i])
            else:
                positions[self.variable[i]] = (i,)
        result_variable = self.variable[:]
        result_polynomial = MultiVariableSparsePolynomial({},result_variable)
        result_polynomial.variable.sort()
        for i in self.coefficient.keys():
            new_index_list = []
            old_index_list = list(i)
            old_position_keys = positions.copy()
            for j in range(len(old_index_list)):
                if len(positions[result_polynomial.variable[j]]) == 1:
                    new_index_list += [old_index_list[positions[result_polynomial.variable[j]][0]]]
                else:
                    new_index_list += [old_index_list[positions[result_polynomial.variable[j]][0]]]
                    old_position_key = list(positions[result_polynomial.variable[j]])
                    del(old_position_key[0])
                    new_position_key = tuple(old_position_key)
                    positions[result_polynomial.variable[j]] = new_position_key
            if tuple(new_index_list) in result_polynomial.coefficient:
                result_polynomial.coefficient[tuple(new_index_list)] += self.coefficient[i]
            else:
                result_polynomial.coefficient[tuple(new_index_list)] = self.coefficient[i]
            for l in old_position_keys:
                positions[l] = old_position_keys[l]
        return result_polynomial

    def merge_variable(self):
        old_variable_list = self.variable
        merge_variable = [old_variable_list[0]]
        for i in range(len(old_variable_list) - 1):
            if old_variable_list[i+1] != old_variable_list[i]:
                merge_variable += [old_variable_list[i+1]]
        variable_position = {}
        for i in range(len(merge_variable)):
            position_list = []
            for j in range(len(old_variable_list)):
                if old_variable_list[j] == merge_variable[i]:
                    position_list += [j]
            variable_position[merge_variable[i]] = position_list
        result_polynomial = MultiVariableSparsePolynomial({},merge_variable)
        old_coefficient_keys = self.coefficient.keys()
        old_coefficient_values = self.coefficient.values()
        for i in range(len(old_coefficient_keys)):
            new_coefficient_key = []
            for j in merge_variable:
                new_value = 0
                for k in variable_position[j]:
                    new_value += old_coefficient_keys[i][k]
                new_coefficient_key += [new_value]
            if tuple(new_coefficient_key) in result_polynomial.coefficient:
                result_polynomial.coefficient[tuple(new_coefficient_key)] += old_coefficient_values[i]
            else:
                result_polynomial.coefficient[tuple(new_coefficient_key)] = old_coefficient_values[i]
        return result_polynomial

    def delete_zero_value(self):
        result_coefficient = {}
        for i in self.coefficient:
            if self.coefficient[i] != 0:
                result_coefficient[i] = self.coefficient[i]
        result_polynomial = MultiVariableSparsePolynomial(result_coefficient, self.variable)
        return result_polynomial

    def delete_zero_variable(self):
        old_coefficient_keys = self.coefficient.keys()
        old_coefficient_values = self.coefficient.values()
        old_variable = self.variable
        exist_position_list = []
        for i in range(len(old_variable)):
            for j in range(len(old_coefficient_keys)):
                if old_coefficient_keys[j][i] != 0:
                    exist_position_list += [i]
                    break
        new_variable = [old_variable[position] for position in exist_position_list]
        new_coefficient = {}
        for i in range(len(old_coefficient_keys)):
            new_coefficient_key = []
            for j in exist_position_list:
                new_coefficient_key += [old_coefficient_keys[i][j]]
            new_coefficient[tuple(new_coefficient_key)] = old_coefficient_values[i]
        result_polynomial = MultiVariableSparsePolynomial(new_coefficient, new_variable)
        return result_polynomial

    def differentiate(self, other):
        if isinstance(other, str):
            origin_polynomial = self.adjust()
            if other in origin_polynomial.variable:
                result_variable = origin_polynomial.variable[:]
                variable_position = result_variable.index(other)
                result_coefficient = {}
                for i in origin_polynomial.coefficient:
                    if i[variable_position] > 0:
                        new_coefficient_key = list(i)
                        new_index = new_coefficient_key[variable_position] - 1
                        new_coefficient_value = origin_polynomial.coefficient[i] * (new_index + 1)
                        new_coefficient_key[variable_position] = new_index
                        new_coefficient_key = tuple(new_coefficient_key)
                        result_coefficient[new_coefficient_key] = new_coefficient_value
                result_polynomial = MultiVariableSparsePolynomial(result_coefficient, result_variable)
                return result_polynomial.adjust()
            else:
                return 0
        else:
            raise ValueError, "You input [Polynomial, string]."

    def integrate(self, other = None, min = None, max = None):
        if min == None and max == None and other != None and isinstance(other, str):
            before_polynomial = self.adjust()
            if other in before_polynomial.variable:
                integrate_variable = before_polynomial.variable[:]
                variable_position = integrate_variable.index(other)
                integrate_coefficient = {}
                for i in before_polynomial.coefficient:
                    new_coefficient_key = list(i)
                    new_index = new_coefficient_key[variable_position] + 1
                    new_coefficient_value = before_polynomial.coefficient[i] * rational.Rational(1, new_index)
                    new_coefficient_key[variable_position] = new_index
                    new_coefficient_key = tuple(new_coefficient_key)
                    integrate_coefficient[new_coefficient_key] = new_coefficient_value
                integrate_polynomial = MultiVariableSparsePolynomial(integrate_coefficient, integrate_variable)
                return integrate_polynomial.adjust()
            else:
                return (self * OneVariableDensePolynomial([0,1], other).toMultiVariableSparsePolynomial()).adjust()
        elif min != None and max != None and other != None and isinstance(other, str):
            before_polynomial = self.adjust()
            if other in before_polynomial.variable:
                integrate_variable = before_polynomial.variable[:]
                variable_position = integrate_variable.index(other)
                integrate_coefficient = {}
                for i in before_polynomial.coefficient:
                    new_coefficient_key = list(i)
                    new_index = new_coefficient_key[variable_position] + 1
                    new_coefficient_value = before_polynomial.coefficient[i] * rational.Rational(1, new_index)
                    new_coefficient_key[variable_position] = new_index
                    new_coefficient_key = tuple(new_coefficient_key)
                    integrate_coefficient[new_coefficient_key] = new_coefficient_value
                integrate_polynomial = MultiVariableSparsePolynomial(integrate_coefficient, integrate_variable)
                integrate_dict_max = {}
                integrate_dict_min = {}
                integrate_dict_max[integrate_variable[variable_position]] = max
                integrate_dict_min[integrate_variable[variable_position]] = min
                return integrate_polynomial.__call__(**integrate_dict_max) - integrate_polynomial.__call__(**integrate_dict_min)
                return 0
            else:
                return self * (OneVariableDensePolynomial([0,1],other).__call__(max) - OneVariableSparsePolynomial([0,1],other).__call__(min))
        else:
            raise ValueError, "You must input integrate(polynomial,variable) or integrate(polynomial,variable,min,max)."

    def toOneVariableDensePolynomial(self):
        origin_polynomial = self.adjust()
        if not isinstance(origin_polynomial, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
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
            raise ValueError, "You must input OneVariablePolynomial."

    def toOneVariableSparsePolynomial(self):
        origin_polynomial = self.adjust()
        if not isinstance(origin_polynomial, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
            return origin_polynomial
        elif len(origin_polynomial.variable) == 1:
            return_coefficient = {}
            return_variable = origin_polynomial.variable[:]
            return_coefficient.update(origin_polynomial.coefficient)
            return OneVariableSparsePolynomial(return_coefficient, return_variable)
        else:
            raise ValueError, "You must input OneVariablePolynomial."

    def toMultiVariableDensePolynomial(self):
        origin_polynomial = self.adjust()
        if not isinstance(origin_polynomial, (MultiVariableDensePolynomial, MultiVariableSparsePolynomial, OneVariableDensePolynomial, OneVariableSparsePolynomial)):
            return origin_polynomial
        elif len(origin_polynomial.variable) == 1:
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                return_coefficient[i[0]] += origin_polynomial.coefficient[i]
            return MultiVariableDensePolynomial(return_coefficient, origin_polynomial.variable[0])
        else:
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[-1] > max_index:
                    max_index = i[-1]
            return_polynomial = MultiVariableDensePolynomial([0]*(max_index+1), origin_polynomial.variable[-1])
            sum_polynomial_list = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                for j in range(max_index+1):
                    if i[-1] == j:
                        new_key = list(i)
                        del(new_key[-1])
                        new_key = tuple(new_key)
                        new_value = origin_polynomial.coefficient[i]
                        new_coefficient = {}
                        new_coefficient[new_key] = new_value
                        new_polynomial = MultiVariableSparsePolynomial(new_coefficient, origin_polynomial.variable[:-1])
                        sum_polynomial_list[j] += new_polynomial
            for i in range(max_index+1):
                if isinstance(sum_polynomial_list[i], MultiVariableSparsePolynomial) or isinstance(sum_polynomial_list[i], OneVariableSparsePolynomial):
                    return_polynomial.coefficient[i] = sum_polynomial_list[i].toMultiVariableDensePolynomial()
                else:
                    return_polynomial.coefficient[i] = sum_polynomial_list[i]
            return return_polynomial

    def getRing(self):
        ring = None
        for c in self.coefficient.values():
            if isinstance(c, (int,long)):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        if not ring:
            return rational.theIntegerRing
        return PolynomialRing(ring, self.variable)


class PolynomialRing (ring.CommutativeRing):
    """

    The class of polynomial ring.

    """
    def __init__(self, aRing, vars):
        if isinstance(vars, str):
            self.vars = sets.Set((vars,))
        else:
            self.vars = sets.Set(vars)
        self.properties = ring.CommutativeRingProperties()
        if not isinstance(aRing, ring.Ring):
            raise TypeError, '%s should not be passed as ring' % aRing.__class__
        self.coefficientRing = aRing
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
            vars = sets.Set()
        elif isinstance(var, str):
            vars = sets.Set((var,))
        else:
            vars = sets.Set(var)
        vars &= self.vars
        varsInRing = self.vars - vars
        if vars and varsInRing:
            return PolynomialRing(self.coefficientRing, varsInRing)
        elif vars:
            return self.coefficientRing
        elif varsInRing:
            if len(varsInRing) == 1:
                return self.coefficientRing
            raise TypeError, "The meaning of `coefficient ring' is ambiguous."
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
            return RationalFunctionField(coefficientField, self.vars)
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

    def __str__(self):
        retval = str(self.coefficientRing)
        retval += "["
        for v in self.vars:
            retval += str(v) + ", "
        retval = retval[:-2] + "]"
        return retval

    def __contains__(self, element):
        """

        `in' operator is provided for checking the element be in the
        ring.

        """
        try:
            ring = element.getRing()
            if ring.issubring(self):
                return True
            return False
        except AttributeError:
            if isinstance(element, (int,long)):
                return rational.theIntegerRing.issubring(self)

    def issubring(self, other):
        """

        reports whether another ring contains this polynomial ring.

        """
        if isinstance(other, PolynomialRing):
            if self.coefficientRing.issubring(other.getCoefficientRing(other.getVars())) and \
                   self.vars.issubset(other.getVars()):
                return True
            else:
                return False
        elif isinstance(other, RationalFunctionField):
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
        PolynomialRing(Q, sets.Set(["x","y"])).

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
        if not isinstance(seed, (int, long)) and seed.getRing() == self:
            return +seed
        if len(self.vars) == 1:
            variable = [v for v in self.vars][0]
            if seed in self.coefficientRing:
                return OneVariableDensePolynomial([self.coefficientRing.createElement(seed)], variable)
            if isinstance(seed, OneVariableSparsePolynomial):
                seed = seed.toOneVariableDensePolynomial()
            if isinstance(seed, OneVariableDensePolynomial):
                return OneVariableDensePolynomial([self.coefficientRing.createElement(c) for c in seed.coefficient], variable)
            raise TypeError, "larger ring element cannot be a seed."
        else:
            if seed in self.coefficientRing:
                return MultiVariableSparsePolynomial({tuple([0]*len(self.vars)): self.coefficientRing.createElement(seed)}, list(self.vars))
            listvars = list(self.vars)
            if isinstance(seed, OneVariableSparsePolynomial):
                seed = seed.toOneVariableDensePolynomial()
            if isinstance(seed, OneVariableDensePolynomial):
                position = listvars.index(seed.variable)
                new_coef = {}
                for i,c in enumerate(seed.coefficient):
                    index = [0]*len(listvars)
                    index[position] = i
                    new_coef[tuple(index)] = self.coefficientRing.createElement(c)
                return MultiVariableSparsePolynomial(new_coef, listvars)
        # seed cannot be a multi-variable polynomial now
        raise NotImplementedError

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
            return subResultantGCD(a,b)
        else:
            raise NotImplementedError

def construct(polynomial, kwd={}):
    """

    construct compiles a string to a polynomial.  The first argument
    should be a valid python code string representing a polynomial.
    The second optional argument is a dictionary which maps names to
    their values.

    """
    id = re.compile("[A-Za-z_][A-Za-z0-9_]*")
    start = 0
    while 1:
        m = id.search(polynomial[start:])
        if m:
            v = m.group()
            if v not in kwd:
                kwd[v] = OneVariableDensePolynomial([0,rational.Integer(1)], v)
            start += m.end()
        else:
            break
    r = eval(polynomial, kwd)
    return r

import matrix

def resultant(f, g):
    """

    returns the resultant of 2 polynomials.

    """
    m = f.degree()
    n = g.degree()
    M = matrix.Matrix(m+n, m+n)

    # set upper half
    for i in range(n):
        for j in range(m+1):
            M.compo[i][i+j] = f[j]
    # set lower half
    for i in range(m):
        for j in range(n+1):
            M.compo[n+i][i+j] = g[j]

    return M.determinant()

import copy

# Algorithm 3.1.2 of Cohen's book
def pseudoDivision(A, B):
    """

    pseudoDivision(A, B) -> (Q, R)

    Q, R are polynomials such that
    d**(deg(A)-deg(B)+1) * A == B * Q + R,
    where d is the leading coefficient of B.

    """
    if isinstance(A, OneVariableDensePolynomial):
        m = A.degree()
    else:
        m = 0
    if isinstance(B, OneVariableDensePolynomial):
        n = B.degree()
        d = B[n]
    else:
        n = 0
        d = B

    # step 1
    R = copy.deepcopy(A)
    Q = OneVariableDensePolynomial([0], A.variable)
    e = m-n+1
    while 1:
        # step 2
        if isinstance(R, OneVariableDensePolynomial):
            degR = R.degree()
        else:
            degR = 0
        if isinstance(B, OneVariableDensePolynomial):
            degB = B.degree()
        else:
            degB = 0

        if degR < degB:
            q = d ** e
            Q = q * Q
            R = q * R
            return (Q,R)
        # step 3
        if isinstance(R, OneVariableDensePolynomial):
            degR = R.degree()
        else:
            degR = 0

        if isinstance(B, OneVariableDensePolynomial):
            degB = B.degree()
        else:
            degB = 0

        if isinstance(R, OneVariableDensePolynomial):
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
        if isinstance(A, OneVariableDensePolynomial):
            degA = A.degree()
        else:
            degA = 0
        if isinstance(B, OneVariableDensePolynomial):
            degB = B.degree()
        else:
            degB = 0
        delta = degA - degB
        Q, R = pseudoDivision(A, B)
        if not R:
            return d * B.primitivePart()
        if isinstance(R, OneVariableDensePolynomial):
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

class RationalOneVariableDensePolynomial (OneVariableDensePolynomial):
    def __divmod__(self, other):

        """
        About this division , we can treat only a map of
                     Q[x] --> Q[x]
        and only one variable polynomial.
        """
        if other == 0:
            raise ZeroDivisionError, "division or modulo by zero."
        elif isinstance(other, OneVariableDensePolynomial):
            if other.degree() < 1:
                coeff=other.coefficient[0]
                new_coeff=[]
                for i in self.coefficient:
                    new=rational.Rational(i,coeff)
                    new_coeff.append(new)
                return OneVariableDensePolynomial(new_coeff,self.variable),0
            if self.variable != other.variable or self.degree() < other.degree():
                return 0,self
            else:
                self_coeff = self.coefficient.getAsList()
                other_coeff = other.coefficient.getAsList()
                max_term_coeff_of_other = other_coeff[-1]
                new_coeff = []
                i=self.degree()
                k=other.degree()
                while i >= k:
                    q=rational.Rational(self_coeff[-1],1)/max_term_coeff_of_other
                    m=1
                    for j in other_coeff:
                        self_coeff[-(k+m)]=self_coeff[-(k+m)]-j*q
                        m=m-1
                    new_coeff.append(q)
                    self_coeff.pop()
                    i=i-1
                new_coeff.reverse()
                return OneVariableDensePolynomial(new_coeff,self.variable),OneVariableDensePolynomial(self_coeff,self.variable)
        elif isinstance(other, OneVariableSparsePolynomial):
            if other.degree() < 1:
                coeff=other.coefficient[0,]
                new_coeff=[]
                for i in self.coefficient:
                    new=rational.Rational(i,coeff)
                    new_coeff.append(new)
                return OneVariableDensePolynomial(new_coeff,self.variable),0
            elif self.variable != other.variable[0] or self.degree() < other.degree():
                return 0 ,self
            else :
                Dense_other=other.toOneVariableDensePolynomial()
                self_coeff=self.coefficient[:]
                other_coeff=Dense_other.coefficient[:]
                max_term_coeff_of_other=other_coeff[-1]
                new_coeff=[]
                i=self.degree()
                k=Dense_other.degree()
                while i >= k:
                    q=rational.Rational(self_coeff[-1],1)/max_term_coeff_of_other
                    m=1
                    for j in other_coeff:
                        self_coeff[-(k+m)]=self_coeff[-(k+m)]-j*q
                        m=m-1
                    new_coeff.append(q)
                    self_coeff.pop()
                    i=i-1
                new_coeff.reverse() 
                return OneVariableDensePolynomial(new_coeff,self.variable),OneVariableDensePolynomial(self_coeff,self.variable)
        
        elif isinstance(other,rational.Rational) or isinstance(other,rational.Integer):
            new_coeff=[]
            for j in self.coefficient: 
                new_coeff.append(rational.Rational(j,1)//other)
            return OneVariableDensePolynomial(new_coeff,self.variable),0

        elif other in self.getCoefficientRing():
            return 0,self

        else:     #???
            if isinstance(other, (int,long)):
                other = rational.Integer(other)
            commonSuperring = self.getRing().getCommonSuperring(other.getRing())
            return commonSuperring.createElement(self).__divmod__(commonSuperring.createElement(other))

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
        self._using = OneVariablePolynomialCoefficients.USING_LIST

    def __getitem__(self, index):
        if not isinstance(index, (int,long)):
            raise TypeError, "index must be an integer."
        if index < 0:
            raise ValueError, "index must be a positive integer."
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            if len(self._list) > index:
                return self._list[index]
            else:
                return 0
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            return self._dict.get(index,0)

    def __setitem__(self, index, value):
        if not isinstance(index, (int,long)):
            raise TypeError, "index must be an integer."
        if index < 0:
            raise ValueError, "index must be a positive integer."
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            if len(self._list) > index:
                self._list[index] = value
            elif value:
                self._list += [0]*(index - len(self._list)) + [value]
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            self._dict[index] = value

    def degree(self):
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            if not self._list:
                return -1
            deg = len(self._list) - 1
            for index in range(deg, -1, -1):
                if not self._list[index]:
                    deg -= 1
                else:
                    break
            return deg
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            if not self._dict:
                return -1
            deg = -1
            for index in self._dict:
                if index > deg and self._dict[index]:
                    deg = index
                    print deg
            return deg

    def getAsList(self):
        return [+self[i] for i in range(self.degree()+1)]

    def getAsDict(self):
        retval = dict()
        for i in range(self.degree()+1):
            if self[i]:
                retval[i] = +self[i]
        return retval

    def setList(self, aList):
        self._using = OneVariablePolynomialCoefficients.USING_LIST
        self._list = aList

    def setDict(self, aDict):
        self._using = OneVariablePolynomialCoefficients.USING_DICT
        self._dict = aDict

    def changeRepresentation(self, rep):
        """

        Change inner representaion.
        This method is destructive.

        """
        if self._using == rep:
            pass
        elif rep == OneVariablePolynomialCoefficients.USING_LIST:
            self._list = self.getAsList()
            self._using = rep
        elif rep == OneVariablePolynomialCoefficients.USING_DICT:
            self._dict = self.getAsDict()
            self._using = rep
        return

    def __iter__(self):
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            return iter(self._list)
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            return iter(self._dict)

    def __len__(self):
        return self.degree() + 1

    def iteritems(self):
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            return iter([(i,c) for i,c in zip(range(len(self._list)), self._list) if c])
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            return self._dict.iteritems()

    def itercoeffs(self):
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            return iter([c for c in self._list if c])
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            return self._dict.itervalues()

    def iterdegrees(self):
        if self._using == OneVariablePolynomialCoefficients.USING_LIST:
            for i,c in zip(range(len(self._list)), self._list):
                if c:
                    yield i
        elif self._using == OneVariablePolynomialCoefficients.USING_DICT:
            for i in self._dict.itervalues():
                yield i
