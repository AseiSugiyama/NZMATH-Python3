#polynomial.py 
import string

class Polynomial:

    def __init__(self, coefficient, variable):
        "Polynomial(coefficient, char)"
        if(    (isinstance(variable, str) or isinstance(variable, str))  and  isinstance(coefficient, list)    ):
            self.coefficient = coefficient
            self.variable = variable
            self.compo = []
        else:
            raise ValueError, "You must input (list,string)."

    def __add__(self, other):
        if (type(other) == int) or (type(other) == long) or (type(other) == float):
            sum = Polynomial([0]*len(self.coefficient),self.variable)
            for i in range(len(self.coefficient)):
                sum.coefficient[i] = self.coefficient[i]
            sum.coefficient[0] += other
            return Polynomial.adjust(sum) 
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
            raise ValueError, "You must input common variable."

    def __radd__(self, other):
         return Polynomial.__add__(self, other)

    def __sub__(self, other):
        if (type(other) == int) or (type(other) == long) or (type(other) == float):
            return Polynomial.__add__(self, -other)
        return Polynomial.__add__(self, Polynomial.__neg__(other))

    def __rsub__(self, other):
        return -(Polynomial.__sub__(self, other))

    def __neg__(self):
        if (type(self) == int) or (type(self) == long) or (type(self) == float):
            return (-self)
        reciprocal = Polynomial([0]*len(self.coefficient),self.variable)
        for i in range(len(self.coefficient)):
            reciprocal.coefficient[i] -= self.coefficient[i]
        return reciprocal

    def __mul__(self, other):
        if (type(other) == int) or (type(other) == long) or (type(other) == float):
            product = Polynomial([0]*len(self.coefficient),self.variable)
            for i in range(len(self.coefficient)):
                product.coefficient[i] = self.coefficient[i] * other
            return Polynomial.adjust(product)
        elif self.variable == other.variable:
            product = Polynomial([0]*(len(self.coefficient) + len(other.coefficient)),self.variable)
            for l in range(len(self.coefficient)):
                for r in range(len(other.coefficient)):
                    product.coefficient[l + r] += self.coefficient[l] * other.coefficient[r]
            return Polynomial.adjust(product)
        else:
            raise ValueError, "You must input common variable."

    def __rmul__(self, other):
        return Polynomial.__mul__(self, other)
            
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
        sub = Polynomial.__sub__(self, other)
        if (type(sub) == int) or (type(sub) == long) or (type(sub) == float):
            return sub == 0
        else:
            return 0

    def __req__(self, other):
        return Polynomial.__eq__(self, other)

    def __ne__(self, other):
        return Polynomial.__eq__(self, other) != 1 

    def __rne__(self, other):
        return Polynomial.__ne__(self, other)

    def __repr__(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) or (type(self) == float):
            return str(self)
        return_str = ""
        return_str += "Polynomial(["
        for i in range(len(self.coefficient) - 1):
            return_str += str(self.coefficient[i])
            return_str += ","
        return_str += str(self.coefficient[len(self.coefficient) - 1])
        return_str += '],"'
        return_str += self.variable
        return_str += '")'
        return return_str  

    def __str__(self):
        self = Polynomial.adjust(self)
        if (type(self) == int) or (type(self) == long) or (type(self) == float):
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
        result = Polynomial([0]*length,self.variable)
        for i in range(length):
            result.coefficient[i] = self.coefficient[i] 
        return result

    def differentiate(self, other):
        if (type(other) == chr) or (type(other) == str):
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

    