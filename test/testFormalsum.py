"""
test for formalsum module
"""

import unittest
import nzmath.poly.formalsum as formalsum

class DictFormalSumTest (unittest.TestCase):
    def setUp(self):
        self.x = formalsum.DictFormalSum({"x": 1})
        self.y = formalsum.DictFormalSum({"y": 1})
        self.zero = formalsum.DictFormalSum({})

    def tearDown(self):
        pass

    def testNonzero(self):
        self.assertTrue(self.x)
        self.assertFalse(self.zero)

    def testLookup(self):
        self.assertEqual(1, self.x['x'])
        self.assertEqual(None, self.x['y'])

    def testAdd(self):
        z = formalsum.DictFormalSum({'x': 1, 'y': 1})
        d = formalsum.DictFormalSum({'x': 2})
        self.assertEqual(z, self.x + self.y)
        self.assertEqual(d, self.x + self.x)
        self.assertEqual(self.x, self.x + self.zero)
        self.assertEqual(self.x, self.zero + self.x)

    def testPos(self):
        self.assertEqual(self.x, +self.x)
        self.assertTrue(self.x is not +self.x)

    def testNeg(self):
        mx = formalsum.DictFormalSum({'x': -1})
        self.assertEqual(mx, -self.x)

    def testSubtract(self):
        z = formalsum.DictFormalSum({'x': 1, 'y': -1})
        self.assertEqual(z, self.x - self.y)
        self.assertEqual(-z, self.y - self.x)

    def testAttemptToSet(self):
        """
        DictFormalSum is immutable.
        """
        try:
            self.x[1] = 1
            self.fail()
        except TypeError:
            pass

    def testAttemptToDel(self):
        """
        DictFormalSum is immutable.
        """
        try:
            del self.x['x']
            self.fail()
        except TypeError:
            pass

    def testNested(self):
        n = formalsum.DictFormalSum({self.x: self.x})
        self.assertEqual(self.x, n[self.x])

    def testScalarMul(self):
        d = formalsum.DictFormalSum({'x': 2})
        self.assertEqual(d, self.x * 2)
        self.assertEqual(d, 2 * self.x)
        # drak corner: self.x * self.x is somewhat possible

    def testIterations(self):
        self.assertEqual(['x'], self.x.bases())
        self.assertEqual([1], self.x.coefficients())
        self.assertEqual([('x', 1)], self.x.terms())
        self.assertEqual(['x'], [b for b in self.x.iterbases()])
        self.assertEqual([1], [c for c in self.x.itercoefficients()])
        self.assertEqual([('x', 1)], [t for t in self.x.iterterms()])

    def testContains(self):
        self.assertTrue('x' in self.x)

    def testLen(self):
        self.assertEqual(1, len(self.x))

    def testCoefficientMap(self):
        double = lambda x: 2*x
        two_x = formalsum.DictFormalSum({"x": 2})
        self.assertEqual(two_x, self.x.coefficients_map(double))


class ListFormalSumTest (unittest.TestCase):
    def setUp(self):
        self.x = formalsum.ListFormalSum([("x", 1)])
        self.y = formalsum.ListFormalSum([("y", 1)])
        self.zero = formalsum.ListFormalSum([])

    def tearDown(self):
        pass

    def testNonzero(self):
        self.assertTrue(self.x)
        self.assertFalse(self.zero)

    def testLookup(self):
        self.assertEqual(1, self.x['x'])
        self.assertEqual(None, self.x['y'])

    def testAdd(self):
        z = formalsum.ListFormalSum([('x', 1), ('y', 1)])
        d = formalsum.ListFormalSum([('x', 2)])
        self.assertEqual(z, self.x + self.y)
        self.assertEqual(d, self.x + self.x)
        self.assertEqual(self.x, self.x + self.zero)
        self.assertEqual(self.x, self.zero + self.x)

    def testPos(self):
        self.assertEqual(self.x, +self.x)
        self.assertTrue(self.x is not +self.x)

    def testNeg(self):
        mx = formalsum.ListFormalSum([('x', -1)])
        self.assertEqual(mx, -self.x)

    def testSubtract(self):
        z = formalsum.ListFormalSum([('x', 1), ('y', -1)])
        self.assertEqual(z, self.x - self.y)
        self.assertEqual(-z, self.y - self.x)

    def testAttemptToSet(self):
        """
        ListFormalSum is immutable.
        """
        try:
            self.x[1] = 1
            self.fail()
        except TypeError:
            pass

    def testAttemptToDel(self):
        """
        ListFormalSum is immutable.
        """
        try:
            del self.x['x']
            self.fail()
        except TypeError:
            pass

    def testNested(self):
        n = formalsum.ListFormalSum([(self.x, self.x)])
        self.assertEqual(self.x, n[self.x])

    def testScalarMul(self):
        d = formalsum.ListFormalSum([('x', 2)])
        self.assertEqual(d, self.x * 2)
        self.assertEqual(d, 2 * self.x)
        # drak corner: self.x * self.x is somewhat possible

    def testIterations(self):
        self.assertEqual(['x'], self.x.bases())
        self.assertEqual([1], self.x.coefficients())
        self.assertEqual([('x', 1)], self.x.terms())
        self.assertEqual(['x'], [b for b in self.x.iterbases()])
        self.assertEqual([1], [c for c in self.x.itercoefficients()])
        self.assertEqual([('x', 1)], [t for t in self.x.iterterms()])

    def testContains(self):
        self.assertTrue('x' in self.x)

    def testLen(self):
        self.assertEqual(1, len(self.x))

    def testCoefficientMap(self):
        double = lambda x: 2*x
        two_x = formalsum.ListFormalSum([("x", 2)])
        self.assertEqual(two_x, self.x.coefficients_map(double))


def suite(suffix="Test"):
    _suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            _suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return _suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
