import unittest
import ec.elliptic
import rational

a = ec.elliptic.EC([0,-1,1,0,0], 0)
b = ec.elliptic.EC([1,0], 0)
c = ec.elliptic.EC([0,17], 0)

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
        d = ec.elliptic.EC([2,6], 7)
        e = ec.elliptic.EC([1,3], 7)
        f = ec.elliptic.EC([11,3], 13)

        assert d.order() == 11
        assert e.order() == 6
        assert f.order() == 13

    def testPoint(self):
        d = ec.elliptic.EC([2,6], 7)
        e = ec.elliptic.EC([1,3], 7)
        f = ec.elliptic.EC([11,3], 13)

        assert d.whetherOn(d.point())
        assert e.whetherOn(e.point())
        assert f.whetherOn(f.point())

    def testChangeCurve(self):
        assert str(ec.elliptic.EC([2,4],0).changeCurve([1,2,3,4])) == '10/1x + 3/1x**2 - x**3 + 8/1y + 6/1xy + y**2'

    def testPoint(self):
        assert ec.elliptic.EC([1,2],0).changePoint([1,2], [1,2,3,4]) == [-1, 1]


def suite():
    suite = unittest.makeSuite(EllipticTest, 'test') 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
