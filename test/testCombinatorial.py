import unittest
from combinatorial import binomial, factorial

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

    def testNegativeAndPositive(self):
        self.assertRaises(ValueError, binomial, -1, 2)

    def testPositiveAndNegative(self):
        self.assertRaises(ValueError, binomial, 2, -1)

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BinomialTest, 'test'))
    suite.addTest(unittest.makeSuite(FactorialTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
