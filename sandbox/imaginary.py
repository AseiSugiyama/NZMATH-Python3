"""
imaginary -- Complex numbers and the complex number field.
"""

from __future__ import division
# NZMATH modules
import sandbox.real as real
import nzmath.ring as ring
from sandbox.plugins import MATHMODULE as math, FLOATTYPE as Float, \
     CMATHMODULE as cmath, COMPLEXTYPE as BaseComplex


class Complex(ring.FieldElement):
    """
    Complex is a class for complex numbers.  Each instance has a coupled
    numbers; real and imaginary part of the number.
    """
    def __init__(self, re, im=0):
        ring.FieldElement.__init__(self)
        self.data = BaseComplex(re, im)

    def __add__(self, other):
        if isinstance(other, (Complex, real.Real)):
            result = self.data + other.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = self.data + other
        else:
            return NotImplemented
        return self.__class__(result)

    def __radd__(self, other):
        if isinstance(other, real.Real):
            result = other.data + self.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = other + self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __sub__(self, other):
        if isinstance(other, (Complex, real.Real)):
            result = self.data - other.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = self.data - other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rsub__(self, other):
        if isinstance(other, real.Real):
            result = other.data - self.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = other - self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __mul__(self, other):
        if isinstance(other, (Complex, real.Real)):
            result = self.data * other.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = self.data * other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rmul__(self, other):
        if isinstance(other, real.Real):
            result = other.data * self.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = other * self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __truediv__(self, other):
        if isinstance(other, (Complex, real.Real)):
            result = self.data / other.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = self.data / other
        else:
            return NotImplemented
        return self.__class__(result)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, real.Real):
            result = other.data / self.data
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = other / self.data
        else:
            return NotImplemented
        return self.__class__(result)

    __rdiv__ = __rtruediv__

    def __pow__(self, other):
        if isinstance(other, (Complex, real.Real)):
            result = cmath.pow(self.data, other.data)
        elif isinstance(other, (BaseComplex, Float, int, long)):
            result = cmath.pow(self.data, other)
        return self.__class__(result)

    def __eq__(self, other):
        if isinstance(other, (Complex, real.Real)):
            return self.data == other.data
        else:
            return self.data == other

    def __abs__(self):
        data = abs(self.data)
        return self.__class__(data.real, data.imag)

    def __pos__(self):
        return self.__class__(self.real, self.imag)

    def __neg__(self):
        return self.__class__(-self.real, -self.imag)

    def __nonzero__(self):
        return bool(self.data)

    def __repr__(self):
        return "Complex(" + repr(self.real) + ", " + repr(self.imag) + ")"

    def __str__(self):
        return str(self.real) + " + " + str(self.imag) + "j"

    def inverse(self):
        denominator = self.real ** 2 + self.imag ** 2
        re = self.real / denominator
        im = -self.imag / denominator
        return self.__class__(re, im)

    def conjugate(self):
        """
        complex conjugate
        """
        return self.__class__(self.real, -self.imag)

    def copy(self):
        return self.__class__(self.real, self.imag)

    ## comparisons are prohibited
    def __lt__(self, other):
        raise TypeError("cannot compare complex numbers using <, <=, >, >=")

    def __le__(self, other):
        raise TypeError("cannot compare complex numbers using <, <=, >, >=")

    def __gt__(self, other):
        raise TypeError("cannot compare complex numbers using <, <=, >, >=")

    def __ge__(self, other):
        raise TypeError("cannot compare complex numbers using <, <=, >, >=")

    def arg(self):
        x = self.real
        y = self.imag
        return math.atan2(y, x)

    def __complex__(self):
        return complex(float(self.real), float(self.imag))

    def getRing(self):
        """
        Return the complex field instance.
        """
        return theComplexField

    # properties real/imag
    def _get_real(self):
        return self.data.real

    def _get_imag(self):
        return self.data.real

    real = property(_get_real, None, None, "real component")
    imag = property(_get_imag, None, None, "imaginary component")


class ComplexField (ring.Field):
    """
    ComplexField is a class of the field of complex numbers.
    The class has the single instance 'theComplexField'.
    """

    def __init__(self):
        ring.Field.__init__(self)
        self._one = Complex(Float(1))
        self._zero = Complex(Float(0))

    def __str__(self):
        return "C"

    def __repr__(self):
        return "%s()" % self.__class__.__name__

    def __contains__(self, element):
        reduced = +element
        if reduced in real.theRealField:
            return True
        if isinstance(reduced, complex) or isinstance(reduced, Complex):
            return True
        return False  ## How to know an object be complex ?

    def __eq__(self, other):
        return isinstance(other, ComplexField)

    def __hash__(self):
        return 3

    def createElement(self, seed):
        return Complex(seed)

    def _getOne(self):
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")

    def issubring(self, aRing):
        if isinstance(aRing, ComplexField):
            return True
        elif self.issuperring(aRing):
            return False
        return aRing.issuperring(self)

    def issuperring(self, aRing):
        if isinstance(aRing, ComplexField):
            return True
        elif real.theRealField.issuperring(aRing):
            return True
        return aRing.issubring(self)

    def getCharacteristic(self):
        """
        The characteristic of the complex field is zero.
        """
        return 0


theComplexField = ComplexField()

pi = cmath.pi
e = cmath.e

j = Complex(0, 1)
