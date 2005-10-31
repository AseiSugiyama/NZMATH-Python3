import unittest
import nzmath.factor.misc as misc


class MiscTest (unittest.TestCase):
    def testPrimeDivisors(self):
        self.assertEqual([3, 5], misc.primeDivisors(15))

    def testSquarePart(self):
        self.assertEqual(1, misc.squarePart(15))
        self.assertEqual(17, misc.squarePart(17**2 * 19))

    def testAllDivisors(self):
        self.assertEqual([1], misc.allDivisors(1))
        self.assertEqual([1, 2], misc.allDivisors(2))
        self.assertEqual([1, 2, 4], misc.allDivisors(4))
        self.assertEqual([1, 2, 3, 6], misc.allDivisors(6))
        self.assertEqual([1, 2, 3, 4, 6, 12], misc.allDivisors(12))
        self.assertEqual([1, 2, 3, 5, 6, 10, 15, 30], misc.allDivisors(30))

    def testPrimePowerTest(self):
        # not a power
        self.assertEqual((12, 0), misc.primePowerTest(12))
        self.assertEqual((53, 1), misc.primePowerTest(53))
        # powers
        self.assertEqual((7, 2), misc.primePowerTest(49))
        self.assertEqual((3, 4), misc.primePowerTest(81))
        self.assertEqual((5, 3), misc.primePowerTest(125))
        self.assertEqual((2, 7), misc.primePowerTest(128))


def suite():
    suite = unittest.makeSuite(MiscTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
