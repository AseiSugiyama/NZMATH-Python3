import unittest
from nzmath.algorithm import *
from nzmath import matrix

class DigitalMethodTest(unittest.TestCase):
    def testDigitalMethod(self):
        zero1 = matrix.zeroMatrix(3,0)
        one1 = matrix.identityMatrix(3,1)
        d_func1 = digital_method_func(
        lambda a,b:a+b, lambda a,b:a*b, lambda i,a:i*a, lambda a,i:a**i, 
        zero1, one1)
        coefficients11 = []
        coefficients12 = [(2,1), (1,2), (0,1)]
        coefficients13 = [(3,1), (2,2), (1,3)]
        A = matrix.SquareMatrix(3, [1,2,3]+[4,5,6]+[7,8,9])
        self.assertEqual(d_func1(coefficients11, A), zero1)
        self.assertEqual(d_func1(coefficients12, A), A**2+2*A+one1)
        self.assertEqual(d_func1(coefficients13, A), (A**3+2*A**2+3*A))

class PoweringTest(unittest.TestCase):
    def testPowering(self):
        one1 = matrix.identityMatrix(3,1)
        A = matrix.SquareMatrix(3, [1,2,3]+[4,5,6]+[7,8,9])
        p_func10 = powering_func(lambda a,b:a*b, one=one1, type=0)
        p_func11 = powering_func(lambda a,b:a*b, one=one1, type=1)
        p_func12 = powering_func(lambda a,b:a*b, one=one1, type=2)
        #trivial test
        self.assertEqual(p_func10(A, 0), one1)
        self.assertEqual(p_func11(A, 0), one1)
        self.assertEqual(p_func12(A, 0), one1)
        self.assertEqual(p_func10(A, 1), A)
        self.assertEqual(p_func11(A, 1), A)
        self.assertEqual(p_func12(A, 1), A)
        #normal test
        self.assertEqual(p_func10(A, 12345), A**12345)
        self.assertEqual(p_func11(A, 12345), A**12345)
        self.assertEqual(p_func12(A, 12345), A**12345)


def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
