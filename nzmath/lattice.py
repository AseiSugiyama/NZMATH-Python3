from matrix import Matrix
import ring

class Lattice(Matrix):
    
#    def __init__(self, row, column):
#        if ( row in ring.theIntegerRing and row > 0
#            and column in ring.theIntegerRing and column > 0):
#            self.row = row
#            self.column = column
#            self.compo = []
#            for i in range(self.row):
#                self.compo.append([0] * self.column)
#        else:
#            raise ValueError, "Arguments are not integer > 0."
#
#    def __getitem__(self, *arg):
#        if isinstance(arg[0], tuple):
#            return self.compo[ arg[0][0]-1 ][ arg[0][1]-1 ]
#        elif isinstance(arg[0], int) or isinstance(arg[0], long): 
#            vector = Matrix(self.row, 1)
#            for k in range(self.row):
#                vector.compo[k][0] = self.compo[k][arg[0]-1]
#            return vector
#        else:
#            raise IndexError
#
#    def __setitem__(self, j, vector):
#        if isinstance(vector, list):
#            for k in range(self.row):
#                self.compo[k][j-1] = vector[k]
#        elif isinstance(vector, Matrix):
#            for k in range(self.row):
#                self.compo[k][j-1] = vector.compo[k][0]
#        else:
#            raise TypeError, "neither a list nor a Matrix."

    def __delitem__(self, j):
        self.column -= 1
        for k in range(self.row):
            del self.compo[k][j-1]
        
#    def __repr__(self):
#        return_str = ""
#        width = [1] * self.column      # width of each column
#        for j in range(self.column):
#            for i in range(self.row):
#                if len(str(self.compo[i][j])) > width[j]:
#                    width[j] = len(str(self.compo[i][j]))
#        for i in range(self.row):
#            for j in range(self.column):
#                return_str += "%*s " % (width[j], str(self.compo[i][j]))
#            return_str += "\n"
#        return return_str[:-1]
#
#    __str__ = __repr__ 


# utility methods-----------------------------------------------------
#    def set(self, list):
#        for i in range(self.row):
#            for j in range(self.column): 
#                self.compo[i][j] = list[self.column * i + j]

    def append(self, vector):
        if isinstance(vector, list):
            for k in range(self.row):
                self.compo[k].append(vector[k])
            self.column += 1
        elif isinstance(vector, Matrix):
            for j in range(vector.column):
                for k in range(self.row):
                    self.compo[k].append(vector.compo[k][j])
            self.column += 1
        else:
            raise TypeError, "Argument must be a list or a Matrix."

    def copy(self):
        copy = Lattice(self.row, self.column)
        copy.row = self.row
        copy.column = self.column
        for i in range(1, self.column+1):
            copy[i] = self[i]
        return copy

# Mathematical functions ---------------------------------------------

    def hermite_normal_form(self):  # using Cohen's Algorithm 2.4.4
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
                    A.swap_column(k,j0)
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

# data for debugging -------------------------------------------------

if __name__ == '__main__':
    latticeA = Lattice(3,3)
    latticeA.set([1,2,5,4,0,6,7,8,9])
    print "latticeA.set([1,2,5,4,0,6,7,8,9])"
    print latticeA

    v=Matrix(3,1)
    v.set([-1,2,0])
    print "v.set([-1,2,0])"
    print v

    latticeA.append(v)
    print "latticeA.append(v)"
    print latticeA

    del latticeA[1]
    print "del latticeA[1]"
    print latticeA

    u = Matrix(3,1)
    u.set([99,7,66])
    print "u.set([99,7,66]"

    latticeA[2] = u
    print "latticeA[2] = u"
    print latticeA

    latticeB = latticeA.copy()
    print "latticeB = latticeA.copy()"
    print latticeB

    print "latticeB.hermite_normal_form()"
    print latticeB.hermite_normal_form()
