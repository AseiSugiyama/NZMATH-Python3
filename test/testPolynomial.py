import unittest
from polynomial import *
import integerResidueClass
from rational import Integer as Int

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

l = OneVariableDensePolynomial([rational.Rational(3,2),rational.Rational(9,8)],"y")

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
        assert self.a == self.a + 0
        assert self.k == self.k + 0

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
        assert self.k * self.a == mul_3

    def testScalarMul(self):
        mul_1 = OneVariableDensePolynomial([0,3,6,9,12],"z")
        mul_2 = MultiVariableSparsePolynomial({(0,0,0):-5,(0,1,0):10,(3,1,0):-15,(1,1,1):20,(1,0,2):-25,(2,2,2):30},["x","y","z"])
        assert e * 3 == mul_1
        assert g * (-5) == mul_2

    def testFloordiv(self):
        assert 0 == self.a // 2
        assert 0 == self.k // 2
        assert 1 == self.a // self.k
        assert c == (c*d) // d
        assert MultiVariableSparsePolynomial({(0, 2): 266240}, ['x', 'y']) == MultiVariableSparsePolynomial({(2, 0): -479232, (0, 4): 266240}, ['x', 'y']) // MultiVariableSparsePolynomial({(0, 2):1}, ['x', 'y'])
        assert 0 == MultiVariableSparsePolynomial({(0, 0): -4096, (2, 0): -479232}, ['x', 'y']) // MultiVariableSparsePolynomial({(0, 2): 1}, ['x', 'y'])
        assert MultiVariableSparsePolynomial({(0, 2): 266240}, ['x', 'y']) == MultiVariableSparsePolynomial({(0, 0): -4096, (2, 0): -479232, (0, 4): 266240}, ['x', 'y']) // MultiVariableSparsePolynomial({(0, 2): 1}, ['x','y'])
        assert 0 == OneVariableSparsePolynomial({(0,): -4096, (2,): -479232, }, ['x']) // MultiVariableSparsePolynomial({(0, 2): 1}, ['x', 'y'])
        # error generated in elliptic
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, ['x', 'y']) // MultiVariableSparsePolynomial({(0, 2): 1}, ['x', 'y'])

    def testMod(self):
        assert self.a == self.a % 2
        assert 1 == self.a % self.k
        # error generated in elliptic
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, ['x', 'y']) % MultiVariableSparsePolynomial({(0, 2): 1}, ['x', 'y'])

    def testTrueDiv(self):
        assert MultiVariableSparsePolynomial({(0, 2): 1, (8, 0): -3}, ['x', 'y']) ==  MultiVariableSparsePolynomial({(0, 4): 1, (8, 2): -3}, ['x', 'y']) / OneVariableSparsePolynomial({(2,):1}, ["y"])
        # error generated in elliptic
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, ['x', 'y']) / MultiVariableSparsePolynomial({(0, 2): 1}, ['x', 'y'])

    def testDivmod(self):
        assert (1,1) == divmod(self.a, self.k)

    def testDifferentiate(self):
        deff_1 = OneVariableDensePolynomial([1,4,9,16],"z")
        deff_2 = MultiVariableSparsePolynomial({(2,1,0):9,(0,1,1):-4,(0,0,2):5,(1,2,2):-12},['x', 'y',"z"])
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
        assert MultiVariableSparsePolynomial({}, ["x", "y"]) == 0

    def testGetitem(self):
        assert 1 == self.a[0]
        assert 0 == self.a[100]
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
        assert 2 == (2*self.a).content()
        assert 1 == self.k.content()

    def testToOneVariableDensePolynomial(self):
        f = MultiVariableDensePolynomial([1,OneVariableDensePolynomial([1,2],"y")],"z")
        self.assertRaises(ValueError, f.toOneVariableDensePolynomial)

class RationalPolynomialTest(unittest.TestCase):
    def testAdd(self):
        sum_1 = OneVariableDensePolynomial([rational.Rational(3,2),rational.Rational(7,8),rational.Rational(15,26),rational.Rational(5,2)],"x")
        sum_2 = MultiVariableSparsePolynomial({(0,0):2,(1,0):rational.Rational(7,8),(0,1):rational.Rational(9,4),(2,0):rational.Rational(1,13)},['x', 'y'])
        sum_3 = OneVariableDensePolynomial([rational.Rational(3,2), 1], "x")
        assert h + i == sum_1
        assert h + j == sum_2
        assert a + rational.Rational(1,2) == sum_3
    def testSub(self):
        sub_1 = OneVariableDensePolynomial([rational.Rational(-1,2),rational.Rational(7,8),rational.Rational(-11,26),rational.Rational(-5,2)],"x")
        sub_2 = MultiVariableSparsePolynomial({(0,0):-1,(1,0):rational.Rational(7,8),(0,1):rational.Rational(-9,4),(2,0):rational.Rational(1,13)},['x', 'y'])
        assert h - i == sub_1
        assert h - j == sub_2

    def testMul(self):
        mul_1 = OneVariableDensePolynomial([rational.Rational(1,2),rational.Rational(7,8),rational.Rational(17,52),rational.Rational(27,16),rational.Rational(463,208),rational.Rational(5,26)],"x")
        mul_2 = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8),(1,1):rational.Rational(63,32),(2,0):rational.Rational(3,26),(2,1):rational.Rational(9,52)},['x', 'y'])
        assert h * i == mul_1
        assert h * j == mul_2

    def testFloordiv(self):
        assert 2 == j//l 
        assert rational.Rational(73, 104) == OneVariableDensePolynomial([rational.Rational(1,2), rational.Rational(73, 104)], "x") // OneVariableDensePolynomial([rational.Rational(1,1), rational.Rational(1,1)], "x")

    def testMod(self):
        assert rational.Rational(-3,2) == (j % l).coefficient[0]
        assert rational.Rational(-21, 104) == (OneVariableDensePolynomial([rational.Rational(1,2), rational.Rational(73, 104)], "x") % a).coefficient[0]
                                               
    def testGetRing(self):
        Qx = PolynomialRing(rational.theRationalField, "x")
        Qy = PolynomialRing(rational.theRationalField, "y")
        Qxy = PolynomialRing(rational.theRationalField, ['x', 'y'])
        assert Qx == i.getRing()
        assert Qy == j.getRing()
        assert Qxy == (i*j).getRing(), (i*j).getRing()

    def testContent(self):
        assert rational.Rational(1,2) == i.content()

class IntegerResidueClassPolynomialTest(unittest.TestCase):
    def setUp(self):
        self.f1 = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(3,5), integerResidueClass.IntegerResidueClass(1,5)], "x")
        self.f2 = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(4,5), integerResidueClass.IntegerResidueClass(1,5), integerResidueClass.IntegerResidueClass(1,5)], "x")

    def testAdd(self):
        sum = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(2,5), integerResidueClass.IntegerResidueClass(2,5), integerResidueClass.IntegerResidueClass(1,5)], "x")
        assert sum == (self.f1 + self.f2)

    def testEquals(self):
        assert self.f1 == self.f1

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
        class Domain:
            def isdomain(self):
                return True
            def __getattr__(self, attr):
                if attr in ['isfield', 'iseuclidean', 'ispid', 'isufd', 'isnoetherian']:
                    return lambda : False
        domainPolyRing = PolynomialRing(Domain(), "x")
        assert domainPolyRing.isdomain()

    def testGetCommonSuperring(self):
        assert self.Qxz == self.Qx.getCommonSuperring(self.Zxz), self.Qx.getCommonSuperring(self.Zxz)

    def testGcd(self):
        assert 1 == self.Qx.gcd(h,a)
        assert 1 == self.Zx.gcd(a,b)

class PolynomialCompilerTest(unittest.TestCase):
    def setUp(self):
        self.x = OneVariableDensePolynomial([0,1],"x")
        self.y = OneVariableDensePolynomial([0,1],"y")
        self.s = OneVariableDensePolynomial([1,1],"x")
        self.multi = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8)},['x', 'y'])

    def testOneVariableInteger(self):
        assert self.x == construct("x")
        assert self.x != construct("y")
        assert self.y == construct("y")
        assert self.x != construct("1 + x")
        assert self.s == construct("1 + x")
        assert self.x**2 + 1 == construct("1 + x**2")
        assert self.multi == construct("Q(3,4) + Q(21,16) * x + Q(9,8) * y", {"Q": rational.Rational})

class PolynomialGCDTest(unittest.TestCase):
    def setUp(self):
        import matrix
        self.f = OneVariableDensePolynomial([1,2,3,4,5], "x")
        self.g = OneVariableDensePolynomial([7,8,9], "x")
        self.correctResult = matrix.Matrix(6,6,
                                                [1,2,3,4,5,0]
                                            +   [0,1,2,3,4,5]
                                            +   [7,8,9,0,0,0]
                                            +   [0,7,8,9,0,0]
                                            +   [0,0,7,8,9,0]
                                            +   [0,0,0,7,8,9] ).determinant()
        self.f2 = OneVariableDensePolynomial([-3,-2,2,2,1], "x")
        self.g2 = OneVariableDensePolynomial([-6,-5,2,5,4], "x")
                                            
    def testResultant(self):
        assert resultant(self.f, self.g) == self.correctResult

    def testPseudoDivision(self): 
        A = self.f
        B = self.g

        d = B[B.degree()]
        Q, R = pseudoDivision(A, B)
#        print "end"
#        print "Q=", Q
#        print "R=", R
#        print pseudoDivision(f, g)
        assert d**(A.degree()-B.degree()+1) * A == B * Q + R

    def testSubResultantGCD(self):
        assert subResultantGCD(self.f2, self.g2) == OneVariableDensePolynomial([-1,0,1], "x")

class SquareFreeDecompositionChar0Test(unittest.TestCase):
    def setUp(self):
        self.pow1 = OneVariableDensePolynomial([1,1],"x")
        self.pow1pow2 = OneVariableDensePolynomial([1,2,2,2,1],"x")
        self.pow1pow3 = OneVariableDensePolynomial([8,20,18,7,1],"x")

    def testSuccess(self):
        assert self.pow1.squareFreeDecomposition()
        assert self.pow1pow2.squareFreeDecomposition()
        assert self.pow1pow3.squareFreeDecomposition()
        result1 = {1: self.pow1}
        result2 = {1: OneVariableDensePolynomial([1,0,1],"x"),
                   2: OneVariableDensePolynomial([1,1],"x")}
        result3 = {1: OneVariableDensePolynomial([1,1],"x"),
                   3: OneVariableDensePolynomial([2,1],"x")}
        assert result1 == self.pow1.squareFreeDecomposition()
        assert result2 == self.pow1pow2.squareFreeDecomposition(), self.pow1pow2.squareFreeDecomposition()
        assert result3 == self.pow1pow3.squareFreeDecomposition(), self.pow1pow3.squareFreeDecomposition()

class FiniteFieldPolynomialTest(unittest.TestCase):
    def setUp(self):
        import finitefield
        F2 = lambda x: finitefield.FinitePrimeFieldElement(x, 2)
        self.mapF2 = lambda seq: map(F2,seq)
        self.f = OneVariableDensePolynomial(self.mapF2([1,1]),"x")
        self.g = OneVariableDensePolynomial(self.mapF2([1,0,1]),"x")

    def testAdd(self):
        result = OneVariableDensePolynomial(self.mapF2([0,1,1]),"x")
        assert result == self.f + self.g
        assert self.f.getRing() == (self.f + self.g).getRing()
        assert 0 == self.f + self.f

    def testSub(self):
        result = OneVariableDensePolynomial(self.mapF2([0,1,1]),"x")
        assert result == self.f - self.g
        assert self.f.getRing() == (self.f - self.g).getRing()

    def testMul(self):
        result = OneVariableDensePolynomial(self.mapF2([1,1,1,1]),"x")
        assert result == self.f * self.g
        assert self.f.getRing() == (self.f * self.g).getRing()
        assert self.f == 1 * self.f
        assert 0 == 0 * self.f

    def testMod(self):
        assert self.f == self.f % self.g

    def testFloordiv(self):
        assert 0 == self.f // self.g

    def testDifferentiate(self):
        import finitefield
        result = finitefield.FinitePrimeFieldElement(1,2)
        assert result == self.f.differentiate(self.f.variable)
        assert 0 == self.g.differentiate(self.g.variable)

    def testGcd(self):
        assert self.f == self.f.getRing().gcd(self.f, self.g)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegerPolynomialTest, "test"))
    suite.addTest(unittest.makeSuite(RationalPolynomialTest, "test"))
    suite.addTest(unittest.makeSuite(IntegerResidueClassPolynomialTest, "test"))
    suite.addTest(unittest.makeSuite(PolynomialRingTest, "test"))
    suite.addTest(unittest.makeSuite(PolynomialCompilerTest, "test"))
    suite.addTest(unittest.makeSuite(PolynomialGCDTest, "test"))
    suite.addTest(unittest.makeSuite(SquareFreeDecompositionChar0Test, "test"))
    suite.addTest(unittest.makeSuite(FiniteFieldPolynomialTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
