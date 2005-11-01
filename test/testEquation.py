from __future__ import division
import unittest
import nzmath.equation as equation

class GlobalEquationTest (unittest.TestCase):
    def test_e1(self):
        self.assertEqual(-3/2, equation.e1([3, 2]))

    def test_e3(self):
        solutions = equation.e3([1, 0, 0, 1])
        for t in solutions:
            self.assertAlmostEqual(0, abs(t**3 + 1))
        solutions = equation.e3([-6, 11, -6, 1])
        for t in solutions:
            self.assertAlmostEqual(0, abs(((t - 6)*t + 11)*t - 6))
        solutions = equation.e3([-1, -1, 1, 1])
        for t in solutions:
            self.assertAlmostEqual(0, abs(((t + 1)*t - 1)*t - 1))
        solutions = equation.e3([-0.5, 0.5, 0.5, 1])
        for t in solutions:
            self.assertAlmostEqual(0, abs(((t + 0.5)*t + 0.5)*t - 0.5))
        solutions = equation.e3([-0.5j, 0.5, 0.5, 1])
        for t in solutions:
            self.assertAlmostEqual(0, abs(((t + 0.5)*t + 0.5)*t - 0.5j))


class LocalEquationTest (unittest.TestCase):
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
    runner = unittest.TextTestRunner()
    runner.run(suite())
