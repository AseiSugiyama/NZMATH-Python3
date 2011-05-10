from __future__ import division
import unittest
import nzmath.imaginary as imaginary
import nzmath.real as real
import nzmath.rational as rational


class ImaginaryTest (unittest.TestCase):
    def testAdd(self):
        pass

    def testInverse(self):
        a = imaginary.Complex(1, 1)
        self.assertEqual(a, a.inverse().inverse())
        b = imaginary.Complex(2, 0)
        self.assertTrue(b.inverse() in real.theRealField, b.inverse())

    def testConjugate(self):
        a = imaginary.Complex(1, 1)
        b = imaginary.Complex(1, -1)
        self.assertEqual(a.conjugate(), b)
        self.assertEqual(a, a.conjugate().conjugate())

    def testAbs(self):
        pass

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

    def testGetRing(self):
        self.assertEqual(imaginary.theComplexField, imaginary.Complex(1).getRing())


class ComplexFieldTest (unittest.TestCase):
    def testtConstants(self):
        self.assertEqual(1, imaginary.theComplexField.one)
        self.assertEqual(0, imaginary.theComplexField.zero)

    def testStrings(self):
        self.assertEqual("C", str(imaginary.theComplexField))
        self.assertEqual("ComplexField()", repr(imaginary.theComplexField))

    def testSubring(self):
        C = imaginary.theComplexField
        self.assertTrue(C.issuperring(real.theRealField))
        self.assertTrue(C.issuperring(rational.theRationalField))

    def testHash(self):
        dictionary = {}
        dictionary[imaginary.theComplexField] = 1
        self.assertEqual(1, dictionary[imaginary.ComplexField()])


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
