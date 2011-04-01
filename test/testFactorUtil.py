import unittest
import nzmath.factor.util as util


class FactoringIntegerTest (unittest.TestCase):
    def setUp(self):
        self.tracker100 = util.FactoringInteger(100)

    def testGetNextTarget(self):
        self.assertEqual(100, self.tracker100.getNextTarget())

    def testGetNextTargetAfterRegister(self):
        assert 100 == self.tracker100.getNextTarget()
        self.tracker100.register(2, isprime = True)
        self.assertEqual(25, self.tracker100.getNextTarget())
        self.tracker100.register(5) # Unknown primality
        self.assertEqual(5, self.tracker100.getNextTarget())
        self.tracker100.register(5, True) # 5 is prime
        self.assertRaises(LookupError, self.tracker100.getNextTarget)

    def testPrime(self):
        self.tracker100.register(2, isprime=True)
        self.assertEqual([(2, 2), (25, 1)], self.tracker100.getResult())
        self.tracker100.register(5, isprime=True)
        self.assertEqual([(2, 2), (5, 2)], self.tracker100.getResult())
        self.assertEqual({2: True, 5: True}, self.tracker100.primality)

    def testComposite(self):
        self.tracker100.register(10)
        self.assertEqual([(10, 2)], self.tracker100.getResult())
        self.tracker100.register(25)
        self.tracker100.sortFactors()
        self.assertEqual([(2, 2), (5, 2)], self.tracker100.getResult())
        self.assertEqual({2: util.Unknown, 5: util.Unknown}, self.tracker100.primality)

    def testCoprime(self):
        # register a coprime number
        self.tracker100.register(11)
        # doesn't affect
        self.assertEqual([(100, 1)], self.tracker100.getResult())
        self.assertEqual(100, self.tracker100.getNextTarget())
        self.assertEqual({100: False}, self.tracker100.primality)

    def testHighPower(self):
        tracker = util.FactoringInteger(3**9)
        tracker.register(3**2)
        # 3**9 = (3**2)**4 * 3 and 3 divides 3**2 again
        # so 3 is a smaller factor, then 3**9 = (3)**9 * 1
        self.assertEqual([(3, 9)], tracker.getResult())
        self.assertEqual({3: util.Unknown}, tracker.primality)


class FactoringMethodTest (unittest.TestCase):
    def setUp(self):
        self.method = util.FactoringMethod()

    def testVerbose(self):
        # initial value
        self.assertFalse(self.method.verbose)
        # set value
        self.method.verbose = True
        # confirm the value
        self.assertTrue(self.method.verbose)


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
