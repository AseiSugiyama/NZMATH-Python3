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
            sum = Polynomial([0]*len(self.coefficient),self.variable)
            for i in range(len(self.coefficient)):
                sum.coefficient[i] = self.coefficient[i]
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

    def __eq__(self, other):
        return self - other == 0

    __call__=__mul__

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
             
    def toFlatPolynomial(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long):
            return self
#        elif isinstance(self) == FlatPolynomial:
#            return FlatPolynomial.adjust(self)
        else:
            for i in range(len(self.coefficient)):
                if (type(self.coefficient[i]) != int) and (type(self.coefficient[i]) != long):
                    raise ValueError, "You input pure polynomial of single variable."
            result_variable = [self.variable]
            result_coefficients = {}
            for i in range(len(self.coefficient)):
                key = tuple([i])
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
        if(type(other) == int) or (type(other) == long):
            result_polynomial = FlatPolynomial({},self.variables)
            for i in range(len(self.coefficients)):
                result_polynomial.coefficients[self.coefficients.keys()[i]] = other * self.coefficients.values()[i]
            return FlatPolynomial.adjust(result_polynomial)
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
            return FlatPolynomial.adjust(result_polynomial)
        else:
            self_adjust = FlatPolynomial.adjust(self)
            other_adjust = FlatPolynomial.adjust(other)
            if (type(self_adjust) == int) or (type(self_adjust) == long):
                return other_adjust * self_adjust
            elif (type(other_adjust) == int) or (type(other_adjust) == long):
                return self_adjust * other_adjust
            if self_adjust.variables == other_adjust.variables:
                return self_adjust * other_adjust
            sum_variables = []
            for i in self_adjust.variables:
                sum_variables += [i]
            for i in other_adjust.variables:
                if (i in sum_variables) != 1:
                    sum_variables += [i]
            sum_variables.sort()
            return FlatPolynomial.arrange_variables(self_adjust, sum_variables) * FlatPolynomial.arrange_variables(other_adjust, sum_variables)

    __rmul__=__mul__

    def __pow__(self, other):
        if (type(other) == int) or (type(other) == long):
            if other == 0:
                return 1
            elif other > 0:
                result_variables = []
                for i in range(len(self.variables)):
                    result_variables += [self.variables[i]]
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

    def __eq__(self, other):
        return self - other == 0

    __call__=__mul__

    def __repr__(self):
        self = FlatPolynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) :
            return str(self)
        return_str = ""
        return_str += "FlatPolynomial(" + repr(self.coefficients) + ", "
        return_str += repr(self.variables) + ")"
        return return_str

    def __str__(self):
        self = FlatPolynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) :
            return str(self)
        elif len(self.variables) == 1:
            max_index = 0
            for i in range(len(self.coefficients)):
                if self.coefficients.keys()[i][0] > max_index:
                    max_index = self.coefficients.keys()[i][0]
            return_polynomial = Polynomial([0]*(max_index + 1),self.variables[0])
            for i in range(len(self.coefficients)):
                return_polynomial.coefficient[self.coefficients.keys()[i][0]] += self.coefficients.values()[i]
            return Polynomial.__str__(return_polynomial)
        else:
            old_variables = []
            for i in range(len(self.variables)):
                old_variables += [self.variables[i]]
            reverse_coefficients = {}
            for i in range(len(self.coefficients)):
                reverse_coefficients[self.coefficients.keys()[i]] = self.coefficients.values()[i]
            reverse_variables = []
            for i in range(len(old_variables)):
                reverse_variables += [old_variables[len(old_variables) - 1 - i]]
            reverse_polynomial = FlatPolynomial(reverse_coefficients, reverse_variables)
            reverse_polynomial = FlatPolynomial.sort_variables(reverse_polynomial)
            result_coefficients = reverse_polynomial.coefficients.keys()
            result_coefficients.sort()
            test_key = (0,) * len(self.variables)
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
                    if result_coefficients[i][len(result_coefficients[i]) - 1 - j] == 1:
                        return_str += old_variables[j]
                    elif result_coefficients[i][len(result_coefficients[i]) - 1 - j] > 1:
                        if result_coefficients[i][len(result_coefficients[i]) - 1 - j] != index_total:
                            return_str += '('
                        return_str += old_variables[j]
                        return_str += '**'
                        return_str += str(result_coefficients[i][len(result_coefficients[i]) - 1 - j])
                        if result_coefficients[i][len(result_coefficients[i]) - 1 - j] != index_total:
                            return_str += ')'
            test_return_str = string.split(return_str)
            if test_return_str[0] != '+':
                return return_str
            else:
                del(test_return_str[0])
                for i in range(len(test_return_str)):
                    print test_return_str[i],
                return ""

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
        result_polynomial = FlatPolynomial.sort_variables(self)
        result_polynomial = FlatPolynomial.merge_variables(result_polynomial)
        result_polynomial = FlatPolynomial.delete_zero_value(result_polynomial)
        result_polynomial = FlatPolynomial.delete_zero_variable(result_polynomial)
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
        result_variables = []
        for i in range(len(self.variables)):
            result_variables += [self.variables[i]]
        result_polynomial = FlatPolynomial({},result_variables)
        result_polynomial.variables.sort()
        for i in self.coefficients.keys():
            new_index_list = []
            old_index_list = list(i)
            old_position_keys = {}
            for l in range(len(positions)):
                old_position_keys[positions.keys()[l]] = positions.values()[l]
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
            for l in range(len(old_position_keys)):
                positions[old_position_keys.keys()[l]] = old_position_keys.values()[l]
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
        for i in range(len(self.coefficients.keys())):
            if self.coefficients.values()[i] != 0:
                result_coefficient[self.coefficients.keys()[i]] = self.coefficients.values()[i]
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
        new_variables = []
        for i in range(len(exist_position_list)):
            new_variables += old_variables[exist_position_list[i]]
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
            self = FlatPolynomial.adjust(self)
            if other in self.variables:
                result_variables = []
                for i in range(len(self.variables)):
                    result_variables += self.variables[i]
                    if self.variables[i] == other:
                        variable_position = i
                result_coefficients = {}
                for i in range(len(self.coefficients)):
                    if self.coefficients.keys()[i][variable_position] > 0:
                        new_coefficients_key = list(self.coefficients.keys()[i])
                        new_index = new_coefficients_key[variable_position] - 1
                        new_coefficients_value = self.coefficients.values()[i] * (new_index + 1)
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
        self = FlatPolynomial.adjust(self)
        if (type(self) == int) or (type(self) == long):
            return self
        elif len(self.variables) == 1:
            max_index = 0
            for i in range(len(self.coefficients)):
                if self.coefficients.keys()[i][0] > max_index:
                    max_index = self.coefficients.keys()[i][0]
            return_polynomial = Polynomial([0]*(max_index + 1),self.variables[0])
            for i in range(len(self.coefficients)):
                return_polynomial.coefficient[self.coefficients.keys()[i][0]] += self.coefficients.values()[i]
            return Polynomial.adjust(return_polynomial)
        else:
            raise ValueError, "You input FlatPolynomial with single variable."