from __future__ import generators
import unittest
import logging
import nzmath.prime as prime

logging.basicConfig()

class PrimeTest(unittest.TestCase):
    def testPrimeqComposite(self):
        assert not prime.primeq(1)
        assert not prime.primeq(2 ** 2)
        assert not prime.primeq(2 * 7)
        assert not prime.primeq(3 * 5)
        assert not prime.primeq(11 * 31)
        assert not prime.primeq(1111111111111111111 * 11111111111111111111111)

    def testPrimeqPrime(self):
        assert prime.primeq(2)
        assert prime.primeq(3)
        assert prime.primeq(23)
        assert prime.primeq(1662803)
        assert prime.primeq(1111111111111111111)
##         assert prime.primeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testBigprimeq(self):
        assert prime.bigprimeq(1111111111111111111)
##         assert prime.bigprimeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testGenerator(self):
        g = prime.generator()
        assert 2 == g.next()
        assert 3 == g.next()
##         g2 = prime.generator(lambda x: x % 5 == 4) # old fashioned
        import itertools
        g2 = itertools.ifilter(lambda x: x % 5 == 4, prime.generator())
        assert 19 == g2.next()
        assert 29 == g2.next()

    def testTrialDivision(self):
        assert prime.trialDivision(3)
        assert prime.trialDivision(23)
        assert not prime.trialDivision(7 * 13)
        assert prime.trialDivision(97)
        assert not prime.trialDivision(11 * 13)

    def testPrime(self):
        assert prime.prime(100) == 541

    def testNextPrime(self):
        assert prime.nextPrime(0) == 2
        assert prime.nextPrime(2) == 3
        assert prime.nextPrime(541) == 547
        assert prime.nextPrime(542) == 547

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


class LpspTest (unittest.TestCase):
    def testLucasTestForPrime(self):
        self.assert_(prime.lpsp(101, 2, 3))

    def testLucasTestForPseudoPrime(self):
        # Lucas but not Frobenius example
        self.assert_(prime.lpsp(4187, 1, -1))
        # Frobenius pseudoprime
        self.assert_(prime.lpsp(5777, 1, -1))

    def testLucasTestForDetectedComposite(self):
        self.failIf(prime.lpsp(4181, 1, -1))


class FpspTest (unittest.TestCase):
    def testFrobeniusTestForPrime(self):
        self.assert_(prime.fpsp(101, 2, 3))

    def testFrobeniusTestForPseudoPrime(self):
        # the smallest example with the parameter
        self.assert_(prime.fpsp(5777, 1, -1))
        # Shinohara's example
        self.assert_(prime.fpsp(291409, 3, 8))

    def testFrobeniusTestForDetectedComposite(self):
        # not Lucas => not Frobenius
        self.failIf(prime.fpsp(4181, 1, -1))
        # Lucas pseudoprime but not Frobenius pseudoprime
        self.failIf(prime.fpsp(4187, 1, -1))


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
