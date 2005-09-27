import unittest
import time
import imaginary
import real, rational

"$Id$"

class ImaginaryTest (unittest.TestCase):
    def testAdd(self):
        a = imaginary.Complex(1, 1)
        b = imaginary.Complex(imaginary.pi + 1, 1)
        assert b == a + imaginary.pi

    def testInverse(self):
        a = imaginary.Complex(1, 1)
        assert a == a.inverse().inverse()
        b = imaginary.Complex(2, 0)
        assert b.inverse() in real.theRealField

    def testConjugate(self):
        a = imaginary.Complex(1, 1)
        b = imaginary.Complex(1, -1)
        assert a.conjugate() == b
        assert a == a.conjugate().conjugate()

    def testAbs(self):
        root2 = real.sqrt(2)
        assert root2 == abs(imaginary.Complex(1,1))
        assert 1 == abs(imaginary.Complex(1, 0))
        assert 1 == abs(imaginary.Complex(0, 1.0))

    def testWithFloat(self):
        a = imaginary.Complex(8, 1)
        b = rational.Rational(1, 8)
        a_add_b = imaginary.Complex(8 + rational.Rational(1, 8), 1)
        a_mul_b = imaginary.Complex(1, rational.Rational(1, 8))
        assert a_add_b == a + b
        assert a_add_b == b + a
        assert a_mul_b == a * b
        assert a_mul_b == b * a

    def testComparison(self):
        a = imaginary.Complex(1, 2)
        b = imaginary.Complex(2, 1)
        self.assertRaises(TypeError, a.__lt__, b)
        self.assertRaises(TypeError, a.__le__, b)
        self.assertRaises(TypeError, a.__gt__, b)
        self.assertRaises(TypeError, a.__ge__, b)

    def testNonzero(self):
        a = imaginary.Complex(8.4, 5)
        assert a
        b = imaginary.Complex(rational.Rational(0), rational.Rational(0))
        assert not b

    def testExp(self):
        exp1 = imaginary.exp(1)
        expc1 = imaginary.exp(imaginary.Complex(1, 0))
        rexp1 = real.exp(rational.Integer(1))
        assert 0 < imaginary.exp(imaginary.j).real < 1
        assert 0 < imaginary.exp(imaginary.j).imag < 1
        assert isinstance(imaginary.exp(imaginary.j), imaginary.Complex)

    def testSin(self):
        sin1 = imaginary.sin(1)
        sinc1 = imaginary.sin(imaginary.Complex(1, 0))
        assert imaginary.defaultError.nearlyEqual(imaginary.exp(imaginary.j).imag, sin1)
        assert sin1 == sinc1, (sin1, sinc1, sin1 - sinc1)

    def testCos(self):
        cos1 = imaginary.cos(1)
        cosc1 = imaginary.cos(imaginary.Complex(rational.Integer(1), 0))
        assert isinstance(cos1, rational.Rational) or imaginary.exp(imaginary.Complex(0, rational.Integer(1))).real == cos1.real
        assert cos1 == cosc1, (cos1, cosc1, cos1 - cosc1)

    def testTan(self):
        tan1 = imaginary.tan(1)
        tanc1 = imaginary.tan(imaginary.Complex(rational.Integer(1), 0))
        assert tan1 == tanc1
        assert isinstance(tan1, rational.Rational) and tan1 > 0 or tan1.real > 0

    def testLog(self):
        log2 = imaginary.log(2)
        logf2 = imaginary.log(rational.Integer(2))
        logc2 = imaginary.log(imaginary.Complex(2,0))
        assert log2 == logf2 == logc2
        log2inverse = real.log(.5)
        assert abs(imaginary.log(2) + log2inverse) <= rational.Rational(1, 2**(-53))

    def testHyperbolic(self):
        assert imaginary.sinh(1)
        assert imaginary.cosh(1)
        assert imaginary.tanh(1)

    def testConstants(self):
        assert imaginary.pi ==real.pi
        assert (0,1) == (imaginary.j.real, imaginary.j.imag)


class ErrorTest (unittest.TestCase):
    def testRelativeError(self):
        assert imaginary.RelativeError(1,2)
        assert isinstance(imaginary.RelativeError(1,2).absoluteerror(imaginary.Complex(3,4)), imaginary.AbsoluteError)

    def testAbsoluteError(self):
        assert imaginary.AbsoluteError(rational.Rational(1,2))

    def testDiv(self):
        re2 = imaginary.RelativeError(rational.Rational(1, 6)) / 5
        assert re2.relativeerrorrange == rational.Rational(1,30)
        ae2 = imaginary.AbsoluteError(rational.Rational(1, 6)) / 5
        assert ae2.absoluteerrorrange == rational.Rational(1,30)


class ComplexFieldTest (unittest.TestCase):
    def testtConstants(self):
        self.assertEqual(1, imaginary.theComplexField.one)
        self.assertEqual(0, imaginary.theComplexField.zero)

    def testStrings(self):
        self.assertEqual("C", str(imaginary.theComplexField))
        self.assertEqual("ComplexField()", repr(imaginary.theComplexField))

    def testSubring(self):
        C = imaginary.theComplexField
        self.failUnless(C.issuperring(real.theRealField))
        self.failUnless(C.issuperring(rational.theRationalField))


def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name[-len(suffix):] == suffix:
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
