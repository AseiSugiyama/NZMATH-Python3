"""

Class definitions of polynomials.

"""
import math
import sets
import rational
import ring
from rationalFunction import RationalFunctionField

class OneVariableDensePolynomial:

    def __init__(self, coefficient, variable):
        "OneVariableDensePolynomial(coefficient, variable)"
        if isinstance(variable, str) and isinstance(coefficient, list):
            self.coefficient = coefficient
            self.variable = variable
##             self.ring = self.getRing()
        else:
            raise ValueError, "You must input (list, string)."

    def __setitem__(self, index, value):
        if rational.isIntegerObject(index) and (rational.isIntegerObject(value) or isinstance(value, rational.Rational)):
            if len(self.coefficient) - 1 >= index and index >= 0:
                self.coefficient[index] = value
            elif len(self.coefficient) - 1 < index:
                self.coefficient += [0]*(index - len(self.coefficient)) + [value]
            else:
                raise ValueError, "You must input non-negative integer for index."
        else:
            raise ValueError, "You must input polynomial[index, value]."

    def __getitem__(self, index):
        if rational.isIntegerObject(index):
            if len(self.coefficient) - 1 >= index and index >= 0:
                return self.coefficient[index]
            elif len(self.coefficient) - 1 < index:
                return 0
        else:
            raise ValueError, "You must input non-negative integer for index."

    def __add__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
##         if other in self.ring.getCoefficientRing():
            sum = OneVariableDensePolynomial(self.coefficient[:],self.variable)
            sum.coefficient[0] += other
            return sum.adjust()
        elif isinstance(other, OneVariableSparsePolynomial):
            return self + other.toOneVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableDensePolynomial() + other
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() + other
        elif self.variable == other.variable:
            sum = OneVariableDensePolynomial([0]*max(len(self.coefficient),len(other.coefficient)),self.variable)
            if len(self.coefficient) < len(other.coefficient):
                for i in range(len(other.coefficient)):
                    sum.coefficient[i] = other.coefficient[i]
            else:
                for i in range(len(self.coefficient)):
                    sum.coefficient[i] = self.coefficient[i]
            for i in range(min(len(self.coefficient),len(other.coefficient))):
                sum.coefficient[i] = 0
                sum.coefficient[i] = self.coefficient[i] + other.coefficient[i]
            return sum.adjust()
        else:
            return (self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()).toMultiVariableDensePolynomial()

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        reciprocal = OneVariableDensePolynomial([0]*len(self.coefficient),self.variable)
        for i in range(len(self.coefficient)):
            reciprocal.coefficient[i] -= self.coefficient[i]
        return reciprocal

    def __mul__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            product = OneVariableDensePolynomial([0]*len(self.coefficient),self.variable)
            for i in range(len(self.coefficient)):
                product.coefficient[i] = self.coefficient[i] * other
            return product.adjust()
        elif isinstance(other, OneVariableSparsePolynomial):
            return self * other.toOneVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableDensePolynomial() * other
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() * other
        elif self.variable == other.variable:
            product = OneVariableDensePolynomial([0]*(len(self.coefficient) + len(other.coefficient)), self.variable)
            for l in range(len(self.coefficient)):
                for r in range(len(other.coefficient)):
                    product.coefficient[l + r] += self.coefficient[l] * other.coefficient[r]
            return product.adjust()
        else:
            return (self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()).toMultiVariableDensePolynomial()

    __rmul__ = __mul__

    def __pow__(self, other, mod = None):
        if rational.isIntegerObject(other):
            if mod == None:
                if other == 0:
                    return 1
                elif other > 0:
                    index = other
                    power_product = OneVariableDensePolynomial([1],self.variable)
                    power_of_2 = OneVariableDensePolynomial(self.coefficient[:],self.variable)
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
                    power_product = OneVariableDensePolynomial([1],self.variable)
                    power_of_2 = OneVariableDensePolynomial(self.coefficient[:],self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                            power_product %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return power_product.adjust()
        raise ValueError, "You must input positive integer for index."

    def __rpow__(self, other):
        raise ValueError, "You must input [IntegerPolynomial**index.]"

    def __floordiv__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            if other == 0:
                raise ZeroDivisionError, "integer division or modulo by zero."
            floordiv_coefficient = []
            for i in range(len(self.coefficient)):
#    MATHEMATICA
#                floordiv_coefficient += [(self.coefficient[i] - (self.coefficient[i] % other)) / other]
#    MATHEMATICA
                floordiv_coefficient += [self.coefficient[i] / other]
            floordiv_polynomial = OneVariableDensePolynomial(floordiv_coefficient, self.variable)
            return floordiv_polynomial.adjust()
        elif isinstance(other, OneVariableSparsePolynomial):
            return self // other.toOneVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return (self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()).toMultiVariableDensePolynomial()
        elif isinstance(other, OneVariableDensePolynomial):
            other_adjust = other.adjust()
            if rational.isIntegerObject(other_adjust) or isinstance(other_adjust, rational.Rational):
                return self // other_adjust
            elif other_adjust.integertest():
                self_adjust = self.adjust()
                if isinstance(self_adjust,int) or isinstance(self_adjust,long) or self_adjust.variable != other_adjust.variable:
                    return 0
                else:
                    floordiv_polynomial = 0
                    while isinstance(self_adjust, OneVariableDensePolynomial) and len(self_adjust.coefficient) >= len(other_adjust.coefficient):
                        old_length = len(self_adjust.coefficient)
                        quotient_position = len(self_adjust.coefficient) - len(other_adjust.coefficient)
                        quotient_value = self_adjust.coefficient[-1] // other_adjust.coefficient[-1]
#    MATHEMATICA
#                        if abs((self_adjust.coefficient[-1] % other_adjust.coefficient[-1]) * 2) == abs(other_adjust.coefficient[-1]):
#                            quotient_value = (self_adjust.coefficient[-1] - abs(other_adjust.coefficient[-1] / 2)) / other_adjust.coefficient[-1]
#                        else:
#                            quotient_value =  self_adjust.coefficient[-1]*1.0 / other_adjust.coefficient[-1]
#                            quotient_value = int(quotient_value + 0.5 * abs(quotient_value) / quotient_value)
#    MATHEMATICA
                        quotient_polynomial = OneVariableDensePolynomial([0]*(quotient_position+1), self.variable)
                        quotient_polynomial.coefficient[quotient_position] = quotient_value
                        floordiv_polynomial += quotient_polynomial
                        self_adjust -= other_adjust * quotient_polynomial
                        if isinstance(self_adjust,int) or isinstance(self_adjust,long):
                            return floordiv_polynomial
                        elif len(self_adjust.coefficient) == old_length:
                            new_coefficient = self_adjust.coefficient[:]
                            del(new_coefficient[-1])
                            self_adjust = OneVariableDensePolynomial(new_coefficient,self.variable).adjust()
                    return floordiv_polynomial
            elif other_adjust.rationaltest():
                self_adjust = self.adjust()
                if isinstance(self_adjust,int) or isinstance(self_adjust,long) or isinstance(self_adjust,rational.Rational) or self_adjust.variable != other_adjust.variable :
                    return 0
                else:
                    floordiv_polynomial = 0
                    while isinstance(self_adjust, OneVariableDensePolynomial) and len(self_adjust.coefficient) >= len(other_adjust.coefficient):
                        old_length = len(self_adjust.coefficient)
                        quotient_position = len(self_adjust.coefficient) - len(other_adjust.coefficient)
                        quotient_value = self_adjust.coefficient[-1] / other_adjust.coefficient[-1]
                        quotient_polynomial = OneVariableDensePolynomial([0]*(quotient_position+1), self.variable)
                        quotient_polynomial.coefficient[quotient_position] = quotient_value
                        floordiv_polynomial += quotient_polynomial
                        self_adjust -= other_adjust * quotient_polynomial
                        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust,rational.Rational):
                            return floordiv_polynomial
                        elif len(self_adjust.coefficient) == old_length:
                            new_coefficient = self_adjust.coefficient[:]
                            del(new_coefficient[-1])
                            self_adjust = OneVariableDensePolynomial(new_coefficient,self.variable).adjust()
                    return floordiv_polynomial
        else:
            raise ValueError, "You must input Polynomial or Rational for other."

    def __rfloordiv__(self, other):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return other // self_adjust
        elif rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return 0
        elif isinstande(other, OneVariableSparsePolynomial):
            return other // self_adjust.toOneVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return (other.toMultiVariableSparsePolynomial() // self_adjust.toMultiVariableSparsePolynomial()).toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return other // self_adjust.toMultiVariableSparsePolynomial()
        else:
            raise ValueError, "Not Defined."

    def __div__(self, other):
        if self % other == 0:
            return self // other
        else:
            raise ValueError, "Not Defined."

#    __truediv__=__div__

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
        if (rational.isIntegerObject(sub_polynomial) or isinstance(sub_polynomial,rational.Rational)) and sub_polynomial == 0:
            return 1
        return 0

    def __call__(self,other):
        if isinstance(other,str):
            result_coefficient = self.coefficient[:]
            return OneVariableDensePolynomial(result_coefficient, other).adjust()
        elif rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_value = 0
            for i in range(len(self.coefficient)):
                return_value = return_value * other + self.coefficient[-1-i]
            return return_value
        elif isinstance(other, OneVariableDensePolynomial) or isinstance(other, OneVariableSparsePolynomial) or isinstance(other, MultiVariableDensePolynomial) or isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial = 0
            for i in range(len(self.coefficient)):
                return_polynomial += self.coefficient[i] * (other**i)
            return return_polynomial.adjust()
        else:
            raise ValueError, "You must input Polynomial and [variable or Rational or polynomial]."

    def __pos__(self):
        return self.adjust()

    def __repr__(self):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust ,rational.Rational):
            return repr(self_adjust)
        return_str = 'OneVariableDensePolynomial(' + repr(self.coefficient) + ', "'
        return_str += self.variable + '")'
        return return_str

    def __str__(self):
        self = self.adjust()
        if rational.isIntegerObject(self) or isinstance(self,rational.Rational):
            return str(self)
        return_str = ""
        first = 0
        while self.coefficient[first] == 0:
            first += 1
        if first == 0:
            return_str += str(self.coefficient[0])
        elif self.coefficient[first] == 1:
            return_str += self.variable
            if first != 1:
                return_str += "**"
                return_str += str(first)
        elif self.coefficient[first] == -1:
            return_str += "-"
            return_str += self.variable
            if first != 1:
                return_str += "**"
                return_str += str(first)
        else:
            return_str += str(self.coefficient[first])
            return_str += self.variable
            if first != 1:
                return_str += "**"
                return_str += str(first)
        if first+1 == len(self.coefficient):
            return return_str
        for i in range(first+1,len(self.coefficient)):
            if self.coefficient[i] > 0:
                return_str += " + "
                if self.coefficient[i] != 1:
                    return_str += str(self.coefficient[i])
                return_str += self.variable
                if i != 1:
                    return_str += "**"
                    return_str += str(i)
            elif self.coefficient[i] < 0:
                return_str += " - "
                if self.coefficient[i] != -1:
                    return_str += str(abs(self.coefficient[i]))
                return_str += self.variable
                if i != 1:
                    return_str += "**"
                    return_str += str(i)
        return return_str

    def adjust(self):
        length = len(self.coefficient)
        while (length != 1) and (self.coefficient[length-1] == 0):
            length -= 1
        if length == 1:
            return self.coefficient[0]
        result = OneVariableDensePolynomial(self.coefficient[:length],self.variable)
        return result

    def differentiate(self, other):
        if isinstance(other, str):
            if self.variable == other:
                if len(self.coefficient) == 1:
                    return 0
                diff = OneVariableDensePolynomial([0]*(len(self.coefficient)-1),self.variable)
                for i in range(len(diff.coefficient)):
                    diff.coefficient[i] = (self.coefficient[i+1]) * (i+1)
                return diff.adjust()
            else:
                return 0
        else:
            raise ValueError, "You must input differentiate(polynomial,string)."

    def integrate(self, other = None, min = None, max = None):
        if min == None and max == None and other != None and isinstance(other, str):
             integrate_coefficient = [0] * ( len(self.coefficient) + 1)
             integrate_variable = other
             if integrate_variable != self.variable:
                 return MultiVariableDensePolynomial([0,self],integrate_variable).adjust()
             else:
                 for i in range(len(self.coefficient)):
                     integrate_coefficient[i+1] = self.coefficient[i] * rational.Rational(1,i+1)
                 return OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust()
        elif min != None and max != None and other != None and isinstance(other, str):
             integrate_coefficient = [0] *(  len(self.coefficient) + 1)
             integrate_variable = other
             if integrate_variable != self.variable:
                 return self * (max - min)
             else:
                 for i in range(len(self.coefficient)):
                     integrate_coefficient[i+1] = self.coefficient[i] * rational.Rational(1, i+1)
                 return OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust().__call__(max) - OneVariableDensePolynomial(integrate_coefficient, integrate_variable).adjust().__call__(min)
        else:
            raise ValueErroe, "You must imput integrate(polynomial, variable) or integrate(polynomial, variable, min, max)."

    def toOneVariableSparsePolynomial(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return adjust_polynomial
        else:
            return_coefficient = {}
            for i in range(len(adjust_polynomial.coefficient)):
                if adjust_polynomial.coefficient[i] != 0:
                    key = (i,)
                    value = adjust_polynomial.coefficient[i]
                    return_coefficient[key] = value
            return_variable = [adjust_polynomial.variable]
            return OneVariableSparsePolynomial(return_coefficient, return_variable)

    def toMultiVariableDensePolynomial(self):
        return MultiVariableDensePolynomial(self.coefficient, self.variable).adjust()

    def toMultiVariableSparsePolynomial(self):
        self = self.adjust()
        if rational.isIntegerObject(self) or isinstance(self, rational.Rational):
            return self
        else:
            return_coefficient = {}
            for i in range(len(self.coefficient)):
                if self.coefficient[i] != 0:
                    key = (i,)
                    value = self.coefficient[i]
                    return_coefficient[key] = value
            return_variable = [self.variable]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable)

    def integertest(self):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust):
            return 1
        elif isinstance(self_adjust, rational.Rational):
            return 0
        else:
            for i in range(len(self_adjust.coefficient)):
                if not rational.isIntegerObject(self_adjust.coefficient[i]):
                    return 0
            return 1

    def rationaltest(self):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return 1
        else:
            for i in range(len(self_adjust.coefficient)):
                if not (rational.isIntegerObject(self_adjust.coefficient[i]) or isinstance(self_adjust.coefficient[i], rational.Rational)):
                    return 0
            return 1

    def getRing(self):
        ring = None
        for c in self.coefficient:
            if rational.isIntegerObject(c):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        return PolynomialRing(ring, self.variable)

    def degree(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return 0
        else:
            return len(self.coefficient) - 1

    def content(self):
        """

        Return content of the polynomial.

        """
        coefring = self.getRing().getCoefficientRing()
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

class OneVariableSparsePolynomial:

    def __init__(self, coefficient, variable):
        "OneVariableSparsePolynomial(coefficient, variable)"
        if isinstance(variable, list) and isinstance(coefficient, dict):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError, "You must input (dict, list)."

    def __setitem__(self, index, value):
        if rational.isIntegerObject(index) and (rational.isIntegerObject(value) or isinstance(value, rational.Rational)):
            if index >= 0:
                self.coefficient[(index,)] = value
            else:
                raise ValueError, "You must input non-negative integer for index."
        else:
            raise ValueError, "You must input polynomial[index, value]."

    def __getitem__(self, index):
        if rational.isIntegerObject(index):
            if (index,) in self.coefficient:
                return self.coefficient[(index,)]
            else:
                return 0
        else:
            raise ValueError, "You must input non-negative integer for index."

    def __add__(self, other):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return other + self_adjust
        elif rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_coefficient.update(self.coefficient)
            return_variable = self.variable[:]
            if (0,) in return_coefficient:
                return_coefficient[(0,)] += other
            else:
                return_coefficient[(0,)] = other
            return OneVariableSparsePolynomial(return_coefficient, return_variable)
        elif isinstance(other, OneVariableDensePolynomial):
            return self + other.toOneVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() + other
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.variable == other.variable:
                return_coefficient = self.coefficient.copy()
                return_variable = self.variable[:]
                for i in other.coefficient:
                    if i in return_coefficient:
                        return_coefficient[i] += other.coefficient[i]
                    else:
                        return_coefficient[i] = other.coefficient[i]
                return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
            else:
                return self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return - adjust_polynomial
        else:
            return_coefficient = {}
            return_variable = adjust_polynomial.variable[:]
            for i in adjust_polynomial.coefficient:
                return_coefficient[i] = - adjust_polynomial.coefficient[i]
            return OneVariableSparsePolynomial(return_coefficient, return_variable)

    def __mul__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] * other
            return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            return self * other.toOneVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return self.toMultiVariableSparsePolynomial() * other
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.variable != other.variable:
                return self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
            else:
                return_coefficient = {}
                return_variable = self.variable[:]
                for i in self.coefficient:
                    for j in other.coefficient:
                        if (i[0] + j[0],) in return_coefficient:
                            return_coefficient[(i[0] + j[0],)] += self.coefficient[i] * other.coefficient[j]
                        else:
                            return_coefficient[(i[0] + j[0],)] = self.coefficient[i] * other.coefficient[j]
                return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()

    __rmul__=__mul__

    def __pow__(self, index, mod = None):
        if rational.isIntegerObject(index):
            if mod == None:
                if index == 0:
                    return 1
                elif index > 0:
                    index_2 = index
                    return_polynomial = OneVariableSparsePolynomial({(0,):1}, self.variable)
                    power_of_2_coefficient = {}
                    power_of_2_coefficient.update(self.coefficient)
                    power_of_2 = OneVariableSparsePolynomial(power_of_2_coefficient, self.variable)
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
                    return_polynomial = OneVariableSparsePolynomial({(0,):1}, self.variable)
                    power_of_2_coefficient = {}
                    power_of_2_coefficient.update(self.coefficient)
                    power_of_2 = OneVariableSparsePolynomial(power_of_2_coefficient, self.variable)
                    while index_2 > 0:
                        if index_2 % 2 == 1:
                            return_polynomial *= power_of_2
                            return_polynomial %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return return_polynomial.adjust()
        raise ValueError, "You must input non-negative integer for index."

    def __floordiv__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            if other == 0:
                raise ZeroDivisionError, "integer division or modulo by zero."
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = self.coefficient[i] / other
            return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            if self.variable == other.variable:
                return self.toOneVariableDensePolynomial() // other
            else:
                return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            if self.variable == other.variable:
                return self.toOneVariableDensePolynomial() // other.toOneVariableDensePolynomial()
            else:
                return self.toMultiVariableSparsePolynomial() // other.toMultiVariableSparsePolynomial()
        else:
            raise ValueError, "Not Defined."

    def __rfloordiv__(self, other):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return other // self_adjust
        elif rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return 0
        elif isinstance(other, OneVariableDensePolynomial):
            return other // self_adjust.toOneVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return other.toMultiVariableSparsePolynomial() // self_adjust.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return other.toMultiVariableSparsePolynomial() // self_adjust.toMultiVariableSparsePolynomial()
        else:
            raise ValueError, "Not Defined."

#    def __div__(self, other):

#    def __truediv__=__div__

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
        if rational.isIntegerObject(sub_polynomial) and sub_polynomial == 0:
            return 1
        return 0

    def __call__(self, other):
        if isinstance(other, str):
            return_coefficient = self.coefficient[:]
            return OneVariableSparsePolynomial(return_coefficient, [other]).adjust()
        elif rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_value = 0
            for i in self.coefficient:
                return_value += (other**i[0]) * self.coefficient[i]
            return return_value
        elif isinstance(other,OneVariableDensePolynomial) or isinstance(other, OneVariableSparsePolynomial) or isinstance(other, MultiVariableDensePolynomial) or isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial = 0
            for i in self.coefficient:
                return_polynomial += self.coefficient[i] * (other**i[0])
            return return_polynomial.adjust()
        else:
            raise ValueError, "You must input variable or Rational or Polynomial for other."

    def __pos__(self):
        return self.adjust()

    def __repr__(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return repr(adjust_polynomial)
        return_str = "OneVariableSparsePolynomial(" + repr(adjust_polynomial.coefficient) + ", "
        return_str += repr(adjust_polynomial.variable) + ")"
        return return_str

    def __str__(self):
        disp_polynomial = self.adjust()
        if rational.isIntegerObject(disp_polynomial) or isinstance(disp_polynomial, rational.Rational):
            return str(disp_polynomial)
        else:
            max_index = 0
            for i in disp_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in disp_polynomial.coefficient:
                return_coefficient[i[0]] += disp_polynomial.coefficient[i]
            return str(OneVariableDensePolynomial(return_coefficient, disp_polynomial.variable[0]))

    def adjust(self):
        if len(self.coefficient.keys()) == 0:
            return 0
        return_coefficient = {}
        return_variable = self.variable[:]
        for i in self.coefficient:
            if self.coefficient[i] != 0:
                return_coefficient[i] = self.coefficient[i]
        if len(return_coefficient) == 0:
            return 0
        zero_test = (0,)
        if (len(return_coefficient) == 1) and (zero_test in return_coefficient):
            return return_coefficient[zero_test]
        return OneVariableSparsePolynomial(return_coefficient, return_variable)

    def differentiate(self, other):
        if isinstance(other, str):
            origin_polynomial = self.adjust()
            if isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
                return 0
            if other in origin_polynomial.variable:
                return_variable = origin_polynomial.variable[:]
                return_coefficient = {}
                for i in origin_polynomial.coefficient:
                    if i[0] != 0:
                        return_coefficient[(i[0] - 1,)] = origin_polynomial.coefficient[i] * i[0]
                return OneVariableSparsePolynomial(return_coefficient, return_variable)
            else:
                return 0
        else:
            raise ValueError, "You must input variable for other."

    def integrate(self, other=None, min=None, max=None):
        if min == None and max == None and other != None and isinstance(other, str):
            adjust_polynomial = self.adjust()
            if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
                return OneVariableSparsePolynomial({(1,):1}, [other]) * adjust_polynomial
            elif adjust_polynomial.variable[0] == other:
                return_coefficient = {}
                return_variable = adjust_polynomial.variable[:]
                for i in adjust_polynomial.coefficient:
                    return_coefficient[(i[0]+1,)] = adjust_polynomial.coefficient[i] * rational.Rational(1,i[0]+1)
                return OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
            else:
                other_polynomial = OneVariableSparsePolynomial({(1,):1}, [other])
                return self * other_polynomial
        elif min != None and max != None and isinstance(other, str):
            adjust_polynomial = self.adjust()
            if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
                other_polynomial = OneVariableSparsePolynomial({(1,):1},[other]) * adjust_polynomial
                return other_polynomial.__call__(max) - other_polynomial.__call__(min)
            elif adjust_polynomial.variable[0] == other:
                return_coefficient = {}
                return_variable = adjust_polynomial.variable[:]
                for i in adjust_polynomial.coefficient:
                    return_coefficient[(i[0]+1,)] = adjust_polynomial.coefficient[i] * rational.Rational(1, i[0]+1)
                return_polynomial = OneVariableSparsePolynomial(return_coefficient, return_variable).adjust()
                return return_polynomial.__call__(max) - return_polynomial.__call__(min)
            else:
                other_polynomial = OneVariableSparsePolynomial({(1,):1}, [other])
                return self * (other_polynomial.__call__(max) - other_polynomial.__call__(min))
        else:
            raise ValueError, "You must input integrate(polynomial, variable (, min, max))."

    def toOneVariableDensePolynomial(self):
        origin_polynomial = self.adjust()
        if rational.isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
            return origin_polynomial
        else:
            return_variable = origin_polynomial.variable[0]
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                return_coefficient[i[0]] += origin_polynomial.coefficient[i]
            return OneVariableDensePolynomial(return_coefficient, return_variable)

    def toMultiVariableDensePolynomial(self):
        origin_polynomial = self.adjust()
        if rational.isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
            return origin_polynomial
        else:
            return_variable = origin_polynomial.variable[0]
            max_index = 0
            for i in origin_polynomial.coefficient:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficient = [0]*(max_index + 1)
            for i in origin_polynomial.coefficient:
                return_coefficient[i[0]] += origin_polynomial.coefficient[i]
            return MultiVariableDensePolynomial(return_coefficient, return_variable)

    def toMultiVariableSparsePolynomial(self):
        origin_polynomial = self.adjust()
        if rational.isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
            return origin_polynomial
        else:
            return_coefficient = {}
            return_coefficient.update(self.coefficient)
            return_variable = self.variable[:]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable)

    def getRing(self):
        ring = None
        for c in self.coefficient.values():
            if rational.isIntegerObject(c):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        return PolynomialRing(ring, self.variable[0])

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
            for c in self.coefficient.values():
                cont = coefring.gcd(cont, c)
            return cont

class MultiVariableDensePolynomial:

    def __init__(self, coefficient, variable):
        "MultiVariableDensePolynomial(coefficient, variable)."
        if isinstance(variable, str) and isinstance(coefficient, list):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError, "You must input (list, string)."

    def __add__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_coefficient = self.coefficient[:]
            return_coefficient[0] += other
            return_variable = self.variable
            return MultiVariableDensePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other.toMultiVariableSparsePolynomial()
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial = self.toMultiVariableSparsePolynomial() + other
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        else:
            raise ValueError, "Not Defined."

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return - adjust_polynomial
        else:
            return_coefficient = adjust_polynomial.coefficient[:]
            return_variable = adjust_polynomial.variable
            for i in range(len(return_coefficient)):
                return_coefficient[i] = - return_coefficient[i]
            return MultiVariableDensePolynomial(return_coefficient, return_variable)

    def __mul__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_coefficient = self.coefficient[:]
            return_variable = self.variable
            for i in range(len(return_coefficient)):
                return_coefficient[i] *= other
            return MultiVariableDensePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
            if isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other.toMultiVariableSparsePolynomial()
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        elif isinstance(other, MultiVariableSparsePolynomial):
            return_polynomial =  self.toMultiVariableSparsePolynomial() * other
            if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
                return return_polynomial
            else:
                return return_polynomial.toMultiVariableDensePolynomial()
        else:
            raise ValueError, "Not Defined."

    __rmul__=__mul__

    def __pow__(self, other, mod = None):
        if rational.isIntegerObject(other):
            if mod == None:
                if other == 0:
                    return 1
                elif other > 0:
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
                if other == 0:
                    return 1
                elif other > 0:
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
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial 
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def __rfloordiv__(self, other):
        return_polynomial = other // self.toMultiVariableSparsePolynomial()
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def __div__(self, other):
        return_polynomial = self.toMultiVariableSparsePolynomial() / other
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

#    def __truediv__(self, other):

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
        if (rational.isIntegerObject(sub_polynomial) or isinstance(sub_polynomial, rational.Rational)) and sub_polynomial == 0:
            return 1
        else:
            return 0

    def __call__(self, **other):
        return_polynomial = self.toMultiVariableSparsePolynomial().__call__(**other)
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def __pos__(self):
        return self.adjust()

    def __repr__(self):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust ,rational.Rational):
            return repr(self_adjust)
        return_str = 'MultiVariableDensePolynomial(' + repr(self.coefficient) + ', "'
        return_str += self.variable + '")'
        return return_str

    def __str__(self):
        self_adjust = self.adjust()
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return str(self)
        else:
            return self.toMultiVariableSparsePolynomial().__str__()

    def adjust(self):
        return_polynomial = self.toMultiVariableSparsePolynomial().adjust()
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def differentiate(self, other):
        return_polynomial = self.toMultiVariableSparsePolynomial().differentiate(other)
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def integrate(self, other = None, min = None, max = None):
        return_polynomial = self.toMultiVariableSparsePolynomial().integrate(other, min, max)
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return return_polynomial
        else:
            return return_polynomial.toMultiVariableDensePolynomial()

    def toOneVariableDensePolynomial(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial):
            return adjust_polynomial
        else:
            for i in adjust_polynomial.coefficient:
                if isinstance(i, MultiVariableDensePolynomial):
                    raise ValueError, "You must input OneVariablePolynomial."
            return_coefficient = adjust_polynomial.coefficient[:]
            return_variable = adjust_variable
            return OneVariableDensePolynomial(return_coefficient, return_variable)

    def toOneVariableSparsePolynomial(self):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial):
            return adjust_polynomial
        else:
            for i in adjust_polynomial.coefficient:
                if isinstance(i, MultiVariableDensePolynomial):
                    raise ValueError, "You must input OneVariablePolynomial."
            return_coefficient = adjust_polynomial.coefficient[:]
            return_variable = adjust_variable
            return OneVariableDensePolynomial(return_coefficient, return_variable).toOneVariableSparsePolynomial()

    def toMultiVariableSparsePolynomial(self):
        length = len(self.coefficient)
        while (length != 1) and (self.coefficient[length-1] == 0):
            length -= 1
        if length == 1:
            return self.coefficient[0]
        self_adjust = MultiVariableDensePolynomial(self.coefficient[:length],self.variable)
        if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
            return self_adjust
        else:
            for i in self_adjust.coefficient:
                if isinstance(i,MultiVariableDensePolynomial) or isinstance(i, OneVariableDensePolynomial):
                    result_polynomial = MultiVariableSparsePolynomial({}, [self_adjust.variable])
                    x = OneVariableDensePolynomial([0,1],self_adjust.variable)
                    for i in range(len(self_adjust.coefficient)):
                        coeff = self_adjust.coefficient[i]
                        if rational.isIntegerObject(coeff) or isinstance(coeff, rational.Rational):
                            result_polynomial += coeff * x**i
                        else:
                            result_polynomial += coeff.toMultiVariableSparsePolynomial() * x**i
                    return result_polynomial.adjust()
            else:
                for coeff in self_adjust.coefficient:
                    if not (rational.isIntegerObject(coeff) or isinstance(coeff,rational.Rational)):
                        raise ValueError, "You must input MultiVariableDensePolynomial for self."
                result_coefficient = {}
                for i in range(len(self_adjust.coefficient)):
                    result_coefficient[(i,)] = self_adjust.coefficient[i]
                result_polynomial = MultiVariableSparsePolynomial(result_coefficient, [self_adjust.variable])
                return result_polynomial.adjust()

    def getRing(self):
        ring = None
        for c in self.coefficient:
            if rational.isIntegerObject(c):
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
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            self_adjust = self.adjust()
            if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
                return self_adjust + other
            else:
                return_coefficient = {}
                return_variable = self_adjust.variable[:]
                return_coefficient.update(self_adjust.coefficient)
                zero_key = (0,) * len(return_variable)
                if zero_key in return_coefficient:
                    return_coefficient[zero_key] += other
                else:
                    return_coefficient[zero_key] = other
                return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            return self + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            return self + other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self + other.toMultiVariableSparsePolynomial()
        elif self.variable == other.variable:
            return_coefficient = {}
            return_variable = self.variable[:]
            return_coefficient.update(self.coefficient)
            for i in other.coefficient:
                if i in return_coefficient:
                    return_coefficient[i] += other.coefficient[i]
                else:
                    return_coefficient[i] = other.coefficient[i]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()
        else:
            self_adjust = self.adjust()
            other_adjust = other.adjust()
            if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
                return other_adjust + self_adjust
            elif rational.isIntegerObject(other_adjust):
                return self_adjust + other_adjust
            if self_adjust.variable == other_adjust.variable:
                return self_adjust + other_adjust
            sum_variable = self_adjust.variable[:]
            for i in other_adjust.variable:
                if i not in sum_variable:
                    sum_variable.append(i)
            sum_variable.sort()
            return self_adjust.arrange_variable(sum_variable) + other_adjust.arrange_variable(sum_variable)

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        return_polynomial = self.adjust()
        if rational.isIntegerObject(return_polynomial) or isinstance(return_polynomial, rational.Rational):
            return ( - return_polynomial)
        for i in return_polynomial.coefficient:
            return_polynomial.coefficient[i] = - return_polynomial.coefficient[i]
        return return_polynomial

    def __mul__(self, other):
        if rational.isIntegerObject(other) or isinstance(other, rational.Rational):
            return_coefficient = {}
            return_variable = self.variable[:]
            for i in self.coefficient:
                return_coefficient[i] = other * self.coefficient[i]
            return MultiVariableSparsePolynomial(return_coefficient, return_variable).adjust()
        elif isinstance(other, OneVariableDensePolynomial):
            return self * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, OneVariableSparsePolynomial):
            return self * other.toMultiVariableSparsePolynomial()
        elif isinstance(other, MultiVariableDensePolynomial):
            return self * other.toMultiVariableSparsePolynomial()
        elif self.variable == other.variable:
            result_coefficient = {}
            result_variable = self.variable[:]
##             result_variable = []
##             for i in range(len(self.variable)):
##                 result_variable += self.variable[i]
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
            other_adjust = other.adjust()
            if rational.isIntegerObject(self_adjust) or isinstance(self_adjust, rational.Rational):
                return other_adjust * self_adjust
            elif rational.isIntegerObject(other_adjust):
                return self_adjust * other_adjust
            if self_adjust.variable == other_adjust.variable:
                return self_adjust * other_adjust
            sum_variable = self_adjust.variable[:]
            for i in other_adjust.variable:
                if i not in sum_variable:
                    sum_variable.append(i)
            sum_variable.sort()
            return self_adjust.arrange_variable(sum_variable) * other_adjust.arrange_variable(sum_variable)

    __rmul__=__mul__

    def __pow__(self, other, mod = None):
        if rational.isIntegerObject(other):
            if mod == None:
                if other == 0:
                    return 1
                elif other > 0:
                    index = other
                    power_product = MultiVariableSparsePolynomial([1],self.variable)
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient[:],self.variable)
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
                    power_product = MultiVariableSparsePolynomial([1],self.variable)
                    power_of_2 = MultiVariableSparsePolynomial(self.coefficient[:],self.variable)
                    while index > 0:
                        if index % 2 == 1:
                            power_product *= power_of_2
                            power_product %= mod
                        power_of_2 = (power_of_2 * power_of_2) % mod
                        index = index // 2
                    return power_product.adjust()
        raise ValueError, "You must input positive integer for index."

    def __rpow__(self, other):
        raise ValueError, "Not Defined."

    def __floordiv__(self, other):
# Not Perfect
        raise ValueError, "Not Defined."

    def __div__(self, other):
# Not Perfect
        raise ValueError, "Not Defined."

    __truediv__=__div__

    def __rfloordiv__(self, other):
# Not Perfect
        raise ValueError, "Not Defined."

    def __rdiv__(self, other):
# Not Perfect
        raise ValueError, "Not Defined."

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
        if(rational.isIntegerObject(sub_polynomial) or isinstance(sub_polynomial, rational.Rational)) and sub_polynomial == 0:
            return 1
        return 0

    def __call__(self, **other):
        adjust_polynomial = self.adjust()
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
            return adjust_polynomial
        substitutions = other
        for i in adjust_polynomial.variable:
            if i in substitutions and (rational.isIntegerObject(substitutions[i]) or isinstance(substitutions[i], rational.Rational)):
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
        if rational.isIntegerObject(adjust_polynomial) or isinstance(adjust_polynomial, rational.Rational):
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
            elif i in substitutions and (isinstance(substitutions[i],OneVariableDensePolynomial) or isinstance(substitutions[i],OneVariableSparsePolynomial) or isinstance(substitutions[i],MultiVariableDensePolynomial) or isinstance(substitutions[i],MultiVariableSparsePolynomial)):
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
        if rational.isIntegerObject(self) or isinstance(self, rational.Rational):
            return repr(self)
        return_str = "MultiVariableSparsePolynomial(" + repr(self.coefficient) + ", "
        return_str += repr(self.variable) + ")"
        return return_str

    def __str__(self):
        disp_polynomial = self.adjust()
        if rational.isIntegerObject(disp_polynomial) or isinstance(disp_polynomial,rational.Rational):
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
            index_list = self.coefficient.keys()
            values_list = self.coefficient.values()
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
        if rational.isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
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
        if rational.isINtegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
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
        if rational.isIntegerObject(origin_polynomial) or isinstance(origin_polynomial, rational.Rational):
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
            if rational.isIntegerObject(c):
                cring = rational.theIntegerRing
            else:
                cring = c.getRing()
            if not ring or ring != cring and ring.issubring(cring):
                ring = cring
            elif not cring.issubring(ring):
                ring = ring * cring
        return PolynomialRing(ring, self.variable)

class PolynomialRing (ring.CommutativeRing):
    """

    The class of polynomial ring.

    """
    def __init__(self, aRing, vars):
        self.coefficientRing = aRing
        if isinstance(vars, str):
            self.vars = sets.Set((vars,))
        else:
            self.vars = sets.Set(vars)
        self.properties = ring.CommutativeRingProperties()
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
            if rational.isIntegerObject(element):
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

import re

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
