import unittest
from rational import *
import finitefield
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
        assert str(+Rational(2,4)) == "1/2"
        assert str(+Rational(-3,4)) == "-3/4"

    def testNeg(self):
        assert -Rational(2,4) == Rational(-1,2)
        assert str(-Rational(-3,4)) == "3/4"

    def testAdd(self):
        assert Rational(2,3) + Rational(3,2) == Rational(13,6)
        assert Rational(13,18) + 1 == Rational(31,18)
        assert 1000000000000000000000000000000000000000 + Rational(1,2) == Rational(2000000000000000000000000000000000000001,2)
        assert Rational(1,2) + Rational(1,3) + Rational(1,6) == 1
        assert Rational(1,2) + 0.5 == 1
        assert 0.5 + Rational(1,2) == 1

    def testIadd(self):
        a = Rational(1,2)
        a += Rational(1,3)
        assert Rational(5,6) == a

    def testSub(self):
        assert Rational(2,3) - Rational(3,2) == Rational(-5,6)
        assert Rational(13,18) - 1 == Rational(-5,18)
        assert 1000000000000000000000000000000000000000 - Rational(1,2) == Rational(1999999999999999999999999999999999999999,2)
        assert Rational(1,2) - Rational(1,3) - Rational(1,6) == 0
        assert Rational(1,2) - 0.5 == 0
        assert 0.5 - Rational(1,2) == 0

    def testIsub(self):
        a = Rational(1,2)
        a -= Rational(1,3)
        assert Rational(1,6) == a

    def testMul(self):
        assert Rational(2,3) * Rational(3,2) == 1
        assert Rational(13,18) * 2 == Rational(26,18)
        assert 1000000000000000000000000000000000000000 * Rational(1,2) == 500000000000000000000000000000000000000
        assert Rational(1,2) * Rational(1,3) * Rational(1,6) == Rational(1, 36)
        assert Rational(1,2) * 0.5 == Rational(1,4)
        assert 0.5 * Rational(1,2) == Rational(1,4)

    def testImul(self):
        a = Rational(1,2)
        a *= Rational(1,3)
        assert Rational(1,6) == a

    def testDiv(self):
        assert Rational(2,3) / Rational(3,2) == Rational(4,9)
        assert Rational(13,18) / 2 == Rational(13,36)
        assert 1000000000000000000000000000000000000000 / Rational(1,2) == 2000000000000000000000000000000000000000
        assert Rational(1,2) / Rational(1,3) / Rational(1,6) == 9
        assert Rational(1,2) / 0.5 == 1
        assert 0.5 / Rational(1,2) == 1

    def testIdiv(self):
        a = Rational(1,2)
        a /= Rational(1,3)
        assert Rational(3,2) == a

    def testPow(self):
        assert Rational(2,3) ** 4 == Rational(2**4, 3**4)
        assert Rational(2,3) ** (-1) == Rational(3,2)

    def testIpow(self):
        a = Rational(1,2)
        a **= 3
        assert Rational(1,8) == a
        a **= -1
        assert 8 == a

    def testLt(self):
        assert Rational(5,7) < Rational(3,4)
        assert not (Rational(3,4) < Rational(5,7))
        assert not (Rational(3,4) < Rational(3,4))
        assert Rational(132,133) < 1
        assert Rational(-13,12) < -1L
        assert 1 > Rational(132,133)
        assert Rational(132,133) < 1.000001

    def testLe(self):
        assert Rational(5,7) <= Rational(3,4)
        assert not (Rational(3,4) <= Rational(5,7))
        assert Rational(3,4) <= Rational(3,4)
        assert Rational(132,133) <= 1
        assert Rational(-13,12) <= -1L
        assert 1 >= Rational(132,133)

    def testEq(self):
        assert Rational(1,2) == Rational(1,2)
        assert Rational(-1,2) == Rational(-1,2)
        assert Rational(4,2) == 2
        assert 2L == Rational(14,7)
        assert not (Rational(3,5) == Rational(27,46))

    def testNe(self):
        assert Rational(1,2) != Rational(1,3)
        assert Rational(1,2) != Rational(-1,2)
        assert not (Rational(1,2) != Rational(1,2))

    def testGt(self):
        assert Rational(3,4) > Rational(5,7)
        assert not (Rational(5,7) > Rational(3,4))
        assert not (Rational(3,4) > Rational(3,4))
        assert Rational(13,12) > 1
        assert Rational(-11,12) > -1L
        assert 1 < Rational(134,133)

    def testGe(self):
        assert Rational(3,4) >= Rational(5,7)
        assert not (Rational(5,7) >= Rational(3,4))
        assert Rational(3,4) >= Rational(3,4)
        assert Rational(13,12) >= 1
        assert Rational(-11,12) >= -1L
        assert 1 <= Rational(134,133)

    def testLong(self):
        assert 1 == long(Rational(13,12))
        assert 0 == long(Rational(12,13))
        assert -1 == long(Rational(-1,14))

    def testInt(self):
        assert 1 == int(Rational(13,12))
        assert 0 == int(Rational(12,13))
        assert -1 == int(Rational(-1,14))

    def testTrim(self):
        assert Rational(1,3) == Rational(333,1000).trim(5)
        assert Rational(13,21) == Rational(34,55).trim(33)
        assert Rational(21,34) == Rational(34,55).trim(34)

    def testExpand(self):
        assert Rational(-33,100) == Rational(-1, 3).expand(10,100)

    def testFloat(self):
        assert 0.25 == float(Rational(1,4))

    def testDecimalString(self):
        assert "0.25000" == Rational(1,4).decimalString(5)
        assert "0.33333" == Rational(1,3).decimalString(5)

    def testNonzero(self):
        self.failUnless(Rational(1,1))
        self.failIf(Rational(0,1))


class IntegerTest(unittest.TestCase):
    def setUp(self):
        self.three = Integer(3)

    def testMul(self):
        assert 24 == self.three * 8
        assert [0,0,0] == self.three * [0]
        assert (0,0,0) == self.three * (0,)
        assert Rational(6,5) == self.three * Rational(2,5)

    def testRmul(self):
        assert 24 == 8 * self.three
        assert [0,0,0] == [0] * self.three
        assert (0,0,0) == (0,) * self.three

    def testRmod(self):
        assert 1 == 4 % self.three

    def testTruediv(self):
        assert Rational(1,3) == 1 / self.three

    def testGetRing(self):
        assert theIntegerRing == self.three.getRing()

    def testNonzero(self):
        self.failUnless(Integer(1))
        self.failIf(Integer(0))


class IntegerRingTest(unittest.TestCase):
    def testContains(self):
        assert 1 in theIntegerRing
        assert 1L in theIntegerRing
        assert Integer(1) in theIntegerRing
        assert Rational(1,2) not in theIntegerRing
        assert (1,) not in theIntegerRing

    def testGetQuotientField(self):
        assert theRationalField is theIntegerRing.getQuotientField()

    def testIssubring(self):
        assert theIntegerRing.issubring(theRationalField)
        assert theIntegerRing.issubring(theIntegerRing)

    def testIssuperring(self):
        assert not theIntegerRing.issuperring(theRationalField)
        assert theIntegerRing.issuperring(theIntegerRing)

    def testProperties(self):
        assert theIntegerRing.isdomain()
        assert theIntegerRing.isnoetherian()
        assert theIntegerRing.iseuclidean()
        assert theIntegerRing.isufd()
        assert theIntegerRing.ispid()
        assert not theIntegerRing.isfield()

    def testGcd(self):
        assert theIntegerRing.gcd(1, 2) == 1
        assert theIntegerRing.gcd(2, 4) == 2
        assert theIntegerRing.gcd(0, 10) == 10
        assert theIntegerRing.gcd(10, 0) == 10
        assert theIntegerRing.gcd(13, 21) == 1

    def testLcm(self):
        assert theIntegerRing.lcm(1, 2) == 2
        assert theIntegerRing.lcm(2, 4) == 4
        assert theIntegerRing.lcm(0, 10) == 0
        assert theIntegerRing.lcm(10, 0) == 0
        assert theIntegerRing.lcm(13, 21) == 273

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


class RationalFieldTest(unittest.TestCase):
    def testContains(self):
        assert 1 in theRationalField
        assert 1L in theRationalField
        assert Integer(1) in theRationalField
        assert Rational(1,2) in theRationalField
        assert 3.14 not in theRationalField
        assert (1,2) not in theRationalField

    def testGetQuotientField(self):
        assert theRationalField is theRationalField.getQuotientField()

    def testIssubring(self):
        assert theRationalField.issubring(theRationalField)
        assert not theRationalField.issubring(theIntegerRing)

    def testIssuperring(self):
        assert theRationalField.issuperring(theRationalField)
        assert theRationalField.issuperring(theIntegerRing)

    def testProperties(self):
        assert theRationalField.isfield()
        assert theRationalField.isdomain()

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


class IntegerIfIntOrLongTest (unittest.TestCase):
    def testInt(self):
        b = IntegerIfIntOrLong(1)
        assert isinstance(b, Integer)

    def testLong(self):
        b = IntegerIfIntOrLong(1L)
        assert isinstance(b, Integer)

    def testRational(self):
        b = IntegerIfIntOrLong(Rational(1,2))
        assert not isinstance(b, Integer)
        assert isinstance(b, Rational)

    def testTuple(self):
        s = IntegerIfIntOrLong((1,1L))
        assert isinstance(s, tuple)
        for i in s:
            assert isinstance(i, Integer)

    def testList(self):
        s = IntegerIfIntOrLong([1,1L])
        assert isinstance(s, list)
        for i in s:
            assert isinstance(i, Integer)

    def testListOfTuple(self):
        ss = IntegerIfIntOrLong([(1,1L),(2L,2)])
        assert isinstance(ss, list)
        for s in ss:
            assert isinstance(s, tuple)
            for i in s:
                assert isinstance(i, Integer)


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
