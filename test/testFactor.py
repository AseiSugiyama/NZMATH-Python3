import unittest
import factor

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        assert factor.trialDivision(60) == [(2,2),(3,1),(5,1)]
        assert factor.trialDivision(128) == [(2,7)]
        assert factor.trialDivision(200819) == [(409,1),(491,1)]
        assert factor.trialDivision(1042387) ==  [(701,1),(1487,1)]
    def testPMinusOneMethod(self):
        assert [(19,1), (101,1)] == factor.pmom(1919)
        assert [(3L, 1), (20323L, 1), (415077371L, 1), (7040722789L, 1)] == factor.pmom(178178531231211235719711)

def suite():
    suite = unittest.makeSuite(FactorTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
