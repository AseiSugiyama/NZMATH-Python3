import unittest
from nzmath.rationalFunction import RationalFunction, RationalFunctionField
from nzmath.rational import theRationalField as Q
from nzmath.rational import theIntegerRing as Z
import nzmath.polynomial as polynomial

class RationalFunctionTest (unittest.TestCase):
    def setUp(self):
        self.f = RationalFunction(polynomial.construct("x**3 + 1"), polynomial.construct("x**2 - 2"))
        self.f2 = RationalFunction(polynomial.construct("x**3 + 1"), polynomial.construct("x**2 - 2"))
        self.f3 = RationalFunction(polynomial.construct("x**4 + x"), polynomial.construct("x**3 - 2 * x"))
    
    def testInit(self):
        assert self.f

    def testEquals(self):
        assert self.f == self.f2
        assert self.f == self.f3

    def testGetRing(self):
        assert isinstance(self.f.getRing(), RationalFunctionField)
        assert self.f.getRing() == RationalFunctionField(Q, "x")

class RationalFunctionFieldTest (unittest.TestCase):
    def setUp(self):
        self.Qx = RationalFunctionField(Q, "x")

    def testEquals(self):
        assert self.Qx == RationalFunctionField(Q, "x")
        assert not self.Qx == RationalFunctionField(Q, "X")
        assert not self.Qx == Q
        assert RationalFunctionField(Q, ("x", "y")) == RationalFunctionField(RationalFunctionField(Q, "x"), "y")

    def testIssubring(self):
        assert self.Qx.issubring(self.Qx)
        assert not self.Qx.issubring(Q)
        assert self.Qx.issubring(RationalFunctionField(Q, ("x", "y")))

    def testIssuperring(self):
        assert self.Qx.issuperring(self.Qx)
        assert self.Qx.issuperring(polynomial.PolynomialRing(Z, "x"))
        assert self.Qx.issuperring(polynomial.PolynomialRing(Q, "x"))
        assert self.Qx.issuperring(Q)
        assert not self.Qx.issuperring(RationalFunctionField(Q, ("x", "y")))

    def testContains(self):
        assert 1 in self.Qx
        assert Q.createElement(3,4) in self.Qx

    def testCreateElement(self):
        assert self.Qx.createElement(Z.createElement(8))

    def testConstants(self):
        self.assertNotEqual(self.Qx.zero, self.Qx.one)
        self.assertEqual(Q.createElement(1), self.Qx.one)
        self.assertEqual(Q.createElement(0), self.Qx.zero)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RationalFunctionTest, 'test'))
    suite.addTest(unittest.makeSuite(RationalFunctionFieldTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
