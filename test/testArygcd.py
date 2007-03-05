import unittest
from nzmath.arygcd import *

class ArygcdTest(unittest.TestCase):
    def testBinarygcd(self):
        self.assertEqual(6, binarygcd(36, 30))

    def testArygcd_i(self):
        self.assertEqual((-3, 1), arygcd_i(1, 13, 13, 9))

    def testArygcd_w(self):
        self.assertEqual((4, 5), arygcd_w(2, 13, 33, 15))

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
