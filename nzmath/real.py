from prime import vp
import rational

"""

The module `real' provides arbitrary precision real numbers and their
utilities.

"""

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
            self.defaultPrecision = max((53, getNumberOfBits(mantissa)))
        else:
            self.defaultPrecesion = self.precision

    def __add__(self, other):
        if rational.isIntegerObject(other):
            return self + self.__class__(other, 0, None)
        # adjust with precision
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
            sbits, obits = getNumberOfBits(self.mantissa), getNumberOfBits(other.mantissa)
            if sbits < precision:
                smantissa = self.mantissa << (precision - sbits)
                sexponent = self.exponent - (precision - sbits)
            else:
                smantissa = self.mantissa
                sexponent = self.exponent
            if obits < precision:
                omantissa = other.mantissa << (precision - obits)
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
            mantissa = smantissa + (omantissa << (oexponent - exponent))
        elif sexponent > oexponent:
            exponent = oexponent
            mantissa = (smantissa << (sexponent - exponent)) + omantissa
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
                smantissa = self.mantissa << (precision - sbits)
                sexponent = self.exponent - (precision - sbits)
            else:
                smantissa = self.mantissa
                sexponent = self.exponent
            if obits < precision:
                omantissa = other.mantissa << (precision - obits)
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
            mantissa = smantissa - (omantissa << (oexponent - exponent))
        elif sexponent > oexponent:
            exponent = oexponent
            mantissa = (smantissa << (sexponent - exponent)) - omantissa
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
            return self / self.__class__(other, 0, None)
        elif isinstance(other, rational.Rational):
            return self / self.__class__(other, 0, None)
        exponent = self.exponent - other.exponent
        if self.precision or other.precision:
            precision = min( filter(None, (self.precision, other.precision)) )
        elif other.mantissa != 1:
            precision = self.defaultPrecision
        if self.mantissa < 0:
            sign = -1
            mantissa = -self.mantissa
        else:
            sign = 1
            mantissa = self.mantissa
        bits = getNumberOfBits(other.mantissa)
        mantissa *= 2**(bits + precision)
        exponent -= bits + precision
        quotient, remainder = divmod(mantissa, other.mantissa)
        bits = getNumberOfBits(quotient)
        # normalize
        if precision:
            if bits > precision:
                quotient >>= (bits - precision)
                exponent += (bits - precision)
            elif exponent > 0 and bits + exponent < precision: #underflow
                precision = bits + exponent
            elif exponent <= 0 and bits < precision: # underflow
                precision = bits
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

    def __neg__(self):
        return self.__class__(-mantissa, exponent, precision)

    def __pos__(self):
        return self.__class__(+mantissa, exponent, precision)

    def setDefaultPrecision(self, newPrecision):
        self.defaultPrecision = newPrecision

def getNumberOfBits(anInteger):
    """returns the number of binary digits of a given integer."""
    absInteger = abs(anInteger)
    if absInteger == 0:
        return 0
    if absInteger == 1:
        return 1
    bits = 1
    scale = 2L # 2L can be replaced by 2 someday...
    while scale <= absInteger:
        bits += 1
        scale <<= 1
    return bits

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
