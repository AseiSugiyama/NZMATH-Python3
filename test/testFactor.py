import unittest
import factor
import prime

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        assert factor.trialDivision(60) == [(2,2),(3,1),(5,1)]
        assert factor.trialDivision(128) == [(2,7)]
        assert factor.trialDivision(200819) == [(409,1),(491,1)]
        assert factor.trialDivision(1042387) ==  [(701,1),(1487,1)]
    def testPMinusOneMethod(self):
        assert [(19,1), (101,1)] == factor.pmom(1919)
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        assert [(p,1), (154858631,1)] == factor.pmom(p*154858631)

def suite():
    suite = unittest.makeSuite(FactorTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
