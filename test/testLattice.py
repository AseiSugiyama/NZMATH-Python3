import unittest
import lattice, matrix

class LatticeTest (unittest.TestCase):
    def testLLL(self):
        basis = matrix.Matrix(3,3,[1,2,3,6,2,5,0,-1,2])
        qForm = matrix.Matrix(3,3,[7,3,0,2,6,0,2,1,2])
        L = lattice.Lattice(basis, qForm)
        assert L.LLL()

def suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LatticeTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
