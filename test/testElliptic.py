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

F1 = polynomial.OneVariableSparsePolynomial({0:2},["x"])
F2 = polynomial.OneVariableSparsePolynomial({1:1,0:1,2:1,3:4},["x"])
f2 = polynomial.OneVariableSparsePolynomial({1:1,0:1,2:1,3:4},["x"],finitefield.FinitePrimeField(101))
F3 = polynomial.OneVariableSparsePolynomial({1:10,0:87,3:17,2:22,4:60,6:4},["x"])
F4 = polynomial.OneVariableSparsePolynomial({9:5,8:65,10:85,12:5,1:58,0:48,3:60,2:53,5:93,4:28,7:52,6:79},["x"])
F5 = polynomial.OneVariableSparsePolynomial({3:10,4:2,13:65,7:1},["x"])

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
        D=({-1:polynomial.OneVariableSparsePolynomial({0:-1},['x'],finitefield.FinitePrimeField(self.ch)),
            0:polynomial.OneVariableSparsePolynomial({},['x'],finitefield.FinitePrimeField(self.ch)),
            1:polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(self.ch)),
            2:polynomial.OneVariableSparsePolynomial({0:2},['x'],finitefield.FinitePrimeField(self.ch)),
            3:polynomial.OneVariableSparsePolynomial({1:48,0:92,2:18,4:3},["x"],finitefield.FinitePrimeField(self.ch)),
            4:polynomial.OneVariableSparsePolynomial({0:87,1:10,2:22,3:17,4:60,6:4},["x"],finitefield.FinitePrimeField(self.ch)),
            5:polynomial.OneVariableSparsePolynomial({9:5,8:65,10:85,12:5,1:58,0:48,3:60,2:53,5:93,4:28,7:52,6:79},["x"],finitefield.FinitePrimeField(self.ch)),
            6:polynomial.OneVariableSparsePolynomial({0:60,1:62,2:25,3:58,4:50,5:23,6:81,7:37,8:68,9:24,10:57,11:34,12:55,13:69,14:24,16:56},["x"],finitefield.FinitePrimeField(self.ch)),
            7:polynomial.OneVariableSparsePolynomial({9:76,8:44,11:49,10:5,13:74,12:49,15:53,14:76,1:77,0:94,3:65,2:87,5:45,4:97,7:22,6:80,24:7,17:47,16:69,19:70,18:63,21:20,20:78,22:15},["x"],finitefield.FinitePrimeField(self.ch)),
            8:polynomial.OneVariableSparsePolynomial({0:19,1:17,2:81,3:77,4:68,5:23,6:59,7:66,8:65,9:52,10:12,11:98,12:1,13:58,14:63,15:38,17:42,18:43,19:36,20:50,21:36,22:6,23:39,24:7,26:66,27:85,28:19,30:99},["x"],finitefield.FinitePrimeField(self.ch))},
           [3,5,7])
        assert E.divPoly()==D

def suite():
    suite = unittest.makeSuite(EllipticTest, 'test') 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
