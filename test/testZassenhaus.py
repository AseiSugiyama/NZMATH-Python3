import unittest
import zassenhaus
import polynomial

class ZassenhausTest (unittest.TestCase):
    pass

class VanHoeijTest (unittest.TestCase):
    pass

class PadicFactorizationTest (unittest.TestCase):
    def testRegular(self):
        zassenhaus.padicFactorization(polynomial.OneVariableDensePolynomial([12,7,1],'X'))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZassenhausTest, "test"))
    suite.addTest(unittest.makeSuite(VanHoeijTest, "test"))
    suite.addTest(unittest.makeSuite(PadicFactorizationTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
