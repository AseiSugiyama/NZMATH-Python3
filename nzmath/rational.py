#rationalnumber add,sub,mul,div,comp

import ring
from gcd import gcd

def toRational(value):
    if isinstance(value, int) or isinstance(value, long):
        return Rational(value, 1)
    elif isinstance(value, Rational):
        return value

class Rational:

    def __init__(self, numerator, denominator=1):
        if denominator < 0:
            self.numerator = -numerator
            self.denominator = -denominator
        elif denominator == 1 and isinstance(numerator, Rational):
            self.numerator = numerator.numerator
            self.denominator = numerator.denominator
        else :
            self.numerator = numerator
            self.denominator = denominator    

    def __add__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator+self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            return  +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator+self.denominator*other
            denominator=self.denominator
            return  +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __sub__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator-self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            return +Rational(numerator,denominator) 
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator-self.denominator*other
            denominator=self.denominator            
            return +Rational(numerator,denominator) 
        else:
            return NotImplemented

    def __mul__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.numerator
            denominator=self.denominator*other.denominator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator*other
            denominator=self.denominator
            return +Rational(numerator,denominator) 
        else:
            return NotImplemented

    def __div__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator
            denominator=self.denominator*other.numerator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator
            denominator=self.denominator*other
            return +Rational(numerator,denominator)
        else:
            return NotImplemented
    def __radd__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator+self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator+self.denominator*other
            denominator=self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rsub__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator-self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.denominator*other-self.numerator
            denominator=self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rmul__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.numerator
            denominator=self.denominator*other.denominator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator*other
            denominator=self.denominator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __rdiv__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator
            denominator=self.denominator*other.numerator
            return +Rational(numerator,denominator)
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.denominator*other
            denominator=self.numerator
            return +Rational(numerator,denominator)
        else:
            return NotImplemented

    def __lt__(self,other):
        return self.compare(other) < 0

    def __le__(self,other):
        return self.compare(other) <= 0

    def __eq__(self,other):
        return self.compare(other) == 0

    def __ne__(self,other):
        return self.compare(other) != 0

    def __gt__(self,other):
        return self.compare(other) > 0

    def __ge__(self,other):
        return self.compare(other) >= 0

    def __pos__(self):
        g=gcd(self.numerator,self.denominator)
        if g != 1:
            self.numerator=self.numerator//g
            self.denominator=self.denominator//g
        if self.denominator == 1:
            return self.numerator
        else:
            return Rational(self.numerator, self.denominator)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __abs__(self):
        return Rational(abs(self.numerator), self.denominator)

    def __str__(self):
        return str(self.numerator)+"/"+str(self.denominator)

    __repr__ = __str__

    def compare(self, other):
        if isinstance(other, int) or isinstance(other, long):
            return self.numerator - self.denominator * other
        return self.numerator*other.denominator - self.denominator*other.numerator
