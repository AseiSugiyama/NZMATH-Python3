# written by Aoyama
# This file may be modified without notice.
# Don't edit this for the present, please.
# 06/18

class Matrix:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.compo = {}
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                self.compo[(i,j)] = 0

    def __repr__(self):
        rtnstr = ""
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                rtnstr += `self.compo[(i,j)]` + " "
            rtnstr += "\n"
        return rtnstr

    def display(self):
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                print self.compo[(i,j)],
            print

    def __add__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise "Matrix size error"
            return

        sum = Matrix(self.row, self.column)

        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                sum.compo[(i,j)] = self.compo[(i,j)] + other.compo[(i,j)]

        return sum

    def __mul__(self, other):
        if self.column != other.row:
            raise "Matrix size error"
            return

        product = Matrix(self.row, other.column)

        for i in range(1, self.row+1):
            for j in range(1, other.column+1):
                for k in range(1, self.column+1):
                    product.compo[(i,j)] += self.compo[(i,k)] * other.compo[(k,j)]

        return product

    def set(self, list):
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                self.compo[(i,j)] = list[self.column * (i-1) + (j-1)]
    
    def getrow(self, m):
       row_m = []
       for i in range(1, self.row+1):
           row_m += [self.compo[(m, i)]]
       return row_m

    def getcolumn(self, n):
        column_n = []
        for j in range(1, self.column+1):
            column_n += [self.compo[(j, n)]
        return column_n

