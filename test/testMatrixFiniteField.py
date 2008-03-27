import unittest
import nzmath.finitefield as _finitefield
import nzmath.matrix as _matrix


class FiniteFieldMatrixTest (unittest.TestCase):
    """
    Test classes must inherite unittest.TestCase.
    They have name suffixed with 'Test'.
    """
    def setUp(self):
        """
	setUp is run before each test method run.
	"""
        self.F7 = _finitefield.FinitePrimeField.getInstance(7)

    def tearDown(self):
        """
	tearDown is run after each test method run.
	"""
        pass

    def testDeterminant(self):
        """
	Every test method have name prefixed with 'test'.
	"""
        invertible = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [2, 5, 3, 1]])
        noninvertible = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [2, 6, 6, 4]])
	# asserting something
        self.assertEqual(self.F7.one, invertible.determinant())
	# asserting equality
        self.assertEqual(self.F7.zero, noninvertible.determinant())

    def testInverse(self):
        """
	Every test method have name prefixed with 'test'.
	"""
        invertible = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [2, 5, 3, 1]])
        inverse = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [1, 2, 4, 2]])
        noninvertible = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [2, 6, 3, 2]])
	# asserting something
        self.assertEqual(inverse, invertible.inverse())
	# asserting equality
        self.assertRaises(_matrix.NoInverse, noninvertible.inverse)

    def testGetRing(self):
        invertible = _matrix.createMatrix(2, [self.F7.createElement(c) for c in [2, 5, 3, 1]])
        self.assert_(invertible.getRing())
        M2F7 = _matrix.MatrixRing.getInstance(2, self.F7)
        self.assertEqual(M2F7, invertible.getRing())
        M3F7 = _matrix.MatrixRing.getInstance(3, self.F7)
        self.assertNotEqual(M3F7, invertible.getRing())


class SubspaceTest(unittest.TestCase):
    def testSupplementBasisF2(self):
        F2 = _finitefield.FinitePrimeField.getInstance(2)
        ba = _matrix.Subspace(3, 2, [F2.one, F2.one, F2.one, F2.zero, F2.zero, F2.one])
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
