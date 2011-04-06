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
        self.assertTrue(termorder.UnivarTermOrder(lambda x, y: 0))
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
        self.assertTrue(termorder.ascending_order.degree(zero) < 0)

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
        self.assertTrue(self.lex)
        self.assertTrue(self.deglex)
        self.assertTrue(self.degrevlex)
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

    def testFormatHomogeneousTwoVars(self):
        """
        format works for homogeneous polynomials.
        """
        f = multivar.BasicPolynomial({(0, 2): 4, (1, 1): 1, (2, 0): 3})
        qf = "4 * Y ** 2 + X * Y + 3 * X ** 2"
        self.assertEqual(qf, self.lex.format(f, varnames=("X", "Y")))
        self.assertEqual(qf, self.deglex.format(f, varnames=("X", "Y")))
        self.assertEqual(qf, self.degrevlex.format(f, varnames=("X", "Y")))
        qfr = "3 * X ** 2 + X * Y + 4 * Y ** 2"
        self.assertEqual(qfr, self.lex.format(f, varnames=("X", "Y"), reverse=True))

    def testFormatHomogeneous(self):
        """
        format works for homogeneous polynomials.
        """
        f = multivar.BasicPolynomial({(1, 0, 2): 4, (0, 2, 1): 1, (2, 1, 0): 3})
        fl = "Y ** 2 * Z + 4 * X * Z ** 2 + 3 * X ** 2 * Y"
        self.assertEqual(fl, self.lex.format(f, varnames=("X", "Y", "Z")))
        self.assertEqual(fl, self.deglex.format(f, varnames=("X", "Y", "Z")))
        flr = "3 * X ** 2 * Y + 4 * X * Z ** 2 + Y ** 2 * Z"
        self.assertEqual(flr, self.lex.format(f, varnames=("X", "Y", "Z"), reverse=True))
        frl = "4 * X * Z ** 2 + Y ** 2 * Z + 3 * X ** 2 * Y"
        self.assertEqual(frl, self.degrevlex.format(f, varnames=("X", "Y", "Z")))

    def testFormatInhomogeneous(self):
        """
        format works for inhomogeneous polynomials.
        """
        f = multivar.BasicPolynomial({(1, 1, 2): 2, (1, 2, 0): 1, (2, 0, 1): 3})
        fl = "2 * X * Y * Z ** 2 + X * Y ** 2 + 3 * X ** 2 * Z"
        self.assertEqual(fl, self.lex.format(f, varnames=("X", "Y", "Z")))
        fdl = "X * Y ** 2 + 3 * X ** 2 * Z + 2 * X * Y * Z ** 2"
        self.assertEqual(fdl, self.deglex.format(f, varnames=("X", "Y", "Z")))
        flr = "3 * X ** 2 * Z + X * Y ** 2 + 2 * X * Y * Z ** 2"
        self.assertEqual(flr, self.lex.format(f, varnames=("X", "Y", "Z"), reverse=True))
        self.assertEqual(flr, self.degrevlex.format(f, varnames=("X", "Y", "Z")))

    def testFormatNull(self):
        """
        format works for null terms polynomials.
        """
        f = multivar.BasicPolynomial({(0, 2): 0, (1, 1): 0, (1, 0): 0})
        flex = "0"
        self.assertEqual(flex, self.lex.format(f, varnames=("X", "Y")))


class WeightOrderTest(unittest.TestCase):
    """
    tests for weight_order
    """
    def test_wikipedia(self):
        """
        A case in wikipedia.
        weight = (1,2,4), then x**2*z**2 > x*y**2*z > z**2 > x**3.
        (in this case, tie breaker is not used)
        """
        t1 = (2, 0, 2)
        t2 = (1, 2, 1)
        t3 = (0, 0, 2)
        t4 = (3, 0, 0)
        order = termorder.weight_order((1, 2, 4), tie_breaker=None)
        self.assertEqual(1, order(t1, t2))
        self.assertEqual(1, order(t2, t3))
        self.assertEqual(1, order(t3, t4))
        self.assertEqual(1, order(t1, t3)) # transitive
        self.assertEqual(-1, order(t2, t1)) # reverse direction

    def test_tie_breaker(self):
        """
        tie breaker use cases.
        """
        order = termorder.weight_order((1, 2, 4), cmp) # LEX tie breaker
        # trivially, the same monomials are equal
        self.assertEqual(0, order((1, 2, 0), (1, 2, 0)))
        # non-trivial case
        self.assertEqual(1, order((1, 2, 0), (1, 0, 1)))

        # Note that if no tie breaker is given, an exception occurs.
        order = termorder.weight_order((1, 2, 4))
        self.assertRaises(TypeError, order, (1, 2, 0), (1, 2, 0))
        # TypeError: 'NoneType' object is not callable
        self.assertRaises(TypeError, order, (1, 2, 0), (1, 0, 1))
        # TypeError: 'NoneType' object is not callable



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
