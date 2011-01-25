import unittest
from sandbox.ternary import *


class TernaryValueTest (unittest.TestCase):
    def testWrongValueInit(self):
        self.assertRaises(ValueError, TernaryValue, 2)

    def testSingletonViolation(self):
        self.assertRaises(ValueError, TernaryValue, False)
        # 1 == True
        self.assertRaises(ValueError, TernaryValue, 1)

    def testT_not(self):
        self.assertEqual(FALSE, TRUE.t_not())
        self.assertEqual(TRUE, FALSE.t_not())
        self.assertEqual(UNKNOWN, UNKNOWN.t_not())

    def testT_or(self):
        self.assertEqual(TRUE, TRUE.t_or(TRUE))
        self.assertEqual(TRUE, TRUE.t_or(FALSE))
        self.assertEqual(TRUE, TRUE.t_or(UNKNOWN))
        self.assertEqual(TRUE, UNKNOWN.t_or(TRUE))
        self.assertEqual(UNKNOWN, UNKNOWN.t_or(FALSE))
        self.assertEqual(UNKNOWN, UNKNOWN.t_or(UNKNOWN))
        self.assertEqual(TRUE, FALSE.t_or(TRUE))
        self.assertEqual(FALSE, FALSE.t_or(FALSE))
        self.assertEqual(UNKNOWN, FALSE.t_or(UNKNOWN))

    def testT_and(self):
        self.assertEqual(TRUE, TRUE.t_and(TRUE))
        self.assertEqual(FALSE, TRUE.t_and(FALSE))
        self.assertEqual(UNKNOWN, TRUE.t_and(UNKNOWN))
        self.assertEqual(UNKNOWN, UNKNOWN.t_and(TRUE))
        self.assertEqual(FALSE, UNKNOWN.t_and(FALSE))
        self.assertEqual(UNKNOWN, UNKNOWN.t_and(UNKNOWN))
        self.assertEqual(FALSE, FALSE.t_and(TRUE))
        self.assertEqual(FALSE, FALSE.t_and(FALSE))
        self.assertEqual(FALSE, FALSE.t_and(UNKNOWN))

    def testBool(self):
        self.assert_(TRUE)
        self.failIf(FALSE)
        self.failIf(UNKNOWN) # This is the convention.
        self.assertEqual(False, bool(UNKNOWN))


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
