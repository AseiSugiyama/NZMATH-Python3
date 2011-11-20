from __future__ import generators
import unittest
import logging
import nzmath.prime as prime

logging.basicConfig()

class PrimeTest(unittest.TestCase):
    def testPrimeqComposite(self):
        self.assertFalse(prime.primeq(1))
        self.assertFalse(prime.primeq(2 ** 2))
        self.assertFalse(prime.primeq(2 * 7))
        self.assertFalse(prime.primeq(3 * 5))
        self.assertFalse(prime.primeq(11 * 31))
        self.assertFalse(prime.primeq(1111111111111111111 * 11111111111111111111111))

    def testPrimeqPrime(self):
        self.assertTrue(prime.primeq(2))
        self.assertTrue(prime.primeq(3))
        self.assertTrue(prime.primeq(23))
        self.assertTrue(prime.primeq(1662803))
        self.assertTrue(prime.primeq(1111111111111111111))
##         assert prime.primeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testBigprimeq(self):
        self.assertTrue(prime.bigprimeq(1111111111111111111))
##         assert prime.bigprimeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testMuller(self):
        self.assertTrue(prime.miller(1111111111111111111))
        self.assertFalse(prime.miller(11111111111111111111111111111))

    def testAPR(self):
        # User Request item #3418110
        self.assertTrue(prime.apr(37))
        self.assertTrue(prime.apr(619))

    def testByPrimitiveRoot(self):
        self.assertTrue(prime.by_primitive_root(2, []))
        self.assertTrue(prime.by_primitive_root(3, [2]))
        self.assertTrue(prime.by_primitive_root(7, [2, 3]))
        self.assertTrue(prime.by_primitive_root(31, [2, 3, 5]))
        self.assertFalse(prime.by_primitive_root(91, [2, 3, 5]))
        self.assertFalse(prime.by_primitive_root(341, [2, 5, 17]))
        self.assertFalse(prime.by_primitive_root(561, [2, 5, 7]))

    def testFullEuler(self):
        self.assertTrue(prime.full_euler(2, []))
        self.assertTrue(prime.full_euler(3, [2]))
        self.assertTrue(prime.full_euler(7, [2, 3]))
        self.assertTrue(prime.full_euler(31, [2, 3, 5]))
        self.assertFalse(prime.full_euler(91, [2, 3, 5]))
        self.assertFalse(prime.full_euler(341, [2, 5, 17]))
        self.assertFalse(prime.full_euler(561, [2, 5, 7]))

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
        self.assertTrue(prime.trialDivision(3))
        self.assertTrue(prime.trialDivision(23))
        self.assertFalse(prime.trialDivision(7 * 13))
        self.assertTrue(prime.trialDivision(97))
        self.assertFalse(prime.trialDivision(11 * 13))

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
            self.assertTrue(10**(n-1) < p < 10**n)
            self.assertTrue(prime.smallSpsp(p)) # primeq is too heavy..
        self.assertTrue(prime.randPrime(1) in (2, 3, 5, 7))


class SpspTest(unittest.TestCase):
    def testSpsp2args(self):
        self.assertTrue(prime.spsp(41, 2))
        self.assertTrue(prime.spsp(4999, 2))
        # composites
        self.assertFalse(prime.spsp(323, 2))
        self.assertFalse(prime.spsp(341, 2))
        # this number is a strong pseudoprime for base 2,3,5,...,31
        spsp31 = 1195068768795265792518361315725116351898245581
        self.assertTrue(all(prime.spsp(spsp31, p) for p in
                            (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)))
        self.assertFalse(prime.spsp(spsp31, 37))

    def testSpsp4args(self):
        self.assertTrue(prime.spsp(41, 2, 3, 5))
        self.assertTrue(prime.spsp(4999, 2, 1, 2499))
        # composites
        self.assertFalse(prime.spsp(323, 2, 1, 161))
        self.assertFalse(prime.spsp(341, 2, 2, 85))
        # this number is a strong pseudoprime for base 2,3,5,...,31
        spsp31 = 1195068768795265792518361315725116351898245581
        oddfactor = 298767192198816448129590328931279087974561395
        self.assertTrue(all(prime.spsp(spsp31, p, 2, oddfactor) for p in
                            (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)))
        self.assertFalse(prime.spsp(spsp31, 37, 2, oddfactor))

    def testSmallSpsp1arg(self):
        self.assertTrue(prime.smallSpsp(41))
        self.assertTrue(prime.smallSpsp(4999))
        # composites
        self.assertFalse(prime.smallSpsp(323))
        self.assertFalse(prime.smallSpsp(341))
        # this number is a strong pseudoprime for base 2,3,5,...,31
        spsp31 = 1195068768795265792518361315725116351898245581
        self.assertFalse(prime.smallSpsp(spsp31))

    def testSmallSpsp3args(self):
        self.assertTrue(prime.smallSpsp(41, 3, 5))
        self.assertTrue(prime.smallSpsp(4999, 1, 2499))
        # composites
        self.assertFalse(prime.smallSpsp(323, 1, 161))
        self.assertFalse(prime.smallSpsp(341, 2, 85))
        # this number is a strong pseudoprime for base 2,3,5,...,31
        spsp31 = 1195068768795265792518361315725116351898245581
        oddfactor = 298767192198816448129590328931279087974561395
        self.assertFalse(prime.smallSpsp(spsp31, 2, oddfactor))


class LpspTest (unittest.TestCase):
    def testLucasTestForPrime(self):
        self.assertTrue(prime.lpsp(101, 2, 3))

    def testLucasTestForPseudoPrime(self):
        # Lucas but not Frobenius example
        self.assertTrue(prime.lpsp(323, 1, -1))
        # Frobenius pseudoprime
        self.assertTrue(prime.lpsp(4181, 1, -1))
        self.assertTrue(prime.lpsp(5777, 1, -1))

    def testLucasTestForDetectedComposite(self):
        self.assertFalse(prime.lpsp(4187, 1, -1))


class FpspTest (unittest.TestCase):
    def testFrobeniusTestForPrime(self):
        self.assertTrue(prime.fpsp(101, 2, 3))

    def testFrobeniusTestForPseudoPrime(self):
        # Prime Numbers example
        self.assertTrue(prime.fpsp(4181, 1, -1)) # smallest
        self.assertTrue(prime.fpsp(5777, 1, -1))
        # Shinohara's example
        self.assertTrue(prime.fpsp(291409, 3, 8))

    def testFrobeniusTestForDetectedComposite(self):
        # not Lucas => not Frobenius
        self.assertFalse(prime.fpsp(4187, 1, -1))
        # Lucas pseudoprime but not Frobenius pseudoprime
        self.assertFalse(prime.fpsp(323, 1, -1))


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
