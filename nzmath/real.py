"""
real -- real numbers and the real number field.

The module real provides arbitrary precision real numbers and their
utilities.  The functions provided are corresponding to the math
standard module.
"""

from __future__ import division
import itertools
import warnings

import nzmath.arith1 as arith1
import nzmath.rational as rational
import nzmath.ring as ring
from nzmath.plugins import MATHMODULE as math, FLOATTYPE as Float, \
     CHECK_REAL_OR_COMPLEX as check_real_or_complex


class Real(ring.FieldElement):
    """
    Real is a class of real. 
    This class is only for consistency for other Ring object.
    """

    convertable = (Float, int, long, rational.Rational)

    def __init__(self, value):
        """
        value will be wrapped in Float.
        """
        ring.FieldElement.__init__(self)
        if isinstance(value, rational.Rational):
            self.data = value.toFloat()
        else:
            self.data = Float(value)

    def __add__(self, other):
        if isinstance(other, Real):
            result = self.data + other.data
        elif isinstance(other, self.convertable):
            result = self.data + other
        else:
            return NotImplemented
        return self.__class__(result)

    def __radd__(self, other):
        if isinstance(other, self.convertable):
            result = other + self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __sub__(self, other):
        if isinstance(other, Real):
            result = self.data - other.data
        elif isinstance(other, self.convertable):
            result = self.data - other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rsub__(self, other):
        if isinstance(other, self.convertable):
            result = other - self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __mul__(self, other):
        if isinstance(other, Real):
            result = self.data * other.data
        elif isinstance(other, self.convertable):
            result = self.data * other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rmul__(self, other):
        if isinstance(other, self.convertable):
            result = other * self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __truediv__(self, other):
        if isinstance(other, Real):
            result = self.data / other.data
        elif isinstance(other, self.convertable):
            result = self.data / other
        else:
            return NotImplemented
        return self.__class__(result)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, self.convertable):
            result = other / self.data
        else:
            return NotImplemented
        return self.__class__(result)

    __rdiv__ = __rtruediv__

    def __pow__(self, other):
        if isinstance(other, Real):
            result = math.pow(self.data, other.data)
        elif isinstance(other, self.convertable):
            result = math.pow(self.data, other)
        return result

    def __eq__(self, other):
        if isinstance(other, Real):
            return self.data == other.data
        elif isinstance(other, self.convertable):
            return self.data == other
        else:
            return NotImplemented

    def getRing(self):
        """
        Return the real field instance.
        """
        return theRealField


class RealField(ring.Field):
    """
    RealField is a class of the field of real numbers.
    The class has the single instance 'theRealField'.
    """

    def __init__(self):
        ring.Field.__init__(self)
        self._one = Real(1)
        self._zero = Real(0)

    def __str__(self):
        return "R"

    def __repr__(self):
        return "%s()" % (self.__class__.__name__, )

    def __contains__(self, element):
        if isinstance(element, Constant):
            element = element.cache
        if isinstance(element, (int, long, float, Float, Real, rational.Rational)):
            return True
        else:
            try:
                if check_real_or_complex(element):
                    return True
            except TypeError:
                if hasattr(element, 'conjugate'):
                    return element == element.conjugate()
                pass
        if hasattr(element, 'getRing') and element.getRing().issubring(self):
            return True
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 2

    # property one
    def _getOne(self):
        "getter for one"
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    # property zero
    def _getZero(self):
        "getter for zero"
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")

    def issubring(self, aRing):
        if isinstance(aRing, RealField):
            return True
        elif self.issuperring(aRing):
            return False
        return aRing.issuperring(self)

    def issuperring(self, aRing):
        if isinstance(aRing, RealField):
            return True
        elif rational.theRationalField.issuperring(aRing):
            return True
        return aRing.issubring(self)

    def createElement(self, seed):
        return Float(seed)

    def getCharacteristic(self):
        """
        The characteristic of the real field is zero.
        """
        return 0


### function rewrite
class ExponentialPowerSeries(object):
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
            yield rational.Rational(self.iterator.next())
        else:
            i = 0
            r = rational.Rational(1, 1)
            for an in self.iterator:
                yield an * r
                i += 1
                r *= rational.Rational(x, i)

    def __call__(self, x, maxerror):
        if self.dirtyflag:
            raise Exception, 'ExponentialPowerSeries cannot be called more than once'
        self.dirtyflag = True
        value, oldvalue = rational.Rational(0), rational.Rational(0)
        maxDenom = minNumer = 0
        if isinstance(maxerror, RelativeError):
            for t in self.terms(x):
                if not t:
                    continue
                if not maxDenom:
                    value += t
                    maxDenom = (maxerror.relativeerrorrange.denominator * value.denominator) ** 2
                elif value.denominator < maxDenom:
                    value += t
                    if maxerror.nearlyEqual(value, oldvalue):
                        break
                else:
                    if not minNumer:
                        minNumer = maxerror.relativeerrorrange.numerator * abs(value.numerator) // maxerror.relativeerrorrange.denominator
                    approx = t.numerator * value.denominator // t.denominator
                    value.numerator += approx
                    if abs(approx) < minNumer:
                        break
                oldvalue = +value
        else:
            for t in self.terms(x):
                if not t:
                    continue
                if not maxDenom:
                    value += t
                    maxDenom = (maxerror.absoluteerrorrange.denominator * value.denominator) ** 2
                elif value.denominator < maxDenom:
                    value += t
                else:
                    if not minNumer:
                        minNumer = maxerror.absoluteerrorrange.numerator * value.numerator // maxerror.absoluteerrorrange.denominator
                    approx = t.numerator * value.denominator // t.denominator
                    value.numerator += approx
                    if abs(approx) < minNumer:
                        break
                oldvalue = +value
        return value


defaultError = RelativeError(0, 1, 2 ** 53)

def exp(x, err=defaultError):
    """
    Return exponential of x.
    """
    if err <= defaultError:
        reduced = rational.Rational(x)
        if reduced < 0:
            reverse = -1
            reduced = -reduced
        else:
            reverse = 1
        i = 0
        while reduced >= 2:
            reduced /= 2
            i += 1
        if reduced == 0:
            retval = rational.Integer(1)
        else:
            series = ExponentialPowerSeries(itertools.cycle((rational.Integer(1),)))
            retval = series(reduced, err)
        if i > 0:
            retval **= 2 ** i
        if reverse < 0:
            retval = 1 / retval
    else:
        retval = rational.Rational(math.exp(x))
    return retval

def sqrt(x, err=defaultError):
    """
    sqrt(x [,err]) returns the positive square root of real number x.
    """
    rx = rational.Rational(x)
    if rx.numerator < 0:
        raise ValueError("negative number is passed to sqrt")
    if rx.numerator == 0:
        return rational.Integer(0)
    if err <= defaultError:
        n = rx.denominator * rx.numerator
        rt = rational.Rational(arith1.floorsqrt(n), rx.denominator)
        newrt = (rt + rx / rt) / 2
        while not err.nearlyEqual(rt, newrt):
            rt = newrt
            newrt = (rt + rx / rt) / 2
    else:
        newrt = rational.Rational(math.sqrt(x.toFloat()))
    return newrt

def log(x, base=None, err=defaultError):
    """
    log(x) returns logarithm of a positive number x.  If an additional
    argument base is given, it returns logarithm of x to the base.
    """
    if isinstance(x, complex):
        raise TypeError("real.log is not for complex numbers.")
    if x <= 0:
        raise ValueError("log is not defined for %s" % str(x))
    if err <= defaultError:
        if base:
            d = log(base, err=err)
        else:
            d = 1
        rx = rational.Rational(x)
        upper = rational.Rational(4, 3)
        lower = rational.Rational(2, 3)
        shift = 0
        while rx > upper:
            rx /= 2
            shift += 1
        while rx < lower:
            rx *= 2
            shift -= 1
        if rx == 1:
            return shift * _log2(err) / d
        value = oldvalue = 0
        for term in log1piter(rx - 1):
            value += term
            if err.nearlyEqual(value, oldvalue):
                break
            oldvalue = +value
        if shift != 0:
            return (value + shift * _log2(err)) / d
    else:
        if base:
            value = rational.Rational(math.log(x, base))
        else:
            value = rational.Rational(math.log(x))
        return value

def log1piter(xx):
    " iterator for log(1+x)."
    d = 1
    positive = True
    t = rational.Rational(xx)
    yield t
    while True:
        d += 1
        positive = not positive
        t *= xx
        if positive:
            yield (t / d)
        else:
            yield (-t / d)

def _log2(err=defaultError):
    """
    _log2([err]) returns the logarithm of 2.
    """
    def log_iter_half():
        """
        log_iter_half generates the terms of Taylor expansion series
        of logarithm of 1/2.
        """
        d = 1
        t = rational.Rational(1, 2)
        yield t
        while True:
            t /= 2
            d += 1
            yield (t / d)

    value = oldvalue = 0
    for term in log_iter_half():
        value += term
        if err.nearlyEqual(value, oldvalue):
            return value
        oldvalue = +value

def piGaussLegendre(err=defaultError):
    """
    piGaussLegendre computes pi by Gauss-Legendre algorithm.
    """
    if isinstance(err, RelativeError):
        _err = err.absoluteerror(3.1415926535897932)
    else:
        _err = err
    werr = AbsoluteError(0, _err.absoluteerrorrange ** 2)
    maxdenom = int(1 / werr.absoluteerrorrange) * 2
    a = rational.Integer(1)
    b = (1 / sqrt(rational.Rational(2), werr)).trim(maxdenom)
    t = rational.Rational(1, 4)
    x = 1
    while not _err.nearlyEqual(a, b):
        a, b, c = (a + b) / 2, sqrt(a * b, werr).trim(maxdenom), (b - a) ** 2 / 4
        t -= x * c
        x *= 2
    return (a + b) ** 2 / (t * 4)

def eContinuedFraction(err=defaultError):
    """
    Compute the base of natural logarithm e by continued fraction expansion.
    """
    if isinstance(err, RelativeError):
        _err = err.absoluteerror(math.e)
    else:
        _err = err
    ipart = rational.Integer(2)
    fpart_old = rational.Rational(1, 1)
    fpart = rational.Rational(2, 3)
    i = 4
    while not _err.nearlyEqual(fpart_old, fpart):
        fpart, fpart_old = rational.Rational(
            fpart.numerator + fpart_old.numerator,
            fpart.denominator + fpart_old.denominator), fpart
        fpart, fpart_old = rational.Rational(
            fpart.numerator + fpart_old.numerator,
            fpart.denominator + fpart_old.denominator), fpart
        fpart, fpart_old = rational.Rational(
            fpart.numerator * i + fpart_old.numerator,
            fpart.denominator * i + fpart_old.denominator), fpart
        i += 2
    return ipart + fpart

def floor(x):
    """
    floor(x) returns the integer; if x is an integer then x itself,
    otherwise the biggest integer less than x.
    """
    rx = rational.Rational(x)
    if rx.denominator == 1:
        return rational.Integer(rx.numerator)
    return rx.numerator // rx.denominator

def ceil(x):
    """
    ceil(x) returns the integer; if x is an integer then x itself,
    otherwise the smallest integer greater than x.
    """
    rx = rational.Rational(x)
    if rx.denominator == 1:
        return rational.Integer(rx.numerator)
    return rx.numerator // rx.denominator + 1

def tranc(x):
    """
    tranc(x) returns the integer; if x is an integer then x itself,
    otherwise the nearest integer to x.  If x has the fraction part
    1/2, then bigger one will be chosen.
    """
    rx = rational.Rational(x)
    if rx.denominator == 1:
        return rational.Integer(rx.numerator)
    return floor(x + rational.Rational(1, 2))

def sin(x, err=defaultError):
    """
    sin(x [,err]) returns the sine of x.
    """
    if not isinstance(err, defaultError.__class__) or err <= defaultError:
        rx = rational.Rational(x)
        sign = rational.Rational(1)
        # sin(-x) = -sin(x)
        if rx < 0:
            sign = -sign
            rx = -rx
        # sin(x + 2 * pi) = sin(x)
        if rx >= 2 * pi:
            rx -= floor(rx / (pi * 2)) * (pi * 2)
        # sin(x + pi) = -sin(x)
        if rx >= pi:
            rx -= pi
            sign = -sign
        # sin(x) = sin(pi - x)
        if rx > pi / 2:
            rx = pi - rx
        # sin(0) = 0 is a special case which must not be computed with series.
        if rx == 0:
            return rational.Rational(0)
        # sin(x) = cos(pi/2 - x) (pi/2 >= x > 4/pi)
        if rx > pi / 4:
            if rx == pi / 3:
                retval = sqrt(3) / 2
            else:
                retval = _cosTaylor(pi / 2 - rx, err)
        elif rx == pi / 4:
            retval = 1 / sqrt(2)
        elif rx == pi / 6:
            retval = rational.Rational(1, 2)
        else:
            retval = _sinTaylor(rx, err)
        if retval > 1:
            retval = rational.Integer(1)
        retval *= sign
    else:
        retval = rational.Rational(math.sin(x))
    return retval

def _sinTaylor(x, err=defaultError):
    """
    _sinTaylor(x [,err]) returns the sine of x by Taylor expansion.
    It is recommended to use only for 0 <= x <= pi / 4.
    """
    rx = rational.Rational(x)
    sinSeries = ExponentialPowerSeries(itertools.cycle((0, rational.Integer(1), 0, rational.Integer(-1))))
    return sinSeries(rx, err)

def cos(x, err=defaultError):
    """
    cos(x [,err]) returns the cosine of x.
    """
    if err <= defaultError:
        rx = rational.Rational(x)
        sign = rational.Rational(1)
        # cos(-x) = cos(x)
        if rx < 0:
            rx = -rx
        # cos(x + 2 * pi) = cos(x)
        if rx > 2 * pi:
            rx -= floor(rx / (pi * 2)) * (pi * 2)
        # cos(x + pi) = -cos(x)
        if rx > pi:
            rx -= pi
            sign = -sign
        # cos(x) = -cos(pi - x)
        if rx > pi / 2:
            rx = pi - rx
            sign = -sign
        # cos(x) = sin(pi/2 - x) (pi/2 >= x > 4/pi)
        if rx > pi / 4:
            if rx == pi / 3:
                retval = rational.Rational(1, 2)
            else:
                retval = _sinTaylor(pi / 2 - rx, err)
        elif rx == pi / 4:
            retval = 1 / sqrt(2)
        elif rx == pi / 6:
            retval = sqrt(3) / 2
        else:
            retval = _cosTaylor(rx, err)
        if retval > 1:
            retval = rational.Integer(1)
        retval *= sign
    else:
        retval = rational.Rational(math.cos(x))
    return retval

def _cosTaylor(x, err=defaultError):
    """
    _cosTaylor(x [,err]) returns the cosine of x by Taylor series.
    It is recomended to use only for 0 <= x <= pi / 4.
    """
    cosSeries = ExponentialPowerSeries(itertools.cycle((rational.Integer(1), 0, rational.Integer(-1), 0)))
    rx = rational.Rational(x)
    return cosSeries(rx, err)

def tan(x, err=defaultError):
    """
    tan(x [,err]) returns the tangent of x.
    """
    return sin(x, err) / cos(x, err)

def sinh(x, err=defaultError):
    """
    sinh(x [,err]) returns the hyperbolic sine of x.
    """
    if not isinstance(err, defaultError.__class__) or err <= defaultError:
        series = ExponentialPowerSeries(itertools.cycle((0, rational.Integer(1),)))
        rx = rational.Rational(x)
        if rx == 0:
            return rational.Rational(0)
        return series(rx, err)
    else:
        return rational.Rational(math.sinh(x))

def cosh(x, err=defaultError):
    """
    cosh(x [,err]) returns the hyperbolic cosine of x.
    """
    if err <= defaultError:
        series = ExponentialPowerSeries(itertools.cycle((rational.Integer(1), 0,)))
        rx = rational.Rational(x)
        if rx == 0:
            return rational.Integer(1)
        return series(rx, err)
    else:
        return rational.Rational(math.cosh(x))

def tanh(x, err=defaultError):
    """
    tanh(x [,err]) returns the hyperbolic tangent of x.
    """
    rx = rational.Rational(x)
    return sinh(rx, err) / cosh(rx, err)

def acos(x, err= defaultError):
    """
    acos(x [,err]) returns arc cosine of x.
    """
    if x > 1 or x < -1:
        raise ValueError("%s is not in the range [-1, 1]." % str(x))
    if x == 0:
        return pi(err) / 2
    if err <= defaultError:
        rx = rational.Rational(x)
        y = sqrt(1 - rx ** 2)
        if rx > 0:
            return asin(y, err)
        else:
            return pi(err) + asin(-y, err)
    else:
        return rational.Rational(math.acos(x))

def asin(x, err=defaultError):
    """
    asin(x [,err]) returns arc sine of x.
    """
    if x > 1 or x < -1:
        raise ValueError("%s is not in the range [-1, 1]." % str(x))
    if x < 0:
        return -asin(-x)
    if err <= defaultError:
        u = sqrt(rational.Rational(1, 2))
        if x > u:
            return pi(err) / 2 - asin(sqrt(1 - x**2))
        if x == 0:
            return rational.Integer(0)
        y = rational.Rational(x)
        y2 = y ** 2
        i = 2
        retval = y
        term = rational.Rational(y)
        oldvalue = 0
        while not err.nearlyEqual(retval, oldvalue):
            oldvalue = +retval
            term *= y2 * (i-1) ** 2 / (i*(i+1))
            i += 2
            retval += term
    else:
        retval = rational.Rational(math.asin(x))
    return retval

def atan(x, err=defaultError):
    """
    atan(x [,err]) returns arc tangent of x.
    """
    if not isinstance(err, defaultError.__class__) or err <= defaultError:
        # atan(x) = -atan(-x)
        if x < 0:
            return -atan(-x, err)
        # atan(x) = pi/2 - atan(1/x)
        elif x > 1:
            return pi(err) / 2 - atan(1 / x, err)
        elif x == 1:
            return pi(err) / 4
        elif x == 0:
            return rational.Integer(0)
        y = rational.Rational(x)
        y2 = y ** 2
        retval = y
        oldvalue = 0
        term = rational.Rational(x)
        i = 1
        while not err.nearlyEqual(retval, oldvalue):
            oldvalue = +retval
            i += 2
            term *= -y2 * (i-2) / i
            retval += term
    else:
        retval = rational.Rational(math.atan(x))
    return retval

def atan2(y, x, err=defaultError):
    """
    atan2(y, x [,err]) returns the arc tangent of y/x.
    Unlike atan(y/x), the signs of both x and y are considered.

    It is unrecomended to obtain the value of pi with atan2(0,1).
    """
    if x > 0 and y > 0:
        return atan(y/x)
    elif x > 0 and y < 0:
        return pi(err) * 2 + atan(y/x)
    elif x < 0:
        return pi(err) + atan(y/x)
    elif x == 0 and y > 0:
        return pi(err) / 2
    elif x == 0 and y < 0:
        return -pi(err) / 2
    return rational.Integer(0)

def hypot(x, y, err=defaultError):
    """
    hypot(x, y [,err]) returns sqrt(x**2 + y**2).
    """
    return sqrt(x**2 + y**2, err)

def pow(x, y, err=defaultError):
    """
    x ** y
    """
    if isinstance(y, (int, long)):
        return rational.Rational(x) ** y
    return exp(y * log(x, err=err), err)

def degrees(rad, err=defaultError):
    """
    converts angle rad from radians to degrees.
    """
    return rad * 180 / pi(err)

def radians(deg, err=defaultError):
    """
    converts angle deg from degrees to radians.
    """
    return deg * pi(err) / 180

def fabs(x):
    """
    returns absolute value of x.
    """
    return abs(rational.Rational(x))

def fmod(x, y):
    """
    returns x - n * y, where n is the quotient of x / y, rounded
    towards zero to an integer.
    """
    fquot = rational.Rational(x) / y
    if fquot < 0:
        n = -floor(-fquot)
    else:
        n = floor(fquot)
    return x - n * y

def frexp(x):
    """
    Return a tuple (m, e) where x = m * 2 ** e, 1/2 <= abs(m) < 1 and
    e is an integer.
    This function is provided as the counter-part of math.frexp, but it
    might not be useful.
    """
    if x == 0:
        return (rational.Rational(0), 0)
    m = rational.Rational(x)
    e = 0
    if x > 0:
        while m >= 1:
            m /= 2
            e += 1
        while m < rational.Rational(1, 2):
            m *= 2
            e -= 1
    else:
        while m <= -1:
            m /= 2
            e += 1
        while m > rational.Rational(-1, 2):
            m *= 2
            e -= 1
    return (m, e)

def ldexp(x, i):
    """
    returns x * 2 ** i.
    """
    return x * 2 ** i

def EulerTransform(iterator):
    """
    Return an iterator which yields terms of Euler transform of the
    given iterator.
    """
    stock = []
    b = rational.Rational(1, 2)
    l = -1
    for term in iterator:
        stock.append(term)
        for i in xrange(l, -1, -1):
            stock[i] += stock[i+1]
        yield b * stock[0]
        b /= 2
        l += 1

# constants
theRealField = RealField()
