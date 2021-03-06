import unittest
import logging
import nzmath.factor.methods as mthd

try:
    _log = logging.getLogger('test.testFactorMethod')
except:
    try:
        _log = logging.getLogger('nzmath.test.testFactorMethod')
    except:
        _log = logging.getLogger('testFactorMethod')
_log.setLevel(logging.INFO)

class FactorTest (unittest.TestCase):
    def testTrialDivision(self):
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.trialDivision(60))
        self.assertEqual([(2,7)], mthd.trialDivision(128))
        self.assertEqual([(409,1),(491,1)], mthd.trialDivision(200819))
        self.assertEqual([(701,1),(1487,1)], mthd.trialDivision(1042387))

    def testRho(self):
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.rhomethod(60))
        self.assertEqual([(2,7)], mthd.rhomethod(128))
        self.assertEqual([(409,1),(491,1)], mthd.rhomethod(200819))
        self.assertEqual([(701,1),(1487,1)], mthd.rhomethod(1042387))
        self.assertEqual([(17,2), (19,1)], mthd.rhomethod(17**2 * 19))

    def testPMinusOneMethod(self):
        self.assertEqual([(19,1), (101,1)], mthd.pmom(1919))
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        self.assertEqual([(p,1), (154858631,1)], mthd.pmom(p*154858631))

    def testMPQS(self):
        p = 4 * 6133 + 1
        result = mthd.mpqs(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)

    def testEllipticCurveMethod(self):
        #self.assertEqual([(19,1), (101,1)], mthd.ecm(1919))
        # 6133 = prime.prime(800) > sqrt(B) & 800 == 0 mod 20
        p = 4 * 6133 + 1
        self.assertEqual([(p,1), (154858631,1)], mthd.ecm(p*154858631))

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
        self.assertEqual([(p,1), (154858631,1)], mthd.factor(p*154858631, 'e'))
        self.assertEqual([(2,2),(3,1),(5,1)], mthd.factor(60, method='r'))

    def testVerbosity(self):
        # default method
        p = 4 * 6133 + 1
        _log.info("silent:")
        result = mthd.mpqs(p*154858631, verbose=False)
        _log.info("verbose:")
        result = mthd.mpqs(p*154858631, verbose=True)


class TrialDivisionTest (unittest.TestCase):
    def testTrialDivisionTracker(self):
        tdm = mthd.TrialDivision()
        factorization_of_49 = tdm.factor(49, return_type='tracker')
        self.assertTrue(isinstance(factorization_of_49, mthd.util.FactoringInteger))
        self.assertTrue(7 in factorization_of_49.primality)

        # fail to factor is iterator is short
        factorization_of_10201 = tdm.factor(10201,
                                            return_type='tracker',
                                            iterator=iter(range(3, 100, 2)))
        self.assertTrue(10201 in factorization_of_10201.primality) # not factored
        self.assertFalse(factorization_of_10201.primality[10201]) # not a prime


def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
