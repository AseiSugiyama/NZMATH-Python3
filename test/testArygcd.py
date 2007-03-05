import unittest
from nzmath.arygcd import *

class ArygcdTest(unittest.TestCase):
    def testBinarygcd(self):
        self.assertEqual(6, binarygcd(36, 30))
        self.assertEqual(10, binarygcd(0, 10))
        self.assertEqual(10, binarygcd(10, 0))
        self.assertEqual(1, binarygcd(13, 21))

    def testArygcd_i(self):
        self.assertEqual((-3, 1), arygcd_i(1, 13, 13, 9))
        self.assertEqual((3, 1), arygcd_i(0, 0, 3, 1))
        self.assertEqual((3, 1), arygcd_i(3, 1, 0, 0))
        self.assertEqual((1, 0), arygcd_i(3, 0, 2, 1))

    def testArygcd_w(self):
        self.assertEqual((4, 5), arygcd_w(2, 13, 33, 15))
        self.assertEqual((4, 5), arygcd_w(0, 0, 4, 5))
        self.assertEqual((4, 5), arygcd_w(4, 5, 0, 0))
        self.assertEqual((1, 0), arygcd_w(3, 5, 4, 0))

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
