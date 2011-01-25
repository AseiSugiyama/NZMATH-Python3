"""
real -- real numbers and the real number field.
"""

from __future__ import division

import nzmath.rational as rational
import nzmath.ring as ring
from sandbox.plugins import MATHMODULE as math, FLOATTYPE as Float, \
     CHECK_REAL_OR_COMPLEX as check_real_or_complex


class Real(ring.FieldElement):
    """
    Real is a class of real. 
    This class is only for consistency for other Ring object.
    """

    def __init__(self, value):
        ring.FieldElement.__init__(self)
        self.data = Float(value)

    def __add__(self, other):
        if isinstance(other, Real):
            result = self.data + other.data
        elif isinstance(other, (Float, int, long)):
            result = self.data + other
        else:
            return NotImplemented
        return self.__class__(result)

    def __radd__(self, other):# = __add__
        if isinstance(other, (Float, int, long)):
            result = other + self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __sub__(self, other):
        if isinstance(other, Real):
            result = self.data - other.data
        elif isinstance(other, (Float, int, long)):
            result = self.data - other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rsub__(self, other):
        if isinstance(other, (Float, int, long)):
            result = other - self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __mul__(self, other):
        if isinstance(other, Real):
            result = self.data * other.data
        elif isinstance(other, (Float, int, long)):
            result = self.data * other
        else:
            return NotImplemented
        return self.__class__(result)

    def __rmul__(self, other):
        if isinstance(other, (Float, int, long)):
            result = other * self.data
        else:
            return NotImplemented
        return self.__class__(result)

    def __truediv__(self, other):
        if isinstance(other, Real):
            result = self.data / other.data
        elif isinstance(other, (Float, int, long)):
            result = self.data / other
        else:
            return NotImplemented
        return self.__class__(result)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        if isinstance(other, (Float, int, long)):
            result = other / self.data
        else:
            return NotImplemented
        return self.__class__(result)

    __rdiv__ = __rtruediv__

    def __pow__(self, other):
        if isinstance(other, Real):
            result = math.pow(self.data, other.data)
        elif isinstance(other, (Float, int, long)):
            result = math.pow(self.data, other)
        return result

    def __eq__(self, other):
        if isinstance(other, Real):
            return self.data == other.data
        elif isinstance(other, (Float, int, long)):
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
        if isinstance(element, Real):
            return True
        else:
            try:
                real_flag = check_real_or_complex(element)
                if real_flag:
                    return True
            except TypeError:
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


theRealField = RealField()
