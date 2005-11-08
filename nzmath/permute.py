class PermClass:

    """
    This is a class to make normal type's element of permutation group.
    Example,[2,3,1,5,4]
    This means [1 2 3 4 5]
               [2 3 1 5 4]
    (It is one-to-one onto map,1->2,2->3,3->1,4->5,5->4)
    """

    def __init__(self, value):
        self.data = value
        a = self.data
        if not isinstance(a, list):
           raise ValueError("This isn't normal form")
        b = range(len(a))
        for x in a:
          if not isinstance(x,int):
             raise ValueError("This number should be integer list")
          elif x <= 0 or x > len(a):
             raise ValueError("This isn't onto")
          elif b[x-1] == -1:
             raise ValueError("This isn't one-to-one")
          else :
             b[x-1] = -1

    """
    def __init__(self, value):
        self.data = value
        a = self.data
        if not isinstance(a, list):
           raise ValueError("This isn't normal form")
        b = list(self.data)
        b.sort()
        for x in a:
            if int(x) != x:
                raise ValueError("This number is not integer")
        for i in range(len(a)):
            if b[i] != i+1:
                raise ValueError("This isn't element of permutation group")
    """

    def __getitem__(self, other):
        if not isinstance(other, int):
            raise ValueError("This number should be integer")
        elif other <= 0 or other > len(self.data):
            raise ValueError("This is out of range")
        return self.data[other-1]

    def __mul__(self, other):
        """
        It is a method to permute's multiply.
        Self is caluculated after other
        """
        a = self.data
        b = other.data
        c = []
        if len(a) != len(b):
           raise ValueError("This can't multiply")
        for i in range(len(a)):
           c.append(a[b[i] - 1])
        return PermClass(c)

    def __rmul__(self, other):
       return other * self

    def __div__(self, other):
        return self * (other.inverse())

    def __rdiv__(self, other):
        return other * (self.inverse())

    def __pow__(self, other):
        b = PermClass(self.data) #other instance
        if not isinstance(other, int):
           raise ValueError("This can't caluculate")
        if other > 0:
          for i in range(other-1):
            b = self * b
        else:
          c = self.inverse()
          for i in range(abs(other) + 1):
            b = c * b
        return b

    def inverse(self):
        a = self.data
        b = range(len(a))
        for i in range(len(a)):
           b[a[i] - 1] = i+1
        return PermClass(b)

    def identify(self):
        return PermClass(range(1, len(self.data) + 1))

    def numbering(self):
        """
        This method is numbering to self permute element.
        It is synmetrical arranging.
        This is inductive definition for dimention.
        Example,
        2-dimension [1,2],[2,1]
        3-dimension [1,2,3],[2,1,3],[1,3,2],[2,3,1],[3,1,2],[3,2,1]
        4-dimension [1,2,3,4],[2,1,3,4],[1,3,2,4],[2,3,1,4],[3,1,2,4],[3,2,1,4],...,[4,3,2,1]
        """
        a = self.data
        b = []
        for i in range(len(a)):
          b.append(-1)
        for i in range(len(a)):
          b[a[i] - 1] = 0
          for j in range(a[i], len(b)):
            if b[j] != -1:
               b[j] += 1
        c = 0
        b[0] = 1
        for j in range(len(b) - 1, -1, -1):
            c = (j+1) * c + b[j]
        return c

    def order(self):
        """
        This method returns self permute element order.
        """
        b=PermClass(self.data)
        i = 1
        while b != b.identify():
          b = self * b
          i += 1
        return i

    def ToTranspose(self):
        """
        This method returns 2-dimentional cyclic type's element of permute group.
        It is recursive program.
        """
        a = list(self.data)
        l = []
        if len(a) == 1:
          return ExPermClass(1, [])
        else:
          if a[len(a) - 1] != len(a):
            l.append((a[len(a) - 1],len(a)))
            a[a.index(len(a))]=a[len(a) - 1]
          b = PermClass(a[:len(a) - 1]).ToTranspose()
          l.extend(b.data)
          return ExPermClass(len(a), l)

    def ToCyclic(self):
        """
        This method returns cyclic type's element of permute group.
        """
        a = self.data
        b = list(self.data)
        l = []
        for i in range(len(a)):
          if b[i] != '*':
             k = [(i+1)]
             b[i] = '*'
             j = i
             while a[j] != (i+1):
               k.append(a[j])
               j = a[j] - 1
               b[j] = '*'
             if len(k) != 1:
               l.append(tuple(k))
        return ExPermClass(len(a), l)

    def sgn(self):
        """
        This method returns sign of permute group.
        I make two patern to this task.
        """
        a = self.data
        k = l = 1
        for j in range(len(a) - 1):
            for i in range(j+1):
              k *= cmp(i, j+1) #cmp is function to return sign of subtraction
              l *= cmp(a[i], a[j+1])
        return l/k

    """
    def sgn(self):
        a = len((self.ToTranspose()).data)
        if (a % 2) != 0:
           return -1
        else:
           return 1 
    """

    def types(self):
        """
        This method returns 'type' by cyclic permute element length.
        """
        a = self.ToCyclic().data
        c = []
        for i in range(len(a)):
          c.append(len(a[i]))
        c.sort()
        return repr(c) + ' type'

    def ToMatrix(self):
        """
        This is difined permute matrix
        """
        import nzmath.matrix as matrix
        a = len(self.data)
        A = matrix.Matrix(a, a)
        for j in range(a):
            A[j+1, self.data[j]] = 1
        return A

    def __eq__(self, other):
        a = self.data
        b = other.data
        if len(a) != len(b):
           return False
        for i in range(len(a)):
           if a[i] != b[i]:
              return False
        return True

    def __ne__(self, other):
       return not self == other

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)


class ExPermClass:

    """
    This is a class to maka cyclic type's element of permutation group.
    Example,(5,[(1,2),(3,4)])   This means (1,2)(3,4)=[2,1,4,3,5]
    """

    def __init__(self, val1, val2):
        self.dim = val1
        self.data = val2
        if not (isinstance(val1, int) and isinstance(val2, list)):
           raise ValueError("This is not cyclic form")
        for x in val2:
          if not isinstance(x, tuple):
             raise ValueError("This is not cyclic form")
          b = range(val1)
          for y in x:
            if not isinstance(y, int):
               raise ValueError("This number should be integer")
            if (y > val1) or (y <= 0):
              raise ValueError("This is out of range")
            elif b[y-1] == -1:
              raise ValueError("This isn't one-to-one")
            else:
              b[y-1] = -1

    def __mul__(self, other):
        if self.dim != other.dim:
           raise ValueError("This can't multiply")
        c = []
        for x in self.data:
           c.append(x)
        for x in other.data:
           c.append(x)
        return ExPermClass(self.dim, c)

    def __rmul__(self, other):
       return other * self

    def __div__(self, other):
        return self * other.inverse()

    def __rdiv__(self, other):
        return other * self.inverse()

    def __pow__(self, other):
        b = ExPermClass(self.dim, self.data) #other instance
        if not isinstance(other, int):
           raise ValueError("This can't caluculate")
        if other > 0:
          for i in range(other-1):
            b = self * b
        else:
          c = self.inverse()
          for i in range(abs(other) + 1):
            b = c * b
        return b

    def inverse(self):
        a = list(self.data)
        a.reverse()
        for i in range(len(a)):
            b = list(a[i])
            if len(a[i]) > 2:
               b.reverse()
            a[i] = tuple(b)
        return ExPermClass(self.dim, a)

    def identify(self):
        return ExPermClass(self.dim, [])

    def order(self):
        """
        This method returns self permute element order.
        """
        return self.ToNormal().order()

    """
    def order(self):
        b = ExPermClass(self.dim, self.data)
        i = 1
        while b != b.identify():
          b = self * b
          i += 1
        return i
    """

    def ToNormal(self):
        """
        This method returns normal type's element of permute group.
        I make two patern to this task.
        """
        dim = self.dim
        a = list(self.data)
        a.reverse()
        b = []
        for i in range(dim):
           b.append('*')
        for x in a:
           c = list(x)
           c.append(c[0])
           d = []
           for y in x:
              if b[y-1] != '*':
                 d.append(b.index(y))
              else:
                 d.append(y-1)
           for j in range(len(d)):
              b[d[j]] = c[j+1]
              if b[d[j]] == d[j] + 1:
                  b[d[j]] = '*'
        for i in range(dim):
           if b[i] == '*':
              b[i] = i+1
        return PermClass(b)

    """
    def ToNormal(self):
        dim = self.dim
        val = self.data
        a = PermClass(range(1, dim+1))
        for x in val:
          b = range(1, dim+1)
          c = list(x)
          c.append(c[0])
          for j in range(len(x)):
            b[c[j] - 1] = c[j+1]
          a = a * PermClass(b)
        return a
    """

    def simplify(self):
        """
        This method returns more simple element.
        """
        return self.ToNormal().ToCyclic()

    def __eq__(self, other):
        if self.dim != other.dim:
           return False
        a = (self.simplify()).data
        b = (other.simplify()).data
        if len(a) != len(b):
           return False
        for i in range(len(a)):
           for j in range(len(a[i])):
             if list(a[i])[j] != list(b[i])[j]:
              return False
        return True

    def __ne__(self, other):
       return not self == other

    def __repr__(self):
        return repr(self.data)+"("+repr(self.dim)+")"

    def __str__(self):
        return str(self.simplify().data)+"("+str(self.dim)+")"
