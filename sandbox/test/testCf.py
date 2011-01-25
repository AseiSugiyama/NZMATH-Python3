import unittest
import itertools
import nzmath.rational as rational
import sandbox.cf as cf


class RegularContinuedFractionTest (unittest.TestCase):
    def testInteger(self):
        self.assertEqual(1, cf.RegularContinuedFraction(iter([1])).convergent(0))
        # more than given length
        self.assertEqual(1, cf.RegularContinuedFraction(iter([1])).convergent(100))

    def testSqrt(self):
        # sqrt(2) = [1; 2, 2, ...]
        sqrt2 = cf.RegularContinuedFraction(itertools.chain([1], itertools.cycle([2])))
        self.assertEqual(rational.Rational(17, 12), sqrt2.convergent(3))
        self.assertEqual(rational.Rational(41, 29), sqrt2.convergent(4))
        # convergent(smaller than previous call) == convergent(previous call)
        self.assertEqual(rational.Rational(41, 29), sqrt2.convergent(3))


class ExpandTest (unittest.TestCase):
    def testExpand(self):
        self.assertEqual([1, 2, 2], [e for e in cf.expand(rational.Rational(7, 5))])


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
