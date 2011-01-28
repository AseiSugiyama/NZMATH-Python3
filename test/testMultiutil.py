from __future__ import division
import unittest
import logging
import nzmath.ring as ring
import nzmath.rational as rational
import nzmath.poly.ratfunc as ratfunc
import nzmath.finitefield as finitefield
import nzmath.poly.termorder as termorder
import nzmath.poly.uniutil as uniutil
import nzmath.poly.multivar as multivar
import nzmath.poly.multiutil as multiutil


logging.basicConfig()


class PseudoDivisionProviderTest (unittest.TestCase):
    """
    use PseudoDivisionProvider
    """
    def setUp(self):
        """
	define a class using DivisionProvider
	"""
        class Polynomial (multiutil.PseudoDivisionProvider,
                          multiutil.NestProvider,
                          multivar.BasicPolynomial,
                          multiutil.RingElementProvider):
            def __init__(self, coefficients, **kwds):
                multivar.BasicPolynomial.__init__(self, coefficients, **kwds)
                multiutil.RingElementProvider.__init__(self)
                multiutil.PseudoDivisionProvider.__init__(self)
                if "coeffring" in kwds:
                    self.set_coefficient_ring(kwds["coeffring"])

        Q = rational.Rational
        self.f0 = Polynomial([((0, 3), Q(1)), ((3, 0), Q(-1))],
                             coeffring=rational.theRationalField)
        self.f = Polynomial([((0, 3), Q(1)), ((3, 0), Q(-1)), ((0, 0), Q(1))],
                            coeffring=rational.theRationalField)
        self.g = Polynomial([((0, 1), Q(1)), ((1, 0), Q(-1))],
                            coeffring=rational.theRationalField)
        self.p = Polynomial

    def testPseudoDivmod(self):
        """
        pseudo divmod test.

        A result of pseudo division depends on the choice of order,
        because the leading term varies.
        """
        Q = rational.Rational
        q = self.p([((0, 2), Q(-1)), ((1, 1), Q(-1)), ((2, 0), Q(-1))])
        r = self.p([((0, 0), Q(-1))])
        # total degree reverse lexicographic order
        self.f.order = termorder.total_degree_reverse_lexicographic_order
        self.assertEqual((q, r), self.f.pseudo_divmod(self.g))
        # lexicographic order (default)
        fz = self.f.bases_map(lambda b: tuple(b) + (1,))
        fz.set_coefficient_ring(rational.theRationalField)
        gz = self.g.bases_map(lambda b: tuple(b) + (1,))
        gz.set_coefficient_ring(rational.theRationalField)
        qz = q.bases_map(lambda b: tuple(b) + (3,))
        rz = r.bases_map(lambda b: tuple(b) + (4,))
        self.assertEqual((qz, rz), fz.pseudo_divmod(gz))

    def testPseudoFloordiv(self):
        """
        pseudo floor division test.

        A result of pseudo division depends on the choice of order,
        because the leading term varies.
        """
        Q = rational.Rational
        q = self.p([((0, 2), Q(-1)), ((1, 1), Q(-1)), ((2, 0), Q(-1))])
        # total degree reverse lexicographic order
        self.f.order = termorder.total_degree_reverse_lexicographic_order
        self.assertEqual(q, self.f.pseudo_floordiv(self.g))
        # lexicographic order (default)
        fz = self.f.bases_map(lambda b: tuple(b) + (1,))
        fz.set_coefficient_ring(rational.theRationalField)
        gz = self.g.bases_map(lambda b: tuple(b) + (1,))
        gz.set_coefficient_ring(rational.theRationalField)
        qz = q.bases_map(lambda b: tuple(b) + (3,))
        self.assertEqual(qz, fz.pseudo_floordiv(gz))

    def testPseudoMod(self):
        """
        pseudo modulo test.

        A result of pseudo division depends on the choice of order,
        because the leading term varies.
        """
        Q = rational.Rational
        r = self.p([((0, 0), Q(-1))])
        # total degree reverse lexicographic order
        self.f.order = termorder.total_degree_reverse_lexicographic_order
        self.assertEqual(r, self.f.pseudo_mod(self.g))
        # lexicographic order (default)
        fz = self.f.bases_map(lambda b: tuple(b) + (1,))
        fz.set_coefficient_ring(rational.theRationalField)
        gz = self.g.bases_map(lambda b: tuple(b) + (1,))
        gz.set_coefficient_ring(rational.theRationalField)
        rz = r.bases_map(lambda b: tuple(b) + (4,))
        self.assertEqual(rz, fz.pseudo_mod(gz))

    def testTruediv(self):
        """
        true division test.
        """
        # lexicographic order (default)
        fz = self.f.bases_map(lambda b: tuple(b) + (1,))
        fz.set_coefficient_ring(rational.theRationalField)
        gz = self.g.bases_map(lambda b: tuple(b) + (1,))
        gz.set_coefficient_ring(rational.theRationalField)
        self.assertEqual(ratfunc.RationalFunction, (fz / gz).__class__)

    def testExactDivision(self):
        Q = rational.Rational
        q = self.p([((0, 2), Q(1)), ((1, 1), Q(1)), ((2, 0), Q(1))])
        # total degree reverse lexicographic order
        self.f0.order = termorder.total_degree_reverse_lexicographic_order
        self.assertEqual(q, self.f0.exact_division(self.g))


class NestProviderTest (unittest.TestCase):
    def setUp(self):
        """
	define a class using DivisionProvider
	"""
        Polynomial = multiutil.UniqueFactorizationDomainPolynomial
        R = rational.Rational
        Q = rational.theRationalField
        self.f1 = f1 = Polynomial([((3, 1), R(1)), ((0, 1), R(1))], coeffring=Q)
        f2 = Polynomial([((0, 1), R(-1))], coeffring=Q)
        self.fn = uniutil.polynomial([(0, f1), (3, f2)], coeffring=f1.getRing())
        self.fz = Polynomial([((0, 3, 1), R(1)), ((3, 0, 1), R(-1)), ((0, 0, 1), R(1))], coeffring=Q)
        u1 = uniutil.polynomial([(1, R(1))], coeffring=Q)
        u2 = uniutil.polynomial([(1, R(1))], coeffring=Q)
        self.u = uniutil.polynomial([(0, u1), (3, u2)], u1.getRing())

    def testNest(self):
        self.assertEqual(self.fn, self.fz.nest(0, rational.theRationalField))
        self.assertEqual(self.u, self.f1.nest(0, rational.theRationalField))

    def testUnnest(self):
        self.assertEqual(self.fz, self.fz.unnest(self.fn, 0, rational.theRationalField))
        self.assertEqual(self.f1, self.f1.unnest(self.u, 0, rational.theRationalField))


class GcdProviderTest (unittest.TestCase):
    """
    use GcdProvider
    """
    def setUp(self):
        """
	define a class using DivisionProvider
	"""
        Polynomial = multiutil.UniqueFactorizationDomainPolynomial
        R = rational.Rational
        Q = rational.theRationalField
        self.f1 = Polynomial([((3, 1), R(1)), ((0, 1), R(1))], coeffring=Q)
        self.f2 = Polynomial([((0, 1), R(-1))], coeffring=Q)
        self.f3 = Polynomial([((0, 3), R(1)), ((3, 0), R(-1))], coeffring=Q)
        self.f4 = Polynomial([((0, 1), R(1)), ((1, 0), R(-1))], coeffring=Q)
        self.fz = Polynomial([((0, 3, 1), R(1)), ((3, 0, 1), R(-1)), ((0, 0, 1), R(1))], coeffring=Q)
        self.gz = Polynomial([((0, 1, 1), R(1)), ((1, 0, 1), R(-1))], coeffring=Q)
        self.g = Polynomial([((0, 0, 1), R(1))], coeffring=Q)

    def testTwoVar(self):
        self.assertEqual(1, len(self.f1.gcd(self.f2)))
        self.assertEqual(self.f4, self.f3.gcd(self.f4))

    def testThreeVar(self):
        self.assertEqual(self.g, self.fz.gcd(self.gz))


class PrepareIndeterinateTest(unittest.TestCase):
    def testXYZ(self):
        ctx = {}
        multiutil.prepare_indeterinates("S T X Y", ctx)
        self.assert_("X" in ctx)
        for var in ctx:
            exec "%s = ctx['%s']" % (var, var)
        self.assert_(S)
        self.assert_(T)
        Z = rational.theIntegerRing
        XY = multiutil.polynomial({(0, 0, 1, 1): 1}, Z)
        self.assertEqual(XY, X * Y)


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
