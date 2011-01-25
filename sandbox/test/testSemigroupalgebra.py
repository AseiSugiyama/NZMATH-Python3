import unittest
#import sandbox.semigroupalgebra as semigroupalgebra
from sandbox.poly.semigroupalgebra import *

class SemigroupAlgebraElementTest (unittest.TestCase):
    """
    SemigroupAlgebraElement
    """
    def setUp(self):
        """
	setUp is run before each test method run.
	"""
        self.a1 = SemigroupAlgebraElement({1: 1}, ADDITIVE)
        self.m1 = SemigroupAlgebraElement({2: 1}, MULTIPLICATIVE)

    def tearDown(self):
        """
	tearDown is run after each test method run.
	"""
        pass

    def testAddHeteroOperationTypes(self):
        """
        additive one and multiplicative one cannot be added.
        """
        self.assertRaises(AssertionError, self.a1.__add__, self.m1)
        self.assertRaises(AssertionError, self.m1.__add__, self.a1)

    def testAdd(self):
        b = SemigroupAlgebraElement({1: 2}, ADDITIVE)
        self.assertEqual(b, self.a1 + self.a1)
        n = SemigroupAlgebraElement({2: 2}, MULTIPLICATIVE)
        self.assertEqual(n, self.m1 + self.m1)

    def testSub(self):
        b = SemigroupAlgebraElement({}, ADDITIVE)
        self.assertEqual(b, self.a1 - self.a1)
        n = SemigroupAlgebraElement({}, MULTIPLICATIVE)
        self.assertEqual(n, self.m1 - self.m1)

    def testNeg(self):
        b = SemigroupAlgebraElement({1: -1}, ADDITIVE)
        self.assertEqual(b, -self.a1)
        n = SemigroupAlgebraElement({2: -1}, MULTIPLICATIVE)
        self.assertEqual(n, -self.m1)

    def testPos(self):
        self.assertEqual(self.a1, +self.a1)
        self.assertEqual(self.m1, +self.m1)

    def testMul(self):
        self.assertEqual(self.a1 + self.a1, self.a1 * 2)
        self.assertEqual(self.a1 + self.a1, 2 * self.a1)
        self.assertEqual(self.m1 + self.m1, self.m1 * 2)
        self.assertEqual(self.m1 + self.m1, 2 * self.m1)

    def testPow(self):
        self.assertEqual(self.a1, self.a1 ** 1)
        self.assertEqual(self.a1 * self.a1, self.a1 ** 2)
        self.assertEqual(self.m1, self.m1 ** 1)
        self.assertEqual(self.m1 * self.m1, self.m1 ** 2)


# The following part is always unedited.
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
