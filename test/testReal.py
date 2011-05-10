from __future__ import division
import unittest
import nzmath.real as real
import nzmath.rational as rational
import nzmath.imaginary as imaginary
from nzmath.plugins import MATHMODULE as math


class NewFunctionTest (unittest.TestCase):
    def setUp(self):
        self.relative = rational.Rational(1 + 2**53, 2**53)
        self.absolute = rational.Rational(1, 2**53)

    def testFloor(self):
        self.assertEqual(3, real.floor(3))
        self.assertEqual(-3, real.floor(-3))
        self.assertEqual(3, real.floor(3.5))
        self.assertEqual(-3, real.floor(-2.5))

    def testCeil(self):
        self.assertEqual(3, real.ceil(3))
        self.assertEqual(-3, real.ceil(-3))
        self.assertEqual(4, real.ceil(3.5))
        self.assertEqual(-2, real.ceil(-2.5))

    def testTranc(self):
        self.assertEqual(3, real.tranc(3))
        self.assertEqual(-3, real.tranc(-3))
        self.assertEqual(3, real.tranc(3.3))
        self.assertEqual(-3, real.tranc(-2.7))

    def testFabs(self):
        self.assertEqual(rational.Rational(3, 2), real.fabs(-1.5))

    def testFrexp(self):
        self.assertEqual((rational.Rational(0), 0), real.frexp(0))
        self.assertEqual((rational.Rational(1, 2), 2), real.frexp(2))
        self.assertEqual((rational.Rational(-5, 8), 2), real.frexp(rational.Rational(-5, 2)))

    def testLdexp(self):
        self.assertEqual(rational.Rational(0), real.ldexp(rational.Rational(0), 0))
        self.assertEqual(rational.Rational(2), real.ldexp(rational.Rational(1, 2), 2))
        self.assertEqual(rational.Rational(-5, 2), real.ldexp(rational.Rational(-5, 8), 2))


class RealFieldTest (unittest.TestCase):
    def testConstants(self):
        self.assertEqual(1, real.theRealField.one)
        self.assertEqual(0, real.theRealField.zero)

    def testStrings(self):
        self.assertEqual("R", str(real.theRealField))
        self.assertEqual("RealField()", repr(real.theRealField))

    def testSubring(self):
        R = real.theRealField
        self.assertTrue(R.issuperring(R))
        self.assertTrue(R.issuperring(rational.theRationalField))
        self.assertTrue(R.issubring(imaginary.theComplexField))
        self.assertFalse(R.issubring(rational.theRationalField))

    def testHash(self):
        dictionary = {}
        dictionary[real.theRealField] = 1
        self.assertEqual(1, dictionary[real.RealField()])


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
