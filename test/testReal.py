import unittest
import math
import real

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

    def testSqrt(self):
        zero = real.Float(0,0,None)
        sqrt0 = real.sqrt(zero)
        assert sqrt0.mantissa == 0
        two = real.Float(2,0,None)
        sqrt2 = real.sqrt(two, 5)
        assert sqrt2.mantissa == 23, sqrt2.mantissa
        assert sqrt2.exponent == -4, sqrt2.exponent

    def testNeg(self):
        zero = real.Float(0,0,None)
        assert zero == -zero

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
        log2 = real.log(2)
        logf2 = real.log(real.Float(2,0))
        assert log2 == logf2
        log2inverse = real.log(.5)
        assert log2 == -log2inverse
        assert "0.6931471805599452" == str(log2)[:18]

    def testAtan2(self):
        assert real.pi / 2 == real.atan2(1,0)
        assert 0 == real.atan2(0, 1)
        assert math.atan2(0, 1) == real.atan2(0, 1)

    def testHyperbolic(self):
        assert real.sinh(1)
        assert real.cosh(1)
        assert real.tanh(1)

def suite():
    suite = unittest.makeSuite(FloatTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
