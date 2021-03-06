from __future__ import division
# standard modules
import itertools
# NZMATH modules
import nzmath.real as real
import nzmath.rational as rational
import nzmath.ring as ring

from nzmath.plugins import MATHMODULE as math, CMATHMODULE as cmath, \
     FLOATTYPE as Float, CHECK_REAL_OR_COMPLEX as check_real_or_complex


class Complex (ring.FieldElement):
    """
    Complex is a class for complex numbers.  Each instance has a coupled
    numbers; real and imaginary part of the number.
    """
    def __init__(self, re, im=None):
        if im:
            self.real = re
            self.imag = im
        elif isinstance(re, complex) or isinstance(re, Complex):
            self.real = re.real
            self.imag = re.imag
        else:
            self.real = re
            self.imag = 0

    def __add__(self, other):
        try:
            re = self.real + other.real
            im = self.imag + other.imag
        except AttributeError:
            if other in real.theRealField:
                re = self.real + other
                im = +self.imag
            else:
                return NotImplemented
        return self.__class__(re, im)

    __radd__ = __add__

    def __sub__(self, other):
        try:
            re = self.real - other.real
            im = self.imag - other.imag
        except AttributeError:
            if other in real.theRealField:
                re = self.real - other
                im = +self.imag
            else:
                return NotImplemented
        return self.__class__(re, im)

    def __rsub__(self, other):
        try:
            re = other.real - self.real
            im = other.imag - self.imag
        except AttributeError:
            if other in real.theRealField:
                re = other - self.real
                im = -self.imag
            else:
                return NotImplemented
        return self.__class__(re, im)

    def __mul__(self, other):
        try:
            re = self.real * other.real - self.imag * other.imag
            im = self.real * other.imag + self.imag * other.real
        except AttributeError:
            if other in real.theRealField:
                re = self.real * other
                im = self.imag * other
            else:
                return NotImplemented
        return self.__class__(re, im)

    __rmul__ = __mul__

    def __div__(self, other):
        try:
            denominator = other.real ** 2 + other.imag ** 2
            re = (self.real * other.real + self.imag * other.imag) / denominator
            im = (self.imag * other.real - self.real * other.imag) / denominator
        except AttributeError:
            if other in real.theRealField:
                re = self.real / other
                im = self.imag / other
            else:
                return NotImplemented
        return self.__class__(re, im)

    __truediv__ = __div__

    def __rdiv__(self, other):
        denominator = self.real ** 2 + self.imag ** 2
        try:
            re = (self.real * other.real + self.imag * other.imag) / denominator
            im = (self.real * other.imag - self.imag * other.real) / denominator
        except AttributeError:
            if other in real.theRealField:
                re = other * self.real / denominator
                im = -self.imag * other / denominator
            else:
                return NotImplemented
        return self.__class__(re, im)

    __rtruediv__ = __rdiv__

    def __pow__(self, other):
        if rational.isIntegerObject(other):
            if other == 0:
                return rational.Integer(1)
            elif other == 1:
                return +self
            elif other < 0:
                return (self**(-other)).inverse()
            elif other == 2:
                return self.__class__(self.real ** 2 - self.imag ** 2, 2 * self.real * self.imag)
            else:
                return rational.Integer(other).actMultiplicative(self)
        return exp(other * log(self))

    def __eq__(self, other):
        try:
            return self.real == other.real and self.imag == other.imag
        except AttributeError:
            if other in real.theRealField:
                return self.imag == 0 and self.real == other
            else:
                return NotImplemented

    def __ne__(self, other):
        try:
            return self.real != other.real or self.imag != other.imag
        except AttributeError:
            if other in real.theRealField:
                return self.imag != 0 or self.real != other
            else:
                return NotImplemented

    def __abs__(self):
        if self.imag == 0:
            return abs(self.real)
        if self.real == 0:
            return abs(self.imag)
        return math.hypot(self.real, self.imag)

    def __pos__(self):
        if self.imag == 0:
            return +self.real
        return self.__class__(+self.real, +self.imag)

    def __neg__(self):
        return self.__class__(-self.real, -self.imag)

    def __nonzero__(self):
        return bool(self.real or self.imag)

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
        return math.atan2(y,x)

    def __complex__(self):
        return complex(float(self.real), float(self.imag))

    def getRing(self):
        """
        Return the complex field instance.
        """
        return theComplexField


class ComplexField (ring.Field):
    """
    ComplexField is a class of the field of real numbers.
    The class has the single instance 'theComplexField'.
    """

    def __init__(self):
        ring.Field.__init__(self)
        self._one = Complex(1)
        self._zero = Complex(0)

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

    def __ne__(self, other):
        return not (self == other)

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
        The characteristic of the real field is zero.
        """
        return 0


theComplexField = ComplexField()

pi = real.pi
e = real.e

j = Complex(0,1)

class RelativeError:
    def __init__(self, numerator, denominator=1):

        self.relativeerrorrange = rational.Rational(numerator, denominator)

    def absoluteerror(self, complexnumeric):
        #r = abs(Complex(re,im))*self.relativeerrorrange
        r = abs(complexnumeric)*self.relativeerrorrange
        return AbsoluteError(r)

    def nearlyEqual(self, x, y):
        """
        Compare two complex numbers with respect to this error,
        whether they are within the given range or not.
        """
        return self.absoluteerror(x).nearlyEqual(x, y)

    def __eq__(self, other):
        if not isinstance(other, RelativeError):
            ###
            ### Note:
            ### all RelativeError comparison methods take a secondary
            ### parameter as class RelativeError only, so if you give
            ### to class AbsoluteError, however, methods are returned
            ### only Boolean, False.
            ###

            #if isinstance(other, AbsoluteError):
            #    if self.absoluteerror(x).absoluteerrorrange == other.absoluteerrorrange :
            #        return True
            #    else:
            #        return False
            #else:
            #    return False
            return False
        if self.relativeerrorrange == other.relativeerrorrange :
            return True
        return False

    def __lt__(self, other):
        if not isinstance(other, RelativeError):
            return False
        if self.relativeerrorrange < other.relativeerrorrange :
            return True
        return False

    def __le__(self, other):
        if not isinstance(other, RelativeError):
            return False
        if self.relativeerrorrange <= other.relativeerrorrange :
            return True
        return False

    def __gt__(self, other):
        if not isinstance(other, RelativeError):
            return False
        if self.relativeerrorrange > other.relativeerrorrange :
            return True
        return False

    def __ge__(self, other):
        if not isinstance(other, RelativeError):
            return False
        if self.relativeerrorrange >= other.relativeerrorrange :
            return True
        return False

    def __div__(self, other):
        return self.__class__(self.relativeerrorrange / other)

    __truediv__ = __div__

class AbsoluteError:
    def __init__(self, numeric):
        """
        AbsoluteError(x) defines absolute error number attribute
        absoluteerrorrange from x. x must be a positive value.
        """
        self.absoluteerrorrange = abs(numeric)

    def nearlyEqual(self, x, y):
        """
        Compare two complex numbers with respect to this error,
        whether they are within the given range or not.
        """
        return abs(x-y) < self.absoluteerrorrange

    def __div__(self, other):
        return self.__class__(self.absoluteerrorrange / other)

    __truediv__ = __div__

### function rewrite
defaultError = RelativeError(1, 2 ** 53)

###
### Note:
### so because of class RelativeError design, follows accept
### class AbsoluteError from user assign parameter, and if
### accept AbsoluteError, not use cmath module.
###

def exp(x, err=defaultError):
    """
    exp(x [,err]) is the exponential function.
    """
    try:
        rx = rational.Rational(x)
        if isinstance(err, RelativeError):
            _err = real.RelativeError(0, err.relativeerrorrange)
        elif isinstance(err, AbsoluteError):
            _err = real.AbsoluteError(0, err.absoluteerrorrange)
        return real.exp(rx, _err)
    except TypeError:
        pass
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        # divide real part and imaginary part
        if isinstance(err, RelativeError):
            _err = real.RelativeError(0, err.relativeerrorrange, 2)
        elif isinstance(err, AbsoluteError):
            _err = real.AbsoluteError(0, err.absoluteerrorrange, 2)
        radius = real.exp(x.real, _err)
        if isinstance(err, RelativeError):
            _err = RelativeError(err.relativeerrorrange / 2)
        elif isinstance(err, AbsoluteError):
            _err = AbsoluteError(err.absoluteerrorrange / 2)
        arg = expi(x.imag, _err)
        return radius * arg
    else:
        return Complex(cmath.exp(complex(x.real,x.imag)))

def expi(x, err=defaultError):
    """
    expi(x [,err]) returns exp(i * x) where i is the imaginary unit
    and x must be a real number.
    """
    if x == 0:
        return rational.Integer(1)
    if isinstance(err, RelativeError):
        _err = real.RelativeError(0, err.relativeerrorrange, 2)
    elif isinstance(err, AbsoluteError):
        _err = real.AbsoluteError(0, err.absoluteerrorrange, 2)
    re = real.cos(x, _err)
    im = real.sin(x, _err)
    return Complex(re, im)

def log(x, err=defaultError):
    """
    log(x [,err]) returns the natural logarithm of x. There is one
    branch cut, from 0 along the negative real axis to -infinity,
    continuous from above.
    """
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        if isinstance(err, RelativeError):
            _err = real.RelativeError(0, err.relativeerrorrange, 2)
        elif isinstance(err, AbsoluteError):
            _err = real.AbsoluteError(0, err.absoluteerrorrange, 2)
        if x in real.theRealField:
            x = +x
            if x > 0:
                return real.log(x, err=_err)
            elif x < 0:
                return Complex(real.log(abs(x), _err), real.pi(_err))
        return Complex(real.log(abs(x), err=_err), real.atan2(x.imag, x.real, _err))
    else:
        return Complex(cmath.log(complex(x.real, x.imag)))

class ExponentialPowerSeries:
    """
    A class for exponential power serieses, whose n-th term has form:
      a_n * x ** n / n!
    """
    def __init__(self, iterator):
        """
        ExponentialPowerSeries(iterator) constructs an exponential
        power series with coefficient generated by the given iterator,
        which can be an infinite iterator.
        """
        self.iterator = iterator
        self.dirtyflag = False

    def terms(self, x):
        """
        Generator of terms of series with assigned x value.
        """
        if x == 0:
            yield self.iterator.next()
        else:
            f = rational.Integer(1)
            i = 0
            y = rational.Integer(1)
            for an in self.iterator:
                yield an * y / f
                y *= x
                i += 1
                f *= i

    def __call__(self, x, maxerror):
        if self.dirtyflag:
            raise Exception, 'ExponentialPowerSeries cannot be called more than once'
        self.dirtyflag = True
        value = oldvalue = 0
        for t in self.terms(x):
            if not t:
                continue
            value += t
            if maxerror.nearlyEqual(value, oldvalue):
                return value
            oldvalue = +value

def sin(z, err=defaultError):
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        series = ExponentialPowerSeries(itertools.cycle((0,rational.Integer(1),0,rational.Integer(-1))))
        return series(z, err)
    else:
        return Complex(cmath.sin(complex(z.real,z.imag)))

def cos(z, err=defaultError):
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        series = ExponentialPowerSeries(itertools.cycle((rational.Integer(1),0,rational.Integer(-1), 0)))
        return series(z, err)
    else:
        return Complex(cmath.cos(complex(z.real,z.imag)))

def tan(z, err=defaultError):
    return sin(z, err) / cos(z,err)

def sinh(z, err=defaultError):
    if z == 0:
        return rational.Integer(0)
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        series = ExponentialPowerSeries(itertools.cycle((0,rational.Integer(1),)))
        return series(z, err)
    else:
        return Complex(cmath.sinh(complex(z.real,z.imag)))

def cosh(z, err=defaultError):
    if z == 0:
        return rational.Integer(1)
    if (defaultError >= err) or isinstance(err, AbsoluteError):
        series = ExponentialPowerSeries(itertools.cycle((rational.Integer(1),0,)))
        return series(z, err)
    else:
        return Complex(cmath.cosh(complex(z.real,z.imag)))

def tanh(z, err=defaultError):
    return sinh(z, err) / cosh(z, err)


def atanh(z, err=defaultError):
    return log((1+z)/(1-z), err=err) / 2


def sqrt(z, err=defaultError):
    return real.sqrt(abs(z))*expi(z.arg()/2)

