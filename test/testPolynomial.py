import unittest
from polynomial import *

# data for debugging

a = OneVariableDensePolynomial([1,1],"x")

b = OneVariableDensePolynomial([1,-2,3,-4],"x")

c = OneVariableDensePolynomial([1,-1,-2],"y")

d = OneVariableDensePolynomial([1,1,2],"y")

e = OneVariableDensePolynomial([0,1,2,3,4],"z")

f = MultiVariableSparsePolynomial({(0,0):1,(1,0):2,(2,0):3,(1,1):4,(0,3):5},["x","z"])

g = MultiVariableSparsePolynomial({(0,0,0):1,(1,0,0):-2,(1,0,3):3,(1,1,1):-4,(0,2,1):5,(2,2,2):-6},["y","z","x"])

h = OneVariableDensePolynomial([rational.Rational(1,2),rational.Rational(7,8),rational.Rational(1,13)],"x")

i =  OneVariableDensePolynomial([rational.Rational(1,1),rational.Rational(0,4),rational.Rational(2,4),rational.Rational(5,2)],"x")

j =  OneVariableDensePolynomial([rational.Rational(3,2),rational.Rational(9,4)],"y")

k = OneVariableSparsePolynomial({(1,):1},["x"])

class IntegerPolynomialTest(unittest.TestCase):
    def setUp(self):
        self.a = OneVariableDensePolynomial([1,1],"x")
        self.k = OneVariableSparsePolynomial({(1,):1},["x"])

    def testAdd(self):
        sx = OneVariableSparsePolynomial({(1,):1},["x"])
        sum_1 = OneVariableDensePolynomial([2,-1,3,-4],"x")
        sum_2 = MultiVariableSparsePolynomial({(0,0,0):2,(1,0,0):1,(0,1,0):-2,(3,1,0):3,(0,0,1):1,(1,1,1):-4,(0,0,2):2,(1,0,2):5,(2,2,2):-6,(0,0,3):3,(0,0,4):4},["x","y","z"])
        sum_3 = OneVariableSparsePolynomial({(1,):2},["x"])
        assert self.a + b == sum_1
        assert self.a + e + g == sum_2
        assert sum_3 == sx + sx

    def testSub(self):
        sub_1 = OneVariableDensePolynomial([0,2,4],"y")
        sub_2 = MultiVariableSparsePolynomial({(0,0,0):-1,(1,0,0):1,(2,0,0):3,(0,1,0):2,(3,1,0):-3,(1,0,1):4,(1,1,1):4,(1,0,2):-5,(2,2,2):6,(0,0,3):5},["x","y","z"])
        assert d - c == sub_1
        assert f - g - self.a == sub_2

    def testMul(self):
        mul_1 = OneVariableDensePolynomial([1,0,-1,-4,-4],"y")
        mul_2 = MultiVariableSparsePolynomial({(0,0,0):1,(1,0,0):2,(2,0,0):3,(0,1,0):-1,(1,1,0):-2,(2,1,0):-3,(0,2,0):-2,(1,2,0):-4,(2,2,0):-6,(1,0,1):4,(1,1,1):-4,(1,2,1):-8,(0,0,3):5,(0,1,3):-5,(0,2,3):-10},["x","y","z"])
        mul_3 = OneVariableDensePolynomial([0,1,1],"x")
        assert c * d == mul_1
        assert c * f == mul_2
        assert self.k * self.a == mul_3 #local variable 'return_variable' referenced before assignment

    def testScalarMul(self):
        mul_1 = OneVariableDensePolynomial([0,3,6,9,12],"z")
        mul_2 = MultiVariableSparsePolynomial({(0,0,0):-5,(0,1,0):10,(3,1,0):-15,(1,1,1):20,(1,0,2):-25,(2,2,2):30},["x","y","z"])
        assert e * 3 == mul_1
        assert g * (-5) == mul_2

    def testDifferentiate(self):
        deff_1 = OneVariableDensePolynomial([1,4,9,16],"z")
        deff_2 = MultiVariableSparsePolynomial({(2,1,0):9,(0,1,1):-4,(0,0,2):5,(1,2,2):-12},["x","y","z"])
        assert deff_1 == e.differentiate("z")
        assert deff_2 == g.differentiate("x")

    def testCall(self):
        call_1 = 49
        call_2 = OneVariableDensePolynomial([0,1,2,3,4],"y")
        call_3 = 4
        call_4 = OneVariableSparsePolynomial({(0,):9,(1,):-8,(3,):5},["y"])
        call_5 = OneVariableDensePolynomial([-2,-8,-9,-4],"x")
        call_6 = MultiVariableSparsePolynomial({(0,0):6,(1,0):8,(2,0):3,(0,1):4,(1,1):4,(0,3):5},["x","z"])
        call_7 = OneVariableDensePolynomial([6,21,22,5],"x")
        assert b(-2) == call_1
        assert e("y") == call_2
        assert f(x = 2,z = -1) == call_3
        assert f(x = -2,z = "y") == call_4
        assert b(a) == call_5
        assert f(x = a) == call_6
        assert f(z = a) == call_7

    def testGetRing(self):
        Zx = PolynomialRing(rational.theIntegerRing, "x")
        Zy = PolynomialRing(rational.theIntegerRing, "y")
        Zxz = PolynomialRing(rational.theIntegerRing, ("x", "z"))
        assert Zx == b.getRing(), b.getRing()
        assert Zx == a.getRing(), a.getRing()
        assert Zy == c.getRing(), c.getRing()
        assert Zxz == f.getRing(), f.getRing()

    def testEquals(self):
        assert OneVariableSparsePolynomial({(1,):1},["x"]) == OneVariableDensePolynomial([0,1],"x")
        assert OneVariableDensePolynomial([0,1],"x") == OneVariableSparsePolynomial({(1,):1},["x"])

    def testGetitem(self):
        assert 1 == self.a[0]
        assert 1 == k[1]

    def testSetitem(self):
        self.a[0] = 2
        assert 2 == self.a[0]
        self.a[4] = 4
        assert OneVariableDensePolynomial([2,1,0,0,4],"x") == self.a
        self.a[0] = 1
        self.a[4] = 0
        self.a = self.a.adjust()
        self.k[0] = 3
        assert 3 == self.k[0]
        self.k[5] = 4
        assert OneVariableSparsePolynomial({(0,):3,(1,):1,(5,):4},["x"]) == self.k
        self.k[0] = 0
        self.k[5] = 0
        self.k = self.k.adjust()

    def testContent(self):
        assert 1 == self.a.content()

class RationalPolynomialTest(unittest.TestCase):
    def testAdd(self):
        sum_1 = OneVariableDensePolynomial([rational.Rational(3,2),rational.Rational(7,8),rational.Rational(15,26),rational.Rational(5,2)],"x")
        sum_2 = MultiVariableSparsePolynomial({(0,0):2,(1,0):rational.Rational(7,8),(0,1):rational.Rational(9,4),(2,0):rational.Rational(1,13)},["x","y"])
        assert h + i == sum_1
        assert h + j == sum_2

    def testSub(self):
        sub_1 = OneVariableDensePolynomial([rational.Rational(-1,2),rational.Rational(7,8),rational.Rational(-11,26),rational.Rational(-5,2)],"x")
        sub_2 = MultiVariableSparsePolynomial({(0,0):-1,(1,0):rational.Rational(7,8),(0,1):rational.Rational(-9,4),(2,0):rational.Rational(1,13)},["x","y"])
        assert h - i == sub_1
        assert h - j == sub_2

    def testMul(self):
        mul_1 = OneVariableDensePolynomial([rational.Rational(1,2),rational.Rational(7,8),rational.Rational(17,52),rational.Rational(27,16),rational.Rational(463,208),rational.Rational(5,26)],"x")
        mul_2 = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8),(1,1):rational.Rational(63,32),(2,0):rational.Rational(3,26),(2,1):rational.Rational(9,52)},["x","y"])
        assert h * i == mul_1
        assert h * j == mul_2

    def testGetRing(self):
        Qx = PolynomialRing(rational.theRationalField, "x")
        Qy = PolynomialRing(rational.theRationalField, "y")
        Qxy = PolynomialRing(rational.theRationalField, ["x","y"])
        assert Qx == i.getRing()
        assert Qy == j.getRing()
        assert Qxy == (i*j).getRing(), (i*j).getRing()

    def testContent(self):
        assert rational.Rational(1,4) == i.content()

class PolynomialRingTest(unittest.TestCase):
    def setUp(self):
        self.Q = rational.theRationalField
        self.Z = rational.theIntegerRing
        self.Qx = PolynomialRing(self.Q, "x")
        self.Zx = PolynomialRing(self.Z, "x")
        self.Zxz = PolynomialRing(self.Z, ("x", "z"))
        self.Qxz = PolynomialRing(self.Q, ("x", "z"))
        self.QwithXwithY = PolynomialRing(self.Qx, "y")
        self.QwithXandY = PolynomialRing(self.Q, ("x", "y"))

    def testEquals(self):
        assert self.QwithXandY == self.QwithXwithY

    def testGetCoefficientRing(self):
        assert self.Q == self.Qx.getCoefficientRing()
        assert self.Z == self.Zxz.getCoefficientRing(("x","z"))
        assert self.Zx == self.Zxz.getCoefficientRing("z")

    def testIssubring(self):
        assert self.Zx.issubring(self.Zxz)
        assert self.Z.issubring(self.Zx)
        assert self.Z.issubring(self.Zxz)
        assert not self.Q.issubring(self.Zxz)

    def testIssuperring(self):
        assert not self.Zx.issuperring(self.Zxz)
        assert self.Zxz.issuperring(self.Zx)
        assert self.Zxz.issuperring(self.Zxz)
        assert not self.Zxz.issuperring(self.Q)

    def testContains(self):
        assert a in self.Zx
        assert a in self.Zxz
        assert i not in self.Zx
        assert a in self.Qx
        assert 1 in self.Zx

    def testProperties(self):
        assert self.Qx.isufd()
        assert self.Qx.ispid()
        assert self.Qx.iseuclidean()
        assert self.Zx.isufd()
        assert not self.Zx.ispid()
        assert self.QwithXwithY.isnoetherian()
        assert self.QwithXwithY.isufd()
        assert self.QwithXandY.isufd() == self.QwithXwithY.isufd()
        assert not self.QwithXwithY.ispid()
        assert self.QwithXandY.ispid() == self.QwithXwithY.ispid()

    def testGetCommonSuperring(self):
        assert self.Qxz == self.Qx.getCommonSuperring(self.Zxz), self.Qx.getCommonSuperring(self.Zxz)

class PolynomialCompilerTest(unittest.TestCase):
    def setUp(self):
        self.x = OneVariableDensePolynomial([0,1],"x")
        self.y = OneVariableDensePolynomial([0,1],"y")
        self.s = OneVariableDensePolynomial([1,1],"x")
        self.multi = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8)},["x","y"])

    def testOneVariableInteger(self):
        assert self.x == construct("x")
        assert self.x != construct("y")
        assert self.y == construct("y")
        assert self.x != construct("1 + x")
        assert self.s == construct("1 + x")
        assert self.x**2 + 1 == construct("1 + x**2")
        assert self.multi == construct("Q(3,4) + Q(21,16) * x + Q(9,8) * y", {"Q": rational.Rational})

def suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegerPolynomialTest, "test"))
    suite.addTest(unittest.makeSuite(RationalPolynomialTest, "test"))
    suite.addTest(unittest.makeSuite(PolynomialRingTest, "test"))
    suite.addTest(unittest.makeSuite(PolynomialCompilerTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
