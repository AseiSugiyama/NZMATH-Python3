from __future__ import division, generators
import operator
import real
import rational

class Complex:
    """

    Complex is a class for complex numbers.  Each instance has a coupled
    numbers; real and imaginary part of the number.

    """
    def __init__(self, re, im):
        self.real = re
        self.imag = im

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
        return real.hypot(self.real, self.imag)

    def __pos__(self):
        if self.imag == 0:
            return +self.real
        return self.__class__(+self.real, +self.imag)

    def __neg__(self):
        return self.__class__(-self.real, -self.imag)

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
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

    def __le__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

    def __gt__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

    def __ge__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

class ComplexField:
    """

    ComplexField is a class of the field of real numbers.
    The class has the single instance 'theComplexField'.

    """

    def __contains__(self, element):
        reduced = +element
        if reduced in real.theRealField:
            return 1
        if isinstance(reduced, complex) or isinstance(reduced, Complex):
            return 1
        return 0  ## How to know a number is complex ?

theComplexField = ComplexField()

pi = real.pi
e = real.e

def sum(iter, precision):
    """

    sum(iter, precision) computes sum of the series given by iter to
    the precision.  It is assumed that:
    1) iter does not yield zeros,
    2) the series converges to zero.

    """
    def abscmp(a, b):
        absa = abs(a)
        absb = abs(b)
        if absa < absb:
            return -1
        elif absa == absb:
            return 0
        return 1
    roughEvaluation = Complex(real.Float(0,0,precision), real.Float(0,0,precision))
    termList = []
    for term in iter:
        roughEvaluation += term
        termList.append(term)
        if abs(term) < abs(roughEvaluation) / 2**(2*precision):
            break
    termList.sort(abscmp)
    return reduce(operator.add, termList, Complex(0, 0))

def exp(x, precision=real.doubleprecision):
    def exp_iter(xx, pp):
        yield 1
        try:
            y = real.Float(xx, 0, pp)
        except:
            y = xx.copy()
        f = i = 1
        yield y
        while 1:
            i += 1
            f *= i
            y *= xx
            yield y / f
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        if isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    elif x in real.theRealField:
        return real.exp(x, precision)
    if x == 0:
        return real.Float(1, 0, None)
    return sum(exp_iter(x, precision), precision)

def sin(x, precision=real.doubleprecision):
    def sin_iter(xx, pp):
        yield xx
        try:
            y = real.Float(xx, 0, pp)
        except:
            y = xx.copy()
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
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    try:
        y = real.Float(x, 0, precision)
    except:
        y = x.copy()
    return sum(sin_iter(y, precision), precision)

def cos(x, precision=real.doubleprecision):
    def cos_iter(xx, pp):
        yield 1
        try:
            y = real.Float(xx, 0, pp)
        except:
            y = xx.copy()
        y2 = xx ** 2
        i = f = 1
        while 1:
            f *= i*(i+1)
            i += 2
            y *= y2
            yield (-y / f)
            f *= i*(i+1)
            i += 2
            y *= y2
            yield (y / f)
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    try:
        y = real.Float(x, 0, precision)
    except:
        y = x.copy()
    return sum(cos_iter(y, precision), precision)

def tan(x, precision=real.doubleprecision):
    """

    tan(x [,precision]) returns the tangent of x.

    """
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    return sin(x, precision) / cos(x, precision)

def log(x, precision=real.doubleprecision):
    """

    log(x [,precision]) returns the natural logarithm of x. There is
    one branch cut, from 0 along the negative real axis to -infinity,
    continuous from above.

    """
    if isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        if isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    if x in real.theRealField:
        x = +x
        if x > 0:
            return real.log(x, precision)
        elif x < 0:
            return Complex(real.log(abs(x)), pi)
    return Complex(real.log(abs(x)), real.atan2(x.real, x.imag))

def sinh(x, precision=real.doubleprecision):
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
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    try:
        y = real.Float(x, 0, precision)
    except:
        y = x.copy()
    return sum(sinh_iter(y, precision), precision)

def cosh(x, precision=real.doubleprecision):
    """

    cosh(x [,precision]) returns the hyperbolic cosine of x.

    """
    def cosh_iter(xx, pp):
        yield 1
        x2 = xx ** 2
        y = real.Float(1, 0 ,2*precision)
        i = f = 1
        while 1:
            f *= i*(i+1)
            y *= x2
            i += 2
            yield (y / f)
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    try:
        y = real.Float(x, 0, precision)
    except:
        y = x.copy()
    return sum(cosh_iter(y, precision), precision)

def tanh(x, precision=real.doubleprecision):
    """

    tanh(x [,precision]) returns the hyperbolic tangent of x.

    """
    if isinstance(x, real.Float) and precision < x.precision:
        precision = x.precision
    elif isinstance(x, Complex):
        if isinstance(x.real, real.Float) and precision < x.real.precision:
            precision = x.real.precision
        elif isinstance(x.imag, real.Float) and precision < x.imag.precision:
            precision = x.imag.precision
    return sinh(x, precision) / cosh(x, precision)

j = Complex(0,1)

class RelativeError:
    def __init__(self, numerator, denominator=1):

        self.relativeerrorrange = rational.Rational(numerator, denominator)

    def absoluteerror(self, complexnumeric):
        #r = abs(Complex(re,im))*self.relativeerrorrange
        r = abs(complexnumeric)*self.relativeerrorrange
        return AbsoluteError(r)


class AbsoluteError:
    def __init__(self, numeric):
        """

        AbsoluteError(x) defines absolute error number attribute
        absoluteerrorrange from x. x must be a positive value.

        """

        self.absoluteerrorrange = abs(numeric)
        
### function rewrite
defaultError = RelativeError(1, 2 ** 53)

def exp_new(x, err=defaultError):
    """

    exp(x [,err]) is the exponential function.

    """
    try:
        rx = rational.Rational(x)
        if isinstance(err, RelativeError):
            _err = real.RelativeError(0, err.relativeerrorrange)
        elif isinstance(err, AbsoluteError):
            _err = real.AbsoluteError(0, err.absoluteerrorrange)
        return real.exp_new(x, _err)
    except TypeError:
        pass
    # divide real part and imaginary part?
    if isinstance(err, RelativeError):
        _err = real.RelativeError(0, err.relativeerrorrange, 2)
    elif isinstance(err, AbsoluteError):
        _err = real.AbsoluteError(0, err.absoluteerrorrange, 2)
    radius = real.exp_new(x.real, _err)
    if isinstance(err, RelativeError):
        _err = RelativeError(err.relativeerrorrange, 2)
    elif isinstance(err, AbsoluteError):
        _err = AbsoluteError(err.absoluteerrorrange, 2)
    arg = expi(x.imag, _err)
    return radius * arg

def expi(x, err=defaultError):
    """

    expi(x [,err]) returns exp(i * x) where i is the imaginary unit
    and x must be a real number.

    """
    # err shoud be converted somehow
    if isinstance(err, RelativeError):
        _err = real.RelativeError(0, err.relativeerrorrange, 2)
    elif isinstance(err, AbsoluteError):
        _err = real.AbsoluteError(0, err.absoluteerrorrange, 2)
    re = real.cos_new(x, _err)
    im = real.sin_new(x, _err)
    return Complex(re, im)
