import unittest
import math
import real
import rational

class FloatTest (unittest.TestCase):
    def testAdd(self):
        sum1 = real.Float(-3,0,None) + real.Float(125,2,None)
        assert sum1.mantissa == 497
        assert sum1.exponent == 0
        assert sum1.precision == None
        sum2 = real.Float(1001,0,40) + real.Float(-125,3,None)
        assert sum2.mantissa == 1
        assert sum2.exponent == 0
        assert sum2.precision == 31
        sum3 = real.Float(-1001,0,40) + 1000
        assert sum3.mantissa == -1
        assert sum3.exponent == 0
        assert sum3.precision == 31
        sum4 = 1000 + real.Float(-1001,0,40)
        assert sum4.mantissa == -1
        assert sum4.exponent == 0
        assert sum4.precision == 31
        sum5 = real.Float(1,0, 100) + real.Float(1,1, 100)
        assert sum5.mantissa == 3

    def testMul(self):
        prod1 = real.Float(3,0,None) * real.Float(125,2,None)
        assert prod1.mantissa == 375
        assert prod1.exponent == 2
        assert prod1.precision == None

    def testSub(self):
        dif1 = real.Float(-3,0,None) - real.Float(125,2,None)
        assert dif1.mantissa == -503
        assert dif1.exponent == 0
        assert dif1.precision == None
        dif2 = real.Float(1001,0,40) - real.Float(125,3,None)
        assert dif2.mantissa == 1
        assert dif2.exponent == 0
        assert dif2.precision == 31
        dif3 = real.Float(1001,0,40) - 1000
        assert dif3.mantissa == 1
        assert dif3.exponent == 0
        assert dif3.precision == 31
        dif4 = 1000 - real.Float(1001,0,40)
        assert dif4.mantissa == -1
        assert dif4.exponent == 0
        assert dif4.precision == 31

    def testDiv(self):
        divisee = real.Float(-3,0,None)
        quot1 = divisee / real.Float(125,2,None)
        assert quot1.precision == 53
        assert quot1.mantissa == -6917529027641081, quot1.mantissa
        assert quot1.exponent == -60, quot1.exponent
        divisee.setDefaultPrecision(1000)
        quot2 = divisee / real.Float(125,2,None)
        assert quot2.precision == 1000

    def testNeg(self):
        zero = real.Float(0,0,None)
        assert zero == -zero

class FunctionTest (unittest.TestCase):
    def testSqrt(self):
        zero = real.Float(0,0,None)
        sqrt0 = real.sqrt(zero)
        assert sqrt0.mantissa == 0
        two = real.Float(2,0,None)
        sqrt2 = real.sqrt(two, 5)
        assert sqrt2.mantissa == 23, sqrt2.mantissa
        assert sqrt2.exponent == -4, sqrt2.exponent

    def testExp(self):
        exp1 = real.exp(1)
        expf1 = real.exp(real.Float(1,0))
        assert exp1 == expf1
        assert exp1 == real.e

    def testSin(self):
        sin1 = real.sin(1)
        sinf1 = real.sin(real.Float(1,0))
        assert sin1 == sinf1
        assert 1 >= sin1 >= -1

    def testCos(self):
        cos1 = real.cos(1)
        cosf1 = real.cos(real.Float(1,0))
        assert cos1 == cosf1
        assert 1 >= cos1 >= -1

    def testLog(self):
        log3 = real.log(3)
        logF3 = real.log(real.Float(3,0))
        logf3 = real.log(3.0)
        assert log3 == logF3 == logf3
        log2inverse = real.log(.5)
        assert abs(real.log(2,53) + log2inverse) <= real.Float(1, -53)
        assert "0.69314718055994530" == str(real.Log2)[:19], str(real.Log2)

    def testAtan(self):
        assert real.atan(0.5, 0)

    def testAtan2(self):
        assert real.pi / 2 == real.atan2(1,0)
        assert 0 == real.atan2(0, 1)
        assert math.atan2(0, 1) == real.atan2(0, 1)

    def testHyperbolic(self):
        assert real.sinh(1)
        assert real.cosh(1)
        assert real.tanh(1)

class ErrorTest (unittest.TestCase):
    def testRelativeError(self):
        assert real.RelativeError(0,1,2)
        assert isinstance(real.RelativeError(0,1,2).absoluteerror(3,4), real.AbsoluteError)

    def testAbsoluteError(self):
        assert real.AbsoluteError(0,1,2)

    def testRelativeNearlyEqual(self):
        assert real.RelativeError(0,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.RelativeError(-1,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert not real.RelativeError(1,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.RelativeError(1,1,3).nearlyEqual(rational.Rational(1,3), rational.Rational(1,4))

    def testAbsoluteNearlyEqual(self):
        assert real.AbsoluteError(0,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.AbsoluteError(-1,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert not real.AbsoluteError(1,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.AbsoluteError(1,1,10).nearlyEqual(rational.Rational(1,3), rational.Rational(1,4))

class NewFunctionTest (unittest.TestCase):
    def setUp(self):
        self.err = real.RelativeError(0, 1, 2**100)
        self.relative = rational.Rational(1 + 2**53, 2**53)
        self.absolute = rational.Rational(1, 2**53)

    def testSqrt(self):
        sqrt0 = real.sqrt_new(0)
        assert sqrt0 == 0
        sqrt2 = real.sqrt_new(2)
        assert abs(sqrt2 ** 2 - 2) < self.absolute

    def testExp(self):
        assert 1 == real.exp_new(0)
        exp1 = real.exp_new(1)
        exp1e = real.exp_new(1, self.err)
        assert exp1 < exp1e < exp1 * self.relative
        exp2 = real.exp_new(2)
        exp2e = real.exp_new(2, self.err)
        assert exp2 < exp2e < exp2 * self.relative
        assert "2.718281828459045" == exp1.decimalString(15)

    def testLog(self):
        log1 = real.log_new(1)
        assert 0 == log1
        log2inverse = real.log_new(.5)
        assert log2inverse < 0
        assert abs(real.log_new(2) + log2inverse) < self.absolute
        assert abs(real.log_new(real.exp_new(1)) - 1)  < 2 * self.absolute
        assert abs(real.log_new(real.exp_new(1).trim(2**53)) - 1) < 2 * self.absolute

    def testPiGaussLegendre(self):
        pi = real.piGaussLegendre_new()
        assert rational.Rational(355,113) == pi.trim(365)
        assert abs(pi - real.piGaussLegendre_new(self.err)) < self.absolute

    def testFloor(self):
        assert 3 == real.floor_new(3)
        assert -3 == real.floor_new(-3)
        assert 3 == real.floor_new(3.5)
        assert -3 == real.floor_new(-2.5)

    def testCeil(self):
        assert 3 == real.ceil_new(3)
        assert -3 == real.ceil_new(-3)
        assert 4 == real.ceil_new(3.5)
        assert -2 == real.ceil_new(-2.5)

    def testTranc(self):
        assert 3 == real.tranc_new(3)
        assert -3 == real.tranc_new(-3)
        assert 3 == real.tranc_new(3.3)
        assert -3 == real.tranc_new(-2.7)

    def testTrigonometric(self):
        assert 0 == real.sin_new(0)
        assert 1 == real.cos_new(0)
        assert 0 == real.tan_new(0)
        pi = real.piGaussLegendre_new()
        assert abs(real.sin_new(pi)) < self.absolute
        assert -1 <= (real.cos_new(pi)) < -1 + self.absolute
        assert abs(real.tan_new(pi)) < self.absolute

    def testHyperbolic(self):
        assert 0 == real.sinh_new(0)
        assert 1 == real.cosh_new(0)
        assert 0 == real.tanh_new(0)

    def testInverseTrigonometric(self):
        assert 0 == real.asin_new(0)
        pi = real.piGaussLegendre_new()
        assert abs(pi / 2 - real.acos_new(0)) < self.absolute
        assert 0 == real.atan_new(0)

    def testHypot(self):
        assert abs(real.hypot_new(3,4) - 5) < self.absolute

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FloatTest, 'test'))
    suite.addTest(unittest.makeSuite(FunctionTest, 'test'))
    suite.addTest(unittest.makeSuite(ErrorTest, 'test'))
#    suite.addTest(unittest.makeSuite(NewFunctionTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
