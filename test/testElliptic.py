import unittest
import elliptic
import finitefield
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

class EllipticTest(unittest.TestCase):
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
        assert str(a.simple()) == ' y ** 2=8208 - 432 * x + x ** 3' 

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
        assert str(elliptic.EC([2,4],0).changeCurve([1,2,3,4])) == '8/1 * y + 6/1 * x * y + y ** 2=-10/1 * x - 3/1 * x ** 2 + x ** 3'

    def testPoint(self):
        assert elliptic.EC([1,2],0).changePoint([1,2], [1,2,3,4]) == [-1, 1]

    def testDivPoly(self):
        E=elliptic.EC([3,4],101)
        D=({-1:polynomial.OneVariableSparsePolynomial({0:-1},['x'],finitefield.FinitePrimeField(E.ch)),
            0:polynomial.OneVariableSparsePolynomial({},['x'],finitefield.FinitePrimeField(E.ch)),
            1:polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(E.ch)),
            2:polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(E.ch))*2,
            3:polynomial.OneVariableSparsePolynomial({0:92,1:48,2:18,4:3},["x"],finitefield.FinitePrimeField(E.ch)),
            4:polynomial.OneVariableSparsePolynomial({0:94,1:5,2:11,3:59,4:30,6:2},["x"],finitefield.FinitePrimeField(E.ch))*2,
            5:polynomial.OneVariableSparsePolynomial({0:48,1:58,2:53,3:60,4:28,5:93,6:79,7:52,8:65,9:5,10:85,12:5},["x"],finitefield.FinitePrimeField(E.ch)),
            6:polynomial.OneVariableSparsePolynomial({0:9,1:12,2:44,3:16,4:64,5:22,6:76,7:28,8:42,9:96,10:87,12:57,13:62,14:14,16:3},["x"],finitefield.FinitePrimeField(E.ch))*2,
            7:polynomial.OneVariableSparsePolynomial({0:94,1:77,2:87,3:65,4:97,5:45,6:80,7:22,8:44,9:76,10:5,11:49,12:49,13:74,14:76,15:53,16:69,17:47,18:63,19:70,20:78,21:20,22:15,24:7},["x"],finitefield.FinitePrimeField(E.ch)),
            8:polynomial.OneVariableSparsePolynomial({0:16,1:50,2:29,3:10,4:62,5:80,6:41,7:66,8:79,9:48,10:77,11:53,12:67,13:70,14:5,15:18,16:36,17:28,18:58,19:95,20:67,21:91,22:37,23:93,24:25,25:93,26:61,27:34,28:68,30:4},["x"],finitefield.FinitePrimeField(E.ch))*2},
           [3,5,7])
        assert E.divPoly([])==D
        ## NotImplemented
        # F=elliptic.EC([3,4],7,3)
        # D=F.divPoly(1)[0]
        # assert F.divPoly(1,7)==D[7]

class OrderTest (unittest.TestCase):
    def testEqual(self):
        e = elliptic.EC([1,4],5)
        bySchoof = e.Schoof()
        byNaive = e.naive()
        assert bySchoof == byNaive
        e = elliptic.EC([1,3,4,0,1],5)
        bySchoof = e.Schoof()
        byNaive = e.naive()
        assert bySchoof == byNaive
class PairingTest (unittest.TestCase):
    def testLine(self):
        e = elliptic.EC([0,0,1,-1,0],17)
        P = [0,0]
        l = e.line(P,P)
        assert l[0] == 2
        assert l[1](x=P[0],y=P[1]) == finitefield.FinitePrimeFieldElement(0, 17)
        P2 = e.mul(2,P)
        l2 = e.line(P,P2)
        assert l2[0] == -1
        assert l2[1](0) == finitefield.FinitePrimeFieldElement(0, 17)
def suite():
    suite  = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EllipticTest, 'test'))
    suite.addTest(unittest.makeSuite(OrderTest, 'test'))
    suite.addTest(unittest.makeSuite(PairingTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
