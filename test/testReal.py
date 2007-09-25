import unittest
import math
import nzmath.real as real
import nzmath.rational as rational
import nzmath.imaginary as imaginary


class ErrorTest (unittest.TestCase):
    def testRelativeError(self):
        self.assert_(real.RelativeError(0, 1, 2))
        self.assert_(isinstance(real.RelativeError(0, 1, 2).absoluteerror(3, 4), real.AbsoluteError))

    def testAbsoluteError(self):
        self.assert_(real.AbsoluteError(0, 1, 2))

    def testRelativeNearlyEqual(self):
        self.assert_(real.RelativeError(0, 1, 2).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.assert_(real.RelativeError(-1, 1, 2).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.failIf(real.RelativeError(1, 1, 2).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.assert_(real.RelativeError(1, 1, 3).nearlyEqual(rational.Rational(1, 3), rational.Rational(1, 4)))

    def testAbsoluteNearlyEqual(self):
        self.assert_(real.AbsoluteError(0, 1, 8).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.assert_(real.AbsoluteError(-1, 1, 8).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.failIf(real.AbsoluteError(1, 1, 8).nearlyEqual(rational.Rational(1, 4), rational.Rational(1, 3)))
        self.assert_(real.AbsoluteError(1, 1, 10).nearlyEqual(rational.Rational(1, 3), rational.Rational(1, 4)))

    def testLt(self):
        self.assert_(real.RelativeError(0, 1, 4) < real.RelativeError(0, 1, 3))
        self.assert_(real.AbsoluteError(0, 1, 4) < real.AbsoluteError(0, 1, 3))
        self.failIf(real.RelativeError(0, 1, 4) < real.RelativeError(0, 1, 5))
        self.failIf(real.AbsoluteError(0, 1, 4) < real.AbsoluteError(0, 1, 5))
        self.assert_(real.RelativeError(1, 1, 4) < real.RelativeError(0, 1, 3))
        self.assert_(real.AbsoluteError(1, 1, 4) < real.AbsoluteError(0, 1, 3))
        self.failIf(real.RelativeError(1, 1, 4) < real.RelativeError(-1, 1, 3))
        self.failIf(real.AbsoluteError(1, 1, 4) < real.AbsoluteError(-1, 1, 3))
        self.failIf(real.RelativeError(0, 1, 4) < real.AbsoluteError(0, 1, 3))
        self.failIf(real.AbsoluteError(0, 1, 4) < real.RelativeError(0, 1, 3))
        self.failIf(real.RelativeError(1, 1, 4) < real.RelativeError(1, 1, 4))
        self.failIf(real.AbsoluteError(1, 1, 4) < real.AbsoluteError(1, 1, 4))

    def testLe(self):
        # same for "less than"
        self.assert_(real.RelativeError(0, 1, 4) <= real.RelativeError(0, 1, 3))
        self.assert_(real.AbsoluteError(0, 1, 4) <= real.AbsoluteError(0, 1, 3))
        self.failIf(real.RelativeError(0, 1, 4) <= real.RelativeError(0, 1, 5))
        self.failIf(real.AbsoluteError(0, 1, 4) <= real.AbsoluteError(0, 1, 5))
        self.assert_(real.RelativeError(1, 1, 4) <= real.RelativeError(0, 1, 3))
        self.assert_(real.AbsoluteError(1, 1, 4) <= real.AbsoluteError(0, 1, 3))
        self.failIf(real.RelativeError(1, 1, 4) <= real.RelativeError(-1, 1, 3))
        self.failIf(real.AbsoluteError(1, 1, 4) <= real.AbsoluteError(-1, 1, 3))
        self.failIf(real.RelativeError(0, 1, 4) <= real.AbsoluteError(0, 1, 3))
        self.failIf(real.AbsoluteError(0, 1, 4) <= real.RelativeError(0, 1, 3))
        # equal
        self.assert_(real.RelativeError(1, 1, 4) <= real.RelativeError(1, 1, 4))
        self.assert_(real.AbsoluteError(1, 1, 4) <= real.AbsoluteError(1, 1, 4))

    def testDiv(self):
        re2 = real.RelativeError(0, 1, 6) / 5
        self.assertEqual(rational.Rational(1, 30), re2.relativeerrorrange)
        ae2 = real.AbsoluteError(0, 1, 6) / 5
        self.assertEqual(rational.Rational(1, 30),  ae2.absoluteerrorrange)


class NewFunctionTest (unittest.TestCase):
    def setUp(self):
        self.err = real.RelativeError(0, 1, 2**100)
        self.relative = rational.Rational(1 + 2**53, 2**53)
        self.absolute = rational.Rational(1, 2**53)

    def testSqrt(self):
        sqrt0 = real.sqrt(0)
        self.assertEqual(0, sqrt0)
        sqrt2 = real.sqrt(2)
        self.assert_(abs(sqrt2 ** 2 - 2) < self.absolute)

    def testExp(self):
        self.assertEqual(1, real.exp(0))
        exp1 = real.exp(1)
        exp1e = real.exp(1, self.err)
        self.assert_(exp1 < exp1e < exp1 * self.relative)
        exp2 = real.exp(2)
        exp2e = real.exp(2, self.err)
        self.assert_(exp2 < exp2e < exp2 * self.relative)
        self.assertEqual("2.718281828459045", exp1.decimalString(15))

    def testLog(self):
        log1 = real.log(1)
        self.assertEqual(0, log1)
        log2inverse = real.log(.5)
        self.assert_(log2inverse < 0)
        self.assert_(abs(real.log(2) + log2inverse) < self.absolute)
        self.assert_(abs(real.log(real.exp(1)) - 1)  < 2 * self.absolute)
        self.assert_(abs(real.log(real.exp(1).trim(2**53)) - 1) < 2 * self.absolute)

    def testPiGaussLegendre(self):
        pi = real.pi
        self.assertEqual(rational.Rational(355, 113), pi.trim(365))
        self.assert_(abs(pi - real.piGaussLegendre(self.err)) < self.absolute)

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
        self.assert_(abs(real.sin(pi)) < self.absolute)
        self.assert_(-1 <= (real.cos(pi)) < -1 + self.absolute)
        self.assert_(abs(real.tan(pi)) < self.absolute)
        abs7 = real.sin(7, real.AbsoluteError(0, 1, 10**20))
        rel7 = real.sin(7, real.RelativeError(0, 1, 10**20))
        self.assert_(abs(abs7 - rel7) < rational.Rational(1, 10**20), abs(abs7 - rel7).trim(10**20))

    def testHyperbolic(self):
        self.assertEqual(0, real.sinh(0))
        self.assertEqual(1, real.cosh(0))
        self.assertEqual(0, real.tanh(0))
        self.assertEqual(real.cosh(2), real.cosh(-2))
        self.assertEqual(real.sinh(2), -real.sinh(-2))
        self.assertEqual(real.sinh(4), -real.sinh(-4))

    def testInverseTrigonometric(self):
        self.assertEqual(0, real.asin(0))
        self.assert_(abs(real.pi / 2 - real.acos(0)) < self.absolute)
        self.assertEqual(0, real.atan(0))
        self.assert_(real.defaultError.nearlyEqual(real.pi/4, real.atan(1.0/2)+real.atan(1.0/3)))

    def testHypot(self):
        self.assert_(abs(real.hypot(3, 4) - 5) < self.absolute)

    def testPow(self):
        self.assertEqual(32, real.pow(2, 5))
        self.assertEqual(rational.Rational(1, 32), real.pow(2, -5))
        self.assert_(real.defaultError.nearlyEqual(real.sqrt(2), real.pow(2, rational.Rational(1, 2))))

    def testDegrees(self):
        self.assert_(real.defaultError.nearlyEqual(real.degrees(real.pi / 2), 90))

    def testRadians(self):
        self.assert_(real.defaultError.nearlyEqual(real.radians(90), real.pi / 2))

    def testFabs(self):
        self.assertEqual(rational.Rational(3, 2), real.fabs(-1.5))

    def testFmod(self):
        self.assertEqual(0, real.fmod(2 * real.pi, real.pi))
        self.assert_(real.defaultError.nearlyEqual(real.pi / 6, real.fmod(real.pi / 2, real.pi / 3)))
        self.assert_(real.defaultError.nearlyEqual(- real.pi / 6, real.fmod(-real.pi / 2, real.pi / 3)))

    def testFrexp(self):
        self.assertEqual((rational.Rational(0), 0), real.frexp(0))
        self.assertEqual((rational.Rational(1, 2), 2), real.frexp(2))
        self.assertEqual((rational.Rational(-5, 8), 2), real.frexp(rational.Rational(-5, 2)))

    def testLdexp(self):
        self.assertEqual(rational.Rational(0), real.ldexp(rational.Rational(0), 0))
        self.assertEqual(rational.Rational(2), real.ldexp(rational.Rational(1, 2), 2))
        self.assertEqual(rational.Rational(-5, 2), real.ldexp(rational.Rational(-5, 8), 2))


class ConstantTest (unittest.TestCase):
    def testToRational(self):
        self.assert_(isinstance(real.pi.toRational(), rational.Rational))

    def testRadd(self):
        self.assert_(4 + real.pi)
        self.assert_(rational.Integer(4) + real.pi)
        self.assert_(rational.Rational(4, 3) + real.pi)

    def testRmul(self):
        self.assert_(4 * real.pi)
        self.assert_(rational.Integer(4) * real.pi)
        self.assert_(rational.Rational(4, 3) * real.pi)


class RealFieldTest (unittest.TestCase):
    def testConstants(self):
        self.assertEqual(1, real.theRealField.one)
        self.assertEqual(0, real.theRealField.zero)

    def testStrings(self):
        self.assertEqual("R", str(real.theRealField))
        self.assertEqual("RealField()", repr(real.theRealField))

    def testSubring(self):
        R = real.theRealField
        self.failUnless(R.issuperring(R))
        self.failUnless(R.issuperring(rational.theRationalField))
        self.failUnless(R.issubring(imaginary.theComplexField))
        self.failIf(R.issubring(rational.theRationalField))

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
