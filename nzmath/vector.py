class Vector:

    def __init__(self, compo):
        if isinstance(compo, list):
            self.compo = compo
        elif rational.isIntegerObject(compo):
            self.compo = [0] * compo 
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
            tmp[i] = self.compo[i] * -1
        return self.__class__(tmp)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if len(self) != other.row:
                raise VectorSizeError
            tmp = [0] * len(self)
            for j in range(other.column):
                for i in range(len(self)):
                    tmp[j] += self.compo[i] * other.compo[i][j]
            return self.__class__(tmp)
        else:
            tmp = []
            for each in self.compo:
                tmp.append(each * other)
            return self.__class__(tmp)

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            if len(self) != other.column:
                raise VectorSizeError
            tmp = [0] * len(self)
            for i in range(other.row):
                for j in range(other.column):
                    tmp[i] += other.compo[i][j] * self.compo[j]
            return self.__class__(tmp)
        else:
            tmp = []
            for each in self.compo:
                tmp.append(each * other)
            return self.__class__(tmp)

    def __repr__(self):
        return "Vector " + repr(self.compo)

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

    def indexNoneZero(self):
        for i in range(self.size):
            if self.compo[i] != 0:
                return i + 1
        raise ValueError, "all zero"


class VectorSizeError(Exception):
    pass


if __name__ == '__main__':
    u=Vector(3)
    v=Vector([3,5,2])
    w=Vector([-7,2,0])
    print "u=",u
    print "v=",v
    print "w=",w
    print "v+w", v+w
    w = u-v
    print "w=u-v", w
    print c
    print v
    print v * c
    print c * v
