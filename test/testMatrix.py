from __future__ import division
import unittest
from nzmath.matrix import *
import nzmath.vector as vector

# sub test
from nzmath.test.testMatrixFiniteField import *


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
    def testGetitem(self):
        self.assertEqual(2, a[1,2])
        self.assertRaises(IndexError, a.__getitem__, "wrong")

    def testEqual(self):
        self.assert_(a == a)
        self.assert_(isinstance(a == a, bool))

    def testAdd(self):
        sum = createMatrix(2,2,[1,1,4,2])
        self.assertEqual(sum, a + b)

    def testSub(self):
        sub = createMatrix(2,2,[1,3,2,6])
        self.assertEqual(sub, a - b)

    def testMul(self):
        mul = createMatrix(1,2,[2,-7])
        self.assertEqual(mul, e * b)

    def testScalarMul(self):
        mul = createMatrix(2,2,[3,6,9,12])
        self.assertEqual(mul, 3 * a)

    def testVectorMul(self):
        mul = vector.Vector([9,19])
        self.assertEqual(mul, a * vector.Vector([1,4]))

    def testDiv(self):
        div = createMatrix(1,2)
        div.set([1,rational.Rational(2,3)])
        self.assertEqual(div, e / 3)

    def testGetRow(self):
        self.assertEqual(vector.Vector([1,2]), a.getRow(1))

    def testGetColumn(self):
        self.assertEqual(vector.Vector([1,3]), a.getColumn(1))

    def testInsertRow(self):
        insert_3 = createMatrix(3, 2, [1, 2] + [3, 4] + [5, 6])
        self.assertEqual(insert_3, a.insertRow(3, [5,6]))

    def testInsertColumn(self):
        insert_3 = createMatrix(2, 3, [1, 2, 5] + [3, 4, 6])
        self.assertEqual(insert_3, a.insertColumn(3, [5,6]))

    def testDeleteRow(self):
        delete_3 = createMatrix(2, 3, [1, 2, 3] + [0, 5, -2])
        self.assertEqual(delete_3, c.deleteRow(3))

    def testDeleteColumn(self):
        delete_3 = createMatrix(3, 2, [1, 2] + [0, 5] + [7, 1])
        self.assertEqual(delete_3, c.deleteColumn(3))

    def testTranspose(self):
        trans = createMatrix(2,1,[3,2])
        self.assertEqual(trans, e.transpose())

    def testTriangulate(self):
        triangle = createMatrix(3,3)
        triangle.set([1,2,3]+[0,5,-2]+[0,0,rational.Rational(-86,5)])
        self.assertEqual(triangle, c.triangulate())

    def testIsUpperTriangularMatrix(self):
        UT = createMatrix(4,4,[1,2,3,4]+[0,5,6,7]+[0,0,8,9]+[0,0,0,1])
        notUT = createMatrix(4,4,[1,2,3,4]+[0,5,6,7]+[0,0,8,9]+[0,0,1,1])
        assert UT.isUpperTriangularMatrix()
        assert not notUT.isUpperTriangularMatrix()

    def testSubMatrix(self):
        sub = createMatrix(2,2,[0,5,7,1])
        self.assertEqual(sub, c.submatrix(1,3))

    def testRank(self):
        self.assertEqual(3, c.rank())

    def testInverseImage(self):
        M = createMatrix(4,4,[2,-1,0,0]+[-1,2,-1,0]+[0,-1,2,-1]+[0,0,-1,2])
        V = createMatrix(4,4,[1,2,3,4]+[2,3,4,5]+[3,4,5,6]+[4,5,6,7])
        noinverse = createMatrix(3,3,[1,2,3]+[4,5,6]+[5,7,9])
        self.assertEqual(V, M * M.inverseImage(V))
        self.assertRaises(VectorsNotIndependent, noinverse.inverseImage, unitMatrix(3))


class SquareMatrixTest(unittest.TestCase):
    def testPow(self):
        mul2 = createMatrix(2,2,[7,10,15,22])
        self.assertEqual(mul2, a ** 2)
        mul0 = createMatrix(2,2,[1,0,0,1])
        self.assertEqual(mul0, a ** 0)
        Ra = rational.Rational
        mulminus2 = createMatrix(2,2)
        mulminus2.set([Ra(11,2),Ra(-5,2),Ra(-15,4),Ra(7,4)])
        self.assertEqual(mulminus2, a ** (-2))

    def testIsDiagonalMatrix(self):
        diag = createMatrix(2,2,[-3,0,0,5])
        assert diag.isDiagonalMatrix()

    def testIsScalarMatrix(self):
        scaler = createMatrix(2,2,[10,0,0,10])
        assert scaler.isScalarMatrix()

    def testIsSymmetricMatrix(self):
        symmetric = createMatrix(2,2,[2,3,3,5])
        assert symmetric.isSymmetricMatrix()

    def testIsOrthogonalMatrix(self):
        Ra = rational.Rational
        orthogonal = createMatrix(2,2,[Ra(3,5),Ra(4,5),Ra(-4,5),Ra(3,5)])
        assert orthogonal.isOrthogonalMatrix()

    def testIsAlternateMatrix(self):
        alternate = createMatrix(2,2,[0,2,-2,0])
        assert alternate.isAlternateMatrix()

    def testCommutator(self):
        commutator = createMatrix(2,2,[5,-1,9,-5])
        self.assertEqual(commutator, a.commutator(b))

    def testTrace(self):
        self.assertEqual(15, c.trace())

    def testDeterminant(self):
        self.assertEqual(-2, a.determinant())

    def testCofactor(self):
        cofactors = createMatrix(3,3,[47,-15,-19,-14,-12,2,-35,13,5])
        self.assertEqual(cofactors, c.cofactors())

    def testInverse(self):
        Ra = rational.Rational
        cinverse = createMatrix(3,3)
        cinverse.set([Ra(-47,86),Ra(15,86),Ra(19,86),
        Ra(7,43),Ra(6,43),Ra(-1,43),Ra(35,86),Ra(-13,86),Ra(-5,86)])
        noinverse = createMatrix(3,3,[1,2,3]+[4,5,6]+[5,7,9])
        self.assertEqual(cinverse, c.inverse())
        self.assertRaises(VectorsNotIndependent, noinverse.inverse)

    def testInverseNoChange(self):
        # sf bug#1849220
        M1 = SquareMatrix(2, 2, [rational.Rational(1, 2),
                                 rational.Rational(1, 2),
                                 rational.Rational(1, 1),
                                 rational.Rational(-3, 2)])
        M1.inverse()
        M2 = SquareMatrix(2, 2, [rational.Rational(1, 2),
                                 rational.Rational(1, 2),
                                 rational.Rational(1, 1),
                                 rational.Rational(-3, 2)])
        self.assertEqual(M2, M1)

    def testCharacteristicPolynomial(self):
        assert a.characteristicPolynomial()

    def testLUDecomposition(self):
        L, U = d.LUDecomposition()
        assert L * U == d
        assert L.isLowerTriangularMatrix()
        assert U.isUpperTriangularMatrix()

    def testHessenbergForm(self):
        pass


class IntegerMatrixTest (unittest.TestCase):
    def testHermiteNormalForm(self):
        already = IntegerMatrix(4,3,[1,0,0,0,1,0,0,0,1,0,0,1])
        h = already.hermiteNormalForm()
        self.assertEqual(h, already)

        lessrank = IntegerMatrix(2,3,[1,0,0,0,1,0])
        h = lessrank.hermiteNormalForm()
        self.assertEqual(h.row, lessrank.row)
        self.assertEqual(h.column, lessrank.column)
        zerovec = vector.Vector([0, 0])
        self.assertEqual(zerovec, h.getColumn(1))

        square = IntegerMatrix(3,3,[1,0,0,0,1,1,0,1,1])
        h = square.hermiteNormalForm()
        self.assertEqual(h.row, square.row)
        self.assertEqual(h.column, square.column)
        hermite = IntegerMatrix(3,3,[0,1,0,0,0,1,0,0,1])
        self.assertEqual(hermite, h)


class IntegerSquareTest(unittest.TestCase):
    def testSmithNormalForm(self):
        s1 = IntegerSquareMatrix(3,3,[1,3,2,4,6,5,6,8,9])
        s2 = IntegerSquareMatrix(3,3,[1,2,4,0,3,5,0,0,0])
        s3 = IntegerSquareMatrix(3,3,[1,0,0,9,1,0,5,6,1])
        self.assertEqual(h1, s1.smithNormalForm())
        self.assertRaises(ValueError, s2.smithNormalForm)
        self.assertEqual(h3, s3.smithNormalForm())

    def testExtSmithNormalForm(self):
        s = IntegerSquareMatrix(3,3,[1,3,2,4,6,5,6,8,9])
        self.assertEqual(i, s.extsmithNormalForm())

    def testDeterminant(self):
        m = IntegerSquareMatrix(3, 3, [3,1,2,5,4,6,7,9,8])
        self.assert_(isinstance(m.determinant(), (int, long)))
        self.assertEqual(-30, m.determinant())


class MatrixRingTest (unittest.TestCase):
    def setUp(self):
        import nzmath.rational as rational
        self.m2z = MatrixRing.getInstance(2, rational.theIntegerRing)
        # XXX coefficient ring should be able to be specified.

    def testZero(self):
        z = self.m2z.zero
        self.assertEqual(0, z[1, 1])
        self.assertEqual(0, z[1, 2])
        self.assertEqual(0, z[2, 1])
        self.assertEqual(0, z[2, 2])

    def testOne(self):
        o = self.m2z.one
        self.assertEqual(1, o[1, 1])
        self.assertEqual(0, o[1, 2])
        self.assertEqual(0, o[2, 1])
        self.assertEqual(1, o[2, 2])


class SubspaceTest(unittest.TestCase):
    def testSupplementBasis(self):
        ba = Subspace(3, 2, [1,2,3,4,5,7])
        supbase = createMatrix(3,3,[1,2,0,3,4,0,5,7,1])
        self.assertEqual(supbase, ba.supplementBasis())

    def testSupplementBasisF2(self):
        import nzmath.finitefield as finitefield
        F2 = finitefield.FinitePrimeField.getInstance(2)
        ba = Subspace(3, 2, [F2.one, F2.one, F2.one, F2.zero, F2.zero, F2.one])
        self.assertEqual(3, ba.supplementBasis().column)


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
