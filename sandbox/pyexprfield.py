"""
Python Expression field, another finite prime field characteristic two definition.
field element is defined by bool(Python Expression).

This module is reference design for finite field characteristic two.
but I recommend that this field should be used only checking Python syntax.
"""

from __future__ import division
import logging
import operator

_log = logging.getLogger('sandbox.pyexprfield')

import sandbox.finitefield as finitefield

class PythonExpressionFieldElement(finitefield.FiniteFieldElement):
    """
    The element of boolean field.
    """
    def __init__(self, expression):
        """ boolean must be Python expression.
        """
        self.boolean = bool(expression)

    def __eq__(self, other):
        return self.boolean == other

    def getRing(self):
        return PythonExpressionField()

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.boolean)

    def __str__(self):
        return str(self.boolean)

    def xor(self, other):
        """ return self xor other .
        """
        return self.__class__(not (self == other))

    def __add__(self, other):
        return self.__class__(self.xor(other))

    __radd__ = __add__
    __sub__ = __add__
    __rsub__ = __add__

    def __mul__(self, other):
        return self.__class__(self.boolean and other)

    __rmul__ = __mul__

    def __div__(self, other):
        """ compute formal division.
        In Python expression, 0 is False, so dividing False causes ZeroDivisionerror.
        """
        if not other:
            raise ZeroDivisionError("False represents zero, this operation is ZeroDivision.")
        return self.__class__(self.boolean)

    __truediv__ = __div__
    __floordiv__ = __div__
    __rdiv__ = __div__
    __rtruediv__ = __div__
    __rfloordiv__ = __div__

    def __nonzero__(self):
        return not self.boolean

    def __pow__(self, index):
        if index == 0:
            return self.__class__(True)
        return self.__class__(self.boolean)

    def __neg__(self):
        return self.__class__(not self.boolean)

    def __pos__(self):
        return self.__class__(self.boolean)

    __invert__ = __neg__

    def __coerce__(self, other):
        return (self, self.__class__(other))

    def toFinitePrimeFieldElement(self):
        """ get FinitePrimeField(2) element with bijective map.
        """
        if self.boolean:
            return finitefield.FinitePrimeFieldElement(1, 2)
        return finitefield.FinitePrimeFieldElement(0, 2)

class PythonExpressionField(finitefield.FiniteField):
    def __init__(self):
        characteristic = 2 # BooleanField = {True, False}
        finitefield.FiniteField.__init__(self, characteristic)

    def __contains__(self, element):
        """Python expressions are either pass or raise SyntaxError.
        in other words, always true.
        """
        return True

    def card(self):
        return self.char

    def createElement(self, expression):
        return PythonExpressionFieldElement(expression)

    def order(self, element):
        if element:
            return 1
        raise ValueError("False is zero, not in the group.")

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)

    def __hash__(self):
        return self.char & 0xFFFFFFFF

    def issubring(self, other):
        """
        Report whether another ring contains the field as a subring.
        """
        if self == other:
            return True
        # FIXME: Undefined variable 'FiniteField'
        if isinstance(other, FiniteField) and other.getCharacteristic() == self.char:
            return True
        try:
            return other.issuperring(self)
        except:
            return False

    def issuperring(self, other):
        """
        Report whether the field is a superring of another ring.
        Since the field is a prime field, it can be a superring of
        itself only.
        """
        if self == other:
            return True
        # FIXME Undefined variable 'FiniteField'
        if isinstance(other, FiniteField) and other.getCharacteristic() == self.char:
            return True
        return False

    def __nonzero__(self):
        return True

    # properties
    def _getOne(self):
        "getter for one"
        if self._one is None:
            # FIXME: Undefined variable 'PythonExpressionElement'
            self._one = PythonExpressionElement(1)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            # FIXME: Undefined variable 'PythonExpressionElement'
            self._zero = PythonExpressionElement(0)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")
