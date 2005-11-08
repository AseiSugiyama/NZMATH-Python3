import unittest
import doctest
import nzmath.combinatorial as combinatorial

# for short
binomial = combinatorial.binomial
factorial = combinatorial.factorial
bernoulli = combinatorial.bernoulli
catalan = combinatorial.catalan


class BinomialTest (unittest.TestCase):
    def testPositiveAndPositive(self):
        assert 1 == binomial(1,1)
        assert 2 == binomial(2,1)
        assert 6 == binomial(4,2)
        assert 2000 == binomial(2000, 1999)
        assert 0 == binomial(1999, 2000)

    def testZero(self):
        assert 1 == binomial(0,0)
        assert 1 == binomial(1111111111111111111111111111111111111111111, 0)
        self.assertRaises(ValueError, binomial, 0, 3)
        self.assertRaises(ValueError, binomial, -1, 0)

    def testNegativeAndPositive(self):
        self.assertRaises(ValueError, binomial, -1, 2)

    def testPositiveAndNegative(self):
        self.assertRaises(ValueError, binomial, 2, -1)

    def testNegativeAndNegative(self):
        self.assertRaises(ValueError, binomial, -2, -3)
        self.assertRaises(ValueError, binomial, -1, -1)

    def testNonInteger(self):
        self.assertRaises(TypeError, binomial, 1.8, 1)
        self.assertRaises(TypeError, binomial, 1, 1.8)


class FactorialTest (unittest.TestCase):
    def testPositive(self):
        assert 1 == factorial(1)
        assert 2 == factorial(2)
        assert 6 == factorial(3)
        assert 24 == factorial(4)

    def testZero(self):
        assert 1 == factorial(0)

    def testError(self):
        self.assertRaises(TypeError, factorial, 1.5)
        self.assertRaises(ValueError, factorial, -1)


class BernoulliTest (unittest.TestCase):
    def testZero(self):
        assert 1 == bernoulli(0)

    def testOdd(self):
        import nzmath.rational as rational
        assert rational.Rational(-1, 2) == bernoulli(1)
        assert 0 == bernoulli(3)
        assert 0 == bernoulli(101)
        assert 0 == bernoulli(1010111111111111777979797979794555)

    def testEven(self):
        import nzmath.rational as rational
        assert rational.Rational(1, 6) == bernoulli(2)
        assert rational.Rational(-1, 30) == bernoulli(4)
        assert rational.Rational(1, 42) == bernoulli(6)


class CatalanTest (unittest.TestCase):
    def testNormal(self):
        assert [1, 1, 2, 5, 14] == [catalan(i) for i in range(5)]


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    # doctest for combinationIndexGenerator
    suite.addTest(doctest.DocTestSuite(combinatorial))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
