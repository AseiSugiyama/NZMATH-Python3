#polynomial.py 
import string

class Polynomial:

    def __init__(self, coefficient, variable):
        "Polynomial(coefficient, variable)"
        if isinstance(variable, str) and isinstance(coefficient, list):
            self.coefficient = coefficient
            self.variable = variable
        else:
            raise ValueError, "You must input (list,string)."

    def __add__(self, other):
        if (type(other) == int) or (type(other) == long):
            sum = Polynomial(self.coefficient[:],self.variable)
            sum.coefficient[0] += other
            return Polynomial.adjust(sum) 
        elif isinstance(other, FlatPolynomial):
            return other + self
        elif self.variable == other.variable:
            sum = Polynomial([0]*max(len(self.coefficient),len(other.coefficient)),self.variable)
            if len(self.coefficient) < len(other.coefficient):
                for i in range(len(other.coefficient)):
                    sum.coefficient[i] = other.coefficient[i]
            else:
                for i in range(len(self.coefficient)):
                    sum.coefficient[i] = self.coefficient[i]
            for i in range(min(len(self.coefficient),len(other.coefficient))):
                sum.coefficient[i] = 0
                sum.coefficient[i] = self.coefficient[i] + other.coefficient[i]
            return Polynomial.adjust(sum) 
        else:
            return Polynomial.toFlatPolynomial(self) + Polynomial.toFlatPolynomial(other)

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        if (type(self) == int) or (type(self) == long) :
            return (-self)
        reciprocal = Polynomial([0]*len(self.coefficient),self.variable)
        for i in range(len(self.coefficient)):
            reciprocal.coefficient[i] -= self.coefficient[i]
        return reciprocal

    def __mul__(self, other):
        if (type(other) == int) or (type(other) == long) :
            product = Polynomial([0]*len(self.coefficient),self.variable)
            for i in range(len(self.coefficient)):
                product.coefficient[i] = self.coefficient[i] * other
            return Polynomial.adjust(product)
        elif isinstance(other, FlatPolynomial):
            return other * self
        elif self.variable == other.variable:
            product = Polynomial([0]*(len(self.coefficient) + len(other.coefficient)),self.variable)
            for l in range(len(self.coefficient)):
                for r in range(len(other.coefficient)):
                    product.coefficient[l + r] += self.coefficient[l] * other.coefficient[r]
            return Polynomial.adjust(product)
        else:
            return Polynomial.toFlatPolynomial(self) * Polynomial.toFlatPolynomial(other)

    __rmul__ = __mul__

    def __pow__(self, other):
        if (type(other) == int) or (type(other) == long):
            if other == 0:
                return 1
            elif other > 0:
                power_product = Polynomial([1],self.variable)
                for i in range(other):
                    power_product = Polynomial.__mul__(self, power_product)
                return Polynomial.adjust(power_product)
        raise ValueError, "You must input positive integer for index."

    def __rpow__(self, other):
        raise ValueError, "You must input [Polynomial**index.]" 

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, long):
            if other == 0:
                raise ZeroDivisionError, "integer division or modulo by zero."
            floordiv_coefficient = []
            for i in range(len(self.coefficient)):
#    MATHEMATICA
#                floordiv_coefficient += [(self.coefficient[i] - (self.coefficient[i] % other)) / other]
#    MATHEMATICA
                floordiv_coefficient += [self.coefficient[i] / other]
            floordiv_polynomial = Polynomial(floordiv_coefficient, self.variable)
            return floordiv_polynomial.adjust()
        elif isinstance(other, FlatPolynomial):
            return Polynomial.toFlatPolynomial(self) // other
        elif isinstance(other, Polynomial):
            other_adjust = other.adjust()
            if isinstance(other_adjust,int) or isinstance(other_adjust,long):
                return self // other_adjust
            else:
                self_adjust = self.adjust()
                if isinstance(self_adjust,int) or isinstance(self_adjust,long) or self_adjust.variable != other_adjust.variable:
                    return 0
                else:
                    floordiv_polynomial = 0
                    while isinstance(self_adjust, Polynomial) and len(self_adjust.coefficient) >= len(other_adjust.coefficient):
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
                        quotient_polynomial = Polynomial([0]*(quotient_position+1), self.variable)
                        quotient_polynomial.coefficient[quotient_position] = quotient_value
                        floordiv_polynomial += quotient_polynomial
                        self_adjust -= other_adjust * quotient_polynomial
                        if isinstance(self_adjust,int) or isinstance(self_adjust,long):
                            return floordiv_polynomial
                        elif len(self_adjust.coefficient) == old_length:
                            new_coefficient = self_adjust.coefficient[:]
                            del(new_coefficient[-1])
                            self_adjust = Polynomial(new_coefficient,self.variable).adjust()
                    return floordiv_polynomial
        else:
            raise ValueError, "You must input Polynomial or integer."

    def __rfloordiv__(self, other):
        self_adjust = self.adjust()
        if isinstance(self_adjust,int) or isinstance(self_adjust,long):
            return other // self_adjust
        elif isinstance(other,int) or isinstance(other,long):
            return 0
        elif isinstance(other,FlatPolynomial):
            return other // self_adjust.toFlatPolynomial()
        else:
            raise ValueError, "Not Defined."

#    def __div__(self, other):

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
        if (isinstance(sub_polynomial,int) or isinstance(sub_polynomial,long)) and sub_polynomial == 0:
            return 1
        return 0

    def __call__(self,other):
        if isinstance(other,str):
            result_coefficient = self.coefficient[:]
            return Polynomial(result_coefficient, other).adjust()
        elif isinstance(other, int) or isinstance(other, long):
            return_value = 0
            for i in range(len(self.coefficient)):
                return_value = return_value * other + self.coefficient[-1-i]
            return return_value
        else:
            raise ValueError, "You must input Polynomial and [variable or integer]."

    def __repr__(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) :
            return str(self)
        return_str = ""
        return_str += "Polynomial(" + repr(self.coefficient) + ', "'
        return_str += self.variable
        return_str += '")'
        return return_str  

    def __str__(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) :
            return str(self)
        multi = 0
        for i in self.coefficient:
            if isinstance(i,Polynomial):
                multi = 1
        if multi:
            return self.toFlatPolynomial().__str__()
        else:
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
        result = Polynomial(self.coefficient[:length],self.variable)
        return result

    def differentiate(self, other):
        if type(other) == str:
            multi = 0
            for i in self.coefficient:
                if isinstance(i,Polynomial):
                    multi = 1
            if multi:
                return self.toFlatPolynomial().differentiate(other)
            else:
                if self.variable == other:
                    if len(self.coefficient) == 1:
                        return 0
                    diff = Polynomial([0]*(len(self.coefficient)-1),self.variable)
                    for i in range(len(diff.coefficient)):
                        diff.coefficient[i] = (self.coefficient[i+1]) * (i+1)
                    return Polynomial.adjust(diff)
                else:
                    return 0
        else:
            raise ValueError, "You must input differentiate(polynomial,string)." 

    def change_variable(self, other):
        if isinstance(other) == str:
            result_polynomial = Polynomial(self.coefficient, other)
            return Polynomial.adjust(result_polynomial)
        else:
            raise ValueError, "You must input string for variable."

#    def rearrange(self, other):
#        if (type(other) == list):
#            result_polynomial = Polynomial.toFlatPolynomial(self)
             
    def toFlatPolynomial(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long):
            return self
        else:
            multi = 0
            for i in self.coefficient:
                if isinstance(i,Polynomial):
                    multi = 1
            if multi:
                result_polynomial = 0
                unit_polynomial = Polynomial([0,1],self.variable)
                for i in range(len(self.coefficient)):
                    if isinstance(self.coefficient[i],int) or isinstance(self.coefficient[i],long):
                        result_polynomial += self.coefficient[i] * (unit_polynomial)**i
                    else:
                        result_polynomial += Polynomial.toFlatPolynomial(self.coefficient[i]) * (unit_polynomial)**i
                return FlatPolynomial.adjust(result_polynomial)
            else:
                for i in range(len(self.coefficient)):
                    if (type(self.coefficient[i]) != int) and (type(self.coefficient[i]) != long):
                        raise ValueError, "You must input pure polynomial of single variable."
                result_variable = [self.variable]
                result_coefficients = {}
                for i in range(len(self.coefficient)):
                    key = (i,)
                    result_coefficients[key] = self.coefficient[i]                 
                result_polynomial = FlatPolynomial(result_coefficients, result_variable)
                return FlatPolynomial.adjust(result_polynomial)


class FlatPolynomial:

    def __init__(self, coefficients, variables):   
        "FlatPolynomial(coefficients, variables)"
        if isinstance(variables, list) and isinstance(coefficients, dict):
            self.coefficients = coefficients
            self.variables = variables
        else:
            raise ValueError, "You must input (dict,list)."

    def __add__(self, other):
        if (type(other) == int) or (type(other) == long):
            self = FlatPolynomial.adjust(self)
            sum = FlatPolynomial({}, self.variables)
            for i in range(len(self.coefficients)):
                sum.coefficients[self.coefficients.keys()[i]] = self.coefficients.values()[i]
            if sum.coefficients.has_key((0,)*len(sum.variables)):
                sum.coefficients[(0,)*len(sum.variables)] += other
            else:
                sum.coefficients[(0,)*len(sum.variables)] = other
            return FlatPolynomial.adjust(sum)

        elif isinstance(other, Polynomial):
            return self + Polynomial.toFlatPolynomial(other)
        elif self.variables == other.variables:
            sum = FlatPolynomial({}, self.variables)
            for i in range(len(self.coefficients)):
                sum.coefficients[self.coefficients.keys()[i]] = self.coefficients.values()[i]
            for i in other.coefficients:
                if sum.coefficients.has_key(i):
                    sum.coefficients[i] += other.coefficients[i]
                else:
                    sum.coefficients[i] = other.coefficients[i]
            return FlatPolynomial.adjust(sum)

        else:
            self_adjust = FlatPolynomial.adjust(self)
            other_adjust = FlatPolynomial.adjust(other)
            if (type(self_adjust) == int) or (type(self_adjust) == long):
                return other_adjust + self_adjust
            elif (type(other_adjust) == int) or (type(other_adjust) == long):
                return self_adjust + other_adjust
            if self_adjust.variables == other_adjust.variables:
                return self_adjust + other_adjust
            sum_variables = []
            for i in self_adjust.variables:
                sum_variables += [i]
            for i in other_adjust.variables:
                if (i in sum_variables) != 1:
                    sum_variables += [i]
            sum_variables.sort()
            return FlatPolynomial.arrange_variables(self_adjust, sum_variables) + FlatPolynomial.arrange_variables(other_adjust, sum_variables)

    __radd__=__add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        result_polynomial = FlatPolynomial.adjust(self)
        if (type(result_polynomial) == int) or (type(result_polynomial) == long):
            return (-result_polynomial)
        for i in result_polynomial.coefficients.keys():
            result_polynomial.coefficients[i] = - result_polynomial.coefficients[i]
        return result_polynomial

    def __mul__(self, other):
        if (type(other) == int) or (type(other) == long):
            result_polynomial = {}
            for i in self.coefficients:
                result_polynomial[i] = other * self.coefficients[i]
            return FlatPolynomial(result_polynomial, self.variables).adjust()
        elif isinstance(other, Polynomial):
            return self * Polynomial.toFlatPolynomial(other)
        elif self.variables == other.variables:
            result_coefficients = {}
            result_variables = []
            for i in range(len(self.variables)):
                result_variables += self.variables[i]
            for i in range(len(self.coefficients)):
                for j in range(len(other.coefficients)):
                    index_list = []
                    for k in range(len(self.variables)):
                        index_list += [self.coefficients.keys()[i][k] + other.coefficients.keys()[j][k]]
                    mul_value = self.coefficients.values()[i] * other.coefficients.values()[j]
                    index_list = tuple(index_list)
                    if index_list in result_coefficients:
                        result_coefficients[index_list] += mul_value
                    else:
                        result_coefficients[index_list] = mul_value
            result_polynomial = FlatPolynomial(result_coefficients, result_variables)
            return result_polynomial.adjust()
        else:
            self_adjust = self.adjust()
            other_adjust = other.adjust()
            if (type(self_adjust) == int) or (type(self_adjust) == long):
                return other_adjust * self_adjust
            elif (type(other_adjust) == int) or (type(other_adjust) == long):
                return self_adjust * other_adjust
            if self_adjust.variables == other_adjust.variables:
                return self_adjust * other_adjust
            sum_variables = self_adjust.variables[:]
            for i in other_adjust.variables:
                if i not in sum_variables:
                    sum_variables += [i]
            sum_variables.sort()
            return FlatPolynomial.arrange_variables(self_adjust, sum_variables) * FlatPolynomial.arrange_variables(other_adjust, sum_variables)

    __rmul__=__mul__

    def __pow__(self, other):
        if (type(other) == int) or (type(other) == long):
            if other == 0:
                return 1
            elif other > 0:
                result_variables = self.variables[:]
                result_coefficients = {}
                one_key = (0,)*len(self.variables)
                result_coefficients[one_key] = 1
                result_polynomial = FlatPolynomial(result_coefficients, result_variables)
                for i in range(other):
                    result_polynomial = result_polynomial * self
                return FlatPolynomial.adjust(result_polynomial)
            else:
                raise ValueError, "You must input positive integer for index."
        else:
            raise ValueError, "You must input integer for index."

    def __rpow__(self, other):
        raise ValueError, "You must input integer for index."

#    def __floordiv__(self, other):

#    def __div__(self, other):

#    __truediv__=__div__

#    def __rfloordiv__(self, other):

#    def __rdiv__(self, other):

#    __rtruediv__=__rdiv__

#    def __mod__(self, other):
#        return self - (self // other) * other

#    def __rmod__(self, other):
#        return other - (other // self) * self

#    def __divmod__(self, other):
#        return (self // other, self % other)

#    def __rdivmod__(self, other):
#        return (other // self, other % self)

    def __eq__(self, other):
        sub_polynomial = self - other
        if (isinstance(sub_polynomial,int) or isinstance(sub_polynomial,long)) and sub_polynomial == 0:
            return 1
        return 0
        
    def __call__(self,**other):
        adjust_polynomial = self.adjust()
        if isinstance(adjust_polynomial,int) or isinstance(adjust_polynomial, long):
            return adjust_polynomial
        substitutions = other
        for i in adjust_polynomial.variables:            
            if i in substitutions and (isinstance(substitutions[i],int) or isinstance(substitutions[i],long)):
                variable_position = adjust_polynomial.variables.index(i)
                new_coefficients = {}
                for j in adjust_polynomial.coefficients:
                    new_value = adjust_polynomial.coefficients[j]
                    new_key = list(j)
                    new_key[variable_position] = 0
                    new_value *= substitutions[i]**j[variable_position]
                    new_key = tuple(new_key)
                    if new_key in new_coefficients:
                        new_coefficients[new_key] += new_value
                    else:
                        new_coefficients[new_key] = new_value
                adjust_polynomial.coefficients = new_coefficients
        adjust_polynomial = adjust_polynomial.adjust()
        if isinstance(adjust_polynomial,int) or isinstance(adjust_polynomial, long):
            return adjust_polynomial
        new_variables = adjust_polynomial.variables[:]
        for i in adjust_polynomial.variables:
            variable_position = adjust_polynomial.variables.index(i)
            if i in substitutions and isinstance(substitutions[i],str):
                new_variables[variable_position] = substitutions[i]
        adjust_polynomial.variables = new_variables
        result_polynomial = adjust_polynomial.adjust()
        return result_polynomial

    def __repr__(self):
        self = FlatPolynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) :
            return str(self)
        return_str = ""
        return_str += "FlatPolynomial(" + repr(self.coefficients) + ", "
        return_str += repr(self.variables) + ")"
        return return_str

    def __str__(self):
        disp_polynomial = FlatPolynomial.adjust(self)
        if (type(disp_polynomial) == int) or (type(disp_polynomial) == long) :
            return str(disp_polynomial)
        elif len(disp_polynomial.variables) == 1:
            max_index = 0
            for i in disp_polynomial.coefficients:
                if i[0] > max_index:
                    max_index = i[0]
            return_coefficients = [0]*(max_index + 1)
            for i in disp_polynomial.coefficients:
                return_coefficients[i[0]] += disp_polynomial.coefficients[i]
            return str(Polynomial(return_coefficients, disp_polynomial.variables[0]))
        else:
            old_variables = disp_polynomial.variables[:]
            reverse_coefficients = disp_polynomial.coefficients.copy()
            reverse_variables = old_variables[:]
            reverse_variables.reverse()
            reverse_polynomial = FlatPolynomial(reverse_coefficients, reverse_variables)
            reverse_polynomial = reverse_polynomial.sort_variables()
            result_coefficients = reverse_polynomial.coefficients.keys()
            result_coefficients.sort()
            test_key = (0,) * len(disp_polynomial.variables)
            return_str = ""
            for i in range(len(result_coefficients)):
                if reverse_polynomial.coefficients[result_coefficients[i]] >= 1:
                    return_str += ' + '
                    if (reverse_polynomial.coefficients[result_coefficients[i]] != 1) or (result_coefficients[i] == test_key):
                        return_str += str(reverse_polynomial.coefficients[result_coefficients[i]])
                else:
                    return_str += ' - '
                    if (reverse_polynomial.coefficients[result_coefficients[i]] != -1) or (result_coefficients[i] == test_key):
                        return_str += str(abs(reverse_polynomial.coefficients[result_coefficients[i]]))
                index_total = 0
                for k in range(len(result_coefficients[i])):
                    index_total += result_coefficients[i][k]
                for j in range(len(result_coefficients[i])):
                    if result_coefficients[i][- 1 - j] == 1:
                        return_str += old_variables[j]
                    elif result_coefficients[i][- 1 - j] > 1:
                        if result_coefficients[i][- 1 - j] != index_total:
                            return_str += '('
                        return_str += old_variables[j]
                        return_str += '**'
                        return_str += str(result_coefficients[i][- 1 - j])
                        if result_coefficients[i][- 1 - j] != index_total:
                            return_str += ')'
            if return_str[1] != '+':
                return return_str[1:]
            else:
                return return_str[3:]

    def arrange_variables(self, other):
        if type(other) != list:
            raise ValueError, "You must input list for other."
        else:
            result_polynomial = FlatPolynomial({},other)
            index_list = self.coefficients.keys()
            values_list = self.coefficients.values()
            position_infomation = []
            for i in range(len(other)):
                if other[i] in self.variables:
                    position_infomation += [i]
            for i in range(len(index_list)):
                key = [0]*len(other)
                for j in range(len(position_infomation)):
                    key[(position_infomation[j])] = index_list[i][j]
                result_polynomial.coefficients[tuple(key)] = values_list[i]
            return result_polynomial

    def adjust(self):
        if (len(self.variables) == 0) or (len(self.coefficients.keys()) == 0):
            return 0
        result_polynomial = self.sort_variables()
        result_polynomial = result_polynomial.merge_variables()
        result_polynomial = result_polynomial.delete_zero_value()
        result_polynomial = result_polynomial.delete_zero_variable()
        result_coefficient = result_polynomial.coefficients
        if len(result_coefficient) == 0:
            return 0
        zero_test = (0,)*len(result_polynomial.variables)
        if (len(result_coefficient) == 1) and (zero_test in result_coefficient):
            return result_coefficient[zero_test]
        return result_polynomial

    def sort_variables(self):
        positions = {}
        for i in range(len(self.variables)):
            if self.variables[i] in positions:
                positions[self.variables[i]] = tuple(list(positions[self.variables[i]]) + [i])
            else:
                positions[self.variables[i]] = (i,)
        result_variables = self.variables[:]
        result_polynomial = FlatPolynomial({},result_variables)
        result_polynomial.variables.sort()
        for i in self.coefficients.keys():
            new_index_list = []
            old_index_list = list(i)
            old_position_keys = positions.copy()
            for j in range(len(old_index_list)):
                if len(positions[result_polynomial.variables[j]]) == 1:
                    new_index_list += [old_index_list[positions[result_polynomial.variables[j]][0]]]
                else:
                    new_index_list += [old_index_list[positions[result_polynomial.variables[j]][0]]]
                    old_position_key = list(positions[result_polynomial.variables[j]])
                    del(old_position_key[0])
                    new_position_key = tuple(old_position_key)
                    positions[result_polynomial.variables[j]] = new_position_key
            if tuple(new_index_list) in result_polynomial.coefficients:
                result_polynomial.coefficients[tuple(new_index_list)] += self.coefficients[i]
            else:
                result_polynomial.coefficients[tuple(new_index_list)] = self.coefficients[i]
            for l in old_position_keys:
                positions[l] = old_position_keys[l]
        return result_polynomial

    def merge_variables(self):
        old_variables_list = self.variables
        merge_variables = [old_variables_list[0]]
        for i in range(len(old_variables_list) - 1):
            if old_variables_list[i+1] != old_variables_list[i]:
                merge_variables += [old_variables_list[i+1]]
        variables_position = {}
        for i in range(len(merge_variables)):
            position_list = []
            for j in range(len(old_variables_list)):
                if old_variables_list[j] == merge_variables[i]:
                    position_list += [j]
            variables_position[merge_variables[i]] = position_list
        result_polynomial = FlatPolynomial({},merge_variables)
        old_coefficients_keys = self.coefficients.keys()
        old_coefficients_values = self.coefficients.values()
        for i in range(len(old_coefficients_keys)):
            new_coefficients_key = []
            for j in merge_variables:
                new_value = 0
                for k in variables_position[j]:
                    new_value += old_coefficients_keys[i][k]
                new_coefficients_key += [new_value]
            if tuple(new_coefficients_key) in result_polynomial.coefficients:
                result_polynomial.coefficients[tuple(new_coefficients_key)] += old_coefficients_values[i]
            else:
                result_polynomial.coefficients[tuple(new_coefficients_key)] = old_coefficients_values[i]
        return result_polynomial

    def delete_zero_value(self):
        result_coefficient = {}
        for i in self.coefficients:
            if self.coefficients[i] != 0:
                result_coefficient[i] = self.coefficients[i]
        result_polynomial = FlatPolynomial(result_coefficient, self.variables)
        return result_polynomial

    def delete_zero_variable(self):
        old_coefficients_keys = self.coefficients.keys()
        old_coefficients_values = self.coefficients.values()
        old_variables = self.variables
        exist_position_list = []
        for i in range(len(old_variables)):
            for j in range(len(old_coefficients_keys)):
                if old_coefficients_keys[j][i] != 0:
                    exist_position_list += [i]
                    break
        new_variables = [old_variables[position] for position in exist_position_list]
        new_coefficients = {}
        for i in range(len(old_coefficients_keys)):
            new_coefficients_key = []
            for j in exist_position_list:
                new_coefficients_key += [old_coefficients_keys[i][j]]
            new_coefficients[tuple(new_coefficients_key)] = old_coefficients_values[i]
        result_polynomial = FlatPolynomial(new_coefficients, new_variables)
        return result_polynomial

    def differentiate(self, other):
        if type(other) == str:
            origin_polynomial = FlatPolynomial.adjust(self)
            if other in origin_polynomial.variables:
                result_variables = origin_polynomial.variables[:]
                variable_position = result_variables.index(other)
                result_coefficients = {}
                for i in origin_polynomial.coefficients:
                    if i[variable_position] > 0:
                        new_coefficients_key = list(i)
                        new_index = new_coefficients_key[variable_position] - 1
                        new_coefficients_value = origin_polynomial.coefficients[i] * (new_index + 1)
                        new_coefficients_key[variable_position] = new_index
                        new_coefficients_key = tuple(new_coefficients_key)
                        result_coefficients[new_coefficients_key] = new_coefficients_value
                result_polynomial = FlatPolynomial(result_coefficients, result_variables)
                return FlatPolynomial.adjust(result_polynomial)
            else:
                return 0
        else:
            raise ValueError, "You input [FlatPolynomial, string]."

    def toPolynomial(self):
        origin_polynomial = FlatPolynomial.adjust(self)
        if (type(origin_polynomial) == int) or (type(origin_polynomial) == long):
            return origin_polynomial
        elif len(origin_polynomial.variables) == 1:
            max_index = 0
            for i in origin_polynomial.coefficients:
                if i[0] > max_index:
                    max_index = i[0]
            return_polynomial = [0]*(max_index + 1)
            for i in origin_polynomial.coefficients:
                return_polynomial[i[0]] += origin_polynomial.coefficients[i]
            return Polynomial(return_polynomial, origin_polynomial.variables[0]).adjust()
        else:
            max_index = 0
            for i in origin_polynomial.coefficients:
                if i[-1] > max_index:
                    max_index = i[-1]            
            return_polynomial = Polynomial([0]*(max_index+1),origin_polynomial.variables[-1])
            sum_polynomial_list = [0]*(max_index + 1)
            for i in origin_polynomial.coefficients:
                for j in range(max_index+1):
                    if i[-1] == j:
                        new_key = list(i)
                        del(new_key[-1])
                        new_key = tuple(new_key)
                        new_value = origin_polynomial.coefficients[i]
                        new_coefficients = {}
                        new_coefficients[new_key] = new_value
                        new_polynomial = FlatPolynomial(new_coefficients, origin_polynomial.variables[:-1])
                        sum_polynomial_list[j] += new_polynomial
            for i in range(max_index+1):
                return_polynomial.coefficient[i] = sum_polynomial_list[i].toPolynomial()
            return return_polynomial