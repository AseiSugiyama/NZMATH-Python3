# matrix.py

from rational import * 
import ring

MatrixSizeError = "MatrixSizeError"
NoInverse = "NoInverse"

class Matrix:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.compo = []
        for i in range(self.row):
            self.compo.append([0] * self.column)

    def __repr__(self):
        return_str = ""
        for i in range(self.row):
            for j in range(self.column):
                return_str += `self.compo[i][j]` + " "
            return_str += "\n"
        return return_str[:-1]

    def __eq__(self, other):
        if (self.row != other.row) or (self.column != other.column):
            return 0

        for i in range( self.row):
            for j in range( self.column):
                if self.compo[i][j] != other.compo[i][j]:
                    return 0
        return 1

    def __add__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError
            return

        sum = Matrix(self.row, self.column)

        for i in range( self.row):
            for j in range( self.column):
                sum.compo[i][j] = self.compo[i][j] + other.compo[i][j]

        return sum

    def __sub__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError
            return

        diff = Matrix(self.row, self.column)

        for i in range( self.row):
            for j in range( self.column):
                diff.compo[i][j] = self.compo[i][j] - other.compo[i][j]

        return diff

    def __mul__(self, other):
        """multiplication with a Matrix of a scalar"""
        if isinstance(other, Matrix):
            if self.column != other.row:
                raise MatrixSizeError
                return
            product = Matrix(self.row, other.column) 
            for i in range(self.row):
                for j in range(other.column):
                    for k in range(self.column):
                        product.compo[i][j] += self.compo[i][k] * other.compo[k][j]
            return product

        # product with a scalar
        elif isinstance(other, int) or isinstance(other, long) or isinstance(other, Rational):
            product = Matrix(self.row, self.column)
            for i in range(self.row):
                for j in range(self.column):
                    product.compo[i][j] = self.compo[i][j] * other
            return product

    def __div__(self, other):
        """division by a scalar"""
        if other in ring.theIntegerRing:
            return self * Rational(1, other)
        elif other in ring.theRationalField:    
            return self * (1/other)

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return self.__mul__(other) 
        
        elif isinstance(other, int) or isinstance(other, long) or isinstance(other, Rational):
            product = Matrix(self.row, self.column)
            for i in range(self.row):
                for j in range(self.column):
                    product.compo[i][j] = self.compo[i][j] * other
            return product

    def copy(self):
        """create a copy of instance"""
        copy = Matrix(self.row, self.column)
        copy.row = self.row
        copy.column = self.column
        for i in range(1, self.row+1):
            copy.set_row(i, self.get_row(i))
        return copy

    def set(self, list):
        """set(list) : substitute list for components"""
        for i in range( self.row):
            for j in range( self.column):
                self.compo[i][j] = list[self.column * i + j]

    def set_row(self, m, row_vector):
        """set_row(m, list) : substitute list for m-th row"""
        self.compo[m-1] = row_vector[:]
    
    def set_column(self, n, column_vector):
        """set_column(n, list) : substitute list for n-th column"""
        for i in range(self.row):
            self.compo[i][n-1] = column_vector[i]

    def set_compo(self, m, n, value):
        self.compo[m-1][n-1] = value

    def get_compo(self, m, n):
        return self.compo[m-1][n-1]

    def get_row(self, m):
        return self.compo[m-1]

    def get_column(self, n):
        column_n = []
        for j in range( self.row):
            column_n += [self.compo[j][n-1]]
        return column_n

    def swap_row(self, m1, m2):
        tmp = self.compo[m1-1][:]
        self.compo[m1-1] = self.compo[m2-1][:]
        self.compo[m2-1] = tmp[:]

    def swap_column(self, n1, n2):
        tmp = self.get_column(n1)
        self.set_column(n1, self.get_column(n2))
        self.set_column(n2, tmp)

    def transpose(self):
        """returns transposed matrix of self"""
        trans = Matrix(self.column, self.row)
        for i in range(trans.row):
            for j in range(trans.column):
                trans.compo[i][j] = self.compo[j][i]
        return trans

    def triangulate(self):
        """returns triangulated matrix of self"""
        triangle = self.copy()
        print triangle
        for i in range(triangle.row):
            if triangle.compo[i][i] == 0:
                for k in range(i+1, triangle.row):
                    if triangle.compo[k][i] != 0:
                        triangle.swap_row(i+1, k+1)
                        for l in range(triangle.column):     # for calculation of determinant
                            triangle.compo[i+1][l] *= -1
                        break        # break the second loop
                else:
                    continue         # the below components are all 0. Back to the first loop
            for k in range(i+1, triangle.row):
                ratio = triangle.compo[k][i] / toRational(triangle.compo[i][i])
                for l in range(i, triangle.column):
                    triangle.compo[k][l] -= toRational(triangle.compo[i][l] * ratio)
            
        return triangle

    def trace(self):
        """returns trace of self"""
        trace = 0
        for i in range(self.row):
            trace += self.compo[i][i]
        return trace

    def determinant(self):
        """returns determinant of self"""
        det = 1
        if self.row != self.column:
            raise MatrixSizeError
        triangle = self.triangulate()
        for i in range(self.row):
            det *= triangle.compo[i][i]
        return det

    def delete_row(self, i):
        deleted = Matrix(self.row-1, self.column)
        isover_i = 0
        for k in range(1, deleted.row+1):
            if k == i:
                isover_i = 1
            deleted.set_row(k, self.get_row(k+isover_i))
        return deleted

    def delete_column(self, j):
        deleted = Matrix(self.row, self.column-1)
        isover_j = 0
        for l in range(1, deleted.column+1):
            if l == j:
                isover_j = 1
            deleted.set_column(l, self.get_column(l+isover_j))
        return deleted

    def submatrix(self, i, j):
        """returns submatrix which deleted i-th row and j-th column from self"""
        return (self.delete_row(i)).delete_column(j)

    def cofactors(self):
        cofactors = Matrix(self.row, self.column)
        for i in range(cofactors.row):
            for j in range(cofactors.column):
                cofactors.compo[j][i] = (-1)**(i+j) * (self.submatrix(i+1, j+1)).determinant()
        return cofactors

    def inverse(self):
        """returns inverse matrix of self"""
        if self.determinant == 0:
            raise NoInverse
        else:
            return self.cofactors() / self.determinant()

    def characteristic_polynomial(self):        # using Cohen's Algorithm 2.2.7
        if self.row != self.column:
            raise MatrixSizeError
        i = 0
        C = unit_matrix(self.row)
        coeff = [0] * (self.row+1)
        coeff[0] = 1
        for i in range(1, self.row+1):
            C = self * C
            coeff[i] = (-1) * C.trace() / Rational(i, 1)
            C = C + coeff[i] * unit_matrix(self.row)
        return coeff

    def cohens_simplify(self):      # common processes of image() and kernel()
        """cohens_simplify is used in image() and kernel()"""
        M = self.copy()
        c = [0] * (M.row + 1)
        d = [-1] * (M.column + 1)
        for k in range(1, M.column+1):
            j = 1
            while j <= M.row:
                if M.get_compo(j,k) != 0 and c[j] == 0:
                    break
                j = j+1
            else:           # not found j such that m(j,k)!=0 and c[j]==0
                d[k] = 0
                continue
            top = (-1) / toRational(M.get_compo(j,k))
            M.set_compo(j,k,-1)
            for s in range(k+1, M.column+1):
                M.set_compo(j,s, top*M.get_compo(j,s) )
            for i in range(1, M.row+1):
                if i == j:
                    continue
                top = M.get_compo(i,k)
                M.set_compo(i,k,0)
                for s in range(k+1, M.column+1):
                    M.set_compo(i,s, M.get_compo(i,s) + top * M.get_compo(j,s))
            c[j] = k
            d[k] = j
        return [M,c,d]

    def kernel(self):       # using Cohen's Algorithm 2.3.1
        """returns a basis of self's Kernel in form of a list of vectors"""
        tmp = self.cohens_simplify()
        M = tmp[0]
        c = tmp[1]
        d = tmp[2]
        # output
        basis = []
        vector = [0] * (M.column+1)
        for k in range(1, M.column+1):
            if d[k] != 0:
                continue
            for i in range(1, M.column+1):
                if d[i] > 0:
                    vector[i] = M.get_compo(d[i],k)
                elif i == k:
                    vector[i] = 1
                else:
                    vector[i] = 0
            basis.append(vector[1:])
        return basis

    def image(self):        # using Cohen's Algorithm 2.3.2
        """returns basis of self's Image in form of a list of vectors"""
        tmp = self.cohens_simplify()
        M = tmp[0]
        c = tmp[1]
       # output
        basis = []
        for j in range(1, M.row+1):
            if c[j] != 0:
                basis.append(self.get_column(c[j]))
        return basis


        
# the belows are not methods
def unit_matrix(size):
    """returns unit matrix whose size is the given argument"""
    unit_matrix = Matrix(size, size)
    for i in range(size):
        unit_matrix.compo[i][i] = 1
    return unit_matrix

# data for debugging
a=Matrix(2,2)
a.set([1,2,3,3])

if __name__ == '__main__':
    print a.kernel()
    print a.image()
