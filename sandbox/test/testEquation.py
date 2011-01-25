from __future__ import division
import unittest
import logging
import nzmath.equation as equation
from operator import mul
from nzmath.polynomial import OneVariableDensePolynomial


class GlobalEquationTestBase (unittest.TestCase):
    """
    Base class for global equation tests.
    """
    def assert_solve(self, method, coefficients):
        """
        assert that the given 'method' solves the algebraic equation
        f(X) = 0, where f is given by its 'coefficients'.
        """
        solutions = method(coefficients)
        f = OneVariableDensePolynomial(coefficients, "T")
        self.assert_roots(f, solutions)
        self.assert_roots_coefficients(solutions, coefficients)

    def assert_roots(self, polynomial, solutions):
        """
        assert that the given 'polynomial' has 'solutions' as its
        zeros.
        """
        for t in solutions:
            self.assertAlmostEqual(0, abs(polynomial(t)))

    def assert_roots_coefficients(self, solutions, coefficients):
        """
        assert that the given 'solutions' and 'coefficients' satisfies
        the relations between roots and coefficients.

        limitation: only norm and trace are tested, now.
        """
        # norm
        degree = len(coefficients) - 1
        self.assertAlmostEqual(0, abs((-1)**degree*coefficients[0] - reduce(mul, solutions, 1)))
        # trace
        self.assertAlmostEqual(0, abs(-coefficients[-2] - sum(solutions)))


class GlobalEquationTest (GlobalEquationTestBase):
    def test_e1(self):
        self.assertEqual(-3/2, equation.e1([3, 2]))

    def test_e3(self):
        self.assert_solve(equation.e3, [1, 0, 0, 1])
        self.assert_solve(equation.e3, [-6, 11, -6, 1])
        self.assert_solve(equation.e3, [-1, -1, 1, 1])
        self.assert_solve(equation.e3, [-0.5, 0.5, 0.5, 1])
        self.assert_solve(equation.e3, [-0.5j, 0.5, 0.5, 1])


class SimMethodTest (GlobalEquationTestBase):
    def test_degree3(self):
        self.assert_solve(equation.SimMethod, [1, 0, 0, 1])
        self.assert_solve(equation.SimMethod, [-2, 0, 0, 1])

    def test_degree4(self):
        self.assert_solve(equation.SimMethod, [-2, 0, 1, 0, 1])

    def test_degree5(self):
        self.assert_solve(equation.SimMethod, [-2, 1, 0, 0, 1, 1])

    def test_degree6(self):
        # example from H.Cohen's book p.169 (Olivier's example)
        self.assert_solve(equation.SimMethod, [4, 17, 10, -12, -7, 2, 1])

class SimMethodPluginTest (GlobalEquationTestBase):
    def setUp(selt):
        from sandbox.plugins import SETPRECISION
        SETPRECISION(200)

    def tearDown(self):
        from sandbox.plugins import SETPRECISION
        SETPRECISION(53)

    def test_degree3(self):
        self.assert_solve(equation.SimMethod, [1, 0, 0, 1])
        self.assert_solve(equation.SimMethod, [-2, 0, 0, 1])

    def test_degree4(self):
        self.assert_solve(equation.SimMethod, [-2, 0, 1, 0, 1])

    def test_degree5(self):
        self.assert_solve(equation.SimMethod, [-2, 1, 0, 0, 1, 1])

    def test_degree6(self):
        # example from H.Cohen's book p.169 (Olivier's example)
        self.assert_solve(equation.SimMethod, [4, 17, 10, -12, -7, 2, 1])


class LocalEquationTest (unittest.TestCase):
    def test_e1_ZnZ(self):
        solution = equation.e1_ZnZ([1, 3], 7) # 1 + 3*t = 0 (mod 7)
        self.assertEqual(2, solution)
        self.assertRaises(ValueError, equation.e1_ZnZ, [1, 6], 12)

    def test_e2_Fp(self):
        # mod 2
        solutions = equation.e2_Fp([0, 1, 1], 2) # single roots
        self.assertEqual(2, len(solutions))
        for s in solutions:
            self.assertEqual(0, (s + s**2) % 2)
        solutions = equation.e2_Fp([1, 0, 1], 2)
        self.assertEqual(2, len(solutions)) # a double root
        for s in solutions:
            self.assertEqual(0, (1 + s**2) % 2)
        solutions = equation.e2_Fp([1, 1, 1], 2)
        self.assertEqual(0, len(solutions)) # no roots
        # mod 5
        solutions = equation.e2_Fp([1, 0, 1], 5)
        self.assertEqual(2, len(solutions))
        for s in solutions:
            self.assertEqual(0, (1 + s**2) % 5)
        solutions = equation.e2_Fp([2, 0, 3], 5)
        self.assertEqual(2, len(solutions))
        for s in solutions:
            self.assertEqual(0, (2 + 3*s**2) % 5)

    def test_e2_Fp_degenerate(self):
        solutions = equation.e2_Fp([1, 3, 7], 7)
        self.assertEqual(1, len(solutions))
        self.assertEqual(2, solutions[0])

    def test_e3_Fp(self):
        solutions = equation.e3_Fp([2, 0, 0, 1], 43)
        for s in solutions:
            self.assertEqual(0, (2 + s**3) % 43)
        thesolutions = [9, 11, 23]
        self.assertEquals(len(thesolutions), len(solutions))
        for s in thesolutions:
            self.assert_(s in solutions)


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
