from prime import vp
import rational

"""

The module `real' provides arbitrary precision real numbers and their
utilities.

"""

doubleprecision = 53

class Float:
    """

    Float is an arbitrary precision real number class.  A number is
    represented as mantissa * (2**exponent), where mantissa is an odd
    integer.  If precision is set to None, it means the number has
    infinite precision.

    """
    def __init__(self, mantissa, exponent, precision=None):
        if isinstance(mantissa, rational.Rational):
            aRational = mantissa
            if not precision:
                if mantissa == 0:
                    mantissa, exponent, precision = 0,0,None
                v, t = vp(aRational.denominator,2)
                if t != 1:
                    raise ValueError, "precision must be a positive integer."
                mantissa, exponent, precision = aRational.numerator, -v, None
            bits = getNumberOfBits(aRational.denominator)
            mantissa = (aRational.numerator * 2**(bits + precision)) // aRational.denominator
            exponent = -(bits + precision)
        if mantissa != 0:
            k, odd = vp(mantissa,2)
            self.mantissa, self.exponent = odd, exponent + k
        else:
            self.mantissa, self.exponent = 0, 0
        self.precision = precision
        if not self.precision:
            self.defaultPrecision = max((doubleprecision, getNumberOfBits(mantissa)))
        else:
            self.defaultPrecision = self.precision

    def __add__(self, other):
        if rational.isIntegerObject(other):
            return self + self.__class__(other, 0, None)
        # adjust with precision
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
            sbits, obits = getNumberOfBits(self.mantissa), getNumberOfBits(other.mantissa)
            if sbits < precision:
                smantissa = self.mantissa * 2 ** (precision - sbits)
                sexponent = self.exponent - (precision - sbits)
            else:
                smantissa = self.mantissa
                sexponent = self.exponent
            if obits < precision:
                omantissa = other.mantissa * 2 ** (precision - obits)
                oexponent = other.exponent - (precision - obits)
            else:
                omantissa = other.mantissa
                oexponent = other.exponent
        else:
            precision = None
            smantissa, sexponent = self.mantissa, self.exponent
            omantissa, oexponent = other.mantissa, other.exponent
        # do addition
        if sexponent < oexponent:
            exponent = sexponent
            mantissa = smantissa + (omantissa * 2 ** (oexponent - exponent))
        elif sexponent > oexponent:
            exponent = oexponent
            mantissa = (smantissa * 2 ** (sexponent - exponent)) + omantissa
        else:
            exponent = sexponent
            mantissa = smantissa + omantissa
        # normalize
        bits = getNumberOfBits(mantissa)
        if precision:
            if bits > precision:
                mantissa >>= (bits - precision)
                exponent += (bits - precision)
            elif exponent > 0 and bits + exponent < precision: #underflow
                precision = bits + exponent
            elif exponent <= 0 and bits < precision: # underflow
                precision = bits
        if mantissa != 0:
            k, odd = vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __radd__(self, other):
        if rational.isIntegerObject(other):
            return self.__class__(other, 0, None) + self
        elif isinstance(other, rational.Rational):
            return self.__class__(other, 0, None) + self

    def __sub__(self, other):
        if rational.isIntegerObject(other):
            return self - self.__class__(other, 0, None)
        # adjust with precision
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
            sbits, obits = getNumberOfBits(self.mantissa), getNumberOfBits(other.mantissa)
            if sbits < precision:
                smantissa = self.mantissa * 2 ** (precision - sbits)
                sexponent = self.exponent - (precision - sbits)
            else:
                smantissa = self.mantissa
                sexponent = self.exponent
            if obits < precision:
                omantissa = other.mantissa * 2 ** (precision - obits)
                oexponent = other.exponent - (precision - obits)
            else:
                omantissa = other.mantissa
                oexponent = other.exponent
        else:
            precision = None
            smantissa, sexponent = self.mantissa, self.exponent
            omantissa, oexponent = other.mantissa, other.exponent
        # do subtraction
        if sexponent < oexponent:
            exponent = sexponent
            mantissa = smantissa - (omantissa * 2 ** (oexponent - exponent))
        elif sexponent > oexponent:
            exponent = oexponent
            mantissa = (smantissa * 2 ** (sexponent - exponent)) - omantissa
        else:
            exponent = sexponent
            mantissa = smantissa - omantissa
        # normalize
        bits = getNumberOfBits(mantissa)
        if precision:
            if bits > precision:
                mantissa >>= (bits - precision)
                exponent += (bits - precision)
            elif exponent > 0 and bits + exponent < precision: #underflow
                precision = bits + exponent
            elif exponent <= 0 and bits < precision: # underflow
                precision = bits
        if mantissa != 0:
            k, odd = vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __rsub__(self, other):
        if rational.isIntegerObject(other):
            return self.__class__(other, 0, None) - self
        elif isinstance(other, rational.Rational):
            return self.__class__(other, 0, None) - self

    def __mul__(self, other):
        if rational.isIntegerObject(other):
            v2, c2 = vp(other, 2)
            return self.__class__(self.mantissa * c2,
                                  self.exponent + v2,
                                  self.precision)
        elif isinstance(other, rational.Rational):
            return self * self.__class__(other, 0)
        mantissa = self.mantissa * other.mantissa
        exponent = self.exponent + other.exponent
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
        else:
            precision = None
        # normalization
        bits = getNumberOfBits(mantissa)
        if precision:
            if bits > precision:
                mantissa >>= (bits - precision)
                exponent += (bits - precision)
        if mantissa != 0:
            k, odd = vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __rmul__(self, other):
        if rational.isIntegerObject(other):
            return self.__class__(other, 0, None) * self
        elif isinstance(other, rational.Rational):
            return self.__class__(other, 0, None) * self

    def __div__(self, other):
        """

        division: The result is less than or equal to the exact
        quotient as absolute value.
        
        """
        if rational.isIntegerObject(other):
            v2, c2 = vp(other, 2)
            retval = self.__class__(self.mantissa,
                                    self.exponent - v2,
                                    self.precision)
            return retval / self.__class__(c2, 0, self.precision)
        elif isinstance(other, rational.Rational):
            return self / self.__class__(other, 0, self.precision)
        exponent = self.exponent - other.exponent
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
        elif other.mantissa != 1:
            precision = self.defaultPrecision
        else:
            precision = None
        if self.mantissa < 0:
            sign = -1
            mantissa = -self.mantissa
        else:
            sign = 1
            mantissa = self.mantissa
        bits = getNumberOfBits(other.mantissa)
        if precision:
            mantissa *= 2 ** (bits + precision)
            exponent -= bits + precision
        else:
            mantissa *= 2 ** bits
            exponent -= bits
        quotient, remainder = divmod(mantissa, other.mantissa)
        bits = getNumberOfBits(quotient)
        # normalize
        if precision:
            if bits > precision:
                quotient >>= (bits - precision)
                exponent += (bits - precision)
        if quotient != 0:
            k, mantissa = vp(quotient,2)
            exponent += k
        else:
            mantissa = 0
            exponent = 0
        if sign == 1:
            return self.__class__(mantissa, exponent, precision)
        else:
            return self.__class__(-mantissa, exponent, precision)

    __truediv__ = __div__

    def __rdiv__(self, other):
        if rational.isIntegerObject(other):
            return self.__class__(other, 0, None) / self
        elif isinstance(other, rational.Rational):
            return self.__class__(other, 0, None) / self

    __rtruediv__ = __rdiv__

    def __pow__(self, other, dummy=None):
        if rational.isIntegerObject(other):
            if other == 0:
                return self.__class__(1,0,None)
            elif other == 1:
                return +self
            elif other < 0:
                return (self**(-other)).inverse()
            elif other == 2:
                mantissa = self.mantissa * self.mantissa
                exponent = self.exponent + self.exponent
            else:
                mantissa = self.mantissa ** other
                exponent = self.exponent * other
            precision = self.precision
            # normalization
            bits = getNumberOfBits(mantissa)
            if precision:
                if bits > precision:
                    mantissa >>= (bits - precision)
                    exponent += (bits - precision)
            return self.__class__(mantissa, exponent, precision)

    def __neg__(self):
        return self.__class__(-self.mantissa, self.exponent, self.precision)

    def __pos__(self):
        return self.__class__(+self.mantissa, self.exponent, self.precision)

    def __eq__(self, other):
        try:
            return (self - other).mantissa == 0
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return (self - other).mantissa != 0
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return (self - other).mantissa < 0
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self - other).mantissa > 0
        except AttributeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return (self - other).mantissa <= 0
        except AttributeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return (self - other).mantissa >= 0
        except AttributeError:
            return NotImplemented

    def __repr__(self):
        return "Float(" + repr(self.mantissa) + ", " + repr(self.exponent) + ", " + repr(self.precision) + ")"

    def __str__(self):
        if self.exponent >= 0:
            return str(self.mantissa * 2**self.exponent)
        else:
            if self.mantissa >= 0:
                q,r = divmod(self.mantissa, 2**(-self.exponent))
                retval = str(q) + "."
            else:
                q,r = divmod(-self.mantissa, 2**(-self.exponent))
                retval = "-" + str(q) + "."
            for i in range(20):
                q,r = divmod(r*10, 2**(-self.exponent))
                retval += str(q)
            return retval

    def setDefaultPrecision(self, newPrecision):
        self.defaultPrecision = newPrecision

    def toRational(self):
        if self.exponent < 0:
            return rational.Rational(self.mantissa, 2 ** (-self.exponent))
        elif self.exponent > 0:
            return rational.Rational(self.mantissa * 2 ** self.exponent)
        else:
            return rational.Rational(self.mantissa)

    def inverse(self):
        return self.__class__(1,0,None) / self

    def copy(self):
        retval = self.__class__(self.mantissa, self.exponent, self.precision)
        retval.setDefaultPrecision(self.defaultPrecision)
        return retval

def getNumberOfBits(anInteger):
    """

    returns the number of binary digits of a given integer ignoring the sign.

    """
    if anInteger == 0:
        return 0
    absInteger = abs(anInteger)
    if absInteger == 1:
        return 1
    squaring, log2 = 2, 1
    while squaring <= absInteger:
        squaring *= squaring
        log2 *= 2
    log2 //= 2
    bits = log2
    approximation = 1L << bits  # 1L can be replaced by 1 someday...
    while not (approximation <= absInteger < approximation * 2):
        log2 //= 2
        if (approximation << log2) <= absInteger:
            approximation <<= log2
            bits += log2
    return bits + 1

def rationalToFloat(aRational, precision):
    if not precision:
        if aRational == 0:
            return Float(0,0,None)
        v, t = vp(aRational.denominator,2)
        if t != 1:
            raise ValueError, "precision must be a positive integer."
        return (aRational.numerator, -v, None)
    bits = getNumberOfBits(aRational.denominator)
    mantissa = (aRational.numerator * 2**(bits + precision)) // aRational.denominator
    exponent = -(bits + precision)
    return Float(mantissa, exponent, precision)

def sqrt(aFloat, precision=doubleprecision):
    def _isCloseEnough(x, y, prec):
        xrat = x.toRational()
        yrat = y.toRational()
        prat = rational.Rational(1, 2**prec)
        return -prat < (xrat - yrat) / xrat < prat
    if precision < aFloat.precision:
        precision = aFloat.precision
    if aFloat.mantissa < 0:
        raise ValueError, "negative number is passed to sqrt"
    if aFloat.mantissa == 0:
        return Float(0,0,None)
    x = Float(1, getNumberOfBits(aFloat.mantissa) // 2 + aFloat.exponent // 2, precision*2)
    xnew = (x + aFloat / x) / 2
    while not _isCloseEnough(x, xnew, precision):
        x = xnew
        xnew = (x + aFloat / x) / 2
    while x.precision > precision:
        x.mantissa = x.mantissa // 2 + (x.mantissa & 1)
        x.exponent += 1
        x.precision -= 1
    return x

def floor(x):
    """

    floor(x) returns the integer; if x is an integer then x itself,
    otherwise the biggest integer less than x.

    """
    if rational.isIntegerObject(x):
        return x
    if isinstance(x, rational.Rational):
        x = Float(x, 0, None)
    elif not isinstance(x, Float):
        raise TypeError, ("%s cannot be converted to Float." % str(x))
    if x.exponent > 0:
        return x.mantissa * 2 ** x.exponent
    elif x.exponent == 0:
        return x.mantissa
    else:
        if x.mantissa < 0:
            retval = -x.mantissa
            retval >>= -x.exponent
            return -(retval + 1)
        else:
            retval = x.mantissa
            retval >>= -x.exponent
            return retval + 1

def tranc(x):
    """

    tranc(x) returns the integer; if x is an integer then x itself,
    otherwise the nearest integer to x.  If x has the fraction part
    1/2, then bigger one will be chosen.

    """
    if rational.isIntegerObject(x):
        return x
    if isinstance(x, rational.Rational):
        x = Float(x, 0, None)
    elif not isinstance(x, Float):
        raise TypeError, ("%s cannot be converted to Float." % str(x))
    if x.exponent > 0:
        return x.mantissa * 2 ** x.exponent
    elif x.exponent == 0:
        return x.mantissa
    return floor(x + Float(1, -1, None))

def ceil(x):
    """

    ceil(x) returns the integer; if x is an integer then x itself,
    otherwise the smallest integer greater than x.

    """
    if rational.isIntegerObject(x):
        return x
    if isinstance(x, rational.Rational):
        x = Float(x, 0, None)
    elif not isinstance(x, Float):
        raise TypeError, ("%s cannot be converted to Float." % str(x))
    if x.exponent > 0:
        return x.mantissa * 2 ** x.exponent
    elif x.exponent == 0:
        return x.mantissa
    else:
        if x.mantissa < 0:
            retval = -x.mantissa
            retval >>= -x.exponent
            return -retval
        else:
            retval = x.mantissa
            retval >>= -x.mantissa
            return retval + 1

def piGaussLegendre(precision):
    """

    piGaussLegendre computes pi by Gauss-Legendre algorithm.

    """
    def _isCloseEnough(x, y, prec):
        xrat = x.toRational()
        yrat = y.toRational()
        prat = rational.Rational(1, 2**prec)
        return -prat < (xrat - yrat) / xrat < prat
    a = Float(1,0,None)
    b = sqrt(Float(1,-1,None), precision*2)
    t = Float(1, -2, None)
    x = 1
    while not _isCloseEnough(a, b, precision):
        olda = a
        a, b = (a + b) / 2, sqrt(a * b, precision*2)
        t = t - (x * (olda - a) * (olda - a))
        x += x
    return (a + b) ** 2 / (t * 4)

def exp(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    if x < 0:
        return exp(-x, precision).inverse()
    if x == 0:
        return Float(1, 0, None)
    retval = Float(1, 0, precision)
    y = x.copy()
    y.setDefaultPrecision(precision)
    f = i = 1
    oldretval = None
    while oldretval != retval:
        oldretval = retval.copy()
        retval += y / f
        i += 1
        f *= i
        y *= x
    return retval

def sin(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    twopi = piGaussLegendre(2*precision) * 2
    y = x.copy()
    y.setDefaultPrecision(precision)
    if y > twopi:
        y -= floor(y / twopi) * twopi
    elif y < -twopi:
        y += ceil(-y / twopi) * twopi
    retval = Float(0,0,2*precision)
    y2 = y ** 2
    i = f = 1
    sign = -1
    oldretval = None
    while oldretval != retval:
        oldretval = retval.copy()
        if sign == -1:
            retval += y / f
            sign = 1
        else:
            retval -= y / f
            sign = -1
        f *= (i+1)*(i+2)
        i += 2
        y *= y2
    if retval > 1:
        retval = 1
    elif retval < -1:
        retval = -1
    return retval

def cos(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    twopi = piGaussLegendre(2*precision) * 2
    y = x.copy()
    y.setDefaultPrecision(precision)
    if y > twopi:
        y -= floor(y / twopi) * twopi
    elif y < -twopi:
        y += ceil(-y / twopi) * twopi
    retval = Float(0,0,2*precision)
    y2 = y ** 2
    y = Float(1,0,2*precision)
    i = f = 1
    sign = -1
    oldretval = None
    while oldretval != retval:
        oldretval = retval.copy()
        if sign == -1:
            retval += y / f
            sign = 1
        else:
            retval -= y / f
            sign = -1
        f *= i*(i+1)
        i += 2
        y *= y2
    if retval > 1:
        retval = 1
    elif retval < -1:
        retval = -1
    return retval

def tan(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    return sin(x, precision) / cos(x, precision)

def log(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    if x == 1:
        return Float(0, 0, precision)
    if x <= 0:
        raise ValueError, "log(%s) is not defined." % str(x)
    if x > 1:
        return -log(x.inverse(), precision)
    y1 = 1 - x
    y = y1.copy()
    retval = Float(0,0,2*precision)
    i = 1
    oldretval = None
    while retval != oldretval:
        oldretval = retval
        retval += y / i
        y *= y1
        i += 1
    return -retval

def sinh(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    y = x.copy()
    y.setDefaultPrecision(2*precision)
    retval = Float(0,0,2*precision)
    y2 = y ** 2
    i = f = 1
    oldretval = None
    while oldretval != retval:
        oldretval = retval.copy()
        retval += y / f
        f *= (i+1)*(i+2)
        i += 2
        y *= y2
    return retval

def cosh(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    y = x.copy()
    y.setDefaultPrecision(2*precision)
    retval = Float(0, 0, precision)
    y2 = y ** 2
    y = Float(1,0,2*precision)
    i = f = 1
    oldretval = None
    while oldretval != retval:
        oldretval = retval.copy()
        retval += y / f
        f *= i*(i+1)
        i += 2
        y *= y2
    return retval

def tanh(x, precision=doubleprecision):
    if precision < x.precision:
        precision = x.precision
    return sinh(x, precision) / cosh(x, precision)
