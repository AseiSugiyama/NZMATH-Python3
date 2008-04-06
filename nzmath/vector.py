from __future__ import division

class Vector (object):
    """
    Class Vector is an elemental class of vector.
    """
    def __init__(self, compo):
        self.compo = list(compo)

    def __getitem__(self, index):
        return self.compo[index - 1]

    def __setitem__(self, index, value):
        self.compo[index - 1] = value

    def __len__(self):
        return len(self.compo)

    def __iter__(self):
        return iter(self.compo)

    def __eq__(self, other):
        return self.compo == other.compo

    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self) == len(other):
                tmp = [s + c for (s, c) in zip(self.compo, other.compo)]
                return self.__class__(tmp)
            else:
                raise VectorSizeError("unable to add vectors with different sizes")
        else:
            raise TypeError("unable to add")

    def __sub__(self, other):
        if isinstance(other, Vector):
            if len(self) == len(other):
                return self.__class__([s - c for (s, c) in zip(self.compo, other.compo)])
            else:
                raise VectorSizeError("unable to subtract vectors with different sizes")
        else:
            raise TypeError("unable to subtract")

    def __neg__(self):
        return self.__class__([-c for c in self.compo])

    def __mul__(self, other):
        if isinstance(other, Vector):
            raise TypeError("no multiplication")
        elif ismatrix(other):
            return NotImplemented
        else:
            return self.__class__([c * other for c in self.compo])

    def __rmul__(self, other):
        if ismatrix(other):
            return NotImplemented
        else:
            return self.__class__([other * c for c in self.compo])

    def __truediv__(self, other):
        return self.__class__([c / other for c in self.compo])

    __div__ = __truediv__ # for backward compatibility

    def __mod__(self,other):
        if isinstance(other, Vector):
            return TypeError
        else:
            modulus = int(other)
            return self.__class__([int(c) % modulus for c in self.compo])

    def __repr__(self):
        return "Vector(" + repr(self.compo) + ")"

    def __str__(self):
        return str(self.compo)

# utility methods ----------------------------------------------------
    def copy(self):
        return self.__class__(self.compo)

    def set(self, compo):
        if isinstance(compo, list):
            self.compo = compo
        else:
            raise ValueError

    def indexOfNoneZero(self):
        for c, entry in enumerate(self.compo):
            if entry:
                return c + 1
        raise ValueError("all zero")

    def toMatrix(self, as_column=False):
        """
        toMatrix(as_column): convert to Matrix representation.
        If as_column is True, return column matrix, otherwise row matrix.
        """
        import nzmath.matrix as matrix
        if as_column:
            return matrix.createMatrix(len(self), 1, self.compo)
        else:
            return matrix.createMatrix(1, len(self), self.compo)


def innerProduct(self, other):
    v = 0
    for i in range(1, len(self) + 1):
        try:
            v += self[i] * other[i].conjugate()
        except AttributeError:
            v += self[i] * other[i]
    return v

def ismatrix(obj):
    """
    If the given obj is a matrix then return True.  False, otherwise.
    """
    return hasattr(obj, "row") and hasattr(obj, "column")


class VectorSizeError(Exception):
    """
    An exception raised when two vector operands for an operator
    mismatches in size.
    """
