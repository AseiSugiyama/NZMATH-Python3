from matrix import Matrix

class Lattice:

    def __init__(self, basis, quadraticForm):
        self.basis = basis  # in form of Matrix
        self.quadraticForm = quadraticForm  # in form of Matrix

    def createElement(self, compo):
        return LatticeElement(self, compo)

    def q(self, v):
        return self.b(v, v)

    def b(self, v1, v2):
        return v2.transpose() * self.quadraticForm * v1

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
    basis = Matrix(2,2,[1,0,0,1])
    q = Matrix(2,2,[3,0,0,-1])
    L = Lattice(basis, q)
    v = L.createElement([5,6])
    u = L.createElement([-2,0])
    print v
    print L.b(v,u)
    print L.q(u)
