import unittest
import complex

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

def suite():
    suite = unittest.makeSuite(ComplexTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
