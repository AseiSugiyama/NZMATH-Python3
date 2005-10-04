import unittest
import factor.util

class FactoringIntegerTest (unittest.TestCase):
    def setUp(self):
        self.tracker100 = factor.util.FactoringInteger(100)

    def testGetNextTarget(self):
        self.assertEqual(100, self.tracker100.getNextTarget())

    def testGetNextTargetAfterRegister(self):
        assert 100 == self.tracker100.getNextTarget()
        self.tracker100.register(2, isprime = True)
        self.assertEqual(25, self.tracker100.getNextTarget())
        self.tracker100.register(5) # Unknown primality
        self.assertEqual(5, self.tracker100.getNextTarget())
        self.tracker100.register(5, True) # 5 is prime
        self.failUnlessRaises(LookupError, self.tracker100.getNextTarget)

    def testPrime(self):
        self.tracker100.register(2, isprime = True)
        self.assertEqual([(2, 2), (25, 1)], self.tracker100.getResult())
        self.tracker100.register(5, isprime = True)
        self.assertEqual([(2, 2), (5, 2)], self.tracker100.getResult())

    def testComposite(self):
        self.tracker100.register(10)
        self.assertEqual([(10, 2)], self.tracker100.getResult())
        self.tracker100.register(25)
        self.tracker100.sortFactors()
        self.assertEqual([(2, 2), (5, 2)], self.tracker100.getResult())

    def testCoprime(self):
        # register a coprime number
        self.tracker100.register(11)
        # doesn't affect
        self.assertEqual([(100, 1)], self.tracker100.getResult())
        self.assertEqual(100, self.tracker100.getNextTarget())

class FactoringMethodTest (unittest.TestCase):
    def setUp(self):
        self.method = factor.util.FactoringMethod()

    def testVerbose(self):
        # initial value
        self.failIf(self.method.verbose)
        # set value
        self.method.verbose = True
        # confirm the value
        self.failUnless(self.method.verbose)

def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name[-len(suffix):] == suffix:
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
