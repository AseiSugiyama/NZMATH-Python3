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
        self.mantissa = mantissa
        self.exponent = exponent
        self.precision = precision

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
            elif exponent >= 0 and bits + exponent < precision:
                precision = bits + exponent
            elif exponent < 0 and bits < precision:
                precision = bits
        if mantissa != 0:
            k, odd = vp(mantissa,2)
            mantissa, exponent = odd, exponent + k
        else:
            exponent = 0
        return self.__class__(mantissa, exponent, precision)

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
            elif bits < precision: # underflow
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
            elif bits < precision: # underflow
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

def getNumberOfBits(anInteger):
    """returns the number of binary digits of a given integer."""
    absInteger = abs(anInteger)
    if absInteger == 0:
        return 0
    if absInteger == 1:
        return 1
    bits = max(1, (len(oct(absInteger)) - 3) * 3)
    while (1L << bits) <= absInteger: # 1L can be replaced by 1 someday...
        bits += 1
    return bits
