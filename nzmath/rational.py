#rationalnumber add,sub,mul,div,comp
def GCD(a,b):
    if b == 0:
        return a
    while 1:
        r = a%b
        if r == 0:
            if b < 0:
                return -b
            else :
                return  b
        else :
            a=b
            b=r


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
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                sum=Rational(numerator,denominator)
            else:
                sum=Rational(numerator//gcd,denominator//gcd)
            return sum
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator+self.denominator*other
            denominator=self.denominator
            gcd=GCD(numerator,denominator)          
            if gcd == 1:
                sum=Rational(numerator,denominator)
            else:
                sum=Rational(numerator//gcd,denominator//gcd)
            return sum
            
        else:
            return NotImplemented 

    def __sub__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator-self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                dif=Rational(numerator,denominator)
            else:
                dif=Rational(numerator//gcd,denominator//gcd)
            return dif
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator-self.denominator*other
            denominator=self.denominator            
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                dif=Rational(numerator,denominator)
            else:
                dif=Rational(numerator//gcd,denominator//gcd)
            return dif
            
        else:
            return NotImplemented

    def __mul__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.numerator
            denominator=self.denominator*other.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                mul=Rational(numerator,denominator)
            else:
                mul=Rational(numerator//gcd,denominator//gcd)
            return mul
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator*other
            denominator=self.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                mul=Rational(numerator,denominator)
            else:
                mul=Rational(numerator//gcd,denominator//gcd)
            return mul
            
        else:
            return NotImplemented

    def __div__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator
            denominator=self.denominator*other.numerator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                div=Rational(numerator,denominator)
            else:
                div=Rational(numerator//gcd,denominator//gcd)
            return div
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator
            denominator=self.denominator*other
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                div=Rational(numerator,denominator)
            else:
                div=Rational(numerator//gcd,denominator//gcd)
            return div
            
        else:
            return NotImplemented
    def __radd__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator+self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                sum=Rational(numerator,denominator)
            else:
                sum=Rational(numerator//gcd,denominator//gcd)
            return sum
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator+self.denominator*other
            denominator=self.denominator
            gcd=GCD(numerator,denominator)          
            if gcd == 1:
                sum=Rational(numerator,denominator)
            else:
                sum=Rational(numerator//gcd,denominator//gcd)
            return sum
            
        else:
            return NotImplemented 

    def __rsub__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator-self.denominator*other.numerator
            denominator=self.denominator*other.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                dif=Rational(numerator,denominator)
            else:
                dif=Rational(numerator//gcd,denominator//gcd)
            return dif
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.denominator*other-self.numerator
            denominator=self.denominator            
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                dif=Rational(numerator,denominator)
            else:
                dif=Rational(numerator//gcd,denominator//gcd)
            return dif
            
        else:
            return NotImplemented

    def __rmul__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.numerator
            denominator=self.denominator*other.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                mul=Rational(numerator,denominator)
            else:
                mul=Rational(numerator//gcd,denominator//gcd)
            return mul
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.numerator*other
            denominator=self.denominator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                mul=Rational(numerator,denominator)
            else:
                mul=Rational(numerator//gcd,denominator//gcd)
            return mul
            
        else:
            return NotImplemented

    def __rdiv__(self,other):
        if isinstance(other, Rational):
            numerator=self.numerator*other.denominator
            denominator=self.denominator*other.numerator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                div=Rational(numerator,denominator)
            else:
                div=Rational(numerator//gcd,denominator//gcd)
            return div
        elif isinstance(other, int) or isinstance(other, long):
            numerator=self.denominator*other
            denominator=self.numerator
            gcd=GCD(numerator,denominator)
            if gcd == 1:
                div=Rational(numerator,denominator)
            else:
                div=Rational(numerator//gcd,denominator//gcd)
            return div
            
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
        if isinstance(other, int):
            if self.numerator == other and self.denominator == 1: 
                return 1
            else:
                return 0
        if self.numerator*other.denominator == self.denominator*other.numerator:
            return 1
        else:
            return 0
    def __ne__(self,other):
        if isinstance(other, int):
            if self.__eq__(other):
                return 1
            else:
                return 0
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

    def __repr__(self):
        return str(self.numerator)+"/"+str(self.denominator)
