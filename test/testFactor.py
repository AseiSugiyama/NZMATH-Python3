import unittest
import factor

class FactorTest (unittest.TestCase):
    def runTest(self):
        assert factor.trialDivision(60) == [(2,2),(3,1),(5,1)]
        assert factor.trialDivision(128) == [(2,7)]
        assert factor.trialDivision(200819) == [(409,1),(491,1)]
        assert factor.trialDivision(1042387) ==  [(701,1),(1487,1)]
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(FactorTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
