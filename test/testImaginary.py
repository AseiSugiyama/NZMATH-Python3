import unittest
import imaginary
import real

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
        assert root2 == abs(imaginary.Complex(1, real.Float(1)))
        assert root2 == abs(imaginary.Complex(real.Float(1), 1))
        assert root2 == abs(imaginary.Complex(real.Float(1), real.Float(1)))
        assert 1 == abs(imaginary.Complex(1, 0))
        assert 1 == abs(imaginary.Complex(0, 1.0))

    def testWithFloat(self):
        a = imaginary.Complex(8, 1)
        b = real.Float(1, -3)
        a_add_b = imaginary.Complex(8 + real.Float(1, -3), 1)
        a_mul_b = imaginary.Complex(1, real.Float(1, -3))
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

    def testExp(self):
        exp1 = imaginary.exp(1)
        expc1 = imaginary.exp(imaginary.Complex(1, 0))
        rexpf1 = real.exp(real.Float(1, 0))
        assert exp1 == expc1 == rexpf1
        assert -1 < imaginary.exp(imaginary.Complex(0, 1)).imag < 1

    def testSin(self):
        sin1 = imaginary.sin(1)
        sinc1 = imaginary.sin(imaginary.Complex(1, 0))
        assert imaginary.exp(imaginary.Complex(0, 1)).imag == sin1
        assert sin1 == sinc1, (sin1, sinc1, sin1 - sinc1)

    def testCos(self):
        cos1 = imaginary.cos(1)
        cosc1 = imaginary.cos(imaginary.Complex(real.Float(1), 0))
        assert imaginary.exp(imaginary.Complex(0, real.Float(1))).real == cos1.real
        assert cos1 == cosc1, (cos1, cosc1, cos1 - cosc1)

    def testTan(self):
        tan1 = imaginary.tan(1)
        tanc1 = imaginary.tan(imaginary.Complex(real.Float(1), 0))
        assert tan1 == tanc1
        assert tan1.real > 0

    def testLog(self):
        log2 = imaginary.log(2)
        logf2 = imaginary.log(real.Float(2,0))
        logc2 = imaginary.log(imaginary.Complex(2,0))
        assert log2 == logf2 == logc2
        log2inverse = real.log(.5)
        assert log2 == -log2inverse

    def testHyperbolic(self):
        assert imaginary.sinh(1)
        assert imaginary.cosh(1)
        assert imaginary.tanh(1)

def suite():
    suite = unittest.makeSuite(ImaginaryTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
