"""
Cartesian product

This module is useful for constructing a direct product of ring.
"""

from __future__ import division
import operator
import nzmath.cardinality


class Cartesian(object):
    """
    The class Cartesian represents the concept of cartesian (direct)
    product.  All arithmetic operations are interpreted as
    componentwise.

    Note that right operands for each operation can be any sequence
    of the same length for convinience.
    """

    def __init__(self, args):
        """
        Cartesian(args)

        args can be any iterable.
        """
        self._data = tuple(args)

    def __len__(self):
        """
        len(self)

        Return the number of components.
        """
        return len(self._data)

    def __getitem__(self, index):
        """
        self[index]

        Return index-th component.
        """
        result = self._data[index]
        if isinstance(result, self._data.__class__):
            return self.__class__(result)
        else:
            return result

    def __iter__(self):
        """
        Return iterator
        """
        return iter(self._data)

    def __neg__(self):
        """
        -self

        componentwise negation.
        """
        return self.__class__([-s for s in self])

    def __pos__(self):
        """
        +self

        return identical object.
        """
        return self.__class__(self)

    def __pow__(self, index, mod=None):
        """
        self ** index
        pow(self, index, mod)

        index should not be a sequence.
        """
        if mod is None:
            return self.__class__([pow(s, index, mod) for s in self])
        else:
            return self.__class__([s ** index for s in self])

    def __eq__(self, other):
        """
        self == other

        componentwise equality.
        """
        if self is other:
            return True
        if not isinstance(other, Cartesian):
            return False
        return self._data == other._data

    def __neq__(self, other):
        """
        self != other
        """
        if not isinstance(other, Cartesian):
            return True
        if self is other:
            return False
        return self._data != other._data

    def __hash__(self, other):
        """
        hash(self)
        """
        return hash(self._data) ^ hash(self.__class__.__name__)

    def componentwise(self, other, func, *args, **kwds):
        """
        Return componentwise application of 'func' with optional
        arguments.
        """
        assert len(self) == len(other)
        if not args and not kwds:
            return self.__class__([func(s, o) for (s, o) in zip(self, other)])
        elif not args:
            return self.__class__([func(s, o, **kwds) for (s, o) in zip(self, other)])
        elif not kwds:
            return self.__class__([func(s, o, *args) for (s, o) in zip(self, other)])
        else:
            return self.__class__([func(s, o, *args, **kwds) for (s, o) in zip(self, other)])

    def __add__(self, other):
        """
        self + other

        componentwise addition.
        """
        return self.componentwise(other, operator.__add__)

    def __sub__(self, other):
        """
        self - other

        componentwise subtraction.
        """
        return self.componentwise(other, operator.__sub__)

    def __mul__(self, other):
        """
        self * other

        componentwise multiplication.
        """
        return self.componentwise(other, operator.__mul__)

    def __truediv__(self, other):
        """
        self / other

        componentwise true division.
        """
        return self.componentwise(other, operator.__truediv__)

    def __floordiv__(self, other):
        """
        self // other

        componentwise floor division.
        """
        return self.componentwise(other, operator.__floordiv__)

    def __mod__(self, other):
        """
        self % other

        componentwise modulo.
        """
        return self.componentwise(other, operator.__mod__)

    def __divmod__(self, other):
        """
        divmod(self, other)

        componentwise divmod.
        """
        return self.componentwise(other, divmod)

    def card(self):
        if len(self) == 0:
            return 0
        the_card = 1
        for component in self._data:
            the_card *= card(component)
        return the_card
