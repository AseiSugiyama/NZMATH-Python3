import unittest
import elliptic
import polynomial
import rational

a = elliptic.EC([0,-1,1,0,0], 0)
b = elliptic.EC([1,0], 0)
c = elliptic.EC([0,17], 0)

P1 = [-2,3]
P2 = [-1,4]
P3 = [2,5]
P4 = [4,9]
P5 = [8,23]
P6 = [43,282]
P7 = [52,375]
P8 = [5234,378661]

F1 = polynomial.OneVariableSparsePolynomial({(0,):2},["x"])
F2 = polynomial.OneVariableSparsePolynomial({(1,):1,(0,):1,(2,):1,(3,):4},["x"])
F3 = polynomial.OneVariableSparsePolynomial({(1,):10,(0,):87,(3,):17,(2,):22,(4,):60,(6,):4},["x"])
F4 = polynomial.OneVariableSparsePolynomial({(9,):5,(8,):65,(10,):85,(12,):5,(1,):58,(0,):48,(3,):60,(2,):53,(5,):93,(4,):28,(7,):52,(6,):79},["x"])

class EllipticTest(unittest.TestCase):
#    def testMod(self):
#        assert str(elliptic.Mod(F3,3))==

#    def testDiv(self):
#        assert str(elliptic.Div(F3,3))==

#    def testInver_p(self):
#        assert str(elliptic.Inver_p(F2,8,101))==

#    def testPolyMod_p(self):
#        assert str(elliptic.PolyMod_p(F1+F2,F2,))==
#        assert str(elliptic.PolyMod_p(F4,F2,))==

#    def testGCD():
#        assert
        
    def testInit(self):
        assert a.c4 == 16
        assert a.c6 == -152
        assert a.disc == -11
        assert a.j == rational.Rational(a.c4**3, a.disc)

        assert b.c4 == -48
        assert b.c6 == 0
        assert b.disc == -64
        assert b.j == rational.Rational(b.c4**3, b.disc)

    def testSimple(self): 
        assert str(a.simple()) == '- 8208 + 432x - x**3 + y**2' 

    def testWhetherOn(self): 
        assert c.whetherOn(P1)
        assert c.whetherOn(P2)
        assert c.whetherOn(P3)
        assert c.whetherOn(P4)
        assert c.whetherOn(P5)
        assert c.whetherOn(P6)
        assert c.whetherOn(P7)
        assert c.whetherOn(P8)
        assert not c.whetherOn([-15,-2])
        assert not c.whetherOn([99999,66666666])

    def testAdd(self):
        assert c.add(P3, P7) == c.mul(3, P1)

    def testSub(self):
        assert c.sub(P1, P3) == P4

    def testMul(self): 
        assert c.mul(-2, P1) == P5

    def testOrder(self):
        d = elliptic.EC([2,6], 7)
        e = elliptic.EC([1,3], 7)
        f = elliptic.EC([11,3], 13)

        assert d.order() == 11
        assert e.order() == 6
        assert f.order() == 13

    def testPoint(self):
        d = elliptic.EC([2,6], 7)
        e = elliptic.EC([1,3], 7)
        f = elliptic.EC([11,3], 13)

        assert d.whetherOn(d.point())
        assert e.whetherOn(e.point())
        assert f.whetherOn(f.point())

    def testChangeCurve(self):
        assert str(elliptic.EC([2,4],0).changeCurve([1,2,3,4])) == '10/1x + 3/1x**2 - x**3 + 8/1y + 6/1xy + y**2'

    def testPoint(self):
        assert elliptic.EC([1,2],0).changePoint([1,2], [1,2,3,4]) == [-1, 1]

    def testDivPoly(self):
        E=elliptic.EC([3,4],101)
        D=([0, 1, 2, OneVariableSparsePolynomial({(1,): 48, (0,): 92, (2,): 18, (4,): 3}, ['x']), OneVariableSparsePolynomial({(1,): 10, (0,): 87, (3,): 17, (2,): 22, (4,): 60, (6,): 4}, ['x']), OneVariableSparsePolynomial({(9,): 5, (8,): 65, (10,): 85, (12,): 5, (1,): 58, (0,): 48, (3,): 60, (2,): 53, (5,): 93, (4,): 28, (7,): 52, (6,): 79}, ['x']), OneVariableSparsePolynomial({(9,): 24, (8,): 68, (11,): 34, (10,): 57, (13,): 69, (12,): 55, (14,): 24, (1,): 62, (0,): 60, (3,): 58, (2,): 25, (5,): 23, (4,): 50, (7,): 37, (6,): 81, (16,): 56}, ['x']), OneVariableSparsePolynomial({(9,): 76, (8,): 44, (11,): 49, (10,): 5, (13,): 74, (12,): 49, (15,): 53, (14,): 76, (1,): 77, (0,): 94, (3,): 65, (2,): 87, (5,): 45, (4,): 97, (7,): 22, (6,): 80, (24,): 7, (17,): 47, (16,): 69, (19,): 70, (18,): 63, (21,): 20, (20,): 78, (22,): 15}, ['x'])], [3, 5, 7])
        assert str(E.devPoly())==D

def suite():
    suite = unittest.makeSuite(EllipticTest, 'test') 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
