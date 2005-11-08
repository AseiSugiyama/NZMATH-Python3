import rational
import vector

class Matrix:
    """
    
    Matrix is a class for matrices.

    """

    def __init__(self, row, column, compo = 0):
        """

        Matrix(row, column [,components])

        """
        if (rational.isIntegerObject(row)
            and rational.isIntegerObject(column)
            and row > 0
            and column > 0 ): 
            self.row = row
            self.column = column
            self.compo = []
            if compo == 0:
                for i in range(self.row):
                    self.compo.append([0] * self.column)
            else:
                if (len(compo) != self.row * self.column):
                    raise ValueError, "number of given components is not match the matrix size"
                for i in range(self.row):
                    self.compo.append(compo[self.column*i : self.column*(i+1)])
        else:
            raise ValueError, "invalide value for matrix size"

    def __getitem__(self, index):
        """
        M[i,j] : Return (i,j)-component of M. 
        M[i] <==> M.getColumn(i)
        """
        if isinstance(index, tuple):
            return self.compo[index[0]-1][index[1]-1]
        elif isinstance(index, (int, long)):
            return self.getColumn(index)
        else:
            raise IndexError("Matrix invalid index: %s" % index)

    def __setitem__(self, key, value):
        """
        M[i,j] = a   :   Substitute a for (i,j)-component of M.
        M[i] = V <==> M.setColumn(i, V)
        """
        if isinstance(key, tuple):
            self.compo[key[0]-1][key[1]-1] = value
        elif isinstance(key, (int, long)):
            self.setColumn(key, value)
        else:
            raise TypeError, self.__setitem__.__doc__

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if (self.row != other.row) or (self.column != other.column):
                return False
            for i in range(self.row):
                for j in range(self.column):
                    if self.compo[i][j] != other.compo[i][j]:
                        return False
            return True
        elif isinstance(other, int):
            if other == 0:  # zero matrix ?
                for i in range(self.row):
                    for j in range(self.column):
                        if self.compo[i][j] != 0:
                            return False
                return True
        else:
            raise TypeError

    def __add__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError

        sum = self.__class__(self.row, self.column)

        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                sum[i,j] = self[i,j] + other[i,j]

        return sum

    def __sub__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError

        diff = self.__class__(self.row, self.column)

        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                diff[i,j] = self[i,j] - other[i,j]

        return diff

    def __mul__(self, other):
        """
        
        multiplication with a Matrix or a scalar
        
        """
        if isinstance(other, Matrix):
            if self.column != other.row:
                raise MatrixSizeError
            product = self.__class__(self.row, other.column) 
            for i in range(1, self.row+1):
                for j in range(1, other.column+1):
                    for k in range(self.column):
                        product[i,j] += self[i,k] * other[k,j]
            return product 
        elif isinstance(other, vector.Vector):
            if self.column != len(other):
                raise vector.VectorSizeError
            tmp = [0] * self.row
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    tmp[i-1] += self[i,j] * other[j]
            return vector.Vector(tmp) 
        else: 
            product = self.__class__(self.row, self.column)
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    product[i,j] = self[i,j] * other
            return product

    def __div__(self, other):
        """
        
        division by a scalar
        
        """
        return self * (1 / rational.Rational(other)) 

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            product = Matrix(self.row, self.column)
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    product[i,j] = self[i,j] * other
            return product
        elif isinstance(other, vector.Vector):
            if self.row != len(other):
                raise vector.VectorSizeError
            tmp = [0] * self.column
            for j in range(1, self.column+1):
                for i in range(1, self.row+1):
                    tmp[j-1] += other[i] * self[i,j]
            return vector.Vector(tmp)
        else:
            product = self.__class__(self.row, self.column)
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    product[i,j] = self[i,j] * other
            return product 

    def __neg__(self):
        return (-1) * self

    def __pow__(self, other):
        n = +other
        if not n in rational.theIntegerRing:
            raise ValueError 
        if self.row != self.column:
            raise MatrixSizeError

        power = unitMatrix(self.row)
        if n == 0:
            return power
        if n > 0:
            z = self.copy()
        else:
            n = abs(n)
            z = self.inverse() 

        while 1:
            if n % 2 == 1:
                power *= z
            n //= 2
            if n == 0:
                return power
            z = z*z 

    def __repr__(self):
        return_str = ""
        width = [1] * self.column      # width of each column
        for j in range(self.column):
            for i in range(self.row):
                if len(str(self.compo[i][j])) > width[j]:
                    width[j] = len(str(self.compo[i][j]))
        for i in range(self.row):
            for j in range(self.column):
                return_str += "%*s " % (width[j], str(self.compo[i][j]))
            return_str += "\n"
        return return_str[:-1]

    __str__ = __repr__ 

    def __call__(self, arg):
        return self * arg


    # utility methods ----------------------------------------------------

    def copy(self):
        """
        
        Create a copy of the instance.
        
        """
        copy = self.__class__(self.row, self.column)
        copy.row = self.row
        copy.column = self.column
        for i in range(1, self.column+1):
            copy[i] = self[i]
        return copy

    def set(self, list):
        """

        set(list) : Substitute list for components
        
        """
        for i in range(self.row):
            self.compo[i] = list[self.column*i : self.column*(i+1)]

    def setRow(self, m, arg):
        """
        
        setRow(m, new_row) : new_row should be a list/Vector/Matrix
        
        """
        if isinstance(arg, list):
            self.compo[m-1] = arg[:]
        elif isinstance(arg, Matrix):
            for i in range(self.column):
                self.compo[m-1][i] = arg.compo[0][i]
        elif isinstance(arg, vector.Vector):
            for i in range(self.column):
                self.compo[m-1][i] = arg.compo[i]
        else:
            raise TypeError, self.setRow.__doc__
    
    def setColumn(self, n, arg):
        """
        
        setColumn(n, new_column) : new_column should be a list/Vector/Matrix
        
        """ 
        if isinstance(arg, list):
            for i in range(self.row):
                self.compo[i][n-1] = arg[i]
        elif isinstance(arg, Matrix):
            for j in range(self.row):
                self.compo[j][n-1] = arg.compo[j][0]
        elif isinstance(arg, vector.Vector):
            for j in range(self.row):
                self.compo[j][n-1] = arg.compo[j]
        else:
            raise TypeError, self.setColumn.__doc__

    def getRow(self, i):
        """
        
        getRow(i) : Return i-th row in form of Matrix
        
        """
        row = []
        for k in range(self.column):
            row.append(self.compo[i-1][k])
        return vector.Vector(row)

    def getColumn(self, j):
        """

        getColumn(j) : Return j-th column in form of Matrix
        
        """
        column = []
        for k in range(self.row):
            column.append(self.compo[k][j-1])
        return vector.Vector(column)

    def swapRow(self, m1, m2):
        """
        
        swapRow(m1, m2) : Swap self's m1-th row and m2-th row.
        
        """
        tmp = self.compo[m1-1][:]
        self.compo[m1-1] = self.compo[m2-1][:]
        self.compo[m2-1] = tmp[:]

    def swapColumn(self, n1, n2):
        """
        
        swapColumn(n1, n2) : Swap self's n1-th column and n2-th column.
        
        """
        tmp = self[n1]
        self.setColumn(n1, self[n2])
        self.setColumn(n2, tmp)

    def insertRow(self, i, arg):
        """
        
        insertRow(i, new_row) : new_row can be a list or a Matrix
        
        """ 
        if isinstance(arg, list):
            self.compo.insert(i-1, arg)
            self.row += 1
        elif isinstance(arg, Matrix):
            self.compo += arg.compo
            self.row += arg.row
        else:
            raise TypeError

    def insertColumn(self, j, arg):
        """
        
        insertColumn(j, arg) : new_column can be a list or a Matrix
        
        """
        if isinstance(arg, list):
            for k in range(self.row):
                self.compo[k].insert(j-1, list[k])
                self.column += 1
        elif isinstance(arg, Matrix):
            for k in range(arg.row):
                self.compo[k] = self.compo[k][:j-1] + arg.compo[k] + self.compo[k][j-1:]
            self.column += arg.column
        else:
            raise TypeError

    def deleteRow(self, i):
        self.row -= 1
        del self.compo[i-1]

    def deleteColumn(self, j):
        self.column -= 1
        for k in range(self.row):
            del self.compo[k][j-1]

    def getRing(self):
        if self.row == self.column:
            return MatrixRing.getInstance(self.row)
        else:
            raise NoRing


    # Mathematical functions ---------------------------------------------

    def transpose(self):
        """
        
        Return transposed matrix of self.
    
        """
        trans = self.__class__(self.column, self.row)
        for i in range(1, trans.row+1):
            for j in range(1, trans.column+1):
                trans[i,j] = self[j,i]
        return trans

    def triangulate(self):
        """
        
        Return triangulated matrix of self.
    
        """
        triangle = self.copy()
        for i in range(triangle.row):
            if triangle.compo[i][i] == 0:
                for k in range(i+1, triangle.row):
                    if triangle.compo[k][i] != 0:
                        triangle.swapRow(i+1, k+1)
                        for l in range(triangle.column):     # for calculation of determinant
                            triangle.compo[i+1][l] *= -1
                        break        # break the second loop
                else:
                    continue         # the below components are all 0. Back to the first loop
            for k in range(i+1, triangle.row):
                ratio = triangle.compo[k][i] / rational.Rational(triangle.compo[i][i])
                for l in range(i, triangle.column):
                    triangle.compo[k][l] -= rational.Rational(triangle.compo[i][l] * ratio)
            
        return triangle

    def isUpperTriangularMatrix(M):
        for j in range(M.column):
            for i in range(j+1, M.row):
                if M.compo[i][j] != 0:
                    return False
        return True

    def isLowerTriangularMatrix(M):
        return M.transpose().isUpperTriangularMatrix()

    def trace(self):
        """
        
        Return trace of self.
    
        """
        trace = 0
        for i in range(self.row):
            trace += self.compo[i][i]
        return trace

    def determinant(self):
        """
        
        Return determinant of self.
    
        """
        det = 1
        if self.row != self.column:
            raise MatrixSizeError, "not square matrix"
        triangle = self.triangulate()
        for i in range(self.row):
            det *= triangle.compo[i][i]
        return det

    def submatrix(self, i, j):
        """
        
        Return submatrix which deleted i-th row and j-th column from self.
    
        """
        sub = self.copy()
        sub.deleteRow(i)
        sub.deleteColumn(j)
        return sub

    def cofactors(self):
        cofactors = Matrix(self.row, self.column)
        for i in range(cofactors.row):
            for j in range(cofactors.column):
                cofactors.compo[j][i] = (-1)**(i+j) * (self.submatrix(i+1, j+1)).determinant()
        return cofactors

    def inverse(self):
        """
        
        Return inverse matrix of self if exists,
        or return None.
        
        """
        if self.row != self.column:
            raise MatrixSizeError
        return self.inverseImage(unitMatrix(self.row))

    def characteristicPolynomial(self):        # Algorithm 2.2.7 of Cohen's book
        """
        
        characteristicPolynomial() -> Polynomial
        
        """
        if self.row != self.column:
            raise MatrixSizeError, "not square matrix"
        i = 0
        C = unitMatrix(self.row)
        coeff = [0] * (self.row+1)
        coeff[0] = 1
        for i in range(1, self.row+1):
            C = self * C
            coeff[i] = (-1) * C.trace() / rational.Rational(i, 1)
            C = C + coeff[i] * unitMatrix(self.row)
        import polynomial
        coeff.reverse()
        return polynomial.OneVariableDensePolynomial(coeff, "x")

    def LUDecomposition(self):
        """

        LUDecomposition() -> (L, U)

        L and U are matrices such that
            self == L * U
            L : lower triangular matrix
            U : upper triangular matrix

        """

        A = self.copy()
        n = A.row
        L = unitMatrix(n)
        U = unitMatrix(n)

        # initialize L and U
        for i in range(n):
            for j in range(n):
                if i == j:
                    L.compo[i][j] = 1
                else:
                    L.compo[i][j] = 0
                U.compo[i][j] = A.compo[i][j]

        for i in range(n):
            for j in range(i+1, n):
                L.compo[j][i] = U.compo[j][i] / rational.Rational(U.compo[i][i])
                for k in range(i, n):
                    U.compo[j][k] = U.compo[j][k] - U.compo[i][k] * L.compo[j][i]

        return (L, U)

    def cohensSimplify(self):      # common process of image() and kernel()
        """
        
        cohensSimplify is used in image() and kernel()
        
        """
        c = [0] * (self.row + 1)
        d = [-1] * (self.column + 1)
        for k in range(1, self.column+1):
            j = 1
            while j <= self.row:
                if self[j,k] != 0 and c[j] == 0:
                    break
                j = j+1
            else:           # not found j such that m(j,k)!=0 and c[j]==0
                d[k] = 0
                continue
            top = (-1) / rational.Rational(self[j,k])
            self[j,k] = -1
            for s in range(k+1, self.column+1):
                self[j,s] = top * self[j,s] 
            for i in range(1, self.row+1):
                if i == j:
                    continue
                top = self[i,k]
                self[i,k] = 0
                for s in range(k+1, self.column+1):
                    self[i,s] = self[i,s] + top * self[j,s]
            c[j] = k
            d[k] = j
        return (c,d)

    def kernel(self):       # Algorithm 2.3.1 of Cohen's book
        """
        
        Return a Matrix which column vectors are one basis of self's kernel,
        or return None if self's kernel is 0.
        
        """
        M = self.copy()
        tmp = M.cohensSimplify()
        c = tmp[0]
        d = tmp[1]
        basis = []
        vector = [0] * (M.column+1)
        for k in range(1, M.column+1):
            if d[k] != 0:
                continue
            for i in range(1, M.column+1):
                if d[i] > 0:
                    vector[i] = M[d[i],k]
                elif i == k:
                    vector[i] = 1
                else:
                    vector[i] = 0
            basis.append(vector[1:])
        if len(basis) == 0:
            return None
        output = Matrix(self.column, len(basis))
        for j in range(1, output.column + 1):
            if(other==0):
                return ZeroDivisionError
            output.setColumn(j, basis[j-1])
        return output

    def image(self):        # Algorithm 2.3.2 of Cohen's book
        """
        
        Return a Matrix which column vectors are one basis of self's image,
        or return None if self's image is 0.
        
        """
        M = self.copy()
        tmp = M.cohensSimplify()
        c = tmp[0]
        basis = []
        for j in range(1, M.row+1):
            if c[j] != 0:
                basis.append(self[c[j]])
        output = Matrix(self.row, len(basis))
        for j in range(1, output.column + 1):
            output.setColumn(j, basis[j-1])
        return output

    def rank(self):
        """
        
        Return rank of self.

        """
        return len(self.image())

    def inverseImage(self, V):    # Algorithm 2.3.5 of Cohen's book
        """

        inverseImage(V) -> X

        such that
        self * X == V

        """ 
        M = self.copy()
        m = M.row; n = M.column; r = V.column
        X = Matrix(n,r)

        # step 1
        B = V.copy()

        # step 2 - 
        for j in range(n):
            # step 3
            for i in range(j,m):
                if M.compo[i][j] != 0:
                    break
            else:
                raise VectorsNotIndependent
            # step 4
            if i > j:
                for l in range(n):
                    t = M.compo[i][l]; M.compo[i][l] = M.compo[j][l]; M.compo[j][l] = t
                for l in range(r):
                    t = B.compo[i][l]; B.compo[i][l] = B.compo[j][l]; B.compo[j][l] = t 
            # step 5
            d = 1 / rational.Rational(M.compo[j][j])
            for k in range(j+1, m):
                ck = d * rational.Rational(M.compo[k][j])
                for l in range(j+1, n):
                    M.compo[k][l] -= ck * M.compo[j][l]
                for l in range(r):
                    B.compo[k][l] -= ck * B.compo[j][l]
        # step 6
        for i in range(n-1, -1, -1):
            for k in range(r):
                sum = 0
                for j in range(i+1, n):
                    sum += M.compo[i][j] * X.compo[j][k]
                X.compo[i][k] = (B.compo[i][k] - sum) / M.compo[i][i]

        for k in range(n+1, m):
            for j in range(r):
                sum = 0
                for i in range(n):
                    sum += M.compo[k][i] * X.compo[i][j]
                if (sum != B.compo[k][j]): 
                    raise NoInverseImage, "some vectors are not in the inverse image"

        return X

    def hessenbergForm(self):      # Algorithm 2.2.9 of Cohen's book
        if self.row != self.column:
            raise MatrixSizeError 
        n = self.row

        # step 1 
        H = self.copy()
        for m in range(2, H.row):
            # step 2
            for i in range(m+1, n+1):
                if H[i,m-1] != 0:
                    break
            else:
                continue
            t = H[i,m-1]
            if i > m:
                for j in range(m-1, n+1):
                    tmp = H[i,j] ; H[i,j] = H[m,j] ; H[m,j] = tmp
                H.swapColumn(i,m)
            # step 3
            for i in range(m+1,n+1):
                if H[i,m-1] != 0:
                    u = H[i,m-1] / rational.Rational(t)
                    for j in range(m,n+1):
                        H[i,j] -= u * H[m,j]
                        H[i,m-1] = 0 
                    H.setColumn(m, H[m] + u * H[i] )
        return H

    def columnEchelonForm(self):  # Algorithm 2.3.11 of Cohen's book
        """
        
        Return a Matrix in column echelon form whose image is equal to the image of self.
    
        """
        M = self.copy()
        k = M.column
        for i in range(M.row, 0, -1):
            for j in range(k, 0, -1):
                if M[i,j] != 0:
                    break
            else:
                continue
            d = 1 / rational.Rational(M[i,j])
            for l in range(1, i+1):
                t = d * M[l,j]
                M[l,j] = M[l,k]
                M[l,k] = t
            for j in range(1, M.column+1):
                if j == k:
                    continue
                for l in range(1,i+1):
                    M[l,j] = M[l,j] - M[l,k] * M[i,j]
            k = k-1
        return M 


class IntegerMatrix(Matrix):
    """

    IntegerMatrix is a class for matrices
    which coefficients are all integers.

    """

    def __div__(self, other):
        """
        
        division by a scalar
        
        """
        if (other == 1) or (other == -1) :
            return self * other
        else:
            raise NoInverse

    def __mod__(self,other):
        if isinstance(other, vector.Vector):
            return NotImplemented
        else:
            if other == 0:
                return ZeroDivisionError
            for i in range(self.row):
                self[i] = (self[i] % other)
            return self

    def hermiteNormalForm(self):  # Algorithm 2.4.4 of Cohen's book
        """Return a Matrix in Hermite Normal Form."""
        A = self.copy()
        # step 1 [Initialize]
        i = self.row; k = self.column
        if self.row <= self.column:
            l = 1
        else:
            l = self.row - self.column + 1
        while 1:
            while 1:
                # step 2 [Row finished?]
                for j in range(1, k):
                    if A[i,j] != 0:
                        break
                else:       # i.e. all the A[i,j] with j<k are zero
                    if A[i,k] < 0:
                        A[k] = -A[k]
                    break   # go to step 5
                # step 3 [Choose non-zero entry]
                j0 = j  # the first non-zero's index
                for j in range(2, k+1): # Pick among the non-zero A[i,j] for j <= k one with the smallest absolute value
                    if  0 < abs(A[i,j]) < abs(A[i,j0]):
                        j0 = j 
                if j0 < k:
                    A.swapColumn(k,j0)
                if A[i,k] < 0:
                    A[k] = -A[k]
                b = A[i,k]
                # step 4 [Reduce]
                for j in range(1, k):
                    q = A[i,j] // b
                    A[j] = A[j] - q * A[k]
            # step5 [Final reductions]
            b = A[i,k]
            if b == 0:
                k += 1
            else:
                for j in range(k+1, self.column+1):
                    q = A[i,j] // b
                    A[j] = A[j] - q * A[k]
            # step 6 [Finished?]
            if i == l:
                W = Matrix(self.row, self.column-k+1)
                for j in range(1, self.column-k+2):
                    W[j] = A[j+k-1]
                return W
            else:
                i -= 1; k -= 1
                # go to step 2

    def smith(self):
        """
        To find the Smith Normal Form for square non-singular integral matrix.
        Return the list of diagonal elements.
        """

        M = self.copy()
        n = M.row
        if M.row != M.column:
            raise ValueError("not square matrix")

        R = int(M.determinant())
        if R < 0:
            R = -R
        lst = []
        if R == 0:
            raise ValueError("Don't input matrix whose determinant is 0")
        else :
            if R == 1:
                for x in range(n-1):
                    lst.append(1)
                n = 1
        import nzmath.gcd as gcd
        import nzmath.vector as vector
        while n != 1:
            j = n
            c = 0
            while j != 1:
                j = j-1
                if M[n, j] != 0:
                    u, v, d = gcd.extgcd(M[n, n],M[n, j])
                    B = u * M.getColumn(n) + v * M.getColumn(j)
                    M.setColumn(j, (((M[n, n] // d) * M.getColumn(j)
                                     - (M[n, j] // d) * M.getColumn(n)) % R))
                    M.setColumn(n, (B % R))

            j = n
            while j != 1:
                j = j-1
                if M[j, n] != 0:
                    u, v, d = gcd.extgcd(M[n, n],M[j, n])
                    B = u * M.getRow(n) + v * M.getRow(j)
                    M.setRow(j, (((M[n, n] // d) * M.getRow(j)
                                  - (M[j,n] // d) * M.getRow(n)) % R))
                    M.setRow(n, (B % R))
                    c = c+1

            if c <= 0:
                b = int(M[n, n])
                flag = False
                for k in range(1, n):
                    for l in range(1, n):
                        if (M[k, l] % b) != 0:
                            M.setRow(n, M.getRow(n) + M.getRow(k))
                            flag = True

                if not flag:
                    dd = gcd.gcd(M[n,n], R)
                    lst.append(dd)
                    R = (R // dd)
                    n = n-1

        dd = gcd.gcd(M[1,1], R)
        lst.append(dd)
        lst.reverse()
        return lst


class MatrixRing:
    """

    MatrixRing is a class for matrix rings.

    """ 
    _instances = {}

    def __init__(self, size):
        self.size = size

    def __repr__(self):
        return "MatrixRing(%d)" % self.size

    def getInstance(self, size):
        if size not in self._instances:
            anInstance = MatrixRing(size)
            self._instances[size] = anInstance
        return self._instances[size]

    getInstance = classmethod(getInstance)

    def unitMatrix(self):
        return unitMatrix(self.size)

class Subspace(Matrix):
    """
    
    Subspace is a class for subspaces.
    
    """

    def supplementBasis(self):     # Algorithm 2.3.6 of Cohen's book
        """
        
        Return a basis of full space, which including self's column vectors.
    
        """
        if self.row < self.column:
            raise MatrixSizeError

        n = self.row
        k = self.column

        M = self.copy()
        B = unitMatrix(n)

        for s in range(k):
            found = 0; t = s
            while (not found and t < n):
                found  = M.compo[t][s] != 0
                if not found:
                    t += 1
            if not found:
                raise VectorsNotIndependent
            d = 1 / rational.Rational(M.compo[t][s])
            M.compo[t][s] = 1
            if t != s:
                for i in range(n):
                    B.compo[i][t] = B.compo[i][s]
            for i in range(n):
                B.compo[i][s] = self.compo[i][s]
            for j in range(k):
                for i in range(n):
                    if i != s and i != t and i != j:
                        M.compo[i][j] = 0
            for j in range(s+1,k):
                if t != s:
                    tmp = M.compo[s][j]; M.compo[s][j] = M.compo[t][j]; M.compo[t][j] = tmp
                d *= M.compo[s][j]
                for i in range(n):
                    if i != s and i != t:
                        M.compo[i][j] -= M.compo[i][s] * d
                    else:
                        M.compo[i][j] = 0
        return B


# --------------------------------------------------------------------
#       the belows are not class methods
# --------------------------------------------------------------------

def unitMatrix(size):
    unit_matrix = Matrix(size, size)
    for i in range(size):
        unit_matrix.compo[i][i] = 1
    return unit_matrix

def sumOfSubspaces(L, M):             # Algorithm 2.3.8 of Cohen's book
    if L.row != M.row:
        raise MatrixSizeError
    N = L.copy()
    for j in range(1, M.column+1):
        N.insertColumn(L.column+j, M[j])
    return N.image()

def intersectionOfSubspaces(M, M_):    # Algorithm 2.3.9 of Cohen's book
    if M.row != M_.row:
        raise MatrixSizeError
    M1 = Matrix(M.row, M.column + M_.column)
    for j in range(1, M.column+1):
        M1.setColumn(j, M[j])
    for j in range(1, M_.column+1):
        M1.setColumn(M.column + j, M_[j])
    N = M1.kernel()
    N1 = Matrix(M.column , N.column)    # N.column is the dimension of kernel(M1)
    for j in range(1, M.column + 1):
        N1.setRow(j, N.getRow(j))
    M2 = M * N1
    return M2.image()


#--------------------------------------------------------------------
#   define exceptions 
#--------------------------------------------------------------------

class MatrixSizeError(Exception):
    pass

class VectorsNotIndependent(Exception):
    pass

class NoInverseImage(Exception):
    pass

class NoInverse(Exception):
    pass

class NoRing(Exception):
    pass


#--------------------------------------------------------------------
# for debugging
#--------------------------------------------------------------------

if __name__ == '__main__':

    def pause():
        print "--- hit enter key ---"
        raw_input()

    a = Matrix(5,3, [0,1,3]+[0,2,2]+[0,0,5]+[0,1,1]+[2,0,0]) 
    b = Matrix(2,2, [1,2,5,10]) 
    c = Matrix(3,3, [0,1,1,-1,1,0,2,2,3]) 
    d = Matrix(4,2, [0,1,0,1]+[2,0,0,3]) 
    e = Matrix(3,2, [1,0]+[2,1]+[1,1]) 
    f = Matrix(3,2, [0,1]+[-1,4]+[2,6]) 
    h = Matrix(4,4,[-2,-2,-1,2,-1,-3,-13,-2,-1,0,2,0,-8,-8,-14,3]) 
    i = Matrix(2,3,[-1,-2,-3,1,4,5]) 
    sb = Matrix(4,3,[1,0,2]+[0,3,4]+[5,6,7]+[8,0,9]) 
    j = Matrix(2,2,[3,4,5,6]) 
    k = Matrix(3,3,[7,2,8,0,5,-2,0,1,9]) 
    A = Matrix(4,4,[1,1,0,3]+[2,1,-1,1]+[3,-1,-1,2]+[-1,2,3,-1])

    L, U = A.LUDecomposition()
    print A
    print L
    print U
    print L * U
    if L*U == A:
        print "True"
    else:
        print "False"
    B = Matrix(3,3, [1,2,3]+[2,8,11]+[3,22,25])
    print B
    L, U = B.LUDecomposition()
    print L
    print U
    print L * U
    print L * U == B
