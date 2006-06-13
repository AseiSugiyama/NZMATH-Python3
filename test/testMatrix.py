import unittest
from nzmath.matrix import *

a = createMatrix(2,2,[1,2,3,4])

b = createMatrix(2,2,[0,-1,1,-2])

c = createMatrix(3,3,[1,2,3]+[0,5,-2]+[7,1,9])

d = createMatrix(6,6,[4,2,5,0,2,1]+[5,1,2,5,1,1]+[90,7,54,8,4,6]+[7,5,0,8,2,5]+[8,2,6,5,-4,2]+[4,1,5,6,3,1])

e = createMatrix(1,2,[3,2])

f = createMatrix(4,4,[1,1,1,1]+[0,0,0,0]+[3,3,3,3]+[-1,-1,-1,-1])

g = createMatrix(3,3,[7,2,8,0,5,-2,0,1,9])

h1 = [12,1,1]

h2 = [1,1,0]

h3 = [1,1,1]

i = (IntegerMatrix(3,3,[2,1,3,-1,0,-1,1,0,0]),IntegerMatrix(3,3,[11,3,0,3,1,1,-10,-3,-1]),IntegerMatrix(3,3,[12,0,0,0,1,0,0,0,1]))

class MatrixTest(unittest.TestCase):
    def testAdd(self):
        sum = createMatrix(2,2)
        sum.set([1,1,4,2])
        assert a + b == sum

    def testSub(self):
        sub = createMatrix(2,2)
        sub.set([1,3,2,6])
        assert a - b == sub

    def testMul(self):
        mul = createMatrix(1,2)
        mul.set([2,-7])
        assert e * b == mul

    def testScalarMul(self):
        mul = createMatrix(2,2)
        mul.set([3,6,9,12])
        assert 3 * a == mul

    def testDiv(self):
        div = createMatrix(1,2)
        div.set([1,rational.Rational(2,3)])
        assert e / 3 == div

    def testTranspose(self):
        trans = createMatrix(2,1)
        trans.set([3,2])
        assert e.transpose() == trans

    def testTriangulate(self):
        triangle = createMatrix(3,3, [1,2,3]+[0,5,-2]+[0,0,rational.Rational(-86,5)])
        assert c.triangulate() == triangle

    def testInverseImage(self):
        M = createMatrix(4,4,[2,-1,0,0]+[-1,2,-1,0]+[0,-1,2,-1]+[0,0,-1,2])
        V = createMatrix(4,4,[1,2,3,4]+[2,3,4,5]+[3,4,5,6]+[4,5,6,7])
        noinverse = createMatrix(3,3,[1,2,3,
                                4,5,6,
                                5,7,9])
        assert M * M.inverseImage(V) == V
        self.assertRaises(VectorsNotIndependent, noinverse.inverseImage, unitMatrix(3))

    def testIsUpperTriangularMatrix(self):
        UT = createMatrix(4,4,[1,2,3,4]
                       +[0,5,6,7]
                       +[0,0,8,9]
                       +[0,0,0,1])
        notUT = createMatrix(4,4,[1,2,3,4]
                          +[0,5,6,7]
                          +[0,0,8,9]
                          +[0,0,1,1])
        assert UT.isUpperTriangularMatrix()
        assert not notUT.isUpperTriangularMatrix()

    def testGetitem(self):
        self.assertEqual(2, a[1,2])
        self.assertRaises(IndexError, a.__getitem__, "wrong")

    def testEqual(self):
        self.assert_(a == a)
        self.assert_(isinstance(a == a, bool))

    def testDeleteColumn(self):
        m_2_3 = createMatrix(2, 3, [1, 2, 3] + [4, 5, 6])
        m_delete_1 = createMatrix(2, 2, [2, 3, 5, 6])
        self.assertEqual(m_delete_1, m_2_3.deleteColumn(1))
        m_delete_2 = createMatrix(2, 2, [1, 3, 4, 6])
        self.assertEqual(m_delete_2, m_2_3.deleteColumn(2))
        m_delete_3 = createMatrix(2, 2, [1, 2, 4, 5])
        self.assertEqual(m_delete_3, m_2_3.deleteColumn(3))


class SquareMatrixTest(unittest.TestCase):
    def testTrace(self):
        assert c.trace() == 15

    def testDeterminant(self):
        assert a.determinant() == -2 

    def testInverse(self):
        cinverse = createMatrix(3,3,[rational.Rational(-47,86),rational.Rational(15,86), rational.Rational(19,86),
                               rational.Rational(7,43),rational.Rational(6,43),rational.Rational(-1,43),
                               rational.Rational(35,86),rational.Rational(-13,86),rational.Rational(-5,86)])
        noinverse = createMatrix(3,3,[1,2,3,
                                4,5,6,
                                5,7,9])
        assert cinverse == c.inverse()
        self.assertRaises(VectorsNotIndependent, noinverse.inverse)

    def testPow(self):
        square = createMatrix(2,2, [7,10,15,22])
        assert square == a ** 2

    def testCharacteristicPolynomial(self):
        assert a.characteristicPolynomial()

    def testLUDecomposition(self):
        L, U = d.LUDecomposition()
        assert L * U == d
        assert L.isLowerTriangularMatrix()
        assert U.isUpperTriangularMatrix()

    def testHermiteNormalForm(self):
        lessrank = IntegerMatrix(2, 3, [1, 0, 0, 0, 1, 0])
        h = lessrank.hermiteNormalForm()
        self.assertEqual(h.row, lessrank.row)
        self.assertEqual(h.column, lessrank.column)
        import nzmath.vector as vector
        zerovec = vector.Vector([0, 0])
        self.assertEqual(zerovec, h.getColumn(1))

        square = IntegerMatrix(3, 3, [1, 0, 0, 0, 1, 1, 0, 1, 1])
        h = square.hermiteNormalForm()
        self.assertEqual(h.row, square.row)
        self.assertEqual(h.column, square.column)
        hermite = IntegerMatrix(3, 3, [0, 1, 0, 0, 0, 1, 0, 0, 0])
        for i in (1, 2, 3):
            self.assertEqual(hermite.getColumn(i), h.getColumn(i))


class IntegerSquareTest(unittest.TestCase):
    def testSmithNormalForm(self):
        s1 = IntegerSquareMatrix(3,3,[1,3,2,4,6,5,6,8,9])
        s2 = IntegerSquareMatrix(3,3,[1,2,4,0,3,5,0,0,0])
        s3 = IntegerSquareMatrix(3,3,[1,0,0,9,1,0,5,6,1])
        assert h1 == s1.smithNormalForm()
        self.assertRaises(ValueError, s2.smithNormalForm)
        assert h3 == s3.smithNormalForm()

    def testExtSmithNormalForm(self):
        s = IntegerSquareMatrix(3,3,[1,3,2,4,6,5,6,8,9])
        assert i == s.extsmithNormalForm()


class SubspaceTest(unittest.TestCase):
    def testSupplementBasis(self):
        b = Subspace(3, 2, [1,2,3,4,5,7])
        assert b.supplementBasis() == Matrix(3,3,[1,2,0,3,4,0,5,7,1])


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

