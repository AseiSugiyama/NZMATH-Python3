from __future__ import division
from matrix import Matrix
from vector import *


class Lattice:

    def __init__(self, basis, quadraticForm):
        self.basis = basis  # in form of Matrix
        self.quadraticForm = quadraticForm  # in form of Matrix

    def createElement(self, compo):
        return LatticeElement(self, compo)

    def bilinearForm(self, v1, v2):
        return v2.transpose() * self.quadraticForm * v1

    def LLL(self):
        """LLL transforms self.basis into LLL-reduced basis
        and returns its transformation matrix."""
        k=2
        self.kmax = 1
        self.bstar = [0] *( self.basis.column+1)
        self.bstar[1] = self.basis[1].copy()
        self.B = [0] * (self.basis.column+1)
        self.B[1] = innerProduct(self.basis[1],self.basis[1])
        self.H = self.basis.getRing().unitMatrix()

        #step2
        self.mu = {}
        while 1:
            if (k > self.kmax):
                self.kmax = k
                self.bstar[k] = self.basis[k].copy()
                for j in range(1, k):
                    self.mu[(k,j)] = innerProduct(self.basis[k],self.bstar[j]) / self.B[j]
                    self.bstar[k] = self.bstar[k] - self.mu[(k,j)] * self.bstar[j]
                    self.B[k] = innerProduct(self.bstar[k],self.bstar[k])
                    if (self.B[k] == 0):
                        raise VectorsNotIndependent
            #step3
            while 1:
                self.RED(k,k-1)
                #print self.B[k],self.mu[(k,k-1)],self.B[k-1]
                #raw_input()
                if self.B[k] < (0.75-self.mu[(k,k-1)]*self.mu[(k,k-1)]) * self.B[k-1]:
                    self.SWAP(k)
                    k = max([2,k-1])
                else:
                    for l in range(k-2,0,-1):
                        self.RED(k,l)
                    k += 1
                    break
            #step4
            if k <= self.basis.column:
                pass
            else:
                #LLLreduced = Matrix(self.basis.row, self.basis.column)
                #for i in range(1, self.basis.column+1):
                    #LLLreduced.setColumn(i,self.basis[i])
                #return (LLLreduced,self.H)
                del self.kmax
                del self.bstar
                del self.B
                del self.mu

                return self.H
    
    def RED(self,k,l):
        from math import floor
        if abs(self.mu[(k,l)]) <= 0.5:
            return
        q = floor(0.5+self.mu[(k,l)])
        self.basis[k] = self.basis[k] - q*self.basis[l]
        self.H.setColumn(k, self.H[k] - q*self.H[l])
        self.mu[(k,l)] -= q
        for i in range(1, l):
            self.mu[(k,i)] -= q*self.mu[(l,i)]
        return

    def SWAP(self, k):
        #print "SWAP called %d" % k
        self.basis.swapColumn(k,k-1)
        self.H.swapColumn(k,k-1)
        if k > 2:
            for j in range(1,k-1):
                self.mu[(k,j)],self.mu[(k-1,j)] = self.mu[(k-1,j)],self.mu[(k,j)]  
        _mu = self.mu[(k,k-1)]
        _B = self.B[k] + _mu*_mu*self.B[k-1]
        self.mu[(k,k-1)] = _mu*self.B[k-1]/_B
        _b = self.bstar[k-1].copy()
        self.bstar[k-1] = self.bstar[k] + _mu*_b
        self.bstar[k] = -self.mu[(k,k-1)]*self.bstar[k] + (self.B[k]/_B)*_b
        self.B[k] = self.B[k-1]*self.B[k]/_B
        self.B[k-1] = _B
        for i in range(k+1,self.kmax+1):
            t = self.mu[(i,k)]
            self.mu[(i,k)] = self.mu[(i,k-1)] - _mu*t
            self.mu[(i,k-1)]  = t+self.mu[(k,k-1)]*self.mu[(i,k)]
        return



class LatticeElement(Matrix):

    def __init__(self, lattice, compo):
        self.lattice = lattice
        self.row = len(compo)
        self.column = 1
        self.compo = []
        for x in compo:
            self.compo.append([x])

    def getLattice(self):
        return self.lattice

if __name__ == '__main__':
    basis = Matrix(3,3,[1,2,3,6,2,5,0,-1,2])
    qForm = Matrix(3,3,[7,3,0,2,6,0,2,1,2])
    L = Lattice(basis, qForm)
    print L.LLL()
