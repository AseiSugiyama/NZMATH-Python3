from __future__ import division
import unittest
from nzmath.rational import *
import nzmath.finitefield as finitefield
# Rational, Integer, theIntegerRing, theRationalField

class RationalTest (unittest.TestCase):
    def testInit(self):
        self.assertEqual("2/1", str(Rational(2)))
        self.assertEqual("2/1", str(Rational(2L)))
        self.assertEqual("1/2", str(Rational(1,2)))
        self.assertEqual("1/2", str(Rational(Rational(1,2))))
        self.assertEqual("21/26", str(Rational(Rational(7,13),Rational(2,3))))
        self.assertEqual("3/2", str(Rational(1.5)))
        self.assertEqual("3/4", str(Rational(1.5, 2.0)))
        self.assertRaises(ZeroDivisionError, Rational, 1, 0)
        self.assertRaises(TypeError, Rational, 1, finitefield.FinitePrimeFieldElement(1,7))
        self.assertRaises(TypeError, Rational, finitefield.FinitePrimeFieldElement(1,7), 4)

    def testPos(self):
        self.assertEqual("1/2", str(+Rational(2,4)))
        self.assertEqual("-3/4", str(+Rational(-3,4)))

    def testNeg(self):
        self.assertEqual(-Rational(2,4), Rational(-1,2))
        self.assertEqual("3/4", str(-Rational(-3,4)))

    def testAdd(self):
        self.assertEqual(Rational(13,6), Rational(2,3) + Rational(3,2))
        self.assertEqual(Rational(31,18), Rational(13,18) + 1)
        self.assertEqual(Rational(2000000000000000000000000000000000000001,2),
            1000000000000000000000000000000000000000 + Rational(1,2))
        self.assertEqual(1, Rational(1,2) + Rational(1,3) + Rational(1,6))
        self.assertEqual(1, Rational(1,2) + 0.5)
        self.assertEqual(1, 0.5 + Rational(1,2))

    def testIadd(self):
        a = Rational(1,2)
        a += Rational(1,3)
        self.assertEqual(Rational(5,6), a)

    def testSub(self):
        self.assertEqual(Rational(-5,6), Rational(2,3) - Rational(3,2))
        self.assertEqual(Rational(-5,18), Rational(13,18) - 1)
        self.assertEqual(Rational(1999999999999999999999999999999999999999,2),
            1000000000000000000000000000000000000000 - Rational(1,2))
        self.assertEqual(0, Rational(1,2) - Rational(1,3) - Rational(1,6))
        self.assertEqual(0, Rational(1,2) - 0.5)
        self.assertEqual(0, 0.5 - Rational(1,2))

    def testIsub(self):
        a = Rational(1,2)
        a -= Rational(1,3)
        self.assertEqual(Rational(1,6), a)

    def testMul(self):
        self.assertEqual(1, Rational(2,3) * Rational(3,2))
        self.assertEqual(Rational(26,18), Rational(13,18) * 2)
        self.assertEqual(500000000000000000000000000000000000000,
            1000000000000000000000000000000000000000 * Rational(1,2))
        self.assertEqual(Rational(1, 36), Rational(1,2) * Rational(1,3) * Rational(1,6))
        self.assertEqual(Rational(1,4), Rational(1,2) * 0.5)
        self.assertEqual(Rational(1,4), 0.5 * Rational(1,2))

    def testImul(self):
        a = Rational(1,2)
        a *= Rational(1,3)
        self.assertEqual(Rational(1,6), a)

    def testDiv(self):
        self.assertEqual(Rational(4,9), Rational(2,3) / Rational(3,2))
        self.assertEqual(Rational(13,36), Rational(13,18) / 2)
        self.assertEqual(2000000000000000000000000000000000000000,
            1000000000000000000000000000000000000000 / Rational(1,2))
        self.assertEqual(9, Rational(1,2) / Rational(1,3) / Rational(1,6))
        self.assertEqual(1, Rational(1,2) / 0.5)
        self.assertEqual(1, 0.5 / Rational(1,2))

    def testIdiv(self):
        a = Rational(1,2)
        a /= Rational(1,3)
        self.assertEqual(Rational(3,2), a)

    def testPow(self):
        self.assertEqual(Rational(2**4, 3**4), Rational(2,3) ** 4)
        self.assertEqual(Rational(3,2), Rational(2,3) ** (-1))

    def testIpow(self):
        a = Rational(1,2)
        a **= 3
        self.assertEqual(Rational(1,8), a)
        a **= -1
        self.assertEqual(8, a)

    def testLt(self):
        self.assert_(Rational(5,7) < Rational(3,4))
        self.failIf(Rational(3,4) < Rational(5,7))
        self.failIf(Rational(3,4) < Rational(3,4))
        self.assert_(Rational(132,133) < 1)
        self.assert_(Rational(-13,12) < -1L)
        self.assert_(1 > Rational(132,133))
        self.assert_(Rational(132,133) < 1.000001)

    def testLe(self):
        self.assert_(Rational(5,7) <= Rational(3,4))
        self.failIf(Rational(3,4) <= Rational(5,7))
        self.assert_(Rational(3,4) <= Rational(3,4))
        self.assert_(Rational(132,133) <= 1)
        self.assert_(Rational(-13,12) <= -1L)
        self.assert_(1 >= Rational(132,133))

    def testEq(self):
        self.assert_(Rational(1,2) == Rational(1,2))
        self.assert_(Rational(-1,2) == Rational(-1,2))
        self.assert_(Rational(4,2) == 2)
        self.assert_(2L == Rational(14,7))
        self.failIf(Rational(3,5) == Rational(27,46))

    def testNe(self):
        self.assert_(Rational(1,2) != Rational(1,3))
        self.assert_(Rational(1,2) != Rational(-1,2))
        self.failIf(Rational(1,2) != Rational(1,2))

    def testGt(self):
        self.assert_(Rational(3,4) > Rational(5,7))
        self.failIf(Rational(5,7) > Rational(3,4))
        self.failIf(Rational(3,4) > Rational(3,4))
        self.assert_(Rational(13,12) > 1)
        self.assert_(Rational(-11,12) > -1L)
        self.assert_(1 < Rational(134,133))

    def testGe(self):
        self.assert_(Rational(3,4) >= Rational(5,7))
        self.failIf(Rational(5,7) >= Rational(3,4))
        self.assert_(Rational(3,4) >= Rational(3,4))
        self.assert_(Rational(13,12) >= 1)
        self.assert_(Rational(-11,12) >= -1L)
        self.assert_(1 <= Rational(134,133))

    def testLong(self):
        self.assert_(1 == long(Rational(13,12)))
        self.assert_(0 == long(Rational(12,13)))
        self.assert_(-1 == long(Rational(-1,14)))

    def testInt(self):
        self.assert_(1 == int(Rational(13,12)))
        self.assert_(0 == int(Rational(12,13)))
        self.assert_(-1 == int(Rational(-1,14)))

    def testTrim(self):
        self.assertEqual(Rational(1,3), Rational(333,1000).trim(5))
        self.assertEqual(Rational(13,21), Rational(34,55).trim(33))
        self.assertEqual(Rational(21,34), Rational(34,55).trim(34))

    def testExpand(self):
        self.assertEqual(Rational(-33,100), Rational(-1, 3).expand(10,100))

    def testFloat(self):
        self.assert_(isinstance(float(Rational(1,4)), float))
        self.assertEqual(0.25, float(Rational(1,4)))

    def testDecimalString(self):
        self.assertEqual("0.25000", Rational(1,4).decimalString(5))
        self.assertEqual("0.33333", Rational(1,3).decimalString(5))

    def testNonzero(self):
        self.failUnless(Rational(1,1))
        self.failIf(Rational(0,1))

    def testHash(self):
        self.assert_(hash(Rational(1,2)))
        self.assertEqual(hash(Rational(1)), hash(Rational(1)))
        self.assertNotEqual(hash(Rational(1)), hash(Rational(2)))
        self.assertNotEqual(hash(Rational(1,2)), hash(Rational(2,3)))
        self.assertEqual(hash(Rational(3,111)), hash(Rational(36,1332)))


class IntegerTest(unittest.TestCase):
    def setUp(self):
        self.three = Integer(3)

    def testMul(self):
        self.assertEqual(24, self.three * 8)
        self.assertEqual([0,0,0], self.three * [0])
        self.assertEqual((0,0,0), self.three * (0,))
        self.assertEqual(Rational(6,5), self.three * Rational(2,5))

    def testRmul(self):
        self.assertEqual(24, 8 * self.three)
        self.assertEqual([0,0,0], [0] * self.three)
        self.assertEqual((0,0,0), (0,) * self.three)

    def testRmod(self):
        self.assertEqual(1, 4 % self.three)

    def testTruediv(self):
        self.assertEqual(Rational(1, 3), 1 / self.three)
        self.assertEqual(Rational(2, 1), 2 / Integer(1))
        self.assertEqual(Rational, type(2 / Integer(1)))

    def testPow(self):
        self.assertEqual(25, pow(5, Integer(2)))
        self.assertEqual(1, pow(self.three, 4, 5))
        # return Rational when index is negative
        self.assertEqual(Rational(1, 2), pow(Integer(2), -1))
        # ternary pow doesn't call __rpow__, and just fails.
        self.assertRaises(TypeError, pow, 3, Integer(4), 5)
        self.assertRaises(TypeError, pow, 3, 4, Integer(5))
        # raise TypeError when index is negative and modulus is given
        self.assertRaises(TypeError, pow, Integer(2), -1, 5)

    def testGetRing(self):
        self.assertEqual(theIntegerRing, self.three.getRing())

    def testNonzero(self):
        self.failUnless(Integer(1))
        self.failIf(Integer(0))

    def testHash(self):
        self.assert_(hash(Integer(12)))
        self.assertEqual(hash(Integer(1)), hash(Integer(1)))
        self.assertNotEqual(hash(Integer(1)), hash(Integer(2)))


class IntegerRingTest(unittest.TestCase):
    def testContains(self):
        self.assert_(1 in theIntegerRing)
        self.assert_(1L in theIntegerRing)
        self.assert_(Integer(1) in theIntegerRing)
        self.assert_(Rational(1,2) not in theIntegerRing)
        self.assert_((1,) not in theIntegerRing)

    def testGetQuotientField(self):
        self.assert_(theRationalField is theIntegerRing.getQuotientField())

    def testIssubring(self):
        self.assert_(theIntegerRing.issubring(theRationalField))
        self.assert_(theIntegerRing.issubring(theIntegerRing))

    def testIssuperring(self):
        self.failIf(theIntegerRing.issuperring(theRationalField))
        self.assert_(theIntegerRing.issuperring(theIntegerRing))

    def testProperties(self):
        self.assert_(theIntegerRing.isdomain())
        self.assert_(theIntegerRing.isnoetherian())
        self.assert_(theIntegerRing.iseuclidean())
        self.assert_(theIntegerRing.isufd())
        self.assert_(theIntegerRing.ispid())
        self.failIf(theIntegerRing.isfield())

    def testGcd(self):
        self.assertEqual(1, theIntegerRing.gcd(1, 2))
        self.assertEqual(2, theIntegerRing.gcd(2, 4))
        self.assertEqual(10, theIntegerRing.gcd(0, 10))
        self.assertEqual(10, theIntegerRing.gcd(10, 0))
        self.assertEqual(1, theIntegerRing.gcd(13, 21))

    def testLcm(self):
        self.assertEqual(2, theIntegerRing.lcm(1, 2))
        self.assertEqual(4, theIntegerRing.lcm(2, 4))
        self.assertEqual(0, theIntegerRing.lcm(0, 10))
        self.assertEqual(0, theIntegerRing.lcm(10, 0))
        self.assertEqual(273, theIntegerRing.lcm(13, 21))

    def testExtGcd(self):
        self.assertEqual((1, 0, 1), theIntegerRing.extgcd(1, 2))

    def testConstants(self):
        self.assertEqual(1, theIntegerRing.one)
        self.failUnless(isinstance(theIntegerRing.one, Integer))
        self.assertEqual(0, theIntegerRing.zero)
        self.failUnless(isinstance(theIntegerRing.zero, Integer))

    def testStrings(self):
        # str
        self.assertEqual("Z", str(theIntegerRing))
        # repr
        self.assertEqual("IntegerRing()", repr(theIntegerRing))

    def testHash(self):
        dictionary = {}
        dictionary[theIntegerRing] = 1
        self.assertEqual(1, dictionary[IntegerRing()])


class RationalFieldTest(unittest.TestCase):
    def testContains(self):
        self.assert_(1 in theRationalField)
        self.assert_(1L in theRationalField)
        self.assert_(Integer(1) in theRationalField)
        self.assert_(Rational(1,2) in theRationalField)
        self.assert_(3.14 not in theRationalField)
        self.assert_((1,2) not in theRationalField)

    def testGetQuotientField(self):
        self.assert_(theRationalField is theRationalField.getQuotientField())

    def testIssubring(self):
        self.assert_(theRationalField.issubring(theRationalField))
        self.failIf(theRationalField.issubring(theIntegerRing))

    def testIssuperring(self):
        self.assert_(theRationalField.issuperring(theRationalField))
        self.assert_(theRationalField.issuperring(theIntegerRing))

    def testProperties(self):
        self.assert_(theRationalField.isfield())
        self.assert_(theRationalField.isdomain())

    def testConstants(self):
        self.assertEqual(1, theRationalField.one)
        self.failUnless(isinstance(theRationalField.one, Rational))
        self.assertEqual(0, theRationalField.zero)
        self.failUnless(isinstance(theRationalField.zero, Rational))

    def testStrings(self):
        # str
        self.assertEqual("Q", str(theRationalField))
        # repr
        self.assertEqual("RationalField()", repr(theRationalField))

    def testHash(self):
        dictionary = {}
        dictionary[theRationalField] = 1
        self.assertEqual(1, dictionary[RationalField()])


class IntegerIfIntOrLongTest (unittest.TestCase):
    def testInt(self):
        b = IntegerIfIntOrLong(1)
        self.assert_(isinstance(b, Integer))

    def testLong(self):
        b = IntegerIfIntOrLong(1L)
        self.assert_(isinstance(b, Integer))

    def testRational(self):
        b = IntegerIfIntOrLong(Rational(1,2))
        self.failIf(isinstance(b, Integer))
        self.assert_(isinstance(b, Rational))

    def testTuple(self):
        s = IntegerIfIntOrLong((1,1L))
        self.assert_(isinstance(s, tuple))
        for i in s:
            self.assert_(isinstance(i, Integer))

    def testList(self):
        s = IntegerIfIntOrLong([1,1L])
        self.assert_(isinstance(s, list))
        for i in s:
            self.assert_(isinstance(i, Integer))

    def testListOfTuple(self):
        ss = IntegerIfIntOrLong([(1,1L),(2L,2)])
        self.assert_(isinstance(ss, list))
        for s in ss:
            self.assert_(isinstance(s, tuple))
            for i in s:
                self.assert_(isinstance(i, Integer))


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
