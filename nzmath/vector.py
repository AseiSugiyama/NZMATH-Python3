from __future__ import division

class Vector (object):

    def __init__(self, compo):
        if isinstance(compo, list):
            self.compo = compo
        else:
            raise ValueError

    def __getitem__(self, i):
        return self.compo[i-1]

    def __setitem__(self, *arg):
        self.compo[arg[0]-1] = arg[1]

    def __len__(self):
        return len(self.compo)

    def __iter__(self):
        return iter(self.compo)

    def __eq__(self, other):
        return self.compo == other.compo

    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self) == len(other):
                tmp = []
                for i in range(len(self.compo)):
                    tmp.append(self.compo[i] + other.compo[i])
                return self.__class__(tmp)
            else:
                raise VectorSizeError
        else:
            return NotImplemented

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        tmp = self.compo[:]
        for i in range(len(self)):
            tmp[i] = -self.compo[i]
        return self.__class__(tmp)

    def __mul__(self, other):
        from nzmath.matrix import Matrix
        if isinstance(other, Vector):
            return TypeError
        elif isinstance(other, Matrix):
            return NotImplemented
        else:
            product = Vector([0]*len(self))
            for i in range(1, len(self)+1):
                product[i] = self[i] * other
            return product

    def __rmul__(self, other):
        from nzmath.matrix import Matrix
        if isinstance(other, Vector):
            return TypeError
        elif isinstance(other, Matrix):
            return NotImplemented
        else:
            product = Vector([0]*len(self))
            for i in range(1, len(self)+1):
                product[i] = other * self[i]
            return product

    def __div__(self, other):
        return self * (1/other)

    def __mod__(self,other):
        if isinstance(other, Vector):
            return TypeError
        else:
            if(other==0):
                return ZeroDivisionError
            V = Vector([0]*len(self))
            for i in range(len(self)):
                V[i] = ((int(self[i]) % int(other)))
            return V

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
            self.size = len(compo)
        else:
            raise ValueError

    def indexOfNoneZero(self):
        c = 1
        for entry in self.compo:
            if entry != 0:
                return c
            c += 1
        raise ValueError, "all zero"

    def toMatrix(self, type = 0):
        """
        toMatrix(type): convert Matrix representation.
        if type is set, return column matrix, otherwise row matrix.
        """
        import nzmath.matrix as matrix
        if type:
            return matrix.createMatrix(len(self), 1, self.compo)
        else:
            return matrix.createMatrix(1, len(self), self.compo)

    def isDiagonal(self, other):
        return innerProduct(self, other) == 0

def innerProduct(self, other):
    from nzmath.imaginary import Complex
    v=0
    for i in range(1,len(self)+1):
        try:
            v += self[i] * Complex(other[i].real, -other[i].imag)
        except AttributeError:
            v += self[i] * other[i]
    return v



class VectorSizeError(Exception):
    pass
