from __future__ import generators
import unittest
import prime

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

    def testSqrt(self):
        assert prime.sqrt(2**60 - 1) ** 2 <= 2**60 - 1
        assert prime.sqrt(2**59 - 1) ** 2 <= 2**59 - 1
        assert prime.sqrt(10) == 3
        assert prime.sqrt(4) == 2

def suite():
    suite = unittest.makeSuite(PrimeTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
