# matrix.py

from rational import * 
import ring

MatrixSizeError = "MatrixSizeError"
NoInverse = "NoInverse"
NoSolution = "NoSolution"
VectorsNotIndependent = "VectorsNotIndependent"

class Matrix:

    def __init__(self, row, column):
        if row <= 0 or column <= 0:
            raise ValueError
        self.row = row
        self.column = column
        self.compo = []
        for i in range(self.row):
            self.compo.append([0] * self.column)

    def __repr__(self):
        return_str = ""
        maxlen = [1] * self.column      # width of each column
        for j in range(self.column):
            for i in range(self.row):
                if len(`self.compo[i][j]`) > maxlen[j]:
                    maxlen[j] = len(`self.compo[i][j]`)
        for i in range(self.row):
            for j in range(self.column):
                return_str += "%*s " % (maxlen[j], `self.compo[i][j]`)
            return_str += "\n"
        return return_str[:-1]

    def __eq__(self, other):
        if isinstance(other, int):
            if other == 0:          # Is self zero vector/matrix ?
                for i in range(self.row):
                    for j in range(self.column):
                        if self.compo[i][j] != 0:
                            return 0
                return 1 

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

    def set_row(self, m, arg):
        """set_row(m, new_row) : new_row can be a list or a row vector(Matrix)"""
        if isinstance(arg, list):
            self.compo[m-1] = arg[:]
        elif isinstance(arg, Matrix):
            for i in range(self.column):
                self.compo[m-1][i] = arg.compo[0][i]
        else:
            raise NotImplementedError
    
    def set_column(self, n, arg):
        """set_column(n, new_column) : new_column can be a list or a column vector(Matrix)"""
        if isinstance(arg, list):
            for i in range(self.row):
                self.compo[i][n-1] = arg[i]
        elif isinstance(arg, Matrix):
            for j in range(self.row):
                self.compo[j][n-1] = arg.compo[j][0]
        else:
            raise TypeError


    def set_compo(self, m, n, value):
        """set_compo(m, n, value) : set value for (m,n)-component"""
        self.compo[m-1][n-1] = value

    def get_compo(self, m, n):
        """get_compo(m, n) : Return (m,n)-component"""
        return self.compo[m-1][n-1]

    def get_row(self, m):
        """get_row(m) : Return m-th row in form of list"""
        return self.compo[m-1]

    def get_column(self, n):
        """get_column(n) : Return n-th column in form of list"""
        column_n = []
        for j in range( self.row):
            column_n += [self.compo[j][n-1]]
        return column_n

    def get_row_vector(self, m):
        """get_row_vector(m) : Return m-th row in form of a Matrix"""
        row_m = Matrix(1, self.column)
        for i in range(self.column):
            row_m.compo[0][i] = self.compo[m-1][i]
        return row_m

    def get_column_vector(self, n):
        """get_column_vector(n) : Return n-th column in form of a Matrix"""
        column_n = Matrix(self.row, 1)
        for j in range(self.row):
            column_n.compo[j][0] = self.compo[j][n-1]
        return column_n

    def __getitem__(self, n):
        """M[i] <==> M.get_column_vector(i)"""
        return self.get_column_vector(n)

    def __setitem__(self, i, vector):
        """M[i] = V <==> M.set_column(i, V)"""
        self.set_column(i, vector)

    def swap_row(self, m1, m2):
        tmp = self.compo[m1-1][:]
        self.compo[m1-1] = self.compo[m2-1][:]
        self.compo[m2-1] = tmp[:]

    def swap_column(self, n1, n2):
        tmp = self.get_column(n1)
        self.set_column(n1, self.get_column(n2))
        self.set_column(n2, tmp)

    def transpose(self):
        """Return transposed matrix of self"""
        trans = Matrix(self.column, self.row)
        for i in range(trans.row):
            for j in range(trans.column):
                trans.compo[i][j] = self.compo[j][i]
        return trans

    def triangulate(self):
        """Return triangulated matrix of self."""
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
        """Return trace of self."""
        trace = 0
        for i in range(self.row):
            trace += self.compo[i][i]
        return trace

    def determinant(self):
        """Return determinant of self."""
        det = 1
        if self.row != self.column:
            raise MatrixSizeError
        triangle = self.triangulate()
        for i in range(self.row):
            det *= triangle.compo[i][i]
        return det

    def insert_row(self, i, arg):
        """insert_row(i, new_row) : new_row can be a list or a Matrix""" 
        if isinstance(arg, list):
            new_row = arg
        elif isinstance(arg, Matrix):
            new_row = arg.compo[0][:]
        self.row += 1
        self.compo.insert(i-1, new_row)

    def insert_column(self, j, arg):
        """insert_column(j, arg) : new_column can be a list or a Matrix"""
        if isinstance(arg, list):
            new_column = arg
        elif isinstance(arg, Matrix):
            new_column = arg.get_column(1)
        self.column += 1
        for k in range(self.row):
            self.compo[k].insert(j-1, new_column[k])

    def delete_row(self, i):
        self.row -= 1
        del self.compo[i-1]

    def delete_column(self, j):
        self.column -= 1
        for k in range(self.row):
            del self.compo[k][j-1]

    def submatrix(self, i, j):
        """Return submatrix which deleted i-th row and j-th column from self."""
        sub = self.copy()
        sub.delete_row(i)
        sub.delete_column(j)
        return sub

    def cofactors(self):
        cofactors = Matrix(self.row, self.column)
        for i in range(cofactors.row):
            for j in range(cofactors.column):
                cofactors.compo[j][i] = (-1)**(i+j) * (self.submatrix(i+1, j+1)).determinant()
        return cofactors

    def inverse(self):
        """Return inverse matrix of self."""
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

    def cohens_simplify(self):      # common process of image() and kernel()
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
        """Return a Matrix which column vectors are one basis of self's Kernel."""
        tmp = self.cohens_simplify()
        M = tmp[0]
        c = tmp[1]
        d = tmp[2]
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
        output = Matrix(self.column, len(basis))
        for j in range(1, output.column + 1):
            output.set_column(j, basis[j-1])
        return output

    def image(self):        # using Cohen's Algorithm 2.3.2
        """Return a Matrix which column vectors are one basis of self's Image."""
        tmp = self.cohens_simplify()
        M = tmp[0]
        c = tmp[1]
        basis = []
        for j in range(1, M.row+1):
            if c[j] != 0:
                basis.append(self.get_column(c[j]))
        output = Matrix(self.row, len(basis))
        for j in range(1, output.column + 1):
            output.set_column(j, basis[j-1])
        return output

    def rank(self):
        return len(self.image())

    def inverse_image(self, B):      # using Cohen's Algorithm 2.3.4
        """inverse_image(B) : B can be a list or a column vector(Matrix)
        Return a vector belongs to the inverse image of B."""
        M1 = self.copy()
        M1.insert_column(self.column+1, B)
        V = M1.kernel()
        r = V.column
        for j in range(1, r+1):
            if V.get_compo(self.column+1, j) != 0:
                break
        else:
            raise NoSolution
        d = (-1)/toRational(V.get_compo(self.column+1,j))
        x = []
        for i in range(1, self.column+1):
            x.append(d*V.get_compo(i,j))
        inverse_image = Matrix(self.column, 1)
        inverse_image.set_column(1, x)
        return inverse_image
        
    
#    def solution(self, vector):
#        if self.row != len(vector):
#            raise MatrixSizeError
#        M = self.insert_column(self.column+1, vector)
#        M = M.cohens_simplify()[0]
#        print M
#        x = [0]*self.column
#        rows = range(self.row)
#        rows.reverse()
#        for i in rows:
#            for j in range(self.column):
#                if M.compo[i][j] != 0:
#                    x[j] = (-1) * M.compo[i][M.column-1]
#                    for k in range(j+1, M.column-1):
#                        x[j] -= M.compo[i][k] * x[k]
#        return x
# 

    # does not work well ???
    def supplement_basis(self):     # using Cohen's Algorithm 2.3.6
        """Return a basis of full space, which including self's column vectors."""
        if self.row < self.column:
            raise MatrixSizeError

        copy = self.copy()
        B = unit_matrix(copy.row)

        for s in range(1,copy.column+1):
            for t in range(s,copy.row+1):
                if copy.get_compo(t,s) != 0:
                    break
            else:
                raise VectorsNotIndependent
            d = 1 / toRational(copy.get_compo(t,s))
            if t != s:
                B.set_column(t, B.get_column(s))
            B.set_column(s, copy.get_column(s))
            print B
            pause()
            for j in range(s+1, copy.column+1):
                tmp = copy.get_compo(s,j)
                copy.set_compo(s,j, copy.get_compo(t,j))
                copy.set_compo(t,j,tmp)
                copy.set_compo(s,j, d * copy.get_compo(s,j))
                for i in range(1,copy.row+1):
                    if i != s and i != t:
                        copy.set_compo(i,j,copy.get_compo(i,j) - copy.get_compo(i,s)*copy.get_compo(s,j))
        return B

    # does not work well ???
    def hessenberg_form(self):      # using Cohen's Algorithm 2.2.9
        if self.row != self.column:
            raise MatrixSizeError
        H = self.copy()
        for m in range(2, H.row):
            for i in range(m+1, self.row+1):
                if H.get_compo(i,m-1) != 0:
                    break
            else:
                continue
            if H.get_compo(m,m-1) != 0:
                i = m
            t = H.get_compo(i,m-1)
            if i > m:
                for j in range(m-1, H.row+1):
                    tmp = H.get_compo(i,j)
                    H.set_compo(i,j,H.get_compo(m,j))
                    H.set_compo(m,j,tmp)
                    tmpvector = H.get_column(i)
                    H.set_column(i,H.get_column(m))
                    H.set_column(m,tmpvector)
            for i in range(m+1,H.row+1):
                if H.get_compo(i,m-1) != 0:
                    u = H.get_compo(i,m-1) / toRational(t)
                    for j in range(m,H.row+1):
                        H.set_compo(i,j,H.get_compo(i,j)-u*H.get_compo(m,j))
                    H.set_column( m, (H.get_column_vector(m) + u*H.get_column_vector(i)) )
        return H

# the belows are not class methods
def unit_matrix(size):
    """unit_matrix(n) : Return unit matrix whose size is n * n"""
    unit_matrix = Matrix(size, size)
    for i in range(size):
        unit_matrix.compo[i][i] = 1
    return unit_matrix

def intersection_of_subspaces(M, M_):    # using Cohen's Algorithm 2.3.9
    if M.row != M_.row:
        raise MatrixSizeError
    M1 = Matrix(M.row, M.column + M_.column)
    for j in range(1, M.column+1):
        M1.set_column(j, M.get_column(j))
    for j in range(1, M_.column+1):
        M1.set_column(M.column + j, M_.get_column(j))
    N = M1.kernel()
    N1 = Matrix(M.column , N.column)    # N.column is dimension of kernel(M1)
    for j in range(1, M.column + 1):
        N1.set_row(j, N.get_row(j))
    M2 = M * N1
    return M2.image()
    
# data for debugging
a=Matrix(5,3)
a.set([0,1,3]+[0,2,2]+[0,0,5]+[0,1,1]+[2,0,0])

b = Matrix(2,2)
b.set([1,2,5,10])

c = Matrix(3,3)
c.set([0,1,1,-1,1,0,2,2,3])

d = Matrix(4,2)
d.set([0,1,0,1]+[2,0,0,3])

e = Matrix(3,2)
e.set([1,0]+[2,1]+[1,1])

f = Matrix(3,2)
f.set([0,1]+[-1,4]+[2,6])

def pause():
    print "--- hit enter key ---"
    raw_input()

if __name__ == '__main__':
    print "b.kernel"
    print b.kernel()
    print "---"
    print b.inverse_image([3,15])
