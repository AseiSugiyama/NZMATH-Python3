# matrix.py
# written by Aoyama (aoyama-shotaro@c.comp.metro-u.ac.jp)

# This file may be modified without notice.
# Don't edit it for the present
# and if you have an advice, mail me please.
# 06/18

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
        return return_str

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
            raise "Matrix size error"
            return

        sum = Matrix(self.row, self.column)

        for i in range( self.row):
            for j in range( self.column):
                sum.compo[i][j] = self.compo[i][j] + other.compo[i][j]

        return sum

    def __mul__(self, other):
        if self.column != other.row:
            raise "Matrix size error"
            return

        product = Matrix(self.row, other.column)

        for i in range( self.row):
            for j in range( other.column):
                for k in range( self.column):
                    product.compo[i][j] += self.compo[i][k] * other.compo[k][j]

        return product

    def set(self, list):
        for i in range( self.row):
            for j in range( self.column):
                self.compo[i][j] = list[self.column * i + j]

    def set_row(self, m, row_vector):
        self.compo[m-1] = row_vector[:]
    
    def set_column(self, n, column_vector):
        for i in range(self.row):
            self.compo[i][n-1] = column_vector[i]

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
        self.tmp = self.compo[m1-1][:]
        self.compo[m1-1] = self.compo[m2-1][:]
        self.compo[m2-1] = self.tmp[:]

    def swap_column(self, n1, n2):
        self.tmp = self.get_column(n1)
        self.set_column(n1, self.get_column(n2))
        self.set_column(n2, self.tmp)

def matrix_test():
    a = Matrix(2,2)
    a.set([1,2,3,4])
    b = Matrix(2,2)
    b.set([0,-1,1,-2])
    print "a=\n", a
    print "b=\n", b
    print "a+b=\n",  a + b
    print "a*b=\n",  a * b
    print "1st row of a=", a.get_row(1)
    print "2nd column of b=", b.get_column(2)
    print "a.set_row(2,[99,88])"
    a.set_row(2,[99,88])
    print a
    print "b.set_column(1,[-44,-11])"
    b.set_column(1,[-44,-11])
    print b
    
    print "a.swap_row(1,2)"
    a.swap_row(1,2)
    print a

    print "b.swap_column(1,2)"
    b.swap_column(1,2)
    print b

if __name__ == "__main__":
    print "test\n"
    matrix_test()
