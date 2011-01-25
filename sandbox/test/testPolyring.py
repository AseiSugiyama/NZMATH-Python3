import unittest
import nzmath.rational as rational
import sandbox.poly.uniutil as uniutil
import sandbox.poly.multiutil as multiutil
import sandbox.poly.ring as poly_ring


class PolynomialRingTest (unittest.TestCase):
    def setUp(self):
        Z = rational.theIntegerRing
        self.zx = poly_ring.PolynomialRing(Z)

    def testTrivial(self):
        self.assertEqual(self.zx, self.zx)
        zx = "Z[]"
        self.assertEqual(zx, str(self.zx))

    def testCreateElement(self):
        """
        createElement method is tweaked in uniutil.
        """
        one = uniutil.polynomial({0: 1}, rational.theIntegerRing)
        self.assertEqual(one, self.zx.createElement(1))


class MultivarPolynomialRingTest (unittest.TestCase):
    def setUp(self):
        Z = self.Z = rational.theIntegerRing
        self.Z2 = poly_ring.PolynomialRing(Z, 2)

    def testTrivial(self):
        self.assertEqual(self.Z2, self.Z2)
        self.assertEqual("Z[][]", str(self.Z2))

    def testCreateElement(self):
        """
        createElement method is tweaked in uniutil.
        """
        one = multiutil.polynomial({(0, 0): 1}, self.Z)
        self.assertEqual(one, self.Z2.createElement(1))

    def testOne(self):
        one = multiutil.polynomial({(0, 0): 1}, self.Z)
        self.assertEqual(one, self.Z2.one)

    def testZero(self):
        zero = multiutil.polynomial({}, self.Z, 2)
        self.assertEqual(zero, self.Z2.zero)


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
