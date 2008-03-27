from __future__ import division

import nzmath.gcd as gcd
import nzmath.rational as rational
import nzmath.ring as ring
import nzmath.vector as vector


class Matrix(object):
    """
    Matrix is a class for matrices.
    """

    def __init__(self, row, column, compo=0, coeff_ring=0):
        """
        Matrix(row, column [,components])
        """
        self._initialize(row, column, compo, coeff_ring)
        self._selectMatrix()

    def _initialize(self, row, column, compo=0, coeff_ring=0):
        """
        initialize matrix.
        """
        if (rational.isIntegerObject(row)
            and rational.isIntegerObject(column)
            and row > 0
            and column > 0 ): # row and column check
            self.row = row
            self.column = column
            self.compo = []
            if isinstance(compo, ring.Ring):
                coeff_ring = compo
                compo = 0
            if compo == 0:
                zero = 0
                if coeff_ring != 0:
                    zero = coeff_ring.zero
                for i in range(self.row):
                    self.compo.append([zero] * self.column)
            else:
                if (len(compo) != self.row * self.column):
                    raise ValueError, "number of given components is not match the matrix size"
                for i in range(self.row):
                    self.compo.append(compo[self.column*i : self.column*(i + 1)])
            if coeff_ring == 0:
                self.coeff_ring = ring.getRing(self.compo[0][0])
            else:
                self.coeff_ring = coeff_ring
        else:
            raise ValueError, "invalid value for matrix size"

    def _selectMatrix(self):
        """
        Select Matrix class.
        """
        if self.coeff_ring.isfield():
            if self.row == self.column:
                self.__class__ = FieldSquareMatrix
            else:
                self.__class__ = FieldMatrix
        else:
            if self.row == self.column:
                self.__class__ = RingSquareMatrix
            else:
                self.__class__ = RingMatrix

    def __getitem__(self, index):
        """
        M[i,j] : Return (i,j)-component of M.
        M[i] <==> M.getColumn(i)
        """
        if isinstance(index, tuple):
            return self.compo[index[0] - 1][index[1] - 1]
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
            self.compo[key[0] - 1][key[1] - 1] = value
        elif isinstance(key, (int, long)):
            self.setColumn(key, value)
        else:
            raise TypeError, self.__setitem__.__doc__

    def __eq__(self, other):
        """
        Check self == other.
        self == 0 means whether self == zeromatrix or not.
        """
        if isinstance(other, Matrix):
            if (self.row != other.row) or (self.column != other.column):
                return False
            for i in range(self.row):
                for j in range(self.column):
                    if self.compo[i][j] != other.compo[i][j]:
                        return False
            return True
        elif isinstance(other, int) and other == 0: # zero matrix ?
            for i in range(self.row):
                for j in range(self.column):
                    if self.compo[i][j]:
                        return False
            return True
        else:
            raise TypeError

    def __repr__(self):
        return_str = ""
        for i in range(self.row):
            return_str += str(self.compo[i])
            if i + 1 != self.row:
                return_str += "+"
        return return_str

    def __str__(self):
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

    def __call__(self, arg):
        """
        Return matrix applied __call__ to each elements.
        """
        sol = []
        for i in range(self.row):
            for j in range(self.column):
                ele = self.compo[i][j]
                if callable(ele):
                    sol.append(ele(arg))
                else:
                    sol.append(ele)
        return createMatrix(self.row, self.column, sol)


    # utility methods ----------------------------------------------------

    def copy(self):
        """
        Create a copy of the instance.
        """
        compos = []
        for i in range(self.row):
            for j in range(self.column):
                compos.append(self.compo[i][j])
        Mat = self.__class__(self.row, self.column, compos, self.coeff_ring)
        return Mat
    
    def set(self, list):
        """
        set(list) : Substitute list for components
        """
        if (len(list) != self.row * self.column):
            raise ValueError, "number of given components is not match the matrix size"
        for i in range(self.row):
            self.compo[i] = list[self.column*i : self.column*(i + 1)]

    def setRow(self, m, arg):
        """
        setRow(m, new_row) : new_row should be a list/Vector
        """
        if isinstance(arg, list):
            if (len(arg) != self.column):
                raise vector.VectorSizeError, "number of given components is not match the row size"
            self.compo[m - 1] = arg[:]
        elif isinstance(arg, vector.Vector):
            if (len(arg) != self.column):
                raise vector.VectorSizeError, "number of given components is not match the row size"
            self.compo[m - 1] = arg.compo[:]
        else:
            raise TypeError, self.setRow.__doc__

    def setColumn(self, n, arg):
        """
        setColumn(n, new_column) : new_column should be a list/Vector
        """
        if isinstance(arg, list):
            if (len(arg) != self.row):
                raise ValueError, "number of given components is not match the column size"
            for i in range(self.row):
                self.compo[i][n - 1] = arg[i]
        elif isinstance(arg, vector.Vector):
            if (len(arg) != self.row):
                raise ValueError, "number of given components is not match the column size"
            for i in range(self.row):
                self.compo[i][n - 1] = arg.compo[i]
        else:
            raise TypeError, self.setColumn.__doc__

    def getRow(self, i):
        """
        getRow(i) : Return i-th row in form of Matrix
        """
        return vector.Vector(self.compo[i - 1])

    def getColumn(self, j):
        """
        getColumn(j) : Return j-th column in form of Matrix
        """
        column = []
        for k in range(self.row):
            column.append(self.compo[k][j - 1])
        return vector.Vector(column)

    def swapRow(self, m1, m2):
        """
        swapRow(m1, m2) : Swap self's m1-th row and m2-th row.
        """
        tmp = self.compo[m1 - 1][:]
        self.compo[m1 - 1] = self.compo[m2 - 1][:]
        self.compo[m2 - 1] = tmp[:]

    def swapColumn(self, n1, n2):
        """
        swapColumn(n1, n2) : Swap self's n1-th column and n2-th column.
        """
        for k in range(self.row):
            tmp = self.compo[k][n1 - 1]
            self.compo[k][n1 - 1] = self.compo[k][n2 - 1]
            self.compo[k][n2 - 1] = tmp

    def insertRow(self, i, arg):
        """
        insertRow(i, new_row) : added new_row
        new_row can be a list or a Matrix
        """
        if isinstance(arg, list):
            if self.column != len(arg):
                raise vector.VectorSizeError
            self.compo.insert(i - 1, arg)
            self.row += 1
        elif isinstance(arg, vector.Vector):
            if self.column != len(arg):
                raise vector.VectorSizeError
            self.compo.insert(i - 1, arg.compo)
            self.row += 1
        elif isinstance(arg, Matrix):
            if self.column != arg.column:
                raise MatrixSizeError
            self.compo += arg.compo
            self.row += arg.row
        else:
            raise TypeError
        self._selectMatrix()

    def insertColumn(self, j, arg):
        """
        insertColumn(j, arg) : added new_column
        new_column can be a list or a Matrix
        """
        if isinstance(arg, list):
            if self.row != len(arg):
                raise vector.VectorSizeError
            for k in range(self.row):
                self.compo[k].insert(j-1, arg[k])
            self.column += 1
        elif isinstance(arg, vector.Vector):
            if self.row != len(arg):
                raise vector.VectorSizeError
            for k in range(self.row):
                self.compo[k].insert(j-1, arg.compo[k])
            self.column += 1
        elif isinstance(arg, Matrix):
            if self.row != arg.row:
                raise MatrixSizeError
            for k in range(arg.row):
                self.compo[k] = self.compo[k][:j - 1] + arg.compo[k] + self.compo[k][j - 1:]
            self.column += arg.column
        else:
            raise TypeError
        self._selectMatrix()

    def deleteRow(self, i):
        """
        deleteRow(i) : deleted i-th row
        """
        self.row -= 1
        del self.compo[i - 1]
        self._selectMatrix()

    def deleteColumn(self, j):
        """
        deleteColumn(j) : deleted j-th column
        """
        self.column -= 1
        for k in range(self.row):
            del self.compo[k][j - 1]
        self._selectMatrix()

    # Mathematical functions ---------------------------------------------

    def transpose(self):
        """
        Return transposed matrix of self.
        """
        trans = []
        for j in range(1, self.column + 1):
            for i in range(1, self.row + 1):
                trans.append(self[i, j])
        return self.__class__(self.column, self.row, trans, self.coeff_ring)

    def blockMatrix(self, i1, i2, j1, j2):
        """
        Return block matrix whose size is (i2-i1+1) * (j2-j1+1).
        """
        if i1 > i2 or j1 > j2 or i2 > self.row or j2 > self.column:
            raise MatrixSizeError
        mat = []
        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                mat.append(self[i, j])
        return createMatrix(i2 - i1 + 1, j2 - j1 + 1, mat, self.coeff_ring)

    def submatrix(self, i, j):
        """
        Return submatrix which deleted i-th row and j-th column from self.
        """
        mat = self.copy()
        mat.deleteRow(i)
        mat.deleteColumn(j)
        return mat


class SquareMatrix(Matrix):
    """
    SquareMatrix is a class for square matrices.
    """

    def __init__(self, row, column=0, compo=0, coeff_ring=0):
        """
        SquareMatrix(row, column [,components])
        SquareMatrix must be row == column .
        """
        self._initialize(row, column, compo, coeff_ring)
        if self.coeff_ring.isfield():
            self.__class__ = FieldSquareMatrix
        else:
            self.__class__ = RingSquareMatrix

    def _initialize(self, row, column=0, compo=0, coeff_ring=0):
        """
        initialize matrix.
        """
        if isinstance(compo, ring.Ring):
            coeff_ring = compo
            compo = 0
        if isinstance(column, list):
            compo = column
            column = row
        elif isinstance(column, ring.Ring):
            coeff_ring = column
            column = row
        if row != column:
            raise ValueError, "not square matrix"
        if (rational.isIntegerObject(row) and row > 0):
            self.row = self.column = row
            self.compo = []
            if compo == 0:
                zero = 0
                if coeff_ring != 0:
                    zero = coeff_ring.zero
                for i in range(self.row):
                    self.compo.append([zero] * self.column)
            else:
                if (len(compo) != self.row ** 2):
                    raise ValueError, "number of given components is not match the matrix size"
                for i in range(self.row):
                    self.compo.append(compo[self.column*i : self.column*(i + 1)])
            if coeff_ring == 0:
                self.coeff_ring = ring.getRing(self.compo[0][0])
            else:
                self.coeff_ring = coeff_ring
        else:
            raise ValueError, "invalid value for matrix size"

    def isUpperTriangularMatrix(self):
        """
        Check whether self is upper triangular matrix or not.
        """
        for j in range(self.column):
            for i in range(j + 1, self.row):
                if self.compo[i][j]:
                    return False
        return True

    def isLowerTriangularMatrix(self):
        """
        Check whether self is lower triangular matrix or not.
        """
        for i in range(self.row):
            for j in range(i + 1, self.column):
                if self.compo[i][j]:
                    return False
        return True

    def isDiagonalMatrix(self):
        """
        Check whether self is diagonal matrix or not.
        """
        return self.isUpperTriangularMatrix() and self.isLowerTriangularMatrix()

    def isScalarMatrix(self):
        """
        Check whether self is scalar matrix or not.
        Scalar matrix is matrix which is unit matrix times some scalar.
        """
        if not(self.isDiagonalMatrix()):
            return False
        chk = self.compo[0][0]
        for i in range(1, self.row):
            if self.compo[i][i] != chk:
                return False
        return True

    def isSymmetricMatrix(self):
        """
        Check whether self is symmetric matrix or not.
        """
        for i in range(self.row):
            for j in range(i + 1, self.column):
                if self.compo[i][j] != self.compo[j][i]:
                    return False
        return True


class RingMatrix(Matrix):
    """
    RingMatrix is a class for matrices whose elements are in ring.
    """

    def __init__(self, row, column, compo=0, coeff_ring=0):
        """
        RingMatrix(row, column [,components])
        """
        self._initialize(row, column, compo, coeff_ring)

    def __add__(self, other):
        """
        Return matrix addition.
        """
        if (self.row != other.row) or (self.column != other.column):
            raise MatrixSizeError
        sums = []
        for i in range(self.row):
            for j in range(self.column):
                sums.append(self.compo[i][j] + other.compo[i][j])
        return createMatrix(self.row, self.column, sums,
                  self.coeff_ring.getCommonSuperring(other.coeff_ring))

    def __sub__(self, other):
        """
        Return matrix subtraction.
        """
        if (self.row != other.row) or (self.column != other.column):
            raise MatrixSizeError
        diff = []
        for i in range(self.row):
            for j in range(self.column):
                diff.append(self.compo[i][j] - other.compo[i][j])
        return createMatrix(self.row, self.column, diff,
                  self.coeff_ring.getCommonSuperring(other.coeff_ring))

    def __mul__(self, other):
        """
        multiplication with a Matrix or a scalar
        """
        if isinstance(other, Matrix):
            if self.column != other.row:
                raise MatrixSizeError
            product = []
            for i in range(1, self.row + 1):
                for j in range(1, other.column + 1):
                    part_product = self[i, 1] * other[1, j]
                    for k in range(2, self.column + 1):
                        part_product = part_product + self[i, k] * other[k, j]
                    product.append(part_product)
            return createMatrix(self.row, other.column, product,
                      self.coeff_ring.getCommonSuperring(other.coeff_ring))
        elif isinstance(other, vector.Vector):
            if self.column != len(other):
                raise vector.VectorSizeError
            product = []
            for i in range(1, self.row + 1):
                part_product = self[i, 1] * other[1]
                for j in range(2, self.column + 1):
                    part_product = part_product + self[i, j] * other[j]
                product.append(part_product)
            return vector.Vector(product)
        else: #scalar mul
            product = []
            for i in range(1, self.row + 1):
                for j in range(1, self.column + 1):
                    product.append(self[i, j] * other)
            return createMatrix(self.row, self.column, product,
                      self.coeff_ring.getCommonSuperring(ring.getRing(other)))

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            if other.column != self.row:
                raise MatrixSizeError
            product = []
            for i in range(1, other.row + 1):
                for j in range(1, self.column + 1):
                    part_product = other[i, 1] * self[1, j]
                    for k in range(2, self.row + 1):
                        part_product = part_product + other[i, k] * self[k, j]
                    product.append(part_product)
            return createMatrix(other.row, self.column, product,
                     self.coeff_ring.getCommonSuperring(other.coeff_ring))
        elif isinstance(other, vector.Vector):
            if self.row != len(other):
                raise vector.VectorSizeError
            product = []
            for j in range(1, self.column + 1):
                part_product = other[1] * self[1, j]
                for i in range(2, self.row + 1):
                    part_product = part_product + other[i] * self[i, j]
                product.append(part_product)
            return vector.Vector(product)
        else:
            product = []
            for i in range(1, self.row + 1):
                for j in range(1, self.column + 1):
                    product.append(self[i, j] * other)
            return createMatrix(self.row, self.column, product,
                     self.coeff_ring.getCommonSuperring(ring.getRing(other)))

    def __mod__(self, other):
        """
        return self modulo other.
        """
        if not bool(other):
            raise ZeroDivisionError
        mod = []
        for i in range(1, self.row + 1):
            for j in range(1, self.column + 1):
                mod.append(self[i, j] % other)
        return createMatrix(self.row, self.column, mod, self.coeff_ring)

    def __neg__(self):
        return (-1) * self

    def getCoefficientRing(self):
        """
        Set and return coefficient ring.
        """
        if not hasattr(self, "_coeff_ring"):
            scalars = None
            for i in range(self.row):
                for j in range(self.column):
                    cring = ring.getRing(self[i, j])
                    if scalars is None or scalars != cring and scalars.issubring(cring):
                        scalars = cring
                    elif not scalars.issuperring(cring):
                        scalars = scalars.getCommonSuperring(cring)
            self._coeff_ring = self.coeff_ring = scalars
        return self._coeff_ring

    def toFieldMatrix(self):
        """RingMatrix -> FieldMatrix"""
        self.__class__ = FieldMatrix
        self.coeff_ring = self.coeff_ring.getQuotientField()

    def hermiteNormalForm(self):  # Algorithm 2.4.4 of Cohen's book
        """Return a Matrix in Hermite Normal Form."""
        A = self.copy()
        # step 1 [Initialize]
        i = self.row
        k = self.column
        if self.row <= self.column:
            l = 1
        else:
            l = self.row - self.column + 1
        while 1:
            while 1:
                # step 2 [Row finished?]
                for j in range(1, k):
                    if A[i, j]:
                        break
                else:       # i.e. all the A[i, j] with j<k are zero
                    if A[i, k] < 0:
                        A[k] = -A[k]
                    break   # go to step 5
                # step 3 [Choose non-zero entry]
                j0 = j  # the first non-zero's index
                for j in range(2, k + 1): # Pick among the non-zero A[i, j] for j <= k one with the smallest absolute value
                    if  0 < abs(A[i, j]) < abs(A[i, j0]):
                        j0 = j
                if j0 < k:
                    A.swapColumn(k, j0)
                if A[i, k] < 0:
                    A[k] = -A[k]
                b = A[i, k]
                # step 4 [Reduce]
                for j in range(1, k):
                    q = A[i, j] // b
                    A[j] = A[j] - q * A[k]
            # step5 [Final reductions]
            b = A[i, k]
            if not bool(b):
                k += 1
            else:
                for j in range(k + 1, self.column + 1):
                    q = A[i, j] // b
                    A[j] = A[j] - q * A[k]
            # step 6 [Finished?]
            if i == l:
                #W = createMatrix(self.row, self.column-k+1, self.coeff_ring)
                #for j in range(1, self.column-k+2):
                #    W[j] = A[j+k-1]
                return A
            else:
                i -= 1
                k -= 1
                # go to step 2


class RingSquareMatrix(SquareMatrix, RingMatrix):
    """
    RingSquareMatrix is a class for square matrices whose elements are in ring.
    """

    def __init__(self, row, column=0, compo=0, coeff_ring=0):
        """
        RingSquareMatrix(row, column [,components])
        RingSquareMatrix must be row == column .
        """
        self._initialize(row, column, compo, coeff_ring)

    def __pow__(self, other):
        """
        powering self to integer.
        """
        n = +other
        if not isinstance(n, (int, long)):
            raise TypeError("index must be an integer")
        power = unitMatrix(self.row, self.coeff_ring)
        # check n
        if n == 0:
            return power
        if n > 0:
            z = self.copy()
        else:
            if hasattr(self, "inverse"):
                n = abs(n)
                z = self.inverse()
            else:
                raise NoInverse
        while 1:
            if n & 1:
                power = power * z
            n //= 2
            if n == 0:
                return power
            z = z*z

    def toFieldMatrix(self):
        """RingSquareMatrix -> FieldSquareMatrix"""
        self.__class__ = FieldSquareMatrix
        self.coeff_ring = self.coeff_ring.getQuotientField()

    def getRing(self):
        """
        Return matrix ring of self.
        """
        return MatrixRing.getInstance(self.row, self.getCoefficientRing())

    def isOrthogonalMatrix(self):
        """
        Check whether self is orthogonal matrix or not.
        Orthogonal matrix satisfies M*M^T equals unit matrix.
        """
        return self * self.transpose() == unitMatrix(self.row, self.coeff_ring)

    def isAlternativeMatrix(self):
        """
        Check whether self is alternative matrix or not.
        Alternative (skew symmetric, or antisymmetric) matrix satisfies M=-M^T.
        """
        for i in range(self.row):
            for j in range(i, self.column):
                if self.compo[i][j] != -self.compo[j][i]:
                    return False
        return True

    isAntisymmetricMatrix = isAlternativeMatrix

    def trace(self):
        """
        Return trace of self.
        """
        trace = 0
        for i in range(self.row):
            trace = trace + self.compo[i][i]
        return trace

    def determinant(self): # Algorithm 2.2.6 of Cohen's book
        """
        Return determinant of self.
        """
        M = self.copy()
        n = self.row
        c = 1
        sign = True
        for k in range(1, n):
            p = M[k, k]
            if not bool(p): # p==0
                i = k + 1
                while not bool(M[i, k]):
                    if i == n:
                        return 0
                    else:
                        i += 1
                for j in range(k, n + 1):
                    tmp = M[i, j]
                    M[i, j] = M[k, j]
                    M[k, j] = tmp
                sign = not(sign)
                p = M[k, k]
            for i in range(k + 1, n + 1):
                for j in range(k+1, n+1):
                    t = p * M[i, j] - M[i, k] * M[k, j]
                    M[i, j] = t // c
            c = p
        if sign:
            return M[n, n]
        else:
            return -M[n, n]

    def cofactor(self, i, j):
        """
        Return (i, j)-cofactor of self.
        """
        cofactor = (self.submatrix(i, j)).determinant()
        if (i+j) & 1:
            cofactor = cofactor * (-1)
        return cofactor

    def commutator(self, other):
        """
        Return commutator defined as follows:
        [self, other] = self * other - other * self .
        """
        return self*other-other*self

    def characteristicPolynomial(self):        # Algorithm 2.2.7 of Cohen's book
        """
        characteristicPolynomial() -> Polynomial
        """
        C = unitMatrix(self.row, self.coeff_ring)
        coeff = [0] * (self.row + 1)
        coeff[0] = 1
        for i in range(1, self.row + 1):
            C = self * C
            if i == 1:
                coeff[i] = -C.trace()
            else:
                coeff[i] = -C.trace() // i
            C = C + coeff[i] * unitMatrix(self.row, self.coeff_ring)
        import nzmath.poly.uniutil as uniutil
        coeff.reverse()
        return uniutil.polynomial(dict(enumerate(coeff)), self.coeff_ring)

    def adjugateMatrix(self):        # Algorithm 2.2.7 of Cohen's book
        """
        Return adjugate(classical adjoint) matrix.
        """
        C = unitMatrix(self.row, self.coeff_ring)
        coeff = [0] * self.row
        coeff[0] = 1
        for i in range(1, self.row):
            C = self * C
            if i == 1:
                coeff[i] = -C.trace()
            else:
                coeff[i] = -C.trace() // i
            C = C + coeff[i] * unitMatrix(self.row, self.coeff_ring)
        if self.row & 1:
            return C
        else:
            return -C

    def cofactorMatrix(self):
        """
        Return cofactor matrix.
        """
        return self.adjugateMatrix().transpose()

    cofactors = cofactorMatrix

    def smithNormalForm(self):# Algorithm 2.4.14 of Cohen's book
        """
        Find the Smith Normal Form for square non-singular integral matrix.
        Return the list of diagonal elements.
        """
        M = self.copy()
        n = M.row
        R = M.determinant()
        rings = ring.getRing(M[1, 1])
        if not bool(R):
            raise ValueError("Don't input matrix whose determinant is 0")
        if R < 0:
            R = -R
        lst = []
        while n != 1:
            j = n
            c = 0
            while j != 1:
                j -= 1
                if M[n, j]:
                    u, v, d = rings.extgcd(M[n, j], M[n, n])
                    B = v * M.getColumn(n) + u * M.getColumn(j)
                    M.setColumn(j, (((M[n, n] // d) * M.getColumn(j)
                                     - (M[n, j] // d) * M.getColumn(n)) % R))
                    M.setColumn(n, (B % R))
            j = n
            while j != 1:
                j -= 1
                if M[j, n]:
                    u, v, d = rings.extgcd(M[j, n], M[n, n])
                    B = v * M.getRow(n) + u * M.getRow(j)
                    M.setRow(j, (((M[n, n] // d) * M.getRow(j)
                                  - (M[j, n] // d) * M.getRow(n)) % R))
                    M.setRow(n, (B % R))
                    c += 1
            if c <= 0:
                b = M[n, n]
                flag = False
                if not bool(b):
                    b = R
                for k in range(1, n):
                    for l in range(1, n):
                        if (M[k, l] % b) != 0:
                            M.setRow(n, M.getRow(n) + M.getRow(k))
                            flag = True
                if not flag:
                    dd = rings.gcd(M[n, n], R)
                    lst.append(dd)
                    R = (R // dd)
                    n -= 1
        dd = rings.gcd(M[1, 1], R)
        lst.append(dd)
        lst.reverse()
        return lst

    def extsmithNormalForm(self):
        """
        Find the Smith Normal Form M for square matrix,
        Computing U,V which satisfied M=U*self*V.
        Return matrices tuple,(U,V,M).
        """
        M = self.copy()
        n = M.row
        U = unitMatrix(M.row, M.coeff_ring)
        V = unitMatrix(M.row, M.coeff_ring)
        rings = ring.getRing(M[1, 1])
        while n != 1:
            j = n
            c = 0
            while j != 1:
                j -= 1
                if M[n, j]:
                    u, v, d = rings.extgcd(M[n, j], M[n, n])
                    M_nn = M[n, n] // d
                    M_nj = M[n, j] // d
                    B = v * M.getColumn(n) + u * M.getColumn(j)
                    M.setColumn(j, (M_nn * M.getColumn(j) - M_nj *
                    M.getColumn(n)))
                    M.setColumn(n, B)
                    B = v * V.getColumn(n) + u * V.getColumn(j)
                    V.setColumn(j, (M_nn * V.getColumn(j) - M_nj *
                    V.getColumn(n)))
                    V.setColumn(n, B)
            j = n
            while j != 1:
                j = j-1
                if M[j, n]:
                    u, v, d = rings.extgcd(M[j, n], M[n, n])
                    M_nn = M[n, n] // d
                    M_jn = M[j, n] // d
                    B = v * M.getRow(n) + u * M.getRow(j)
                    M.setRow(j, (M_nn * M.getRow(j) - M_jn * M.getRow(n)))
                    M.setRow(n, B)
                    B = v * U.getRow(n) + u * U.getRow(j)
                    U.setRow(j, (M_nn * U.getRow(j) - M_jn * U.getRow(n)))
                    U.setRow(n, B)
                    c += 1
            if c <= 0:
                b = M[n, n]
                flag = False
                for k in range(1, n):
                    for l in range(1, n):
                        if (M[k, l] % b):
                            M.setRow(n, M.getRow(n) + M.getRow(k))
                            U.setRow(n, U.getRow(n) + U.getRow(k))
                            flag = True
                if not flag:
                    n -= 1
        for j in range(1, M.column+1):
            if M[j, j] < 0:
                V[j] = -V[j]
                M[j, j] = -M[j, j]
        return (U, V, M)


class FieldMatrix(RingMatrix):
    """
    FieldMatrix is a class for matrices whose elements are in field.
    """

    def __init__(self, row, column, compo=0, coeff_ring=0):
        """
        FieldMatrix(row, column [,components])
        """
        self._initialize(row, column, compo, coeff_ring)
        if not self.coeff_ring.isfield():
            self.coeff_ring = self.coeff_ring.getQuotientField()

    def __truediv__(self, other):
        """
        division by a scalar.
        """
        return ring.inverse(other) * self

    __div__ = __truediv__ # backward compatibility?

    def _cohensSimplify(self):
        """
        _cohensSimplify is a common process used in image() and kernel()

        Return a tuple of modified matrix M, image data c and kernel data d.
        """
        M = self.copy()
        c = [0] * (M.row + 1)
        d = [-1] * (M.column + 1)
        for k in range(1, M.column + 1):
            for j in range(1, M.row + 1):
                if c[j] == 0 and M[j, k]:
                    break
            else:           # not found j such that m(j, k)!=0 and c[j]==0
                d[k] = 0
                continue
            top = -ring.inverse(M[j, k])
            M[j, k] = -1
            for s in range(k + 1, M.column + 1):
                M[j, s] = top * M[j, s]
            for i in range(1, M.row + 1):
                if i == j:
                    continue
                top = M[i, k]
                M[i, k] = 0
                for s in range(k + 1, M.column + 1):
                    M[i, s] = M[i, s] + top * M[j, s]
            c[j] = k
            d[k] = j
        return (M, c, d)

    def kernel(self):       # Algorithm 2.3.1 of Cohen's book
        """
        Return a Matrix which column vectors are one basis of self's kernel,
        or return None if self's kernel is 0.
        """
        tmp = self._cohensSimplify()
        M, d = tmp[0], tmp[2]
        basis = []
        for k in range(1, M.column + 1):
            if d[k]:
                continue
            vector = []
            for i in range(1, M.column + 1):
                if d[i] > 0:
                    vector.append(M[d[i], k])
                elif i == k:
                    vector.append(1)
                else:
                    vector.append(0)
            basis.append(vector)
        dimension = len(basis)
        if dimension == 0:
            return None
        output = zeroMatrix(self.column, dimension, self.coeff_ring)
        for j in range(1, dimension + 1):
            output.setColumn(j, basis[j - 1])
        return output

    def image(self):        # Algorithm 2.3.2 of Cohen's book
        """
        Return a Matrix which column vectors are one basis of self's image,
        or return None if self's image is 0.
        """
        tmp = self._cohensSimplify()
        M, c = tmp[0], tmp[1]
        basis = []
        for j in range(1, M.row + 1):
            if c[j]:
                basis.append(self[c[j]])
        dimension = len(basis)
        if dimension == 0:
            return None
        output = zeroMatrix(self.row, dimension, self.coeff_ring)
        for j in range(1, dimension + 1):
            output.setColumn(j, basis[j - 1])
        output._selectMatrix()
        return output

    def rank(self):
        """
        Return rank of self.
        """
        img = self.image()
        if img:
            return len(img.compo[0])
        else:
            return 0

    def inverseImage(self, V):    # modified Algorithm 2.3.5 of Cohen's book
        """
        inverseImage(V) -> X
        
        such that self * X == V
        """
        if isinstance(V, vector.Vector):
            if self.row != len(V):
                raise vector.VectorSizeError
            B = createMatrix(len(V), 1, V.compo)
        else:
            if self.row != V.row:
                raise MatrixSizeError
            B = V.copy() # step 1
        M = self.copy()
        m = M.row
        n = M.column
        r = V.column
        X = zeroMatrix(n, r, self.coeff_ring)
        non_zero = []
        i = 1
        # step 2
        for j in range(1, n+1):
            # step 3
            for k in range(i, m+1):
                if M[k, j]:
                    break
            else:
                continue
            # step 4
            if k > i:
                for l in range(j, n+1):
                    t = M[i, l]
                    M[i, l] = M[k, l]
                    M[k, l] = t
                B.swapRow(i, k)
            # step 5
            d = ring.inverse(M[i, j])
            for k in range(i + 1, m + 1):
                ck = d * M[k, j]
                for l in range(j + 1, n + 1):
                    M[k, l] = M[k, l] - ck * M[i, l]
                for l in range(r):
                    B[k, l] = B[k, l] - ck * B[i, l]
            non_zero.insert(0, j)
            i += 1
            if i > m:
                break
        # step 6
        i -= 1
        zero = self.coeff_ring.zero
        for j in non_zero:
            d = ring.inverse(M[i, j])
            for k in range(r):
                sums = zero
                for l in range(j + 1, n + 1):
                    sums = sums + M[i, l] * X[l, k]
                X[j, k] = (B[i, k] - sums) * d
            i -= 1
        # step 7
        i = len(non_zero) + 1
        for j in range(1, r + 1):
            for k in range(i, m + 1):
                if B[k, j]:
                    raise NoInverseImage
        return X

    def solve(self, B):  # modified Algorithm 2.3.4 of Cohen's book
        """
        Return solution X for self * X = B (B is vector).
        This function returns solution vector and kernel of self as vector basis.
        If you want only one solution, use 'inverseImage'.
        """
        M_1 = self.copy()
        M_1.insertColumn(self.column + 1, B.compo)
        V = M_1.kernel()
        ker = []
        flag = False
        if not V:
            raise NoInverseImage, "no solution"
        n = V.row
        for j in range(1, V.column + 1):
            if not bool(V[n, j]): # self's kernel
                ker.append(vector.Vector([V[i, j] for i in range(1, n)]))
            elif not(flag):
                d = -ring.inverse(V[n, j])
                sol = vector.Vector([V[i, j] * d for i in range(1, n)])
                flag = True
        if not(flag):
            raise NoInverseImage, "no solution"
        return sol, ker

    def columnEchelonForm(self):  # Algorithm 2.3.11 of Cohen's book
        """
        Return a Matrix in column echelon form whose image is equal to 
        the image of self.
        """
        M = self.copy()
        k = M.column
        for i in range(M.row, 0, -1):
            for j in range(k, 0, -1):
                if M[i, j]:
                    break
            else:
                continue
            d = ring.inverse(M[i, j])
            for l in range(1, i + 1):
                t = d * M[l, j]
                M[l, j] = M[l, k]
                M[l, k] = t
            for j in range(1, M.column + 1):
                if j == k:
                    continue
                for l in range(1, i+1):
                    M[l, j] = M[l, j] - M[l, k] * M[i, j]
            k -= 1
        return M


class FieldSquareMatrix(RingSquareMatrix, FieldMatrix):
    """
    FieldSquareMatrix is a class for square matrices in field.
    """

    def __init__(self, row, column=0, compo=0, coeff_ring=0):
        """
        FieldSquareMatrix(row, column [,components])
        FieldSquareMatrix must be row == column .
        """
        self._initialize(row, column, compo, coeff_ring)
        if not self.coeff_ring.isfield():
            self.coeff_ring = self.coeff_ring.getQuotientField()

    def triangulate(self):
        """
        Return triangulated matrix of self.
        """
        triangle = self.copy()
        flag = False # for calculation of determinant
        for i in range(triangle.row):
            if not triangle.compo[i][i]:
                for k in range(i + 1, triangle.row):
                    if triangle.compo[k][i]:
                        triangle.swapRow(i + 1, k + 1)
                        flag = not(flag)
                        break        # break the second loop
                else:
                    continue         # the below components are all 0. Back to the first loop
            for k in range(i + 1, triangle.row):
                inv_i_i = ring.inverse(triangle.compo[i][i])
                ratio = triangle.compo[k][i] * inv_i_i
                for l in range(i, triangle.column):
                    triangle.compo[k][l] = triangle.compo[k][l] - triangle.compo[i][l] * ratio
        if flag:
            for j in range(triangle.row, triangle.column + 1):
                triangle[triangle.row, j] = triangle[triangle.row, j] * (-1)
        return triangle

    def determinant(self):
        """
        Return determinant of self.
        """
        det = 1
        if self.row != self.column:
            raise MatrixSizeError, "not square matrix"
        triangle = self.triangulate()
        for i in range(self.row):
            det = det * triangle.compo[i][i]
        return det

    def inverse(self, V=1): # modified Algorithm 2.2.2, 2.3.5 of Cohen's book
        """
        Return inverse matrix of self or self.inverse() * V.
        If inverse does not exist, raise NoInverse error.
        """
        if isinstance(V, vector.Vector):
            if self.row != len(V):
                raise vector.VectorSizeError
            B = createMatrix(len(V), 1, V.compo)
        elif isinstance(V, Matrix):
            if self.row != V.row:
                raise MatrixSizeError
            B = V.copy() # step 1
        else: # V==1
            B = unitMatrix(self.row, self.coeff_ring)
        M = self.copy()
        n = M.row
        r = B.column
        X = zeroMatrix(n, r, self.coeff_ring)
        # step 2
        for j in range(n):
            # step 3
            for i in range(j, n):
                if M.compo[i][j]:
                    break
            else:
                raise NoInverse
            # step 4
            if i > j:
                for l in range(j, n):
                    t = M.compo[i][l]
                    M.compo[i][l] = M.compo[j][l]
                    M.compo[j][l] = t
                B.swapRow(i, j)
            # step 5
            d = ring.inverse(M.compo[j][j])
            for k in range(j + 1, n):
                ck = d * M.compo[k][j]
                for l in range(j + 1, n):
                    M.compo[k][l] = M.compo[k][l] - ck * M.compo[j][l]
                for l in range(r):
                    B.compo[k][l] = B.compo[k][l] - ck * B.compo[j][l]
        # step 6
        for i in range(n - 1, -1, -1):
            d = ring.inverse(M.compo[i][i])
            for k in range(r):
                sums = self.coeff_ring.zero
                for j in range(i + 1, n):
                    sums = sums + M.compo[i][j] * X.compo[j][k]
                X.compo[i][k] = (B.compo[i][k] - sums) * d
        if r != 1:
            return X
        else:
            return X[1]

    def hessenbergForm(self):      # Algorithm 2.2.9 of Cohen's book
        """Return a Matrix in Hessenberg Form."""
        n = self.row
        # step 1
        H = self.copy()
        for m in range(2, H.row):
            # step 2
            for i in range(m+1, n+1):
                if H[i, m - 1]:
                    break
            else:
                continue
            t = H[i, m - 1]
            if i > m:
                for j in range(m-1, n+1):
                    tmp = H[i, j]
                    H[i, j] = H[m, j]
                    H[m, j] = tmp
                H.swapColumn(i, m)
            # step 3
            for i in range(m + 1, n + 1):
                if H[i, m - 1] != 0:
                    u = H[i, m - 1] / t
                    for j in range(m, n + 1):
                        H[i, j] = H[i, j] - u * H[m, j]
                        H[i, m - 1] = 0
                    H.setColumn(m, H[m] + u * H[i])
        return H

    def LUDecomposition(self):
        """
        LUDecomposition() -> (L, U)
        
        L and U are matrices such that
            self == L * U
            L : lower triangular matrix
            U : upper triangular matrix
        """

        n = self.row
        L = unitMatrix(n, self.coeff_ring)
        U = self.copy()
        # initialize L and U
        for i in range(n):
            for j in range(i + 1, n):
                L.compo[j][i] = U.compo[j][i] * ring.inverse(U.compo[i][i])
                for k in range(i, n):
                    U.compo[j][k] = U.compo[j][k] - U.compo[i][k] * L.compo[j][i]
        return (L, U)


class MatrixRing (ring.Ring):
    """
    MatrixRing is a class for matrix rings.
    """

    _instances = {}

    def __init__(self, size, scalars):
        """
        MatrixRing(size, scalars)
        
        size: size of matrices (positive integer)
        scalars: ring of scalars
        """
        ring.Ring.__init__(self)
        self.size = size
        self.scalars = scalars

    def __eq__(self, other):
        """
        self == other
        """
        return (self.__class__ == other.__class__ and
                self.size == other.size and
                self.scalars == other.scalars)

    def __repr__(self):
        return "MatrixRing(%d, %s)" % (self.size, self.scalars)

    def __str__(self):
        return "M_%d(%s)" % (self.size, str(self.scalars))

    def getInstance(cls, size, scalars):
        """
        Return the cached instance of the specified matrix ring.  If
        the specified ring is not cached, it is created, cached and
        returned.
        
        The method is a class method.
        """
        if (size, scalars) not in cls._instances:
            anInstance = MatrixRing(size, scalars)
            cls._instances[size, scalars] = anInstance
        return cls._instances[size, scalars]

    getInstance = classmethod(getInstance)

    def unitMatrix(self):
        """
        Return the unit matrix.
        """
        return self.one.copy()

    def _getOne(self):
        """
        getter for one (unit matrix)
        """
        if self._one is None:
            components = [self.scalars.zero] * (self.size**2)
            for i in range(self.size):
                components[i*self.size + i] = self.scalars.one
            if self.scalars.isfield():
                self._one = FieldSquareMatrix(self.size, components)
            else:
                self._one = RingSquareMatrix(self.size, components)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit")

    def _getZero(self):
        """
        Return zero matrix.
        """
        if self._zero is None:
            components = [self.scalars.zero] * (self.size**2)
            self._zero = SquareMatrix(self.size, components)
        return self._zero

    zero = property(_getZero, None, None, "additive unit")

    def createElement(self, compo):
        """
        Return a newly created matrix from 'compo'.

        'compo' must be a list of n*n components in the scalar ring,
        where n = self.size.
        """
        return createMatrix(self.size, compo, self.scalars)

    def getCharacteristic(self):
        """
        Return the characteristic of the ring.
        """
        return self.scalars.getCharacteristic()

    def issubring(self, other):
        """
        Report whether another ring contains the ring as a subring.
        """
        if other is self:
            return True
        if not isinstance(other, MatrixRing):
            return False
        return self.size == other.size and self.scalars.issubring(other.scalars)

    def issuperring(self, other):
        """
        Report whether the ring is a superring of another ring.
        """
        if other is self:
            return True
        if not isinstance(other, MatrixRing):
            return False
        return self.size == other.size and self.scalars.issuperring(other.scalars)

    def getCommonSuperring(self, other):
        """
        Return common super ring of self and another ring.
        """
        if not isinstance(other, MatrixRing) or self.size != other.size:
            raise TypeError("no common super ring")
        return MatrixRing.getInstance(self.size, self.scalars.getCommonSuperring(other.scalars))


class Subspace(Matrix):
    """
    Subspace is a class for subspaces.
    """

    def __init__(self, row, column, compo=0, coeff_ring=0):
        """
        Subspace(row, column [,components])
        """
        self._initialize(row, column, compo, coeff_ring)

    def supplementBasis(self):     # Algorithm 2.3.6 of Cohen's book
        """
        Return a basis of full space, which including self's column vectors.
        """
        if self.row < self.column:
            raise MatrixSizeError
        n = self.row
        k = self.column
        M = self.copy()
        B = unitMatrix(n, self.coeff_ring)
        for s in range(k):
            for t in range(s, n):
                if M.compo[t][s]:
                    break
            else:
                raise VectorsNotIndependent
            d = ring.inverse(M.compo[t][s])
            M.compo[t][s] = 1
            if t != s:
                for i in range(n):
                    B.compo[i][t] = B.compo[i][s]
            for i in range(n):
                B.compo[i][s] = self.compo[i][s]
            for j in range(s + 1, k):
                if t != s:
                    tmp = M.compo[s][j]
                    M.compo[s][j] = M.compo[t][j]
                    M.compo[t][j] = tmp
                M.compo[s][j] *= d
                for i in range(n):
                    if i != s and i != t:
                        M.compo[i][j] = M.compo[i][j] - M.compo[i][s] * M.compo[s][j]
        return B


# --------------------------------------------------------------------
#       the belows are not class methods
# --------------------------------------------------------------------

def createMatrix(row, column=0, compo=0, coeff_ring=0):
    """
    generate new Matrix or SquareMatrix class.
    """
    if isinstance(compo, ring.Ring):
        coeff_ring = compo
        compo = 0
    if isinstance(column, list):
        compo = column
        column = row
    elif isinstance(column, ring.Ring):
        coeff_ring = column
        column = row
    if compo == 0:
        return zeroMatrix(row, column, coeff_ring)
    if coeff_ring == 0:
        coeff_ring = ring.getRing(compo[0])
    if coeff_ring.isfield():
        if row == column:
            return FieldSquareMatrix(row, compo, coeff_ring)
        else:
            return FieldMatrix(row, column, compo, coeff_ring)
    else:
        if row == column:
            return RingSquareMatrix(row, compo, coeff_ring)
        else:
            return RingMatrix(row, column, compo, coeff_ring)

def unitMatrix(size, coeff=1):
    """
    return unit matrix of size.
    coeff is subclass for ring.Ring or ring.Ring.one.
    """
    if isinstance(coeff, ring.Ring):
        one = coeff.one
        zero = coeff.zero
    else:
        one = coeff
        coeff = ring.getRing(one)
        zero = coeff.zero
    unit_matrix = [one]
    iter = [zero] * size + [one]
    for i in range(size - 1):
        unit_matrix = unit_matrix + iter
    return createMatrix(size, size, unit_matrix, coeff)

def zeroMatrix(row, column=None, coeff=0):
    """
    return zero matrix.
    coeff is subclass for ring.Ring or ring.Ring.zero.
    """
    if column == 0:
        coeff = 0
        column = row
    if not(rational.isIntegerObject(column)):
        if column == None:
            column = row
        else:
            coeff = column
            column = row
    if isinstance(coeff, ring.Ring):
        zero = coeff.zero
    else:
        zero = coeff
        coeff = ring.getRing(coeff)
    zero_matrix = [zero] * (row * column)
    return createMatrix(row, column, zero_matrix, coeff)

def sumOfSubspaces(L, M):             # Algorithm 2.3.8 of Cohen's book
    """
    Return space which is sum of L and M.
    """
    if L.row != M.row:
        raise MatrixSizeError
    N = L.copy()
    for j in range(1, M.column + 1):
        N.insertColumn(L.column + j, M[j])
    N.toFieldMatrix()
    return N.image()

def intersectionOfSubspaces(M, M_):    # Algorithm 2.3.9 of Cohen's book
    """
    Return space which is intersection of M and M_.
    """
    if M.row != M_.row:
        raise MatrixSizeError
    M1 = createMatrix(M.row, M.column + M_.column)
    for j in range(1, M.column + 1):
        M1.setColumn(j, M[j])
    for j in range(1, M_.column + 1):
        M1.setColumn(M.column + j, M_[j])
    M1.toFieldMatrix()
    N = M1.kernel()
    N1 = createMatrix(M.column , N.column)    # N.column is the dimension of kernel(M1)
    for j in range(1, M.column + 1):
        N1.setRow(j, N.getRow(j))
    M2 = M * N1
    M2.toFieldMatrix()
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
