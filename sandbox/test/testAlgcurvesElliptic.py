import unittest
import logging
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil
import nzmath.poly.multiutil as multiutil
import sandbox.algebraiccurve.elliptic as elliptic
import sandbox.finitefield as finitefield


logging.basicConfig(level=logging.INFO)


class EllipticTest(unittest.TestCase):
    def setUp(self):
        self.a = elliptic.EC([0,-1,1,0,0], 0)
        self.b = elliptic.EC([1,0], 0)
        self.c = elliptic.EC([0,17], 0)

        self.P1 = [-2,3]
        self.P2 = [-1,4]
        self.P3 = [2,5]
        self.P4 = [4,9]
        self.P5 = [8,23]
        self.P6 = [43,282]
        self.P7 = [52,375]
        self.P8 = [5234,378661]

    def testInit(self):
        self.assertEqual(16, self.a.c4)
        self.assertEqual(-152, self.a.c6)
        self.assertEqual(-11, self.a.disc)
        self.assertEqual(rational.Rational(self.a.c4**3, self.a.disc), self.a.j)

        self.assertEqual(-48, self.b.c4)
        self.assertEqual(0, self.b.c6)
        self.assertEqual(-64, self.b.disc)
        self.assertEqual(rational.Rational(self.b.c4**3, self.b.disc), self.b.j)

    def testStr(self):
        e = elliptic.EC([1, 3, 4, 0, 1], 7)
        self.assert_(str(e))

    def testSimple(self): 
        self.assertEqual('y ** 2=8208 - 432 * x + x ** 3', str(self.a.simple()))
        # ch > 0
        e = elliptic.EC([1, 1, 1, 3, 4], 7)
        self.assert_(e.simple())

    def testWhetherOn(self):
        self.assert_(self.c.whetherOn(self.P1))
        self.assert_(self.c.whetherOn(self.P2))
        self.assert_(self.c.whetherOn(self.P3))
        self.assert_(self.c.whetherOn(self.P4))
        self.assert_(self.c.whetherOn(self.P5))
        self.assert_(self.c.whetherOn(self.P6))
        self.assert_(self.c.whetherOn(self.P7))
        self.assert_(self.c.whetherOn(self.P8))
        self.failIf(self.c.whetherOn([-15,-2]))
        self.failIf(self.c.whetherOn([99999,66666666]))

    def testAdd(self):
        self.assertEqual(self.c.add(self.P3, self.P7), self.c.mul(3, self.P1))

    def testSub(self):
        self.assertEqual(self.P4, self.c.sub(self.P1, self.P3))

    def testMul(self):
        self.assertEqual(self.P5, self.c.mul(-2, self.P1))

    def testOrder(self):
        d = elliptic.EC([2, 6], 7)
        e = elliptic.EC([1, 3], 7)
        f = elliptic.EC([11, 3], 13)

        self.assertEqual(11, d.order())
        self.assertEqual(6, e.order())
        self.assertEqual(13, f.order())

    def testPoint(self):
        d = elliptic.EC([2, 6], 7)
        e = elliptic.EC([1, 3], 7)
        f = elliptic.EC([11, 3], 13)

        self.assert_(d.whetherOn(d.point()))
        self.assert_(e.whetherOn(e.point()))
        self.assert_(f.whetherOn(f.point()))

    def testChangeCurve(self):
        self.assertEqual('8/1 * y + 6/1 * x * y + y ** 2=-10/1 * x - 3/1 * x ** 2 + x ** 3',
                          str(elliptic.EC([2, 4], 0).changeCurve([1, 2, 3, 4])))

    def testChangePoint(self):
        self.assertEqual([-1, 1], elliptic.EC([1, 2], 0).changePoint([1, 2], [1, 2, 3, 4]))

    def testDivPoly(self):
        E = elliptic.EC([3, 4], 101)
        F101 = finitefield.FinitePrimeField.getInstance(E.ch)
        D = ({-1:uniutil.polynomial({0:-1}, F101),
            0:uniutil.polynomial({}, F101),
            1:uniutil.polynomial({0:1}, F101),
            2:uniutil.polynomial({0:2}, F101),
            3:uniutil.polynomial({0:92, 1:48, 2:18, 4:3}, F101),
            4:uniutil.polynomial({0:188, 1:10, 2:22, 3:118, 4:60, 6:4}, F101),
            5:uniutil.polynomial({0:48, 1:58, 2:53, 3:60, 4:28, 5:93, 6:79,
                                  7:52, 8:65, 9:5, 10:85, 12:5}, F101),
            6:uniutil.polynomial({0:18, 1:24, 2:88, 3:32, 4:128, 5:44, 6:152,
                                  7:56, 8:84, 9:192, 10:174, 12:114, 13:124,
                                  14:28, 16:6}, F101),
            7:uniutil.polynomial({0:94, 1:77, 2:87, 3:65, 4:97, 5:45, 6:80,
                                  7:22, 8:44, 9:76, 10:5, 11:49, 12:49, 13:74,
                                  14:76, 15:53, 16:69, 17:47, 18:63, 19:70,
                                  20:78, 21:20, 22:15, 24:7}, F101),
            8:uniutil.polynomial({0:32, 1:100, 2:58, 3:20, 4:124, 5:160, 6:82,
                                  7:132, 8:158, 9:96, 10:154, 11:106, 12:134,
                                  13:140, 14:10, 15:36, 16:72, 17:56, 18:116,
                                  19:190, 20:134, 21:182, 22:74, 23:186, 24:50,
                                  25:186, 26:122, 27:68, 28:136, 30:8}, F101)},
           [2, 3, 5, 7])
        self.assertEqual(D, E.divPoly([]))
        ## NotImplemented
        # F=elliptic.EC([3,4],7,3)
        # D=F.divPoly(1)[0]
        # assert F.divPoly(1,7)==D[7]


class OrderTest(unittest.TestCase):
    def testCh5(self):
        e = elliptic.EC([1, 4], 5)
        self.assertEqual(5 + 1 - e.trace(), e.order())


class TraceTest(unittest.TestCase):
    # ch <= 229, Shanks_Mestre deligates the computation to naive.
    def testEqualCh5(self):
        e = elliptic.EC([1, 4], 5)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof)
        e = elliptic.EC([2, 0], 5)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof)
        e = elliptic.EC([1, 3, 4, 0, 1], 5)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof)

    def testEqualCh7(self):
        e = elliptic.EC([1, 4], 7)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof, str(e))
        e = elliptic.EC([2, 0], 7)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof, str(e))
        e = elliptic.EC([1, 3, 4, 0, 1], 7)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof, repr(e)) # see EllipticTest.testStr

    def testEqualCh19(self):
        e = elliptic.EC([2, 1], 19)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof)
        e = elliptic.EC([2, 5], 19)
        byNaive = e.naive()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, bySchoof)

    def testEqualCh233(self):
        e = elliptic.EC([2, 1], 233)
        byNaive = e.naive()
        byShanksMestre = e.Shanks_Mestre()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, byShanksMestre)
        self.assertEqual(byNaive, bySchoof)
        # bug #2281173
        e = elliptic.EC([2, 5], 233)
        byNaive = e.naive()
        byShanksMestre = e.Shanks_Mestre()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, byShanksMestre)
        self.assertEqual(byNaive, bySchoof)

    def testEqualCh311(self):
        e = elliptic.EC([12, 179], 311)
        byNaive = e.naive()
        byShanksMestre = e.Shanks_Mestre()
        bySchoof = e.Schoof()
        self.assertEqual(byNaive, byShanksMestre)
        self.assertEqual(byNaive, bySchoof)

    def testEqualCh65537(self):
        # 65537 is too large for naive method.
        e = elliptic.EC([0, 1], 65537)  # supersingular curve
        byShanksMestre = e.Shanks_Mestre()
        bySchoof = e.Schoof()
        self.assertEqual(0, byShanksMestre)
        self.assertEqual(0, bySchoof)


class PairingTest(unittest.TestCase):
    def testLine(self):
        # FIXME: need more appropriate tests
        e = elliptic.EC([0, 0, 1, -1, 0], 17)
        P = [0, 0]
        self.assertEqual(e.basefield.zero, e.line(P, P, P))
        P2 = e.mul(2, P)
        self.assertEqual(e.basefield.zero, e.line(P, P2, e.mul(-1, e.add(P, P2))))

    def testWeilPairing(self):
        # this example was refered to Washington.
        e = elliptic.EC([0, 2], 7)
        P = [5, 1]
        Q = [0, 3]
        R = e.WeilPairing(3, P, Q)
        self.assertEqual(finitefield.FinitePrimeFieldElement(2, 7), R)

        # test case of extension field, characteristic 7
        p = 7
        r = 11
        F = finitefield.FinitePrimeField(p)
        PX = uniutil.polynomial({0:3,1:3,2:2,3:1,4:4,5:1,6:1,10:1},F)
        Fx = finitefield.FiniteExtendedField(p,PX)

        E = elliptic.EC([F.one,-F.one],F)
        Ex = elliptic.EC([Fx.one,-Fx.one],Fx)

        P = [3,6]
        assert E.whetherOn(P)
        assert Ex.whetherOn(P)
        assert E.mul(11,P) == E.infpoint
        Qxcoord = Fx.createElement(6*7**9+7**8+7**6+6*7**3+6*7**2+7+6)
        Qycoord = Fx.createElement(3*7**9+6*7**8+4*7**7+2*7**6+5*7**4+5*7**3+7**2+7+3)
        Q = [Qxcoord,Qycoord]
        assert Ex.whetherOn(Q)
        assert Ex.mul(11,Q) == Ex.infpoint

        w = Ex.WeilPairing(11, P, Q)
        Wp = Fx.createElement(7**9 + 5*7**8 + 4*7**7 + 2*7**5 + 7**4 + 6*7**2)
        assert w == Wp

    def testWeilPairingIsFunction(self):
        # e2 is isomorphic to Z/256 x Z/256
        e2 = elliptic.EC([-1, 0], 65537)
        P1 = [finitefield.FinitePrimeFieldElement(30840, 65537),
              finitefield.FinitePrimeFieldElement(53250, 65537)]
        self.failIf(256 % e2.pointorder(P1))
        P2 = [finitefield.FinitePrimeFieldElement(10657, 65537),
              finitefield.FinitePrimeFieldElement(46245, 65537)]
        self.failIf(256 % e2.pointorder(P2))
        weil10 = set(e2.WeilPairing(256, P1, P2) for i in range(10))
        # since Weil pairing is a function, the result is always same
        self.assertEqual(1, len(weil10))
        # Weil pairing is a function E[m]xE[m] -> mu_m
        self.assertEqual(e2.basefield.one, weil10.pop()**256)

    def testTatePairing(self):
        # this example was refered to Washington.
        # note that Tate pairing is only defined
        # up to a multiple by an lth power.
        e = elliptic.EC([-1, 1], 11)
        self.assertEqual(10, e.order())
        P = [e.basefield.createElement(3), e.basefield.createElement(6)]
        R = e.TatePairing(5, P, P)
        l = map(finitefield.FinitePrimeFieldElement, [5, 6], [11]*2)
        self.assert_(R in l, R)

    def testTatePairing_Extend(self):
        # this example was refered to Kim Nguyen.
        e = elliptic.EC([0, 4], 997)
        P = [0, 2]
        Q = [747, 776]
        R = e.TatePairing_Extend(3, P, P)
        W1 = e.TatePairing_Extend(3, P, Q)
        W2 = e.TatePairing_Extend(3, Q, P)
        self.assertEqual(e.basefield.one, R)
        self.assertEqual(finitefield.FinitePrimeFieldElement(304, 997), W1)
        self.assertEqual(W1, W2.inverse())

    def testStructure(self):
        # this example was rechecked by MAGMA.
        e = elliptic.EC([0, 4], 997)
        f = elliptic.EC([-1, 0], 65537)
        g = elliptic.EC([0, 1], 65537)
        self.assertEqual((12, 84),  e.structure())
        self.assertEqual((256, 256),  f.structure())
        self.assertEqual((1, 65538),  g.structure())


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
