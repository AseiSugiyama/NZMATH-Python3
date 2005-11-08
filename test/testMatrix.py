import unittest
from nzmath.matrix import *

a = Matrix(2,2,[1,2,3,4])

b = Matrix(2,2,[0,-1,1,-2])

c = Matrix(3,3,[1,2,3]+[0,5,-2]+[7,1,9])

d = Matrix(6,6,[4,2,5,0,2,1]+[5,1,2,5,1,1]+[90,7,54,8,4,6]+[7,5,0,8,2,5]+[8,2,6,5,-4,2]+[4,1,5,6,3,1])

e = Matrix(1,2,[3,2])

f = Matrix(4,4,[1,1,1,1]+[0,0,0,0]+[3,3,3,3]+[-1,-1,-1,-1])

g = Matrix(3,3,[7,2,8,0,5,-2,0,1,9])

h1 = [12,1,1]

#h2 = [1,1,0] Error Matrix

h3 = [1,1,1]

class MatrixTest(unittest.TestCase):
    def testAdd(self):
        sum = Matrix(2,2)
        sum.set([1,1,4,2])
        assert a + b == sum

    def testSub(self):
        sub = Matrix(2,2)
        sub.set([1,3,2,6])
        assert a - b == sub

    def testMul(self):
        mul = Matrix(1,2)
        mul.set([2,-7])
        assert e * b == mul

    def testScalarMul(self):
        mul = Matrix(2,2)
        mul.set([3,6,9,12])
        assert 3 * a == mul

    def testDiv(self):
        div = Matrix(1,2)
        div.set([1,rational.Rational(2,3)])
        assert e / 3 == div

    def testPow(self):
        square = Matrix(2,2, [7,10,15,22])
        assert square == a ** 2

    def testCharacteristicPolynomial(self):
        assert a.characteristicPolynomial()

    def testTranspose(self):
        trans = Matrix(2,1)
        trans.set([3,2])
        assert e.transpose() == trans

    def testTriangulate(self):
        triangle = Matrix(3,3, [1,2,3]+[0,5,-2]+[0,0,rational.Rational(-86,5)])
        assert c.triangulate() == triangle

    def testTrace(self):
        assert c.trace() == 15

    def testDeterminant(self):
        assert a.determinant() == -2 

    def testInverse(self):
        cinverse = Matrix(3,3,[rational.Rational(-47,86),rational.Rational(15,86), rational.Rational(19,86),
                               rational.Rational(7,43),rational.Rational(6,43),rational.Rational(-1,43),
                               rational.Rational(35,86),rational.Rational(-13,86),rational.Rational(-5,86)])
        noinverse = Matrix(3,3,[1,2,3,
                                4,5,6,
                                5,7,9])
        assert cinverse == c.inverse()
        self.assertRaises(VectorsNotIndependent, noinverse.inverse)

    def testInverseImage(self):
        M = Matrix(4,4,[2,-1,0,0]+[-1,2,-1,0]+[0,-1,2,-1]+[0,0,-1,2])
        V = Matrix(4,4,[1,2,3,4]+[2,3,4,5]+[3,4,5,6]+[4,5,6,7])
        noinverse = Matrix(3,3,[1,2,3,
                                4,5,6,
                                5,7,9])
        assert M * M.inverseImage(V) == V
        self.assertRaises(VectorsNotIndependent, noinverse.inverseImage, unitMatrix(3))

    def testIsUpperTriangularMatrix(self):
        UT = Matrix(4,4,[1,2,3,4]
                       +[0,5,6,7]
                       +[0,0,8,9]
                       +[0,0,0,1])
        notUT = Matrix(4,4,[1,2,3,4]
                          +[0,5,6,7]
                          +[0,0,8,9]
                          +[0,0,1,1])
        assert UT.isUpperTriangularMatrix()
        assert not notUT.isUpperTriangularMatrix()

    def testLUDecomposition(self):
        L, U = d.LUDecomposition()
        assert L * U == d
        assert L.isLowerTriangularMatrix()
        assert U.isUpperTriangularMatrix()

    def testsmith(self):
        s1 = IntegerMatrix(3,3,[1,3,2,4,6,5,6,8,9])
        s2 = IntegerMatrix(3,3,[1,2,4,0,3,5,0,0,0])
        s3 = IntegerMatrix(3,3,[1,0,0,9,1,0,5,6,1])
        assert h1 == s1.smith()
        #assert h2 == s2.smith()
        assert h3 == s3.smith()

    def testGetitem(self):
        self.assertEqual(2, a[1,2])
        self.assertRaises(IndexError, a.__getitem__, "wrong")

    def testEqual(self):
        self.assert_(a == a)
        self.assert_(isinstance(a == a, bool))


class SubspaceTest(unittest.TestCase):
    def testSupplementBasis(self):
        b = Subspace(3, 2, [1,2,3,4,5,7])
        assert b.supplementBasis() == Matrix(3,3,[1,2,0,3,4,0,5,7,1])

def suite():
    suite = unittest.makeSuite(MatrixTest, "test")
    suite.addTest(unittest.makeSuite(SubspaceTest, "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

