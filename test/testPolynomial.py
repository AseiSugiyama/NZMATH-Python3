import unittest
from polynomial import *

# data for debugging

a = IntegerPolynomial([1,1],"x")

b = IntegerPolynomial([1,-2,3,-4],"x")

c = IntegerPolynomial([1,-1,-2],"y")

d = IntegerPolynomial([1,1,2],"y")

e = IntegerPolynomial([0,1,2,3,4],"z")

f = FlatIntegerPolynomial({(0,0):1,(1,0):2,(2,0):3,(1,1):4,(0,3):5},["x","z"])

g = FlatIntegerPolynomial({(0,0,0):1,(1,0,0):-2,(1,0,3):3,(1,1,1):-4,(0,2,1):5,(2,2,2):-6},["y","z","x"])

class IntegerPolynomialTest(unittest.TestCase):
    def testAdd(self):
        sum_1 = IntegerPolynomial([2,-1,3,-4],"x")
        sum_2 = FlatIntegerPolynomial({(0,0,0):2,(1,0,0):1,(0,1,0):-2,(3,1,0):3,(0,0,1):1,(1,1,1):-4,(0,0,2):2,(1,0,2):5,(2,2,2):-6,(0,0,3):3,(0,0,4):4},["x","y","z"])
        assert a + b == sum_1
        assert a + e + g == sum_2

    def testSub(self):
        sub_1 = IntegerPolynomial([0,2,4],"y")
        sub_2 = FlatIntegerPolynomial({(0,0,0):-1,(1,0,0):1,(2,0,0):3,(0,1,0):2,(3,1,0):-3,(1,0,1):4,(1,1,1):4,(1,0,2):-5,(2,2,2):6,(0,0,3):5},["x","y","z"])
        assert d - c == sub_1
        assert f - g - a == sub_2

    def testMul(self):
        mul_1 = IntegerPolynomial([1,0,-1,-4,-4],"y")
        mul_2 = FlatIntegerPolynomial({(0,0,0):1,(1,0,0):2,(2,0,0):3,(0,1,0):-1,(1,1,0):-2,(2,1,0):-3,(0,2,0):-2,(1,2,0):-4,(2,2,0):-6,(1,0,1):4,(1,1,1):-4,(1,2,1):-8,(0,0,3):5,(0,1,3):-5,(0,2,3):-10},["x","y","z"])
        assert c * d == mul_1
        assert c * f == mul_2

    def testScalarMul(self):
        mul_1 = IntegerPolynomial([0,3,6,9,12],"z")
        mul_2 = FlatIntegerPolynomial({(0,0,0):-5,(0,1,0):10,(3,1,0):-15,(1,1,1):20,(1,0,2):-25,(2,2,2):30},["x","y","z"])
        assert e * 3 == mul_1
        assert g * (-5) == mul_2

    def testDifferentiate(self):
        deff_1 = IntegerPolynomial([1,4,9,16],"z")
        deff_2 = FlatIntegerPolynomial({(2,1,0):9,(0,1,1):-4,(0,0,2):5,(1,2,2):-12},["x","y","z"])
        assert deff_1 == IntegerPolynomial.differentiate(e,"z")
        assert deff_2 == FlatIntegerPolynomial.differentiate(g,"x")

    def testCall(self):
        call_1 = 49
        call_2 = IntegerPolynomial([0,1,2,3,4],"y")
        call_3 = 4
        call_4 = FlatIntegerPolynomial({(0,):9,(1,):-8,(3,):5},["y"])
        assert b(-2) == call_1
        assert e("y") == call_2
        assert f(x = 2,z = -1) == call_3
        assert f(x = -2,z = "y") == call_4

def suite():
    suite = unittest.TestSuite()
    suite.addTest(IntegerPolynomialTest("testAdd"))
    suite.addTest(IntegerPolynomialTest("testSub"))
    suite.addTest(IntegerPolynomialTest("testMul"))
    suite.addTest(IntegerPolynomialTest("testScalarMul"))
    suite.addTest(IntegerPolynomialTest("testDifferentiate"))
    suite.addTest(IntegerPolynomialTest("testCall"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())