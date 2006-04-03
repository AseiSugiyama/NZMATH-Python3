import unittest
import logging

import nzmath.ring as ring
import nzmath.integerResidueClass as integerResidueClass
from nzmath.polynomial import *

try:
    # Python 2.4 has set type
    set
except NameError:
    # Python 2.3 has Set class in sets
    from sets import Set as set

x, y, z = "xyz"
Z = rational.theIntegerRing
Q = rational.theRationalField

class IntegerOneVariableDensePolynomialTest(unittest.TestCase):
    def setUp(self):
        self.a = OneVariableDensePolynomial([1,1], x, Z)
        self.b = OneVariableDensePolynomial([1,-2,3,-4], x, Z)
        self.c = OneVariableDensePolynomial([1,-1,-2], y, Z)
        self.d = OneVariableDensePolynomial([1,1,2], y, Z)
        self.zero = OneVariableDensePolynomial([], x, Z)

    def testAdd(self):
        sum_1 = OneVariableDensePolynomial([2,-1,3,-4], x)
        sum_2 = OneVariableDensePolynomial([2], y)
        assert sum_1 == self.a + self.b
        assert sum_2 == self.c + self.d
        assert self.a == self.a + 0
        assert self.a == self.a + self.zero

    def testSub(self):
        sub_1 = OneVariableDensePolynomial([0,3,-3,4], x)
        sub_2 = OneVariableDensePolynomial([0,2,4],y)
        assert sub_1 == self.a - self.b
        assert sub_2 == self.d - self.c
        assert self.a == self.a - 0

    def testMul(self):
        mul_1 = OneVariableDensePolynomial([1,0,-1,-4,-4],y)
        assert mul_1 == self.c * self.d
        assert self.zero == self.a * self.zero
        assert self.zero == self.zero * self.a

    def testScalarMul(self):
        mul_1 = OneVariableDensePolynomial([2,2], x)
        mul_2 = OneVariableDensePolynomial([0,3,6,9,12],z)
        assert mul_1 == self.a * 2 == 2 * self.a
        e = OneVariableDensePolynomial([0,1,2,3,4], z)
        assert mul_2 == e * 3
        assert self.zero == self.zero * 3
        assert self.zero == 3 * self.zero

    def testFloordiv(self):
        assert 0 == self.a // 2
        assert self.c == (self.c * self.d) // self.d

    def testMod(self):
        assert self.a == self.a % 2, (self.a, (self.a % 2))

    def testGetitem(self):
        assert 1 == self.a[0]
        assert 0 == self.a[100]

    def testSetitem(self):
        self.a[0] = 2
        assert 2 == self.a[0]
        self.a[4] = 4
        assert OneVariableDensePolynomial([2,1,0,0,4],x) == self.a
        self.a[0] = 1
        self.a[4] = 0

    def testCall(self):
        call_1 = 49
        call_2 = OneVariableDensePolynomial([-2,-8,-9,-4],x)
        call_3 = OneVariableDensePolynomial([1,1], y)
        assert call_1 == self.b(-2)
        assert call_2 == self.b(self.a)
        assert call_3 == self.a(y)

    def testContent(self):
        assert 1 == self.a.content()
        assert 2 == (2*self.a).content()

    def testDifferentiate(self):
        diff_1 = OneVariableDensePolynomial([1], x)
        assert diff_1 == self.a.differentiate(x)
        assert 0 == self.a.differentiate(z)

    def testIntegrate(self):
        integrate_1 = OneVariableDensePolynomial([0, 1, 1], x, Z)
        poly_1 = OneVariableDensePolynomial([1, 2], x, Z)
        assert integrate_1 == poly_1.integrate(x)

    def testGetRing(self):
        Zx = PolynomialRing(Z, x)
        Zy = PolynomialRing(Z, y)
        assert Zx == self.a.getRing(), self.a.getRing()
        assert Zx == self.b.getRing(), self.b.getRing()
        assert Zy == self.c.getRing(), self.c.getRing()

    def testLeadingCoefficient(self):
        self.assertEqual(1, self.a.leadingCoefficient())
        self.assertEqual(-4, self.b.leadingCoefficient())
        self.assertEqual(-2, self.c.leadingCoefficient())
        self.assertEqual(2, self.d.leadingCoefficient())
        self.assertEqual(0, self.zero.leadingCoefficient())


class IntegerOneVariableSparsePolynomialTest (unittest.TestCase):
    def setUp(self):
        self.k = OneVariableSparsePolynomial({(1,):1},[x])
        
    def testAdd(self):
        sum_3 = OneVariableSparsePolynomial({(1,):2},[x])
        assert sum_3 == self.k + self.k
        assert self.k == self.k + 0

    def testSub(self):
        assert self.k == self.k - 0

    def testFloordiv(self):
        assert 0 == self.k // 2

    def testSetitem(self):
        self.k[0] = 3
        assert 3 == self.k[0]
        self.k[5] = 4
        assert OneVariableSparsePolynomial({(0,):3,(1,):1,(5,):4},[x]) == self.k
        self.k[0] = 0
        self.k[5] = 0
        self.k = self.k.copy()

    def testGetitem(self):
        assert 1 == self.k[1]

    def testContent(self):
        assert 1 == self.k.content()

    def testGetRing(self):
        Zx = PolynomialRing(Z, x)
        assert Zx == self.k.getRing(), self.k.getRing()

    def testPow(self):
        assert self.k * self.k == self.k ** 2


class IntegerOneVariablePolynomialsTest(unittest.TestCase):
    def setUp(self):
        self.a = OneVariableDensePolynomial([1,1], x, Z)
        self.k = OneVariableSparsePolynomial({(1,):1},[x])

    def testMul(self):
        mul_3 = OneVariableDensePolynomial([0,1,1],x)
        assert self.k * self.a == mul_3

    def testFloordiv(self):
        assert 1 == self.a // self.k

    def testMod(self):
        assert 1 == self.a % self.k

    def testDivmod(self):
        assert (1,1) == divmod(self.a, self.k)

    def testEquals(self):
        assert OneVariableSparsePolynomial({(1,):1},[x]) == OneVariableDensePolynomial([0,1],x)
        assert OneVariableDensePolynomial([0,1],x) == OneVariableSparsePolynomial({(1,):1},[x])

    def testIntegrate(self):
        integ = OneVariableDensePolynomial([0, 0, rational.Rational(1,2)], x)
        ratk = OneVariableSparsePolynomial({(1,): rational.Integer(1)},[x])
        assert integ == self.k.integrate(x), self.k.integrate(x)
        assert integ == ratk.integrate(x), explicit.integrate(x)

class IntegerMultiVariableSparsePolynomialTest (unittest.TestCase):
    def setUp(self):
        self.f = MultiVariableSparsePolynomial({(0,0):1,(1,0):2,(2,0):3,(1,1):4,(0,3):5},[x,z])
        self.g = MultiVariableSparsePolynomial({(0,0,0):1,(1,0,0):-2,(1,0,3):3,(1,1,1):-4,(0,2,1):5,(2,2,2):-6},[y,z,x])
        
    def testScalarMul(self):
        mul_2 = MultiVariableSparsePolynomial({(0,0,0):-5,(0,1,0):10,(3,1,0):-15,(1,1,1):20,(1,0,2):-25,(2,2,2):30},[x,y,z])
        assert self.g * (-5) == mul_2

    def testFloordiv(self):
        assert MultiVariableSparsePolynomial({(0, 2): 266240}, [x, y]) == MultiVariableSparsePolynomial({(2, 0): -479232, (0, 4): 266240}, [x, y]) // MultiVariableSparsePolynomial({(0, 2):1}, [x, y])
        assert 0 == MultiVariableSparsePolynomial({(0, 0): -4096, (2, 0): -479232}, [x, y]) // MultiVariableSparsePolynomial({(0, 2): 1}, [x, y])
        assert MultiVariableSparsePolynomial({(0, 2): 266240}, [x, y]) == MultiVariableSparsePolynomial({(0, 0): -4096, (2, 0): -479232, (0, 4): 266240}, [x, y]) // MultiVariableSparsePolynomial({(0, 2): 1}, [x,y])
        assert 0 == OneVariableSparsePolynomial({(0,): -4096, (2,): -479232, }, [x]) // MultiVariableSparsePolynomial({(0, 2): 1}, [x, y])
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, [x, y]) // MultiVariableSparsePolynomial({(0, 2): 1}, [x, y])

    def testMod(self):
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, [x, y]) % MultiVariableSparsePolynomial({(0, 2): 1}, [x, y])

    def testTrueDiv(self):
        assert MultiVariableSparsePolynomial({(5, 4): -2903040, (3, 0): 1105920, (5, 0): -7575552, (3, 4): 129024, (7, 4): -715776, (7, 0): 20238336, (10, 4): -155904, (8, 0): 4112640, (10, 0): -22851072, (8, 4): 1707648, (17, 0): -2682720, (12, 4): -6496, (12, 0): -33744384, (14, 0): -16920576, (19, 0): -349920, (14, 4): 192, (21, 0): -17496, (2, 4): 1240064, (0, 0): -4096, (2, 0): -479232, (0, 4): 266240, (4, 4): -39424, (4, 0): 1124352, (6, 0): 608256, (6, 4): -1637888, (24, 0): -729, (9, 0): -18994176, (9, 4): 1311616, (18, 4): 44, (13, 4): -26880, (16, 0): -4685040, (11, 0): -32845824, (18, 0): -991440, (13, 0): -22705920, (16, 4): 456, (11, 4): -19968, (15, 4): -384, (20, 0): -169128, (15, 0): -10264320, (22, 0): -17496, (1, 0): 73728, (1, 4): 358400}, [x, y]) / MultiVariableSparsePolynomial({(0, 2): 1}, [x, y])

    def testDifferentiate(self):
        deff_2 = MultiVariableSparsePolynomial({(2,1,0):9,(0,1,1):-4,(0,0,2):5,(1,2,2):-12},[x, y, z])
        assert deff_2 == self.g.differentiate(x)

    def testGetRing(self):
        Zxz = PolynomialRing(Z, (x, z))
        assert Zxz == self.f.getRing(), self.f.getRing()

    def testEquals(self):
        assert MultiVariableSparsePolynomial({}, [x, y]) == 0

class IntegerPolynomialTest(unittest.TestCase):
    def setUp(self):
        self.a = OneVariableDensePolynomial([1,1],x)
        self.f = MultiVariableSparsePolynomial({(0,0):1,(1,0):2,(2,0):3,(1,1):4,(0,3):5},[x,z])
        self.g = MultiVariableSparsePolynomial({(0,0,0):1,(1,0,0):-2,(1,0,3):3,(1,1,1):-4,(0,2,1):5,(2,2,2):-6},[y,z,x])

    def testAdd(self):
        sum_2 = MultiVariableSparsePolynomial({(0,0,0):2,(1,0,0):1,(0,1,0):-2,(3,1,0):3,(0,0,1):1,(1,1,1):-4,(0,0,2):2,(1,0,2):5,(2,2,2):-6,(0,0,3):3,(0,0,4):4},[x,y,z])
        e = OneVariableDensePolynomial([0,1,2,3,4], z)
        assert self.a + e + self.g == sum_2

    def testSub(self):
        sub_2 = MultiVariableSparsePolynomial({(0,0,0):-1,(1,0,0):1,(2,0,0):3,(0,1,0):2,(3,1,0):-3,(1,0,1):4,(1,1,1):4,(1,0,2):-5,(2,2,2):6,(0,0,3):5},[x,y,z])
        assert self.f - self.g - self.a == sub_2

    def testMul(self):
        mul_2 = MultiVariableSparsePolynomial({(0,0,0):1,(1,0,0):2,(2,0,0):3,(0,1,0):-1,(1,1,0):-2,(2,1,0):-3,(0,2,0):-2,(1,2,0):-4,(2,2,0):-6,(1,0,1):4,(1,1,1):-4,(1,2,1):-8,(0,0,3):5,(0,1,3):-5,(0,2,3):-10},[x,y,z])
        c = OneVariableDensePolynomial([1,-1,-2], y)
        assert c * self.f == mul_2

    def testTrueDiv(self):
        assert MultiVariableSparsePolynomial({(0, 2): 1, (8, 0): -3}, [x, y]) ==  MultiVariableSparsePolynomial({(0, 4): 1, (8, 2): -3}, [x, y]) / OneVariableSparsePolynomial({(2,):1}, [y])

    def testCall(self):
        call_4 = OneVariableSparsePolynomial({(0,):9,(1,):-8,(3,):5},[y])
        call_6 = MultiVariableSparsePolynomial({(0,0):6,(1,0):8,(2,0):3,(0,1):4,(1,1):4,(0,3):5},[x,z])
        call_7 = OneVariableDensePolynomial([6,21,22,5],x)
        assert 4 == self.f(x = 2,z = -1)
        assert self.f(x = -2,z = y) == call_4
        assert self.f(x = self.a) == call_6
        assert self.f(z = self.a) == call_7

class RationalPolynomialTest(unittest.TestCase):
    def setUp(self):
        rat = rational.Rational
        poly = RationalOneVariablePolynomial
        self.h = poly([rat(1,2),rat(7,8),rat(1,13)], x)
        self.i = poly([rat(1,1),rat(0,4),rat(2,4),rat(5,2)], x)
        self.j = poly([rat(3,2),rat(9,4)] ,y)
        self.l = poly([rat(3,2),rat(9,8)], y)

    def testAdd(self):
        sum_1 = RationalOneVariablePolynomial([rational.Rational(3,2),rational.Rational(7,8),rational.Rational(15,26),rational.Rational(5,2)],x)
        sum_2 = MultiVariableSparsePolynomial({(0,0):2,(1,0):rational.Rational(7,8),(0,1):rational.Rational(9,4),(2,0):rational.Rational(1,13)},[x, y])
        sum_3 = RationalOneVariablePolynomial([rational.Rational(3,2), 1], x)
        a = OneVariableDensePolynomial([1,1], x)
        assert self.h + self.i == sum_1
        assert self.h + self.j == sum_2
        assert a + rational.Rational(1,2) == sum_3

    def testSub(self):
        sub_1 = OneVariableDensePolynomial([rational.Rational(-1,2),rational.Rational(7,8),rational.Rational(-11,26),rational.Rational(-5,2)],x)
        sub_2 = MultiVariableSparsePolynomial({(0,0):-1,(1,0):rational.Rational(7,8),(0,1):rational.Rational(-9,4),(2,0):rational.Rational(1,13)},[x, y])
        assert self.h - self.i == sub_1
        assert self.h - self.j == sub_2

    def testMul(self):
        mul_1 = OneVariableDensePolynomial([rational.Rational(1,2),rational.Rational(7,8),rational.Rational(17,52),rational.Rational(27,16),rational.Rational(463,208),rational.Rational(5,26)],x)
        mul_2 = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8),(1,1):rational.Rational(63,32),(2,0):rational.Rational(3,26),(2,1):rational.Rational(9,52)},[x, y])
        assert self.h * self.i == mul_1
        assert self.h * self.j == mul_2

    def testFloordiv(self):
        assert 2 == self.j // self.l
        assert rational.Rational(73, 104) == RationalOneVariablePolynomial([rational.Rational(1,2), rational.Rational(73, 104)], x) // RationalOneVariablePolynomial([rational.Rational(1,1), rational.Rational(1,1)], x)

    def testMod(self):
        assert rational.Rational(-3,2) == (self.j % self.l).coefficient[0]
        a = OneVariableDensePolynomial([1,1], x)
        assert rational.Rational(-21, 104) == (RationalOneVariablePolynomial([rational.Rational(1,2), rational.Rational(73, 104)], x) % a).coefficient[0]
                                               
    def testGetRing(self):
        Qx = PolynomialRing(rational.theRationalField, x)
        Qy = PolynomialRing(rational.theRationalField, y)
        Qxy = PolynomialRing(rational.theRationalField, [x, y])
        assert Qx == self.i.getRing()
        assert Qy == self.j.getRing()
        assert Qxy == (self.i * self.j).getRing(), (self.i*self.j).getRing()

    def testContent(self):
        assert rational.Rational(1,2) == self.i.content()


class IntegerResidueClassPolynomialTest(unittest.TestCase):
    def setUp(self):
        self.f1 = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(3,5), integerResidueClass.IntegerResidueClass(1,5)], x)
        self.f2 = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(4,5), integerResidueClass.IntegerResidueClass(1,5), integerResidueClass.IntegerResidueClass(1,5)], x)

    def testAdd(self):
        sum = OneVariableDensePolynomial([integerResidueClass.IntegerResidueClass(2,5), integerResidueClass.IntegerResidueClass(2,5), integerResidueClass.IntegerResidueClass(1,5)], x)
        assert sum == (self.f1 + self.f2)

    def testEquals(self):
        assert self.f1 == self.f1

    def testCall(self):
        f = MultiVariableSparsePolynomial({(1,0): integerResidueClass.IntegerResidueClass(1,101), (0,1): integerResidueClass.IntegerResidueClass(100,101)}, ["x","y"])
        assert not f(x=1,y=1)


class ComplexPolynomialTest (unittest.TestCase):
    def testInit(self):
        f = OneVariableDensePolynomial([1j,2], 'x')
        self.assertEqual(1, f.degree())


class PolynomialRingTest(unittest.TestCase):
    def setUp(self):
        self.Qx = PolynomialRing(Q, x)
        self.Zx = PolynomialRing(Z, x)
        self.Zxz = PolynomialRing(Z, (x, z))
        self.Qxz = PolynomialRing(Q, (x, z))
        self.QwithXwithY = PolynomialRing(self.Qx, y)
        self.QwithXandY = PolynomialRing(Q, (x, y))

    def testEquals(self):
        assert self.QwithXandY == self.QwithXwithY

    def testGetCoefficientRing(self):
        assert Q == self.Qx.getCoefficientRing()
        assert Z == self.Zxz.getCoefficientRing((x,z))
        assert self.Zx == self.Zxz.getCoefficientRing(z)

    def testIssubring(self):
        assert self.Zx.issubring(self.Zxz)
        assert Z.issubring(self.Zx)
        assert Z.issubring(self.Zxz)
        assert not Q.issubring(self.Zxz)

    def testIssuperring(self):
        assert not self.Zx.issuperring(self.Zxz)
        assert self.Zxz.issuperring(self.Zx)
        assert self.Zxz.issuperring(self.Zxz)
        assert not self.Zxz.issuperring(Q)

    def testContains(self):
        assert 1 in self.Zx
        a = OneVariableDensePolynomial([1,1], x)
        assert a in self.Zx
        assert a in self.Zxz
        assert a in self.Qx
        i =  OneVariableDensePolynomial([rational.Rational(1,1),rational.Rational(0,4),rational.Rational(2,4),rational.Rational(5,2)], x)
        assert i not in self.Zx

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
        class Domain (ring.CommutativeRing):
            def __init__(self):
                self.properties = ring.CommutativeRingProperties()
                self.properties.setIsdomain(True)
            def isdomain(self):
                return True
            def __getattr__(self, attr):
                if attr in ['isfield', 'iseuclidean', 'ispid', 'isufd', 'isnoetherian']:
                    return lambda : False
        domainPolyRing = PolynomialRing(Domain(), x)
        assert domainPolyRing.isdomain()

    def testGetCommonSuperring(self):
        assert self.Qxz == self.Qx.getCommonSuperring(self.Zxz), self.Qx.getCommonSuperring(self.Zxz)

    def testGcd(self):
        a = OneVariableDensePolynomial([1,1], x)
        b = OneVariableDensePolynomial([1,-2,3,-4], x)
        h = OneVariableDensePolynomial([rational.Rational(1,2),rational.Rational(7,8),rational.Rational(1,13)], x)
        assert 1 == self.Qx.gcd(h,a)
        assert 1 == self.Zx.gcd(a,b)

    def testConstants(self):
        self.assertEqual(1, self.Zx.one)
        self.failUnless(self.Zx.one)
        self.failUnless(isinstance(self.Zx.one, OneVariablePolynomial))
        self.assertEqual(0, self.Zx.zero)
        self.failIf(self.Zx.zero)
        self.failUnless(isinstance(self.Zx.zero, OneVariablePolynomial))

    def testVariables(self):
        self.assertRaises(AttributeError, self.Zx.__getattr__, 'y')
        self.assertEqual(self.Zx.x, self.Zx.createElement({1:1}))
        self.assertRaises(AttributeError, self.Qxz.__getattr__, 'y')
        self.failUnless(isinstance(self.Qxz.x, MultiVariableSparsePolynomial))
        self.assertEqual('1/1 * x', str(self.Qxz.x))
        self.assertEqual('1/1 * z', str(self.Qxz.z))

    def testCreateElement(self):
        self.failUnless(isinstance(self.Zx.createElement(1), OneVariablePolynomial))
        self.failUnless(isinstance(self.Zx.createElement([1,2,1]), OneVariablePolynomial))
        self.failUnless(isinstance(self.Zx.createElement({100:1}), OneVariablePolynomial))
        coeff = OneVariablePolynomialCoefficients()
        self.failUnless(isinstance(self.Zx.createElement(coeff), OneVariablePolynomial))

    def testStrings(self):
        # str
        self.assertEqual("Z[x]", str(self.Zx))
        self.assertEqual("Q[x, z]", str(self.Qxz))
        # repr
        self.assertEqual(("PolynomialRing(IntegerRing(), %s)" % set(['x'])), repr(self.Zx))
        self.assertEqual(("PolynomialRing(RationalField(), %s)" % set(['x', 'z'])), repr(self.Qxz))


class PolynomialCompilerTest(unittest.TestCase):
    def setUp(self):
        self.x = OneVariableDensePolynomial([0,1],x)
        self.y = OneVariableDensePolynomial([0,1],y)
        self.s = OneVariableDensePolynomial([1,1],x)
        self.multi = MultiVariableSparsePolynomial({(0,0):rational.Rational(3,4),(1,0):rational.Rational(21,16),(0,1):rational.Rational(9,8)},[x, y])

    def testOneVariableInteger(self):
        assert self.x == construct(x)
        assert self.x != construct(y)
        assert self.y == construct(y)
        assert self.x != construct("1 + x")
        assert self.s == construct("1 + x")
        assert self.x**2 + 1 == construct("1 + x**2")
        assert self.multi == construct("Q(3,4) + Q(21,16) * x + Q(9,8) * y", {"Q": rational.Rational})


class PolynomialGCDTest(unittest.TestCase):
    def setUp(self):
        import nzmath.matrix as matrix
        self.f = OneVariableDensePolynomial([1,2,3,4,5], x)
        self.g = OneVariableDensePolynomial([7,8,9], x)
        self.correctResult = matrix.createMatrix(6,6,
                                                [5,4,3,2,1,0]
                                            +   [0,5,4,3,2,1]
                                            +   [9,8,7,0,0,0]
                                            +   [0,9,8,7,0,0]
                                            +   [0,0,9,8,7,0]
                                            +   [0,0,0,9,8,7] ).determinant()
        self.f2 = OneVariableDensePolynomial([-3,-2,2,2,1], x)
        self.g2 = OneVariableDensePolynomial([-6,-5,2,5,4], x)

    def testResultant(self):
        self.assertEqual(self.correctResult, resultant(self.f, self.g))
        self.assertEqual(2, resultant(
            OneVariableDensePolynomial([-2, 0, 0, 1], x),
            OneVariableDensePolynomial([0, 1], x)))

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
        assert subResultantGCD(self.f2, self.g2) == OneVariableDensePolynomial([-1,0,1], x)

class SquareFreeDecompositionChar0Test(unittest.TestCase):
    def setUp(self):
        self.pow1 = OneVariablePolynomialChar0([1,1],x,Q)
        self.pow1pow2 = OneVariablePolynomialChar0([1,2,2,2,1],x,Q)
        self.pow1pow3 = OneVariablePolynomialChar0([8,20,18,7,1],x,Q)

    def testSuccess(self):
        assert self.pow1.squareFreeDecomposition()
        assert self.pow1pow2.squareFreeDecomposition()
        assert self.pow1pow3.squareFreeDecomposition()
        result1 = {1: self.pow1}
        result2 = {1: OneVariableDensePolynomial([1,0,1],x, rational.theRationalField),
                   2: OneVariableDensePolynomial([1,1],x, rational.theRationalField)}
        result3 = {1: OneVariableDensePolynomial([1,1],x, rational.theRationalField),
                   3: OneVariableDensePolynomial([2,1],x, rational.theRationalField)}
        assert result1 == self.pow1.squareFreeDecomposition()
        assert result2 == self.pow1pow2.squareFreeDecomposition(), self.pow1pow2.squareFreeDecomposition()
        assert result3 == self.pow1pow3.squareFreeDecomposition(), self.pow1pow3.squareFreeDecomposition()

class FiniteFieldPolynomialTest(unittest.TestCase):
    def setUp(self):
        import nzmath.finitefield as finitefield
        self.F2 = finitefield.FinitePrimeField(2)
        self.f = OneVariableDensePolynomial([1, 1], x, self.F2)
        self.g = OneVariableDensePolynomial([1, 0, 1], x, self.F2)
        self.h = OneVariableDensePolynomial([0, 1, 1], x, self.F2)

    def testInit(self):
        assert isinstance(self.f, OneVariablePolynomialCharNonZero)
        assert isinstance(self.g, OneVariablePolynomialCharNonZero)

    def testAdd(self):
        result = OneVariableDensePolynomial([0,1,1],x,self.F2)
        assert result == self.f + self.g
        assert self.f.getRing() == (self.f + self.g).getRing()
        assert not (self.f + self.f)

    def testSub(self):
        result = OneVariableDensePolynomial([0,1,1],x,self.F2)
        assert result == self.f - self.g
        assert self.f.getRing() == (self.f - self.g).getRing()

    def testMul(self):
        result = OneVariableDensePolynomial([1,1,1,1],x,self.F2)
        assert result == self.f * self.g
        assert self.f.getRing() == (self.f * self.g).getRing()
        assert self.f == 1 * self.f
        assert 0 == 0 * self.f

    def testMod(self):
        assert self.f == self.f % self.g
        r = self.g % self.h
        for i in range(r.degree() + 1):
            self.failUnless(r[i] in self.g.getCoefficientRing())

    def testFloordiv(self):
        assert 0 == self.f // self.g
        assert 0 == 0 // self.g

    def testDifferentiate(self):
        import nzmath.finitefield as finitefield
        result = finitefield.FinitePrimeFieldElement(1,2)
        assert result == +self.f.differentiate(self.f.variable)
        assert not self.g.differentiate(self.g.variable)
        pX = OneVariableDensePolynomial([0,1,1], 'X', finitefield.FinitePrimeField.getInstance(3))
        dpX = pX.differentiate('X')
        self.failUnless(isinstance(dpX, OneVariablePolynomialCharNonZero))
        for i in range(dpX.degree()+1):
            self.failUnless(isinstance(dpX[i], finitefield.FinitePrimeFieldElement))

    def testGcd(self):
        assert self.f == self.f.getRing().gcd(self.f, self.g)
        import nzmath.finitefield as finitefield
        pX = OneVariableDensePolynomial([0,1,1], 'X', finitefield.FinitePrimeField.getInstance(3))
        dpX = pX.differentiate('X')
        pX.getRing().gcd(pX, dpX)

    def testPow(self):
        assert self.f ** 2

    def testEquality(self):
        self.assertEqual(self.f, self.f)
        one_poly = OneVariableSparsePolynomial({0:1}, x, self.F2)
        one_field = self.F2.one
        self.assertEqual(one_poly, one_field)
        self.assertEqual(one_field, one_poly)
        self.failUnless(not one_poly != one_field)

    def testIsIrreducible(self):
        assert self.f.isIrreducible()
        assert not self.g.isIrreducible()
        assert not self.h.isIrreducible()

    def testSquareFreeDecomposition(self):
        g_decomp = self.g.squareFreeDecomposition()
        assert 1 == len(g_decomp)
        assert 2 == g_decomp.keys()[0]
        h_decomp = self.h.squareFreeDecomposition()
        assert 1 == len(h_decomp)
        assert 1 == h_decomp.keys()[0]
        assert h_decomp.values()[0] == self.h, str(h_decomp.items()[0])

    def testDistinctDegreeFactorization(self):
        h_ddf = self.h.distinctDegreeFactorization()
        assert 1 == len(h_ddf)
        q = OneVariableDensePolynomial([1,1,1], 'x', self.F2) * self.h
        q_ddf = q.distinctDegreeFactorization()
        assert 2 == len(q_ddf)

    def testSplitSameDegrees(self):
        h_ssd = self.h.splitSameDegrees(1)
        assert self.h.degree() == len(h_ssd)

    def testFactor(self):
        import nzmath.finitefield as finitefield
        p = OneVariableDensePolynomial([1,2,3,0,0,3,2,1],
                                       x,
                                       finitefield.FinitePrimeField(5))
        factored = p.factor()
        assert isinstance(factored, list)
        assert 3 == len(factored)
        for i in range(3):
            assert isinstance(factored[i], tuple)
            assert 2 == len(factored[i])
            assert isinstance(factored[i][1], (int,long))
        product = p.getCoefficientRing().createElement(1)
        for i in range(3):
            product = product * factored[i][0] ** factored[i][1]
        assert p == product

        # F2 case
        g_factor = self.g.factor()
        assert 1 == len(g_factor), g_factor
        assert 2 == g_factor[0][1]
        h_factor = self.h.factor()
        assert 2 == len(h_factor), h_factor

class ResidueRingTest (unittest.TestCase):
    def setUp(self):
        Zx = PolynomialRing(Z, x)
        I7 = OneVariablePolynomialIdeal(7, Zx)
        self.Zx_I7 = PolynomialResidueRing(Zx, I7)

    def testInit(self):
        self.failUnless(self.Zx_I7.isnoetherian())

    def testCreateElement(self):
        f = OneVariableDensePolynomial([1, 1], x)
        self.failUnless(isinstance(self.Zx_I7.createElement(f), ring.ResidueClass))


class OneVariablePolynomialCoefficientsTest (unittest.TestCase):
    def setUp(self):
        self.c1 = OneVariablePolynomialCoefficients()
        self.c2 = OneVariablePolynomialCoefficients()

    def testInit(self):
        self.assertEqual(self.c1._using, self.c1.USING_LIST)

    def testEqual(self):
        "trivial cases"
        self.assertEqual(self.c1, self.c1)
        self.assertEqual(self.c1, self.c2)
        self.assertEqual(self.c1 == self.c2, not (self.c1 != self.c2))
        self.assertNotEqual(self.c1, 1)

    def testEqualDifferentRepresentations(self):
        "after changing representation"
        self.c2.changeRepresentation(self.c2.USING_DICT)
        self.assertEqual(self.c1, self.c2)

    def testEqualSetValues(self):
        # change value
        self.c2[0] = 1
        self.assertNotEqual(self.c1, self.c2)
        self.c1[0] = 2
        self.assertNotEqual(self.c1, self.c2)
        # change rep again
        self.c2.changeRepresentation(self.c2.USING_DICT)
        self.assertNotEqual(self.c1, self.c2)
        self.c2[2] = self.c1[2] = 1
        self.assertNotEqual(self.c1, self.c2)
        self.assertNotEqual(self.c2, self.c1)

    def testDegree(self):
        self.assertEqual(-1, self.c1.degree())

    def testList(self):
        self.c1.setList([1,2,3])
        self.assertEqual(2, self.c1.degree())
        self.assertEqual([1,2,3], self.c1.getAsList())

    def testDict(self):
        self.c1.setDict({0:1, 2:3})
        self.assertEqual(2, self.c1.degree())
        self.assertEqual([1,0,3], self.c1.getAsList())
        self.assertEqual({0:1, 2:3}, self.c1.getAsDict())


class PolynomialIdealTest (unittest.TestCase):
    def setUp(self):
        QX = PolynomialRing(Q, 'X')
        self.g = OneVariableDensePolynomial([3, 0, 0, 1], 'X', Q)
        self.I = OneVariablePolynomialIdeal(self.g, QX)

    def testReduce(self):
        f = OneVariableSparsePolynomial({10: 1}, 'X', Q)
        self.I.reduce(f)
        self.assertEqual(self.I.reduce(f), f % self.g)
        f = OneVariableSparsePolynomial({13: 1}, 'X', Q)
        self.I.reduce(f)
        self.assertEqual(self.I.reduce(f), f % self.g)
        f = OneVariableSparsePolynomial({13: 1, 100: 2}, 'X', Q)
        self.I.reduce(f)
        self.assertEqual(self.I.reduce(f), f % self.g)


class OneVariableMonomialTest (unittest.TestCase):
    def testVariable(self):
        x = OneVariableMonomial('X')
        self.assert_(isinstance(x, OneVariablePolynomial))
        self.assertEqual("X", str(x))
        y = OneVariableMonomial('Y')
        self.assert_(isinstance(y, OneVariablePolynomial))
        self.assertEqual("Y", str(y))

    def testIndex(self):
        x = OneVariableMonomial('X', index=2)
        self.assert_(isinstance(x, OneVariablePolynomial))
        self.assertEqual("X ** 2", str(x))

    def testCoefficient(self):
        x = OneVariableMonomial('X', coefficient=2)
        self.assert_(isinstance(x, OneVariablePolynomial))
        self.assertEqual("2 * X", str(x))

    def testRing(self):
        x = OneVariableMonomial('X', coeffring=Q)
        self.assert_(isinstance(x, OneVariablePolynomial))
        self.assertEqual("1/1 * X", str(x))
        self.assertEqual(x.getCoefficientRing(), Q)

    def testRingCharNonZero(self):
        import nzmath.finitefield as finitefield
        F3 = finitefield.FinitePrimeField.getInstance(3)
        x = OneVariableMonomial('X', coeffring=F3)
        self.assert_(isinstance(x, OneVariablePolynomialCharNonZero))
        self.assertEqual(x.getCoefficientRing(), F3)

    def testAllOptions(self):
        x = OneVariableMonomial('X', index=2, coefficient=3, coeffring=Q)
        self.assert_(isinstance(x, OneVariablePolynomial))
        self.assertEqual("3 * X ** 2", str(x))
        self.assertEqual(x.getCoefficientRing(), Q)

    def testConstant(self):
        const = OneVariableMonomial('X', index=0, coefficient=-1)
        self.assert_(isinstance(const, OneVariablePolynomial))
        self.assertEqual("-1", str(const))


class OneVariableDensePolynomialTest (unittest.TestCase):
    def testClassForInteger(self):
        self.assert_(isinstance(OneVariableDensePolynomial([1, 1], 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableDensePolynomial([1, 1], 'x'), OneVariablePolynomialChar0))

    def testClassForRational(self):
        self.assert_(isinstance(OneVariableDensePolynomial([1, rational.Rational(1, 2)], 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableDensePolynomial([1, rational.Rational(1, 2)], 'x'), OneVariablePolynomialChar0))
        self.assert_(isinstance(OneVariableDensePolynomial([1, rational.Rational(1, 2)], 'x'), RationalOneVariablePolynomial))

    def testClassForFiniteField(self):
        import nzmath.finitefield
        element = nzmath.finitefield.FinitePrimeFieldElement
        self.assert_(isinstance(OneVariableDensePolynomial([element(1, 5), element(1, 5)], 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableDensePolynomial([element(1, 5), element(1, 5)], 'x'), OneVariablePolynomialCharNonZero))


class OneVariableSparsePolynomialTest (unittest.TestCase):
    def testClassForInteger(self):
        self.assert_(isinstance(OneVariableSparsePolynomial({1:1, 0:1}, 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableSparsePolynomial({0:1, 1:1}, 'x'), OneVariablePolynomialChar0))

    def testClassForRational(self):
        self.assert_(isinstance(OneVariableSparsePolynomial({0:1, 1:rational.Rational(1, 2)}, 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableSparsePolynomial({0:1, 1:rational.Rational(1, 2)}, 'x'), OneVariablePolynomialChar0))
        self.assert_(isinstance(OneVariableSparsePolynomial({0:1, 1:rational.Rational(1, 2)}, 'x'), RationalOneVariablePolynomial))

    def testClassForFiniteField(self):
        import nzmath.finitefield
        element = nzmath.finitefield.FinitePrimeFieldElement
        self.assert_(isinstance(OneVariableSparsePolynomial({0:element(1, 5), 1:element(1, 5)}, 'x'), OneVariablePolynomial))
        self.assert_(isinstance(OneVariableSparsePolynomial({0:element(1, 5), 1:element(1, 5)}, 'x'), OneVariablePolynomialCharNonZero))


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__== '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
