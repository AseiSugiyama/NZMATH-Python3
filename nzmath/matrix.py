# matrix.py
# written by Aoyama <aoyama-shotaro@c.comp.metro-u.ac.jp>

# This file may be modified without notice.
# Don't edit it for the present
# and if you have advices, mail me please.
# 06/18

from rational import Rational

MATRIX_SIZE_ERROR = "MatrixSizeError"

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
            raise MATRIX_SIZE_ERROR
            return

        sum = Matrix(self.row, self.column)

        for i in range( self.row):
            for j in range( self.column):
                sum.compo[i][j] = self.compo[i][j] + other.compo[i][j]

        return sum

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.column != other.row:
                raise MATRIX_SIZE_ERROR
                return
            product = Matrix(self.row, other.column) 
            for i in range(self.row):
                for j in range(other.column):
                    for k in range(self.column):
                        product.compo[i][j] += self.compo[i][k] * other.compo[k][j]
            return product

        elif isinstance(other, int) or isinstance(other, long) or isinstance(other, Rational):
            product = Matrix(self.row, self.column)
            for i in range(self.row):
                for j in range(self.column):
                    product.compo[i][j] = self.compo[i][j] * other
            return product

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            return self.__mul__(other) 
        
        elif isinstance(other, int) or isinstance(other, long) or isinstance(other, Rational):
            product = Matrix(self.row, self.column)
            for i in range(self.row):
                for j in range(self.column):
                    product.compo[i][j] = self.compo[i][j] * other
            return product

    def create_copy(self):
        copy = Matrix(self.row, self.column)
        copy.row = self.row
        copy.column = copy.column
        for i in range(1, self.row+1):
            copy.set_row(i, self.get_row(i))
        return copy

    def set(self, list):
        for i in range( self.row):
            for j in range( self.column):
                self.compo[i][j] = list[self.column * i + j]

    def set_row(self, m, row_vector):
        self.compo[m-1] = row_vector[:]
    
    def set_column(self, n, column_vector):
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
        trans = Matrix(self.column, self.row)
        for i in range(trans.row):
            for j in range(trans.column):
                tr.compo[i][j] = self.compo[j][i]
        return trans

    def triangulate(self):
        triangle = self.create_copy()

        # int -> Rational
        # This causes errors when a component is already Rational
        for i in range(triangle.row):
            for j in range(triangle.column):
                triangle.compo[i][j] = Rational(triangle.compo[i][j], 1)

        for i in range(triangle.row):
            if triangle.compo[i][i] == Rational(0, 1):
                for k in range(i+1, triangle.row):
                    if triangle.compo[k][i] != Rational(0, 1):
                        triangle.swap_row(i+1, k+1)
                        break        # break the second loop
                else:
                    continue         # the below components are all 0. Back to the first loop
            for k in range(i+1, triangle.row):
                ratio = triangle.compo[k][i] / triangle.compo[i][i]
                for l in range(i, triangle.column):
                    triangle.compo[k][l] -= triangle.compo[i][l] * ratio
            
        return triangle

    def trace(self):
        trace = 0
        for i in range(self.row):
            trace += self.compo[i][i]
        return trace

    def determinant(self):
        det = 1
        if self.row != self.column:
            raise MATRIX_SIZE_ERROR
        triangle = self.triangulate()
        for i in range(self.row):
            det *= triangle.compo[i][i]
        return det
            
        
# data for debugging

a = Matrix(2,2)
a.set([1,2,3,4])
b = Matrix(2,2)
b.set([0,-1,1,-2])
c = Matrix(3,3)
c.set([0,-2,9]+[5,0,1]+[0,2,3])

def matrix_test():

    print "a=\n", a
    print "b=\n", b
    print "c=\n", c
    print "a.triangulate"
    print a.triangulate()
    print "det(a) = ", a.determinant()
    print "b.triangulate()"
    print b.triangulate()
    print "Det(b)" , b.determinant()
    print "triangulate(c)"
    print c.triangulate()
    
if __name__ == "__main__":
    print "Matrix test ==============================\n"
    matrix_test()

