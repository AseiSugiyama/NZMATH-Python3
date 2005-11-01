import unittest
import nzmath.factor as factor
import nzmath.prime as prime

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        assert factor.trialDivision(60) == [(2,2),(3,1),(5,1)]
        assert factor.trialDivision(128) == [(2,7)]
        assert factor.trialDivision(200819) == [(409,1),(491,1)]
        assert factor.trialDivision(1042387) ==  [(701,1),(1487,1)]

    def testRho(self):
        m = "rhomethod sometimes fails to factor anyway."
        self.assertEqual([(2,2),(3,1),(5,1)], factor.rhomethod(60), m)
        self.assertEqual([(2,7)], factor.rhomethod(128), m)
        self.assertEqual([(409,1),(491,1)], factor.rhomethod(200819), m)
        self.assertEqual([(701,1),(1487,1)], factor.rhomethod(1042387), m)
        self.assertEqual([(17,2), (19,1)], factor.rhomethod(17**2 * 19), m)

    def testPMinusOneMethod(self):
        self.assertEqual([(19,1), (101,1)], factor.pmom(1919))
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        self.assertEqual([(p,1), (154858631,1)], factor.pmom(p*154858631))

    def testMPQS(self):
        p = 4 * 6133 + 1
        result = factor.mpqs(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)

    def testPrimeDivisors(self):
        self.assertEqual([3, 5], factor.primeDivisors(15))

    def testSquarePart(self):
        self.assertEqual(1, factor.squarePart(15))
        self.assertEqual(17, factor.squarePart(17**2 * 19))

    def testAllDivisors(self):
        self.assertEqual([1], factor.AllDivisors(1))
        self.assertEqual([1, 2], factor.AllDivisors(2))
        self.assertEqual([1, 2, 4], factor.AllDivisors(4))
        self.assertEqual([1, 2, 3, 6], factor.AllDivisors(6))
        self.assertEqual([1, 2, 3, 4, 6, 12], factor.AllDivisors(12))
        self.assertEqual([1, 2, 3, 5, 6, 10, 15, 30], factor.AllDivisors(30))

    def testPrimePowerTest(self):
        # not a power
        self.assertEqual((12, 0), factor.PrimePowerTest(12))
        self.assertEqual((53, 1), factor.PrimePowerTest(53))
        # powers
        self.assertEqual((7, 2), factor.PrimePowerTest(49))
        self.assertEqual((3, 4), factor.PrimePowerTest(81))
        self.assertEqual((5, 3), factor.PrimePowerTest(125))
        self.assertEqual((2, 7), factor.PrimePowerTest(128))

def suite():
    suite = unittest.makeSuite(FactorTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
