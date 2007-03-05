import unittest
from nzmath.cubic_root import *

class Cubic_rootTest(unittest.TestCase):
    def testC_root_p(self):
        self.assertEqual([0], c_root_p(10, 5))
        self.assertEqual([2], c_root_p(2, 3))
        self.assertEqual([2], c_root_p(8 ,11))
        self.assertEqual([1, 3, 9], c_root_p(1, 13))
        self.assertRaises(ValueError, c_root_p, 2, 13)

    def testC_residue(self):
        self.assertEqual(1, c_residue(1, 7))
        self.assertEqual(-1, c_residue(2, 7))
        self.assertEqual(0, c_residue(14, 7))

    def testC_symbol(self):
        self.assertEqual(1, c_symbol(3, 6, 5, 6))
        self.assertEqual(-1, c_symbol(6, 3, 5, 6))
        self.assertEqual(0, c_symbol(-1, 5, 5, 6))

    def testDecomposite_p(self):
        self.assertEqual((2, 5), decomposite_p(19))

    def testCornacchia(self):
        self.assertEqual((3, 2), cornacchia(5, 29))
        self.assertRaises(ValueError, cornacchia, 5, 7)

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
