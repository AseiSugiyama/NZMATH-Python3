import unittest
from rationalFunction import RationalFunction, RationalFunctionField
from rational import theRationalField as Q
from rational import theIntegerRing as Z
import polynomial

class RationalFunctionTest (unittest.TestCase):
    def testInit(self):
        RationalFunction()

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RationalFunctionTest, 'test'))
    suite.addTest(unittest.makeSuite(RationalFunctionFieldTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
