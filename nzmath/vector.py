import ring

class Vector:

    def __init__(self, arg):
        """Vector(size, components)""" 
        if isinstance(arg, list):
            self.compo = arg
            self.size = len(arg)
        elif arg in ring.theIntegerRing:
            self.compo = [0]* arg
            self.size = arg
        else:
            raise ValueError

    def __getitem__(self, i):
        return self.compo[i-1]

    def __setitem__(self, *arg):
        self.compo[arg[0]-1] = arg[1]

    def __len__(self):
        return len(self.compo)

    def __eq__(self, other):
        return self.compo == other.compo

    def __add__(self, other): 
        if len(self) != len(other):
            raise VectorSizeError
        tmp = []
        for i in range(self.size):
            tmp.append(self.compo[i] + other.compo[i])
        return Vector(tmp)

    def __sub__(self, other):
        if len(self) != len(other):
            raise VectorSizeError
        tmp = []
        for i in range(self.size):
            tmp.append(self.compo[i] - other.compo[i])
        return Vector(tmp)

    def __mul__(self, other):
        mul = []
        for i in self.compo:
            mul.append(i * other)
        return mul

    def __rmul__(self, other):
        mul = []
        for i in self.compo:
            mul.append(other * i)
        return mul

    def __neg__(self):
        return (-1) * self

    def __repr__(self):
        return repr(self.compo)

    __str__ = __repr__

    def copy(self):
        return Vector(self.compo)

    def set(self, compo):
        if isinstance(compo, list):
            self.compo = compo
            self.size = len(compo)
        else:
            raise ValueError

    def innerProduct(self, other):
        if self.size != other.size:
            raise VectorSizeError
        x = 0
        for i in range(self.size):
            x += self.compo[i] * other.compo[i]
        return x

class VectorSizeError(Exception):
    pass

if __name__ == '__main__':
    v = Vector(3)
    u = Vector([1,2,3])
    print v
    print u
    print len(v)
    print v+u
    v.set([-1,-9,-8])
    print v
    print v-u
    print 3 * u
    print u * (-1)
    print u.innerProduct(v)
    print u.copy()
    print -v
    print u == Vector([1,2,3])
