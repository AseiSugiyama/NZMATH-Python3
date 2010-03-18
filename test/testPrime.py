from __future__ import generators
import unittest
import logging
import nzmath.prime as prime

logging.basicConfig()

class PrimeTest(unittest.TestCase):
    def testPrimeqComposite(self):
        self.failIf(prime.primeq(1))
        self.failIf(prime.primeq(2 ** 2))
        self.failIf(prime.primeq(2 * 7))
        self.failIf(prime.primeq(3 * 5))
        self.failIf(prime.primeq(11 * 31))
        self.failIf(prime.primeq(1111111111111111111 * 11111111111111111111111))

    def testPrimeqPrime(self):
        self.assert_(prime.primeq(2))
        self.assert_(prime.primeq(3))
        self.assert_(prime.primeq(23))
        self.assert_(prime.primeq(1662803))
        self.assert_(prime.primeq(1111111111111111111))
##         assert prime.primeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testBigprimeq(self):
        self.assert_(prime.bigprimeq(1111111111111111111))
##         assert prime.bigprimeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testMuller(self):
	self.assert_(prime.miller(1111111111111111111))
	self.failIf(prime.miller(11111111111111111111111111111))

    def testGenerator(self):
        g = prime.generator()
        self.assertEqual(2, g.next())
        self.assertEqual(3, g.next())
##         g2 = prime.generator(lambda x: x % 5 == 4) # old fashioned
        import itertools
        g2 = itertools.ifilter(lambda x: x % 5 == 4, prime.generator())
        self.assertEqual(19, g2.next())
        self.assertEqual(29, g2.next())

    def testTrialDivision(self):
        self.assert_(prime.trialDivision(3))
        self.assert_(prime.trialDivision(23))
        self.failIf(prime.trialDivision(7 * 13))
        self.assert_(prime.trialDivision(97))
        self.failIf(prime.trialDivision(11 * 13))

    def testPrime(self):
        self.assertEqual(541, prime.prime(100))

    def testNextPrime(self):
        self.assertEqual(2, prime.nextPrime(0))
        self.assertEqual(3, prime.nextPrime(2))
        self.assertEqual(547, prime.nextPrime(541))
        self.assertEqual(547, prime.nextPrime(542))

    def testGeneratorEratosthenes(self):
        g = prime.generator_eratosthenes(3)
        self.assertEqual(2, g.next())
        self.assertEqual(3, g.next())
        self.assertRaises(StopIteration, g.next)
        g = prime.generator_eratosthenes(541)
        self.assertEqual(100, len([p for p in g]))

    def testRandPrime(self):
        for n in range(3, 52, 6):
            p = prime.randPrime(n)
            self.assert_(10**(n-1) < p < 10**n)
            self.assert_(prime.smallSpsp(p)) # primeq is too heavy..
        self.assert_(prime.randPrime(1) in (2, 3, 5, 7))


class LpspTest (unittest.TestCase):
    def testLucasTestForPrime(self):
        self.assert_(prime.lpsp(101, 2, 3))

    def testLucasTestForPseudoPrime(self):
        # Lucas but not Frobenius example
        self.assert_(prime.lpsp(323, 1, -1))
        # Frobenius pseudoprime
        self.assert_(prime.lpsp(4181, 1, -1))
        self.assert_(prime.lpsp(5777, 1, -1))

    def testLucasTestForDetectedComposite(self):
        self.failIf(prime.lpsp(4187, 1, -1))


class FpspTest (unittest.TestCase):
    def testFrobeniusTestForPrime(self):
        self.assert_(prime.fpsp(101, 2, 3))

    def testFrobeniusTestForPseudoPrime(self):
        # Prime Numbers example
        self.assert_(prime.fpsp(4181, 1, -1)) # smallest
        self.assert_(prime.fpsp(5777, 1, -1))
        # Shinohara's example
        self.assert_(prime.fpsp(291409, 3, 8))

    def testFrobeniusTestForDetectedComposite(self):
        # not Lucas => not Frobenius
        self.failIf(prime.fpsp(4187, 1, -1))
        # Lucas pseudoprime but not Frobenius pseudoprime
        self.failIf(prime.fpsp(323, 1, -1))


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
