from __future__ import generators
import unittest
import prime

class PrimeTest(unittest.TestCase):
    def testComposite(self):
        assert not prime.primeq(1)
        assert not prime.primeq(2 ** 2)
        assert not prime.primeq(2 * 7)
        assert not prime.primeq(3 * 5)
        assert not prime.primeq(11 * 31)
        assert not prime.primeq(1111111111111111111 * 11111111111111111111111)

    def testPrime(self):
        assert prime.primeq(2)
        assert prime.primeq(3)
        assert prime.primeq(1111111111111111111)
        assert prime.primeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testBigprimeq(self):
        assert prime.bigprimeq(1111111111111111111)
        assert prime.bigprimeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testGenerator(self):
        g = prime.generator()
        assert 2 == g.next()
        assert 3 == g.next()
        g2 = prime.generator(lambda x: x % 5 == 4)
        assert 19 == g2.next()
        assert 29 == g2.next()

    def testTrialDivision(self):
        assert prime.trialDivision(2)
        assert prime.trialDivision(3)
        assert not prime.trialDivision(4)
        assert prime.trialDivision(5)
        assert not prime.trialDivision(91)
        assert prime.trialDivision(97)
        assert not prime.trialDivision(143)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PrimeTest("testComposite"))
    suite.addTest(PrimeTest("testBigprimeq"))
    suite.addTest(PrimeTest("testPrime"))
    suite.addTest(PrimeTest("testGenerator"))
    suite.addTest(PrimeTest("testTrialDivision"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
