import unittest
from rational import Rational

class RationalTest (unittest.TestCase):
    def testInit(self):
        assert str(Rational(1,2)) == "1/2"
        assert str(Rational(2)) == "2/1"
        assert str(Rational(2L)) == "2/1"
        assert str(Rational(Rational(1,2))) == "1/2"

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

    def testSub(self):
        assert Rational(2,3) - Rational(3,2) == Rational(-5,6)
        assert Rational(13,18) - 1 == Rational(-5,18)
        assert 1000000000000000000000000000000000000000 - Rational(1,2) == Rational(1999999999999999999999999999999999999999,2)
        assert Rational(1,2) - Rational(1,3) - Rational(1,6) == 0

    def testMul(self):
        assert Rational(2,3) * Rational(3,2) == 1
        assert Rational(13,18) * 2 == Rational(26,18)
        assert 1000000000000000000000000000000000000000 * Rational(1,2) == 500000000000000000000000000000000000000
        assert Rational(1,2) * Rational(1,3) * Rational(1,6) == Rational(1, 36)

    def testDiv(self):
        assert Rational(2,3) / Rational(3,2) == Rational(4,9)
        assert Rational(13,18) / 2 == Rational(13,36)
        assert 1000000000000000000000000000000000000000 / Rational(1,2) == 2000000000000000000000000000000000000000
        assert Rational(1,2) / Rational(1,3) / Rational(1,6) == 9

    def testLt(self):
        assert Rational(5,7) < Rational(3,4)
        assert not (Rational(3,4) < Rational(5,7))
        assert not (Rational(3,4) < Rational(3,4))
        assert Rational(132,133) < 1
        assert Rational(-13,12) < -1L
        assert 1 > Rational(132,133)

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

def suite():
    suite = unittest.makeSuite(RationalTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
