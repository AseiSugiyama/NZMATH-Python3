import unittest
import nzmath.poly.univar as univar


class BasicPolynomialArithmeticTest (unittest.TestCase):
    def setUp(self):
        self.f = univar.BasicPolynomial({0:1, 1:2, 4:3})
        self.g = univar.BasicPolynomial({1:-1, 3:2})

    def testAdd(self):
        h = univar.BasicPolynomial({0:1, 1:1, 3:2, 4:3})
        self.assertEqual(h, self.f + self.g)
        self.assertEqual(h, self.g + self.f)

    def testNeg(self):
        h = univar.BasicPolynomial({0:-1, 1:-2, 4:-3})
        self.assertEqual(h, -self.f)

    def testMul(self):
        h = univar.BasicPolynomial({1:-1, 2:-2, 3:2, 4:4, 5:-3, 7:6})
        self.assertEqual(h, self.f * self.g)
        self.assertEqual(h, self.g * self.f)
        self.assertEqual(-self.g, self.g*(-1))
        self.assertEqual(-self.g, (-1)*self.g)

    def testPow(self):
        h1 = univar.BasicPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})
        h2 = univar.BasicPolynomial({3:-1, 5:6, 7:-12, 9:8})
        self.assertEqual(h1, self.f ** 2)
        self.assertEqual(h2, self.g ** 3)

    def testDifferentiate(self):
        h = univar.BasicPolynomial({0:-1, 2:6})
        self.assertEqual(h, self.g.differentiate())

    def testSubstitution(self):
        self.assertEqual(45, self.f(-2))


class SortedPolynomialArithmeticTest (unittest.TestCase):
    def testAdd(self):
        f = univar.SortedPolynomial([(1, 2), (4, 3)], True)
        g = univar.SortedPolynomial([(1, -2), (3, 7)], True)
        s = univar.SortedPolynomial([(3, 7), (4, 3)], True)
        self.assertEqual(s, f + g)
        h1 = univar.SortedPolynomial([(0, 1), (1, 4), (2, 4)])
        h2 = univar.SortedPolynomial([(2, 6), (3, 12)])
        s2 = univar.SortedPolynomial([(0, 1), (1, 4), (2, 10), (3, 12)])
        self.assertEqual(s2, h1 + h2)

    def testSub(self):
        f = univar.SortedPolynomial([(1, 2), (4, 3)], True)
        g = univar.SortedPolynomial([(1, 2), (3, 7)], True)
        d = univar.SortedPolynomial([(3, -7), (4, 3)], True)
        self.assertEqual(d, f - g)
        h1 = univar.SortedPolynomial([(0, 1), (1, 4), (2, 4)])
        h2 = univar.SortedPolynomial([(2, 6), (3, 12)])
        d2 = univar.SortedPolynomial([(0, 1), (1, 4), (2, -2), (3, -12)])
        self.assertEqual(d2, h1 - h2)

    def testMul(self):
        s = univar.SortedPolynomial([(0, 1), (1, 4), (2, 10), (3, 12)], True)
        d = univar.SortedPolynomial([(0, 1), (1, 4), (2, -2), (3, -12)], True)
        m = univar.SortedPolynomial([(0, 1), (1, 4), (2, 4)]).square() - univar.SortedPolynomial([(2, 6), (3, 12)]).square()
        self.assertEqual(m, s * d)
        self.assertEqual(m, s.ring_mul(d))
        self.assertEqual(m, s.ring_mul_karatsuba(d))
        self.assertEqual(m, d * s)
        self.assertEqual(m, d.ring_mul(s))
        self.assertEqual(m, d.ring_mul_karatsuba(s))
        s = univar.SortedPolynomial([(0, 1), (1, 4), (2, 10), (3, 12)])
        d = univar.SortedPolynomial([(0, 1), (1, 4), (2, -2), (3, -12)])
        m = univar.SortedPolynomial([(0, 1), (1, 4), (2, 4)]).square() - univar.SortedPolynomial([(2, 6), (3, 12)]).square()
        self.assertEqual(m, s * d)
        self.assertEqual(m, s.ring_mul(d))
        self.assertEqual(m, s.ring_mul_karatsuba(d))
        self.assertEqual(m, d * s)
        self.assertEqual(m, d.ring_mul(s))
        self.assertEqual(m, d.ring_mul_karatsuba(s))

    def testScalarMul(self):
        b = univar.BasicPolynomial([(0, 1), (1, 4), (2, 10), (3, 12)])
        s = univar.SortedPolynomial([(0, 1), (1, 4), (2, 10), (3, 12)])
        d = univar.BasicPolynomial([(0, 2), (1, 8), (2, 20), (3, 24)])
        self.assertEqual(d, b * 2)
        self.assertEqual(d, 2 * b)
        self.assertEqual(d, s * 2)
        self.assertEqual(d, 2 * s)

    def testPow(self):
        f = univar.SortedPolynomial({0:1, 1:2, 4:3})
        g = univar.SortedPolynomial({1:-1, 3:2})
        h1 = univar.SortedPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})
        h2 = univar.SortedPolynomial({3:-1, 5:6, 7:-12, 9:8})
        self.assertEqual(h1, f.square())
        self.assertEqual(h2, g ** 3)

    def testSubstitution(self):
        f = univar.SortedPolynomial([(0, 1), (1, 2), (4, 3)], True)
        self.assertEqual(45, f(-2))


class PolynomialDatTaypeTest (unittest.TestCase):
    def setUp(self):
        self.b = univar.BasicPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})
        self.s = univar.SortedPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})

    def testGetitem(self):
        self.assertEqual(1, self.b[0])
        self.assertEqual(0, self.b[3])
        self.assertEqual(1, self.s[0])
        self.assertEqual(0, self.s[3])

    def testContains(self):
        self.assert_(0 in self.b)
        self.assert_(8 in self.b)
        self.failIf(3 in self.b)
        self.assert_(0 in self.s)
        self.assert_(8 in self.s)
        self.failIf(3 in self.s)

    def testComparability(self):
        self.assertEqual(self.s, self.b)
        self.assertEqual(self.b, self.s)

    def testCoefficientsMap(self):
        double = lambda x: 2*x
        self.assertEqual(2 * self.b, self.b.coefficients_map(double))
        self.assertEqual(2 * self.s, self.s.coefficients_map(double))


class PolynomialIteratorTest (unittest.TestCase):
    def setUp(self):
        self.b = univar.BasicPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})
        self.s = univar.SortedPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})

    def testItercoefficients(self):
        coefficients = [1, 4, 4, 6, 12, 9]
        self.assertEqual(coefficients, [c for c in self.b.itercoefficients()])
        self.assertEqual(coefficients, [c for c in self.s.itercoefficients()])

    def testIterbases(self):
        bases = [0, 1, 2, 4, 5, 8]
        self.assertEqual(bases, [c for c in self.b.iterbases()])
        self.assertEqual(bases, [c for c in self.s.iterbases()])

    def testIterterms(self):
        terms = [(0, 1), (1, 4), (2, 4), (4, 6), (5, 12), (8, 9)]
        self.assertEqual(terms, [t for t in self.b.iterterms()])
        self.assertEqual(terms, [t for t in self.s.iterterms()])
        zipped = zip(self.b.iterbases(), self.b.itercoefficients())
        self.assertEqual(zipped, [t for t in self.b.iterterms()])
        zipped = zip(self.s.iterbases(), self.s.itercoefficients())
        self.assertEqual(zipped, [t for t in self.s.iterterms()])

    def testIter(self):
        """
        iteration over the polynomials are equivalent to over their
        terms.
        """
        terms = [(0, 1), (1, 4), (2, 4), (4, 6), (5, 12), (8, 9)]
        self.assertEqual(terms, [t for t in self.b])
        self.assertEqual(terms, [t for t in self.s])


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
