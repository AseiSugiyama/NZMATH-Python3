#rationalnumber add,sub,mul,div,comp
## def GCD(a,b):
##     while 1:
##         r = a%b
##         if r == 0:
##             if b < 0:
##                 return -b
##             else :
##                 return  b
##         else :
##             a=b
##             b=r
from gcd import gcd

class Rational:

    def __init__(self,numerator,denominator):
        if denominator < 0:
            self.numerator = -numerator
            self.denominator = -denominator
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
        if self.numerator*other.denominator < self.denominator*other.numerator:
            return 1
        else:
            return 0

    def __le__(self,other):
        if self.numerator*other.denominator <= self.denominator*other.numerator:
            return 1 
        else:
            return 0

    def __eq__(self,other):
        if self.numerator*other.denominator == self.denominator*other.numerator:
            return 1
        else:
            return 0
    def __ne__(self,other):
        if self.numerator*other.denominator != self.denominator*other.numerator:
            return 1
        else:
            return 0

    def __gt__(self,other):
        if self.numerator*other.denominator >= self.denominator*other.numerator:
            return 1
        else:
            return 0

    def __ge__(self,other):
        if self.numerator*other.denominator > self.denominator*other.numerator:
            return 1
        else:
            return 0

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

    def __repr__(self):
        return str(self.numerator)+"/"+str(self.denominator)
