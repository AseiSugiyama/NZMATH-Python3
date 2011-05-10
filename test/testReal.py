from __future__ import division
import unittest
import nzmath.real as real
import nzmath.rational as rational
import nzmath.imaginary as imaginary
from nzmath.plugins import MATHMODULE as math


class NewFunctionTest (unittest.TestCase):
    def setUp(self):
        self.err = real.RelativeError(0, 1, 2**100)
        self.relative = rational.Rational(1 + 2**53, 2**53)
        self.absolute = rational.Rational(1, 2**53)

    def testSqrt(self):
        sqrt0 = real.sqrt(0)
        self.assertEqual(0, sqrt0)
        sqrt2 = real.sqrt(2)
        self.assertTrue(abs(sqrt2 ** 2 - 2) < self.absolute)

    def testExp(self):
        self.assertEqual(1, real.exp(0))
        exp1 = real.exp(1)
        exp1e = real.exp(1, self.err)
        self.assertTrue(exp1 < exp1e < exp1 * self.relative)
        exp2 = real.exp(2)
        exp2e = real.exp(2, self.err)
        self.assertTrue(exp2 < exp2e < exp2 * self.relative)
        self.assertEqual("2.718281828459045", exp1.decimalString(15))

    def testLog(self):
        log1 = real.log(1)
        self.assertEqual(0, log1)
        log2inverse = real.log(.5)
        self.assertTrue(log2inverse < 0)
        self.assertTrue(abs(real.log(2) + log2inverse) < self.absolute)
        self.assertTrue(abs(real.log(real.exp(1)) - 1)  < 2 * self.absolute)
        self.assertTrue(abs(real.log(real.exp(1).trim(2**53)) - 1) < 2 * self.absolute)

    def testPiGaussLegendre(self):
        pi = real.pi
        self.assertEqual(rational.Rational(355, 113), pi.trim(365))
        pi_to_err = real.piGaussLegendre(self.err)
        self.assertAlmostEqual(pi, pi_to_err, 14, (pi - pi_to_err).trim(2**80))

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

    def testTrigonometric(self):
        self.assertEqual(0, real.sin(0))
        self.assertEqual(1, real.cos(0))
        self.assertEqual(0, real.tan(0))
        pi = real.pi
        self.assertTrue(abs(real.sin(pi)) < self.absolute)
        self.assertTrue(-1 <= (real.cos(pi)) < -1 + self.absolute)
        self.assertTrue(abs(real.tan(pi)) < self.absolute)
        abs7 = real.sin(7, real.AbsoluteError(0, 1, 10**20))
        rel7 = real.sin(7, real.RelativeError(0, 1, 10**20))
        self.assertTrue(abs(abs7 - rel7) < rational.Rational(1, 10**20), abs(abs7 - rel7).trim(10**20))

    def testHyperbolic(self):
        self.assertEqual(0, real.sinh(0))
        self.assertEqual(1, real.cosh(0))
        self.assertEqual(0, real.tanh(0))
        self.assertEqual(real.cosh(2), real.cosh(-2))
        self.assertEqual(real.sinh(2), -real.sinh(-2))
        self.assertEqual(real.sinh(4), -real.sinh(-4))

    def testInverseTrigonometric(self):
        self.assertEqual(0, real.asin(0))
        self.assertTrue(abs(real.pi / 2 - real.acos(0)) < self.absolute)
        self.assertEqual(0, real.atan(0))
        self.assertAlmostEqual(real.pi / 4, real.atan(1/2) + real.atan(1/3))

    def testHypot(self):
        self.assertTrue(abs(real.hypot(3, 4) - 5) < self.absolute)

    def testPow(self):
        self.assertEqual(32, real.pow(2, 5))
        self.assertEqual(rational.Rational(1, 32), real.pow(2, -5))
        self.assertTrue(real.defaultError.nearlyEqual(real.sqrt(2), real.pow(2, rational.Rational(1, 2))))

    def testDegrees(self):
        self.assertTrue(real.defaultError.nearlyEqual(real.degrees(real.pi / 2), 90))

    def testRadians(self):
        self.assertTrue(real.defaultError.nearlyEqual(real.radians(90), real.pi / 2))

    def testFabs(self):
        self.assertEqual(rational.Rational(3, 2), real.fabs(-1.5))

    def testFmod(self):
        self.assertEqual(0, real.fmod(2 * real.pi, real.pi))
        self.assertTrue(real.defaultError.nearlyEqual(real.pi / 6, real.fmod(real.pi / 2, real.pi / 3)))
        self.assertTrue(real.defaultError.nearlyEqual(- real.pi / 6, real.fmod(-real.pi / 2, real.pi / 3)))

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
