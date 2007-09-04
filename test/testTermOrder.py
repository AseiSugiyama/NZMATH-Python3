import unittest
import nzmath.poly.univar as univar
import nzmath.poly.multivar as multivar
import nzmath.poly.termorder as termorder


class UnivarTermOrderTest (unittest.TestCase):
    """
    tests for UnivarTermOrder.
    """
    def testInit(self):
        """
	__init__ works.
	"""
        self.assert_(termorder.UnivarTermOrder(lambda x, y: 0))
        self.assertRaises(TypeError, termorder.UnivarTermOrder)

    def testFormat(self):
        """
        format works.
        """
        f = univar.BasicPolynomial({0:4.3})
        asc_str = "4.3"
        self.assertEqual(asc_str, termorder.ascending_order.format(f))
        f = univar.BasicPolynomial({1:3, 4:2})
        asc_str = "3 * X + 2 * X ** 4"
        desc_str = "2 * X ** 4 + 3 * X"
        self.assertEqual(asc_str, termorder.ascending_order.format(f))
        self.assertEqual(desc_str, termorder.ascending_order.format(f, reverse=True))
        f = univar.BasicPolynomial({1:3, 4:-2})
        asc_str = "3 * X - 2 * X ** 4"
        self.assertEqual(asc_str, termorder.ascending_order.format(f))
        f = univar.BasicPolynomial({1:1, 4:2})
        asc_str = "X + 2 * X ** 4"
        self.assertEqual(asc_str, termorder.ascending_order.format(f))
        f = univar.BasicPolynomial({1:2, 4:-1})
        asc_str = "2 * Y - Y ** 4"
        self.assertEqual(asc_str, termorder.ascending_order.format(f, "Y"))

    def testFormatSorted(self):
        g = univar.SortedPolynomial([(1, 2), (4, -1)])
        asc_str = "2 * Y - Y ** 4"
        self.assertEqual(asc_str, termorder.ascending_order.format(g, "Y"))

    def testDegree(self):
        f = univar.BasicPolynomial({1:2, 4:-1})
        self.assertEqual(4, termorder.ascending_order.degree(f))
        g = univar.SortedPolynomial([(1, 2), (4, -1)])
        self.assertEqual(4, termorder.ascending_order.degree(g))
        zero = univar.BasicPolynomial(())
        self.assert_(termorder.ascending_order.degree(zero) < 0)

    def testLeadingCoefficient(self):
        f = univar.BasicPolynomial({1:2, 4:-1})
        self.assertEqual(-1, termorder.ascending_order.leading_coefficient(f))
        g = univar.SortedPolynomial([(1, 2), (4, -1)])
        self.assertEqual(-1, termorder.ascending_order.leading_coefficient(g))

    def testLeadingTerm(self):
        f = univar.BasicPolynomial({1:2, 4:-1})
        self.assertEqual((4, -1), termorder.ascending_order.leading_term(f))
        g = univar.SortedPolynomial([(1, 2), (4, -1)])
        self.assertEqual((4, -1), termorder.ascending_order.leading_term(g))


class MultivarTermOrderTest (unittest.TestCase):
    """
    tests for MultivarTermOrder.
    """
    def setUp(self):
        self.lex = termorder.lexicographic_order
        self.deglex = termorder.total_degree_lexicographic_order
        self.degrevlex = termorder.total_degree_reverse_lexicographic_order

    def testInit(self):
        self.assert_(self.lex)
        self.assert_(self.deglex)
        self.assert_(self.degrevlex)
        self.assertRaises(TypeError, termorder.MultivarTermOrder)

    def testFormatConst(self):
        """
        format works for constant.
        """
        f = multivar.BasicPolynomial({(0, 0): 4})
        self.assertRaises(TypeError, self.lex.format, f)
        const4 = "4"
        self.assertEqual(const4, self.lex.format(f, varnames=("X", "Y")))
        self.assertEqual(const4, self.deglex.format(f, varnames=("X", "Y")))
        self.assertEqual(const4, self.degrevlex.format(f, varnames=("X", "Y")))

    def testFormatHomogeneous(self):
        """
        format works for homogeneous polynomials.
        """
        f = multivar.BasicPolynomial({(0, 2): 4, (1, 1): 1, (2, 0): 3})
        qf = "4 * Y ** 2 + X * Y + 3 * X ** 2"
        self.assertEqual(qf, self.lex.format(f, varnames=("X", "Y")))
        self.assertEqual(qf, self.deglex.format(f, varnames=("X", "Y")))
        qfr = "3 * X ** 2 + X * Y + 4 * Y ** 2"
        self.assertEqual(qfr, self.lex.format(f, varnames=("X", "Y"), reverse=True))
        self.assertEqual(qfr, self.degrevlex.format(f, varnames=("X", "Y")))

    def testFormatInhomogeneous(self):
        """
        format works for inhomogeneous polynomials.
        """
        f = multivar.BasicPolynomial({(0, 2): 4, (1, 1): 1, (1, 0): 3})
        flex = "4 * Y ** 2 + 3 * X + X * Y"
        self.assertEqual(flex, self.lex.format(f, varnames=("X", "Y")))
        fdlex = "3 * X + 4 * Y ** 2 + X * Y"
        self.assertEqual(fdlex, self.deglex.format(f, varnames=("X", "Y")))
        fdrl = "3 * X + X * Y + 4 * Y ** 2"
        self.assertEqual(fdrl, self.degrevlex.format(f, varnames=("X", "Y")))

    def testFormatNull(self):
        """
        format works for null terms polynomials.
        """
        f = multivar.BasicPolynomial({(0, 2): 0, (1, 1): 0, (1, 0): 0})
        flex = "0"
        self.assertEqual(flex, self.lex.format(f, varnames=("X", "Y")))


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
