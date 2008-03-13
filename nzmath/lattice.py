from __future__ import division
from math import floor
from nzmath.matrix import Matrix
from nzmath.matrix import VectorsNotIndependent
from nzmath.vector import *


class Lattice:

    def __init__(self, basis, quadraticForm):
        self.basis = basis.copy()  # in form of Matrix
        self.quadraticForm = quadraticForm.copy()  # in form of Matrix

    def createElement(self, compo):
        return LatticeElement(self, compo)

    def bilinearForm(self, v1, v2):
        return v2.transpose() * self.quadraticForm * v1

def LLL(_basis, quadraticForm=None ,delta = 0.75):
    """
    LLL returns LLL-reduced basis
    """
    basis = _basis.copy()
    k=2 
    kmax = 1
    mu = []
    for i in range(basis.column + 1):
        mu.append( [0] * i)

    def _innerProduct(v1, v2):
        if quadraticForm:
            val =  ((v1 * quadraticForm) * v2.toMatrix().transpose())
            return val.compo[0]
        else:
            return innerProduct(v1, v2)
    
    bstar = [0] * ( basis.column + 1)
    bstar[1] = basis[1].copy()
    B = [0] * (basis.column + 1)
    B[1] = _innerProduct(basis[1], basis[1])
    H = basis.getRing().unitMatrix()
    
    def _RED(k, l):
        if 2 * abs(mu[k][l]) <= 1:
            return
        q = int( floor(0.5 + mu[k][l]) )
        basis[k] -= q * basis[l]
        H[k] -= q * H[l] 
        mu[k][l] -= q
        for i in range(1, l):
            mu[k][i] -= q * mu[l][i]
        return

    def _SWAP(k):
        basis.swapColumn(k, k-1)
        H.swapColumn(k, k-1)
        if k > 2:
            for j in range(1, k-1):
                mu[k][j], mu[k-1][j] = mu[k-1][j], mu[k][j]
        _mu = mu[k][k-1]
        _B = B[k] + _mu * _mu * B[k-1]
        
        if abs(_B) < (2**(-30)):
            B[k], B[k-1] = B[k-1], B[k]
            bstar[k], bstar[k-1] = bstar[k-1], bstar[k]
            for i in range(k+1, kmax+1):
                mu[i][k], mu[i][k-1] = mu[i][k-1], mu[i][k]
        elif abs(B[k]) < (2**(-30)) and _mu != 0:
            B[k-1] = _B
            bstar[k-1] = _mu * bstar[k-1]
            mu[k][k-1] = 1 / _mu
            for i in range(k+1, kmax+1):
                mu[i][k-1] = mu[i][k-1] / _mu
        elif B[k] != 0:
            t = B[k-1] / _B
            mu[k][k-1] = _mu * t
            _b = bstar[k-1].copy()
            bstar[k-1] = bstar[k] + _mu * _b
            bstar[k] = -mu[k][k-1]*bstar[k] + (B[k]/_B) * _b
            B[k] = B[k] * t
            B[k-1] = _B
            for i in range(k+1, kmax+1):
                t = mu[i][k]
                mu[i][k] = mu[i][k-1] - _mu * t
                mu[i][k-1]  = t + mu[k][k-1] * mu[i][k]
        return
    
    #step2
    while k <= basis.column :
        if (k > kmax):
            kmax = k
            bstar[k] = basis[k].copy()
            for j in range(1, k):
                if abs(B[j]) < (2**(-30)):
                    mu[k][j] = 0
                else:
                    mu[k][j] = _innerProduct(basis[k], bstar[j]) / B[j]
                bstar[k] -= mu[k][j] * bstar[j]
            B[k] = _innerProduct(bstar[k], bstar[k])
        #step3
        while 1:
            _RED(k,k-1)
            if B[k] < (delta - mu[k][k-1] ** 2) * B[k-1]:
                _SWAP(k)
                k = max([2,k-1])
            else:
                for l in range(k-2, 0, -1):
                    _RED(k, l)
                k += 1
                break
    return basis, H

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

