import unittest
import factor
import prime

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        assert factor.trialDivision(60) == [(2,2),(3,1),(5,1)]
        assert factor.trialDivision(128) == [(2,7)]
        assert factor.trialDivision(200819) == [(409,1),(491,1)]
        assert factor.trialDivision(1042387) ==  [(701,1),(1487,1)]

    def testRho(self):
        assert factor.rhomethod(60) == [(2,2),(3,1),(5,1)]
        assert factor.rhomethod(128) == [(2,7)]
        assert factor.rhomethod(200819) == [(409,1),(491,1)]
        assert factor.rhomethod(1042387) ==  [(701,1),(1487,1)]

    def testPMinusOneMethod(self):
        assert [(19,1), (101,1)] == factor.pmom(1919)
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        assert [(p,1), (154858631,1)] == factor.pmom(p*154858631)

    def testMPQS(self):
        p = 4 * 6133 + 1
        result = factor.mpqs(p*154858631)
        assert [(p,1), (154858631,1)] == result

    def testPrimeDivisors(self):
        assert [3, 5] == factor.primeDivisors(15)

    def testSquarePart(self):
        assert 1 == factor.squarePart(15)
        assert 17 == factor.squarePart(17**2 * 19)

    def testAllDivisors(self):
        assert [1] == factor.AllDivisors(1)
        assert [1, 2] == factor.AllDivisors(2)
        assert [1, 2, 4] == factor.AllDivisors(4)
        assert [1, 2, 3, 6] == factor.AllDivisors(6)
        assert [1, 2, 3, 4, 6, 12] == factor.AllDivisors(12)
        assert [1, 2, 3, 5, 6, 10, 15, 30] == factor.AllDivisors(30)


def suite():
    suite = unittest.makeSuite(FactorTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
