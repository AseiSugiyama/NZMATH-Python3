import unittest
import factor.methods as mthd

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        self.assertEqual(mthd.trialDivision(60), [(2,2),(3,1),(5,1)])
        self.assertEqual(mthd.trialDivision(128), [(2,7)])
        self.assertEqual(mthd.trialDivision(200819), [(409,1),(491,1)])
        self.assertEqual(mthd.trialDivision(1042387),  [(701,1),(1487,1)])

    def testRho(self):
        m = "rhomethod sometimes fails to factor anyway."
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.rhomethod(60), m)
        self.assertEqual([(2,7)], mthd.rhomethod(128), m)
        self.assertEqual([(409,1),(491,1)], mthd.rhomethod(200819), m)
        self.assertEqual([(701,1),(1487,1)], mthd.rhomethod(1042387), m)
        self.assertEqual([(17,2), (19,1)], mthd.rhomethod(17**2 * 19), m)

    def testPMinusOneMethod(self):
        self.assertEqual([(19,1), (101,1)], mthd.pmom(1919))
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        self.assertEqual([(p,1), (154858631,1)], mthd.pmom(p*154858631))

    def testMPQS(self):
        p = 4 * 6133 + 1
        result = mthd.mpqs(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)

    def testFactor(self):
        # default method
        p = 4 * 6133 + 1
        result = mthd.factor(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)

    def testFactorSpecifyMethod(self):
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.factor(60, method='t'))
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.factor(60, method='trial'))
        self.assertEqual([(19,1), (101,1)], mthd.factor(1919, method='p'))
        self.assertEqual([(19,1), (101,1)], mthd.factor(1919, method='pmom'))
        p = 4 * 6133 + 1
        self.assertEqual([(p,1), (154858631,1)], mthd.factor(p*154858631, 'm'))
        m = "rhomethod sometimes fails to factor anyway."
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.factor(60, method='r'), m)


def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())