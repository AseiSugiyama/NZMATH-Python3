from __future__ import division, generators
import operator
import math
from prime import vp as _vp
import rational

"""

The module `real' provides arbitrary precision real numbers and their
utilities.  The functions provided are corresponding to the `math'
standard module.

"""

doubleprecision = 53

class Float:
    """

    Float is an arbitrary precision real number class.  A number is
    represented as mantissa * (2**exponent), where mantissa is an odd
    integer.  If precision is set to None, it means the number has
    infinite precision.

    """
    def __init__(self, mantissa, exponent=0, precision=None):
        if isinstance(mantissa, rational.Rational):
            aRational = mantissa
            if not precision:
                if mantissa == 0:
                    mantissa, exponent, precision = 0,0,None
                v, t = _vp(aRational.denominator,2)
                if t != 1:
                    raise ValueError, "precision must be a positive integer."
                mantissa, exponent, precision = aRational.numerator, -v, None
                bits = getNumberOfBits(aRational.denominator)
                mantissa = (aRational.numerator * 2 ** bits) // aRational.denominator
                exponent = -bits
            else:
                bits = getNumberOfBits(aRational.denominator)
                mantissa = (aRational.numerator * 2**(bits + precision)) // aRational.denominator
                exponent = -(bits + precision)
        if isinstance(mantissa, float):
            mantissa, exponent = long(math.frexp(mantissa)[0] * 2 ** doubleprecision), math.frexp(mantissa)[1] - doubleprecision
            if not precision:
                precision = doubleprecision
        if isinstance(mantissa, Float):
            mantissa, exponent, precision = mantissa.mantissa, mantissa.exponent, mantissa.precision
        if isinstance(mantissa, FloatConstant):
            mantissa, exponent, precision = mantissa.cache.mantissa, mantissa.cache.exponent, mantissa.precision
        if mantissa != 0:
            k, odd = _vp(mantissa,2)
            self.mantissa, self.exponent = odd, exponent + k
        else:
            self.mantissa, self.exponent = 0, 0
        self.precision = precision
        if not self.precision:
            self.defaultPrecision = max((doubleprecision, getNumberOfBits(mantissa)))
        else:
            self.defaultPrecision = self.precision

    def __add__(self, other):
        if not isinstance(other, Float):
            try:
                return self + self.__class__(other, 0, self.precision)
            except:
                return NotImplemented
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
            k, odd = _vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __radd__(self, other):
        if not isinstance(other, Float):
            try:
                return self.__class__(other, 0, self.precision) + self
            except:
                return NotImplemented

    def __sub__(self, other):
        if not isinstance(other, Float):
            try:
                return self - self.__class__(other, 0, self.precision)
            except:
                return NotImplemented
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
            k, odd = _vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __rsub__(self, other):
        if not isinstance(other, Float):
            try:
                return self.__class__(other, 0, self.precision) - self
            except:
                return NotImplemented

    def __mul__(self, other):
        if rational.isIntegerObject(other):
            if other == 0:
                return 0
            v2, c2 = _vp(other, 2)
            return self.__class__(self.mantissa * c2,
                                  self.exponent + v2,
                                  self.precision)
        elif not isinstance(other, Float):
            try:
                return self * self.__class__(other, 0, self.precision)
            except:
                return NotImplemented
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
            k, odd = _vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

    def __rmul__(self, other):
        if rational.isIntegerObject(other):
            if other == 0:
                return 0
            v2, c2 = _vp(other, 2)
            return self.__class__(self.mantissa * c2,
                                  self.exponent + v2,
                                  self.precision)
        elif not isinstance(other, Float):
            try:
                return self.__class__(other, 0, None) * self
            except:
                return NotImplemented

    def __div__(self, other):
        """

        division: The result is less than or equal to the exact
        quotient as absolute value.
        
        """
        if other == 0:
            raise ZeroDivisionError, "Float division by zero"
        if rational.isIntegerObject(other):
            v2, c2 = _vp(other, 2)
            retval = self.__class__(self.mantissa,
                                    self.exponent - v2,
                                    self.precision)
            if c2 > 1:
                return retval / self.__class__(c2, 0, self.precision)
            else:
                return retval
        elif not isinstance(other, Float):
            try:
                return self / self.__class__(other, 0, self.precision)
            except:
                return NotImplemented
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
            k, mantissa = _vp(quotient,2)
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
        if not isinstance(other, Float):
            try:
                return self.__class__(other, 0, self.precision) / self
            except:
                return NotImplemented

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
        # power is not in Z
        if self < 0:
            raise ValueError, "negative number cannot be raised to a fractional power"
        return exp(other * log(self))

    def __neg__(self):
        return self.__class__(-self.mantissa, self.exponent, self.precision)

    def __pos__(self):
        return self.__class__(+self.mantissa, self.exponent, self.precision)

    def __abs__(self):
        return self.__class__(abs(self.mantissa), self.exponent, self.precision)

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

    def __lshift__(self, offset):
        return self.__class__(self.mantissa, self.exponent + offset, self.precision)

    def __rshift__(self, offset):
        return self.__class__(self.mantissa, self.exponent - offset, self.precision)

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
            if self.precision > 80:
                digits = self.precision // 4
            else:
                digits = 20
            if -self.exponent-1 > digits:
                end = -self.exponent-1 -digits
            else:
                end = 0
            for i in range(-self.exponent-1, end, -1):
                q,r = divmod(r*5, 2**i)
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

class FloatConstant:
    """

    FloatConstant provides constant-like behavior for Float
    calculation context.  It caches the constant value and re-computes
    for more precision by request.

    example:
    >>> pi = FloatConstant(piGaussLegendre)
    >>> print pi
    3.14159265358979
    >>> pi + 1
    4.14159265358979
    >>> pi(100) # for 100 bit precision
    3.1415926535897932384626433832795

    """
    def __init__(self, getValue, precision=doubleprecision):
        """

        The first argument must be a function which computes the
        constant with an argument specifies precision.
        The second argument can be used to set the default precision.

        """
        self.getValue = getValue
        self.precision = precision
        self.cache = self.getValue(self.precision)

    def __call__(self, precision):
        """

        Return the value with precision at least the given precision.

        """
        if self.precision < precision:
            self.cache = self.getValue(precision)
            self.precision = precision
        return self.cache

    # delegations
    def __add__(self, other):
        return self.cache.__add__(other)

    def __radd__(self, other):
        return self.cache.__radd__(other)

    def __sub__(self, other):
        return self.cache.__sub__(other)

    def __rsub__(self, other):
        return self.cache.__rsub__(other)

    def __mul__(self, other):
        return self.cache.__mul__.other

    def __rmul__(self, other):
        return self.cache.__rmul__(other)

    def __div__(self, other):
        return self.cache.__div__(other)

    def __rdiv__(self, other):
        return self.cache.__rdiv__(other)

    def __truediv__(self, other):
        return self.cache.__truediv__(other)

    def __rtruediv__(self, other):
        return self.cache.__rtruediv__(other)

    def __divmod__(self, other):
        return self.cache.__divmod__(other)

    def __rdivmod__(self, other):
        return self.cache.__rdivmod__(other)

    def __mod__(self, other):
        return self.cache.__mod__(other)

    def __rmod__(self, other):
        return self.cache.__rmod__(other)

    def __pos__(self):
        return self.cache.__pos__()

    def __neg__(self):
        return self.cache.__neg__()

    def __abs__(self):
        return self.cache.__neg__()

    def toRational(self):
        return self.cache.toRational()

    def inverse(self):
        return self.cache.__rdiv__(Float(1,0,None))

    def __pow__(self, other, dummy=None):
        return self.cache.__pow__(other)

    def __gt__(self, other):
        return self.cache.__gt__(other)

    def __ge__(self, other):
        return self.cache.__ge__(other)

    def __eq__(self, other):
        return self.cache.__eq__(other)

    def __ne__(self, other):
        return self.cache.__ne__(other)

    def __le__(self, other):
        return self.cache.__le__(other)

    def __lt__(self, other):
        return self.cache.__lt__(other)

    def __repr__(self):
        return repr(self.cache)

    def __str__(self):
        return str(self.cache)

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
        v, t = _vp(aRational.denominator,2)
        if t != 1:
            raise ValueError, "precision must be a positive integer."
        return (aRational.numerator, -v, None)
    bits = getNumberOfBits(aRational.denominator)
    mantissa = (aRational.numerator * 2**(bits + precision)) // aRational.denominator
    exponent = -(bits + precision)
    return Float(mantissa, exponent, precision)

def sqrt(aFloat, precision=doubleprecision):
    """

    sqrt(x [,precision]) returns the positive square root of real number x.

    """
    def _isCloseEnough(x, y, prec):
        xrat = x.toRational()
        yrat = y.toRational()
        prat = rational.Rational(1, 2**prec)
        return -prat < (xrat - yrat) / xrat < prat
    if not isinstance(aFloat, Float):
        aFloat = Float(aFloat)
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
        t -= (x * (olda - a) * (olda - a))
        x *= 2
    return (a + b) ** 2 / (t * 4)

def sum(iter, precision):
    """

    sum(iter, precision) returns the sum of the series given by iter,
    which must be an iterator instance.

    The implementation assumes that too small term does not appear
    in the sequence until the sum converges.

    """
    about = Float(0.0)
    termList = []
    for term in iter:
        about = about + term
        termList.append(term)
        if abs(term) < abs(about) / 2**(2*precision):
            break
    termList.reverse()
    return reduce(operator.add, termList, 0)

def exp(x, precision=doubleprecision):
    """

    exp(x [,precision]) returns e raised to the power of x.  If
    precision is not specified, the obtained value is as accurate as
    one obtained with math.exp.

    """
    def exp_iter(xx, pp):
        """

        exp_iter is a generator. exp_iter(x, precision) generates the
        terms of Taylor expansion series of exp with x.

        """
        yield 1
        y = Float(xx, 0, pp)
        f = i = 1
        yield y
        while 1:
            i += 1
            f *= i
            y *= xx
            yield (y / f)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    if x == 0:
        return Float(1, 0, None)
    if x < 0:
        return exp(-x, precision).inverse()
    t = 0
    while x > 1:
        x /= 2
        t += 1
    if t > 0:
        return sum(exp_iter(x, precision), precision) ** (2 ** t)
    return sum(exp_iter(x, precision), precision)

def sin(x, precision=doubleprecision):
    """

    sin(x [,precision]) returns the sine of x.

    """
    def sin_iter(xx, pp):
        """

        sin_iter is a generator. sin_iter(x, precision) generates the
        terms of Taylor expansion series of sine with x.

        """
        yield xx
        y = xx
        y2 = xx ** 2
        i = f = 1
        while 1:
            f *= (i+1)*(i+2)
            i += 2
            y *= y2
            yield (-y / f)
            f *= (i+1)*(i+2)
            i += 2
            y *= y2
            yield (y / f)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    twopi = pi(2*precision) * 2
    y = Float(x, 0, precision)
    if y > twopi:
        y -= floor(y / twopi) * twopi
    elif y < -twopi:
        y += ceil(-y / twopi) * twopi
    retval = sum(sin_iter(y, precision), precision)
    if retval > 1:
        retval = Float(1, 0, precision)
    elif retval < -1:
        retval = Float(-1, 0, precision)
    return retval

def cos(x, precision=doubleprecision):
    """

    cos(x [,precision]) returns the cosine of x.

    """
    def cos_iter(xx, pp):
        """

        cos_iter is a generator. cos_iter(x, precision) generates the
        terms of Taylor expansion series of cosine with x.

        """
        yield 1
        y2 = xx ** 2
        t = Float(1, 0, precision)
        i = f = 1
        while 1:
            f *= i*(i+1)
            i += 2
            t *= y2
            yield (-t / f)
            f *= i*(i+1)
            i += 2
            t *= y2
            yield (t / f)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    twopi = pi(2*precision) * 2
    y = Float(x, 0, precision)
    if y > twopi:
        y -= floor(y / twopi) * twopi
    elif y < -twopi:
        y += ceil(-y / twopi) * twopi
    retval = sum(cos_iter(y, precision), precision)
    if retval > 1:
        retval = Float(1, 0, precision)
    elif retval < -1:
        retval = Float(-1, 0, precision)
    return retval

def tan(x, precision=doubleprecision):
    """

    tan(x [,precision]) returns the tangent of x.

    """
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    return sin(x, precision) / cos(x, precision)

def log(x, precision=doubleprecision):
    """

    log(x [,precision]) returns the logarithm of positive real number x.

    """
    def log_iter(xx, pp):
        """

        log_iter is a generator. log_iter(x, precision) generates the
        terms of Taylor expansion series of log with x, but all negated.

        """
        y = Float(xx, 0, precision)
        yield y
        i = 1
        while 1:
            y *= xx
            i += 1
            yield (y / i)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    if x <= 0:
        raise ValueError, "log(%s) is not defined." % str(x)
    x = Float(x)
    shift = 0
    if x >= 2:
        while x >= 2:
            x /= 2
            shift += 1
    elif x <= Float(1, -1):
        while x <= Float(1, -1):
            x *= 2
            shift -= 1
    if x == 1:
        return shift * Log2(precision)
    if x > 1:
        return -log(x.inverse(), precision) + shift * Log2(precision)
    y1 = 1 - x
    retval = sum(log_iter(y1, precision), precision)
    return -retval + shift * Log2(precision)

def _log2(precision=doubleprecision):
    """

    _log2([precision]) returns the logarithm of 2.

    """
    def log_iter2(pp):
        """

        log_iter_half is a generator. log_iter_half(precision)
        generates the terms of Taylor expansion series of logarithm of
        2.

        """
        y = Float(1,-1,2*pp)
        yield y
        i = 1
        while 1:
            y /= 2
            i += 1
            yield (y / i)
    return sum(log_iter2(precision), precision)

def sinh(x, precision=doubleprecision):
    """

    sinh(x [,precision]) returns the hyperbolic sine of x.

    """
    def sinh_iter(xx, pp):
        yield xx
        y2 = xx ** 2
        i = f = 1
        while 1:
            f *= (i+1)*(i+2)
            xx *= y2
            i += 2
            yield (xx / f)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    y = Float(x, 0, precision)
    return sum(sinh_iter(y, precision), precision)

def cosh(x, precision=doubleprecision):
    """

    cosh(x [,precision]) returns the hyperbolic cosine of x.

    """
    def cosh_iter(xx, pp):
        yield 1
        x2 = xx ** 2
        y = Float(1, 0 ,2*precision)
        i = f = 1
        while 1:
            f *= i*(i+1)
            y *= x2
            i += 2
            yield (y / f)
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    return sum(cosh_iter(x,precision), precision)

def tanh(x, precision=doubleprecision):
    """

    tanh(x [,precision]) returns the hyperbolic tangent of x.

    """
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    return sinh(x, precision) / cosh(x, precision)

def asin(x, precision=doubleprecision):
    """

    asin(x [,precision]) returns arc sine of x.

    """
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    if x > 1 or x < -1:
        raise ValueError, "%s is not in the range [-1, 1]." % str(x)
    if x < 0:
        return -asin(-x)
    u = sqrt(Float(1, -1, precision), precision)
    if x > u:
        return pi(precision) / 2 - asin(sqrt(1-x**2))
    y = x.copy()
    y2 = y ** 2
    i = 2
    series = [y]
    eps = Float(1, -2*precision)
    while series[-1] > eps:
        y *= y2
        i += 2
        series.append(y * rational.Rational(reduce(operator.mul, range(1, i-1, 2), 1), reduce(operator.mul, range(2, i, 2), i-1)))
    series.reverse()
    retval = reduce(operator.add, series, Float(0, 0, 2*precision))
    return retval

def acos(x, precision=doubleprecision):
    """

    acos(x [,precision]) returns arc cosine of x.

    """
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    if x > 1 or x < -1:
        raise ValueError, "%s is not in the range [-1, 1]." % str(x)
    if x == 0:
        return pi(precision) / 2
    y = sqrt(1 - x ** 2)
    if x > 0:
        return asin(y)
    else:
        return pi(precision) + asin(-y)

def atan(x, precision=doubleprecision):
    """

    atan(x [,precision]) returns arc tangent of x.

    """
    if isinstance(x, Float) and precision < x.precision:
        precision = x.precision
    if x < 0:
        # atan(x) = -atan(-x)
        return -atan(-x, precision)
    elif x > 1:
        # atan(x) = pi/2 - atan(1/x)
        return pi(2*precision) / 2 - atan(x.inverse(), precision)
    elif x == 1:
        return pi(precision) / 4
    i = 1
    y = x.copy()
    y2 = y ** 2
    series = [y]
    eps = Float(1, -2*precision)
    while abs(series[-1]) > eps:
        i += 2
        y *= y2
        if i&3 == 1:
            series.append(y / i)
        else:
            series.append(-y / i)
    series.reverse()
    retval = reduce(operator.add, series, 0)
    return retval

def atan2(y, x, precision=doubleprecision):
    """

    atan2(x, y [,precision]) returns the arc tangent of y/x.
    Unlike atan(y/x), the signs of both x and y are considered.

    It is unrecomended to obtain the value of pi with atan2(0,1).

    """
    if x > 0 and y > 0:
        return atan(x/y)
    elif x > 0 and y < 0:
        return pi(precision) * 2 + atan(x/y)
    elif x < 0:
        return pi(precision) + atan(x/y)
    elif x == 0 and y > 0:
        return pi(precision) / 2
    elif x == 0 and y < 0:
        return -pi(precision) / 2
    return Float(0, 0, precision)

def hypot(x, y, precision=doubleprecision):
    """

    hypot(x, y [,precision]) returns sqrt(x**2 + y**2).

    """
    return sqrt(x**2 + y**2, precision)


class RealField:
    """

    RealField is a class of the field of real numbers.
    The class has the single instance 'theRealField'.

    """

    def __contains__(self, element):
        reduced = +element
        if reduced in rational.theRationalField:
            return 1
        if isinstance(reduced, float) or isinstance(reduced, Float):
            return 1
        return 0  ## How to know a number is real ?

theRealField = RealField()

pi = FloatConstant(piGaussLegendre)
e = FloatConstant(lambda precision: exp(1, precision))
Log2 = FloatConstant(lambda precision: _log2(precision))
