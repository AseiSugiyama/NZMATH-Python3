import unittest
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil
import nzmath.poly.multiutil as multiutil
import nzmath.poly.ring as poly_ring


class PolynomialRingTest(unittest.TestCase):
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

    def testOne(self):
        one = uniutil.polynomial({0: 1}, rational.theIntegerRing)
        self.assertEqual(one, self.zx.one)
        try:
            self.zx.one = 0
        except AttributeError:
            # should be raised.
            pass
        except:
            self.failIf(False, "unexcepted error is raised")
        else:
            self.failIf(False, "assignment should be prohibited")

    def testZero(self):
        zero = uniutil.polynomial((), rational.theIntegerRing)
        self.assertEqual(zero, self.zx.zero)
        try:
            self.zx.zero = 0
        except AttributeError:
            # should be raised.
            pass
        except:
            self.failIf(False, "unexcepted error is raised")
        else:
            self.failIf(False, "assignment should be prohibited")


class MultivarPolynomialRingTest(unittest.TestCase):
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


class PolynomialIdealTest(unittest.TestCase):
    def setUp(self):
        self.Z = rational.theIntegerRing
        self.Q = rational.theRationalField
        self.zx = poly_ring.PolynomialRing.getInstance(self.Z)
        self.qx = poly_ring.PolynomialRing.getInstance(self.Q)

    def testNonzero(self):
        self.failIf(poly_ring.PolynomialIdeal(self.Q.zero, self.qx))

    def testReduceFieldPolynomial(self):
        whole = poly_ring.PolynomialIdeal(self.Q.one, self.qx)
        f = uniutil.polynomial([(1, self.Q.createElement(3, 4))], self.Q)
        self.failIf(whole.reduce(f))
        self.assert_(poly_ring.PolynomialIdeal(f, self.qx).reduce(self.Q.one))

    def testReduceEuclideanPolynomial(self):
        whole = poly_ring.PolynomialIdeal(-1, self.zx)
        f = uniutil.polynomial([(0, 3), (1, 2)], self.Z)
        f_ideal = poly_ring.PolynomialIdeal(f, self.zx)
        self.failIf(whole.reduce(f))
        self.assert_(f_ideal.reduce(self.Z.one))

        two_generators = poly_ring.PolynomialIdeal([f, self.zx.createElement(5)], self.zx)
        self.failIf(two_generators.reduce(f))
        self.assert_(two_generators.reduce(self.Z.one))

    def testNormalizeGenerators(self):
        f = uniutil.polynomial([(0, 3), (1, 2)], self.Z)
        i1 = poly_ring.PolynomialIdeal([f, self.zx.createElement(5)], self.zx)
        i2 = poly_ring.PolynomialIdeal([self.zx.createElement(5), f], self.zx)
        self.assertEqual(i1.generators, i2.generators)
        self.assertEqual(i1, i2)

    def testZeroIdeal(self):
        null = poly_ring.PolynomialIdeal(self.zx.zero, self.zx)
        self.assert_(self.zx.zero in null)
        self.failIf(self.zx.one in null)


class MultivariablePolynomialIdealTest (unittest.TestCase):
    def setUp(self):
        self.Z = rational.theIntegerRing
        self.Q = rational.theRationalField
        self.Z2 = poly_ring.PolynomialRing(self.Z, 2)
        self.Q3 = poly_ring.PolynomialRing(self.Q, 3)

    def testNonzero(self):
        self.failIf(poly_ring.PolynomialIdeal(self.Q3.zero, self.Q3))
        self.assert_(poly_ring.PolynomialIdeal([self.Q3.one], self.Q3))

    def testZeroIdeal(self):
        null = poly_ring.PolynomialIdeal(self.Z2.zero, self.Z2)
        self.assert_(self.Z2.zero in null)
        self.failIf(self.Z2.one in null)


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
