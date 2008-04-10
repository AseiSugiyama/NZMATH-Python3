from __future__ import division
import unittest
import nzmath.ring as ring
import nzmath.rational as rational
import nzmath.finitefield as finitefield
import nzmath.poly.termorder as termorder
import nzmath.poly.univar as univar
import nzmath.poly.uniutil as uniutil


class DivisionProviderTest (unittest.TestCase):
    """
    use DivisionProvider
    """
    def setUp(self):
        """
	define a class using DivisionProvider
	"""
        class BasicPolynomialWithDivision (univar.BasicPolynomial,
                                           uniutil.OrderProvider,
                                           uniutil.DivisionProvider):
            def __init__(self, coefficients, **kwds):
                univar.BasicPolynomial.__init__(self, coefficients, **kwds)
                uniutil.OrderProvider.__init__(self, termorder.ascending_order)
                uniutil.DivisionProvider.__init__(self)

        self.f = BasicPolynomialWithDivision([(0, 1.0), (3, 1.0), (1, 2.0)])
        self.g = BasicPolynomialWithDivision([(0, 1.0), (1, 1.0)])
        Q = rational.Rational
        self.h = BasicPolynomialWithDivision([(0, Q(1)), (3, Q(1)), (1, Q(2))])
        self.i = BasicPolynomialWithDivision([(0, Q(1)), (1, Q(1))])

    def testDivision(self):
        """
	divisions
	"""
        self.assertEqual("RationalFunction", (self.f / self.g).__class__.__name__)
        self.assert_(self.f % self.g)

    def testGcd(self):
        one = univar.BasicPolynomial({0: rational.Rational(1)})
        self.assertEqual(one, self.h.gcd(self.i))


class ContentProviderTest (unittest.TestCase):
    """
    use ContentProvider
    """
    def setUp(self):
        """
	define a class using ContentProvider
	"""
        class PolynomialWithContent (univar.SortedPolynomial,
                                     uniutil.OrderProvider,
                                     uniutil.DivisionProvider,
                                     uniutil.ContentProvider):
            def __init__(self, coefficients, **kwds):
                univar.SortedPolynomial.__init__(self, coefficients, **kwds)
                uniutil.OrderProvider.__init__(self, termorder.ascending_order)
                uniutil.DivisionProvider.__init__(self)

        Q = rational.Rational
        self.f = PolynomialWithContent([(0, Q(1)), (3, Q(2)), (1, Q(1, 2))])
        self.g = PolynomialWithContent([(0, Q(8)), (3, Q(2)), (1, Q(2, 3))])

    def testContent(self):
        Q = rational.Rational
        self.assertEqual(Q(1, 2), self.f.content())
        self.assertEqual(Q(2, 3), self.g.content())

    def testPrimitivePart(self):
        Q = rational.Rational
        h = self.g.scalar_mul(Q(3, 2))
        self.assertEqual(self.f * 2, self.f.primitive_part())
        self.assertEqual(h, self.g.primitive_part())


class PrimeCharacteristicFunctionsProviderTest (unittest.TestCase):
    def setUp(self):
        """
	define a class using ContentProvider
	"""
        self.F2 = F2 = finitefield.FinitePrimeField.getInstance(2)
        self.F5 = F5 = finitefield.FinitePrimeField.getInstance(5)
        self.f = uniutil.FinitePrimeFieldPolynomial([(0, F2.one), (3, F2.one), (1, F2.one)], coeffring=F2)
        self.g = uniutil.FinitePrimeFieldPolynomial([(0, F2.one), (2, F2.one)], coeffring=F2)
        self.h = uniutil.FinitePrimeFieldPolynomial([(1, F2.one), (2, F2.one)], coeffring=F2)
        self.p = uniutil.FinitePrimeFieldPolynomial([(0, F5.one), (1, F5.createElement(2)), (2, F5.createElement(3)), (5, F5.createElement(3)), (6, F5.createElement(2)), (7, F5.one)], coeffring=F5)
        self.q = uniutil.FinitePrimeFieldPolynomial([(0, self.F2.one), (1, self.F2.one), (2, self.F2.one)], coeffring=F2) * self.h
        self.thirty = uniutil.FinitePrimeFieldPolynomial([(0, self.F2.one), (3, self.F2.one), (30, self.F2.one)], coeffring=F2)

    def testSquareFreeDecomposition(self):
        g_decomp = self.g.squarefree_decomposition()
        self.assertEqual(1, len(g_decomp))
        self.assertEqual(2, g_decomp.keys()[0])
        h_decomp = self.h.squarefree_decomposition()
        self.assertEqual(1, len(h_decomp))
        self.assertEqual(1, h_decomp.keys()[0])
        self.assertEqual(self.h, h_decomp.values()[0], str(h_decomp.items()[0]))
        self.assert_(self.thirty.gcd(self.thirty.differentiate()))

    def testDistinctDegreeFactorization(self):
        h_ddf = self.h.distinct_degree_factorization()
        self.assertEqual(1, len(h_ddf))
        q_ddf = self.q.distinct_degree_factorization()
        self.assertEqual(2, len(q_ddf))

    def testSplitSameDegrees(self):
        h_ssd = self.h.split_same_degrees(1)
        self.assertEqual(self.h.degree(), len(h_ssd))

    def testFactor(self):
        factored = self.p.factor()
        self.assert_(isinstance(factored, list))
        self.assertEqual(3, len(factored))
        for factor in factored:
            self.assert_(isinstance(factor, tuple))
            self.assertEqual(2, len(factor))
            self.assert_(isinstance(factor[1], (int,long)))
        product = self.p.__class__([(0, ring.getRing(self.p.itercoefficients().next()).one)], coeffring=self.p.getCoefficientRing())
        for factor, index in factored:
            product = product * factor ** index
        self.assertEqual(self.p, product)

        # F2 case
        g_factor = self.g.factor()
        self.assertEqual(1, len(g_factor), g_factor)
        self.assertEqual(2, g_factor[0][1])
        h_factor = self.h.factor()
        self.assertEqual(2, len(h_factor), h_factor)

    def testRamify(self):
        F3 = F3 = finitefield.FinitePrimeField.getInstance(3)
        rami = uniutil.FinitePrimeFieldPolynomial([(0, F3.one), (2, F3.zero), (3, F3.one)], coeffring=F3)
        r_factor = rami.factor()
        self.assertEqual(1, len(r_factor), r_factor)
        r_factor = r_factor[0]
        self.assertEqual(3, r_factor[1])
        self.assertEqual(rami, r_factor[0] ** 3)

    def testIsIrreducible(self):
        self.assert_(self.f.isirreducible())
        self.failIf(self.g.isirreducible())
        self.failIf(self.h.isirreducible())


class SubresultantGcdProviderTest (unittest.TestCase):
    def setUp(self):
        """
	define a class using DivisionProvider
	"""
        R = rational.Rational
        Q = rational.theRationalField
        self.up1 = up1 = uniutil.polynomial([(1, R(1))], coeffring=Q)
        self.u = uniutil.polynomial([(0, up1), (3, up1)], up1.getRing())
        self.v = uniutil.polynomial([(0, -up1)], up1.getRing())

    def testSubResultantGcd(self):
        self.assertEqual(self.up1, self.up1.gcd(self.up1 * self.up1))
        self.assertEqual(-self.v, self.u.subresultant_gcd(self.v))

    def testResultant(self):
        Z = rational.theIntegerRing
        I = rational.Integer
        f = uniutil.polynomial(enumerate(map(I, range(5))), coeffring=Z)
        g = uniutil.polynomial(enumerate(map(I, range(7, 10))), coeffring=Z)
        self.assertEqual(0, f.resultant(f * g))
        h1 = uniutil.polynomial(enumerate(map(I, [-2, 0, 0, 1])), coeffring=Z)
        h2 = uniutil.polynomial(enumerate([Z.zero, Z.one]), coeffring=Z)
        self.assertEqual(2, h1.resultant(h2))
        t = uniutil.polynomial(enumerate(map(I, range(7, 0, -1))), coeffring=Z)
        self.assertEqual(2**16 * 7**4, t.resultant(t.differentiate()))


class IntegerPolynomialTest (unittest.TestCase):
    def testExactDivision(self):
        # sf bug #1922158
        f = uniutil.OneVariableDensePolynomial([0, 9], 'x')
        g = uniutil.OneVariableDensePolynomial([0, 3], 'x')
        q = uniutil.polynomial([(0, 3)], rational.theIntegerRing)
        self.assertEqual(q, f.exact_division(g))

    def testResultant(self):
        Z = rational.theIntegerRing
        f = uniutil.polynomial(enumerate(range(1, 6)), Z)
        g = uniutil.polynomial(enumerate(range(7, 10)), Z)
        self.assertEqual(29661, f.resultant(g))

    def testDiscriminant(self):
        Z = rational.theIntegerRing
        a, b, c = -2, -1, 1
        q1 = uniutil.polynomial(enumerate([c, b, a]), Z)
        d = b ** 2 - 4 * a * c
        self.assertEqual(d, q1.discriminant())

    def testAddition(self):
        Z = rational.theIntegerRing
        f = uniutil.polynomial(enumerate(range(1, 6)), Z)
        g = uniutil.polynomial(enumerate(range(7, 10)), Z)
        h = uniutil.polynomial(enumerate([8, 10, 12, 4, 5]), Z)
        self.assertEqual(h, f + g)
        self.assert_(isinstance(f + g, uniutil.IntegerPolynomial))
        # sf bug # 1937925
        f2 = uniutil.polynomial(enumerate([2, 2, 3, 4, 5]), Z)
        self.assertEqual(f2, f + 1)
        self.assertEqual(f2, 1 + f)

    def testSubtraction(self):
        Z = rational.theIntegerRing
        f = uniutil.polynomial(enumerate(range(1, 6)), Z)
        # sf bug # 1937925
        f2 = uniutil.polynomial([(1, 2), (2, 3), (3, 4), (4, 5)], Z)
        self.assertEqual(f2, f - 1)
        self.assertEqual(-f2, 1 - f)


class FinitePrimeFieldPolynomialTest (unittest.TestCase):
    def testRepr(self):
        f = uniutil.FinitePrimeFieldPolynomial([(0, 2), (8, 1)], coeffring=finitefield.FinitePrimeField.getInstance(311))
        self.assertEqual(0, repr(f).index("Finite"))

    def testMod(self):
        f = uniutil.FinitePrimeFieldPolynomial([(0, 1), (3, 1), (30, 1)], coeffring=finitefield.FinitePrimeField.getInstance(2))
        df = f.differentiate()
        self.assert_(f % df)

    def testDiscriminant(self):
        F7 = finitefield.FinitePrimeField.getInstance(7)
        a, b, c = 2, 5, 1
        q1 = uniutil.polynomial(enumerate([c, b, a]), coeffring=F7)
        d = F7.createElement(b ** 2 - 4 * a * c)
        self.assertEqual(d, q1.discriminant())


class InjectVariableTest (unittest.TestCase):
    def testInject(self):
        f = univar.SortedPolynomial([(0, 1), (1, 3), (2, 2)])
        X = "X"
        self.assert_(uniutil.VariableProvider not in f.__class__.__bases__)
        uniutil.inject_variable(f, X)
        self.assertEqual(X, f.getVariable())
        self.assertEqual([X], f.getVariableList())
        self.assert_(uniutil.VariableProvider in f.__class__.__bases__)
        self.assertEqual("VarSortedPolynomial", f.__class__.__name__)
        f += f
        self.assertEqual("VarSortedPolynomial", f.__class__.__name__)
        # varname lost
        self.assert_(hasattr(f, "getVariable"))
        self.assertRaises(AttributeError, f.getVariable)


class PolynomialRingAnonymousVariableTest (unittest.TestCase):
    def setUp(self):
        Z = rational.theIntegerRing
        self.zx = uniutil.PolynomialRingAnonymousVariable(Z)

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


class PolynomialIdealTest (unittest.TestCase):
    def setUp(self):
        self.Z = rational.theIntegerRing
        self.Q = rational.theRationalField
        self.zx = uniutil.PolynomialRingAnonymousVariable(self.Z)
        self.qx = uniutil.PolynomialRingAnonymousVariable(self.Q)

    def testNonzero(self):
        self.failIf(uniutil.PolynomialIdeal(self.Q.zero, self.qx))

    def testReduceFieldPolynomial(self):
        whole = uniutil.PolynomialIdeal(self.Q.one, self.qx)
        f = uniutil.polynomial([(1, self.Q.createElement(3, 4))], self.Q)
        self.failIf(whole.reduce(f))
        self.assert_(uniutil.PolynomialIdeal(f, self.qx).reduce(self.Q.one))

    def testReduceEuclideanPolynomial(self):
        whole = uniutil.PolynomialIdeal(-1, self.zx)
        f = uniutil.polynomial([(0, 3), (1, 2)], self.Z)
        f_ideal = uniutil.PolynomialIdeal(f, self.zx)
        self.failIf(whole.reduce(f))
        self.assert_(f_ideal.reduce(self.Z.one))

        two_generators = uniutil.PolynomialIdeal([f, self.zx.createElement(5)], self.zx)
        self.failIf(two_generators.reduce(f))
        self.assert_(two_generators.reduce(self.Z.one))

    def testNormalizeGenerators(self):
        f = uniutil.polynomial([(0, 3), (1, 2)], self.Z)
        i1 = uniutil.PolynomialIdeal([f, self.zx.createElement(5)], self.zx)
        i2 = uniutil.PolynomialIdeal([self.zx.createElement(5), f], self.zx)
        self.assertEqual(i1.generators, i2.generators)
        self.assertEqual(i1, i2)

    def testZeroIdeal(self):
        null = uniutil.PolynomialIdeal(self.zx.zero, self.zx)
        self.assert_(self.zx.zero in null)
        self.failIf(self.zx.one in null)


class FieldPolynomialTest (unittest.TestCase):
    def testDivision(self):
        Q = rational.theRationalField
        f = uniutil.FieldPolynomial([(1, 1)], Q)
        g = uniutil.FieldPolynomial([(1, 1)], Q)
        q = uniutil.FieldPolynomial([(0, 1)], Q)
        self.assertEqual(q, f // g)
        self.assertEqual(f.getRing().zero, f % g)

    def testDiscriminant(self):
        Q = rational.theRationalField
        rat = rational.Rational
        a, b, c = rat(2, 7), rat(5, 14), rat(1, 7)
        q1 = uniutil.polynomial(enumerate([c, b, a]), Q)
        d = b ** 2 - 4 * a * c
        self.assertEqual(d, q1.discriminant())


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
