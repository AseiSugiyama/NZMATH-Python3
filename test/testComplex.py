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

    def testConjugate(self):
        a = complex.Complex(1, 1)
        b = complex.Complex(1, -1)
        assert a.conjugate() == b
        assert a == a.conjugate().conjugate()

    def testWithFloat(self):
        a = complex.Complex(8, 1)
        b = real.Float(1, -3)
        a_add_b = complex.Complex(8 + real.Float(1, -3), 1)
        a_mul_b = complex.Complex(1, real.Float(1, -3))
        assert a_add_b == a + b
        assert a_add_b == b + a
        assert a_mul_b == a * b
        assert a_mul_b == b * a

def suite():
    suite = unittest.makeSuite(ComplexTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
