import unittest
import complex
import real

class ComplexTest (unittest.TestCase):
    def testAdd(self):
        a = complex.Complex(1, 1)
        b = complex.Complex(complex.pi + 1, 1)
        assert b == a + complex.pi

    def testInverse(self):
        a = complex.Complex(1, 1)
        assert a == a.inverse().inverse()
        b = complex.Complex(2, 0)
        assert b.inverse() in real.theRealField

    def testConjugate(self):
        a = complex.Complex(1, 1)
        b = complex.Complex(1, -1)
        assert a.conjugate() == b
        assert a == a.conjugate().conjugate()

    def testAbs(self):
        root2 = real.sqrt(2)
        assert root2 == abs(complex.Complex(1,1))
        assert root2 == abs(complex.Complex(1, real.Float(1)))
        assert root2 == abs(complex.Complex(real.Float(1), 1))
        assert root2 == abs(complex.Complex(real.Float(1), real.Float(1)))
        assert 1 == abs(complex.Complex(1, 0))
        assert 1 == abs(complex.Complex(0, 1.0))

    def testWithFloat(self):
        a = complex.Complex(8, 1)
        b = real.Float(1, -3)
        a_add_b = complex.Complex(8 + real.Float(1, -3), 1)
        a_mul_b = complex.Complex(1, real.Float(1, -3))
        assert a_add_b == a + b
        assert a_add_b == b + a
        assert a_mul_b == a * b
        assert a_mul_b == b * a

    def testComparison(self):
        a = complex.Complex(1, 2)
        b = complex.Complex(2, 1)
        self.assertRaises(TypeError, a.__lt__, b)
        self.assertRaises(TypeError, a.__le__, b)
        self.assertRaises(TypeError, a.__gt__, b)
        self.assertRaises(TypeError, a.__ge__, b)

    def testExp(self):
        exp1 = complex.exp(1)
        expc1 = complex.exp(complex.Complex(1, 0))
        rexpf1 = real.exp(real.Float(1, 0))
        assert exp1 == expc1 == rexpf1
        assert -1 < complex.exp(complex.Complex(0, 1)).imag < 1

    def testSin(self):
        sin1 = complex.sin(1)
        sinc1 = complex.sin(complex.Complex(1, 0))
        assert complex.exp(complex.Complex(0, 1)).imag == sin1
        assert sin1 == sinc1, (sin1, sinc1, sin1 - sinc1)

    def testCos(self):
        cos1 = complex.cos(1)
        cosc1 = complex.cos(complex.Complex(real.Float(1), 0))
        assert complex.exp(complex.Complex(0, real.Float(1))).real == cos1.real
        assert cos1 == cosc1, (cos1, cosc1, cos1 - cosc1)

    def testLog(self):
        log2 = complex.log(2)
        logf2 = complex.log(real.Float(2,0))
        logc2 = complex.log(complex.Complex(2,0))
        assert log2 == logf2 == logc2
        log2inverse = real.log(.5)
        assert log2 == -log2inverse

def suite():
    suite = unittest.makeSuite(ComplexTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
