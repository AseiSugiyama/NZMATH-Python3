import unittest
import nzmath.poly.multivar as multivar


class BasicPolynomialTest (unittest.TestCase):
    """
    test for BasicPolynomial
    """
    def setUp(self):
        """
	setUp is run before each test method run.
	"""
        self.f = multivar.BasicPolynomial({(1, 2, 3): 4})
        self.g = multivar.BasicPolynomial({(1, 2, 3): 9})
        self.h = multivar.BasicPolynomial({(1, 1, 1): 1})

    def testAdd(self):
        """
	addition
	"""
        sum1 = multivar.BasicPolynomial({(1, 2, 3): 13})
        sum2 = multivar.BasicPolynomial({(1, 1, 1): 1, (1, 2, 3): 4})
        self.assertEqual(sum1, self.f + self.g)
        self.assertEqual(sum2, self.f + self.h)

    def testPos(self):
        """
        unary +
        """
        self.assertEqual(self.f, +self.f)

    def testNeg(self):
        """
        unary -
        """
        neg = multivar.BasicPolynomial({(1, 2, 3): -4})
        self.assertEqual(neg, -self.f)

    def testMul(self):
        """
        multiplication
        """
        prod1 = multivar.BasicPolynomial({(2, 4, 6): 36})
        self.assertEqual(prod1, self.f * self.g)
        sprod = multivar.BasicPolynomial({(1, 2, 3): 28})
        self.assertEqual(sprod, self.f * 7)
        self.assertEqual(sprod, 7 * self.f)

    def testSquare(self):
        """
        squaring
        """
        hsquare = multivar.BasicPolynomial({(2, 2, 2): 1})
        self.assertEqual(hsquare, self.h ** 2)
        self.assertEqual(hsquare, self.h.square())
        ssquare = multivar.BasicPolynomial({(2, 2, 2): 1, (2, 3, 4): 8, (2, 4, 6): 16})
        self.assertEqual(ssquare, (self.f + self.h) ** 2)
        self.assertEqual(ssquare, (self.f + self.h).square())
        qsquare = multivar.BasicPolynomial({(4, 4, 4): 1, (4, 5, 6): 16, (4, 6, 8): 96, (4, 7, 10): 256, (4, 8, 12): 256})
        self.assertEqual(qsquare, (self.f + self.h) ** 4)
        self.assertEqual(qsquare, ssquare ** 2)
        self.assertEqual(qsquare, ssquare.square())

    def testCall(self):
        """
        substitution
        """
        zero = multivar.BasicPolynomial({}, number_of_variables=3)
        self.assertEqual(zero, self.f(0, 0))
        self.assertEqual(zero, self.f(1, 0))
        self.assertEqual(zero, self.f(2, 0))
        self.assertRaises(IndexError, self.f.__call__, 3, 0)
        subst1 = multivar.BasicPolynomial({(0, 2, 3): 4})
        self.assertEqual(subst1, self.f(0, 1))

    def testMultCall(self):
        """
        substitution simultaneous
        """
        subst12 = multivar.BasicPolynomial({(0, 0, 3,): 16})
        self.assertEqual(subst12, self.f((0, 1), (1, 2)))

    def testEraseVariable(self):
        fxy = multivar.BasicPolynomial({(1, 2): 4})
        fxz = multivar.BasicPolynomial({(1, 3): 4})
        fyz = multivar.BasicPolynomial({(2, 3): 4})
        self.assertEqual(fxy, self.f.erase_variable(2))
        self.assertEqual(fxz, self.f.erase_variable(1))
        self.assertEqual(fyz, self.f.erase_variable(0))
        self.assertEqual(fyz, self.f.erase_variable()) # default
        p = multivar.BasicPolynomial({(1, 0): 1, (2, 0): 2, (1, 1): -2})
        q = multivar.BasicPolynomial({(0,): 3, (1,): -2})
        self.assertEqual(q, p.erase_variable())
        r = multivar.BasicPolynomial({(): 1})
        self.assertEqual(r, p.erase_variable().erase_variable())

    def testCombineSimilarTerm(self):
        p = multivar.BasicPolynomial({(1, 0): 1, (2, 0): 2, (1, 1): -2})
        p0 = [(1, multivar.BasicPolynomial({(0,): 1, (1,): -2})),
              (2, multivar.BasicPolynomial({(0,): 2}))]
        p1 = [(0, multivar.BasicPolynomial({(1,): 1, (2,): 2})),
              (1, multivar.BasicPolynomial({(1,): -2}))]
        self.assertEqual(p0, p.combine_similar_terms(0))
        self.assertEqual(p1, p.combine_similar_terms(1))


class TermIndecesTest (unittest.TestCase):
    def setUp(self):
        self.term = multivar.TermIndeces((1, 2, 3))

    def testEq(self):
        identical = multivar.TermIndeces((1, 2, 3))
        self.assertEqual(identical, self.term)
        different = multivar.TermIndeces((1, 2, 4))
        self.assertNotEqual(self.term, different)

    def testCmp(self):
        """
        comparisons just like for tuples
        """
        identical = multivar.TermIndeces((1, 2, 3))
        self.assertEqual(0, cmp(self.term, identical))
        lower = multivar.TermIndeces((0, 1, 2))
        self.assertEqual(1, cmp(self.term, lower))
        self.assertEqual(-1, cmp(lower, self.term))
        self.assert_(self.term >= lower)
        self.assert_(lower <= self.term)
        self.assert_(self.term > lower)
        self.assert_(lower < self.term)


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
