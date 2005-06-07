import unittest
import zassenhaus
import polynomial

class ZassenhausTest (unittest.TestCase):
    def testRegular(self):
        r = zassenhaus.zassenhaus(polynomial.OneVariableDensePolynomial([12,7,1],'X'))
        assert isinstance(r, list)
        assert 2 == len(r), r

class VanHoeijTest (unittest.TestCase):
    def testRegular(self):
        r = zassenhaus.vanHoeij(polynomial.OneVariableDensePolynomial([12,7,1],'X'))
        assert isinstance(r, list)
        assert 2 == len(r), r

class PadicFactorizationTest (unittest.TestCase):
    def testRegular(self):
        r = zassenhaus.padicFactorization(polynomial.OneVariableDensePolynomial([12,7,1],'X'))
        assert isinstance(r, tuple)
        assert 2 == len(r)
        import prime
        assert prime.primeq(r[0])
        assert isinstance(r[1], list)
        assert 2 == len(r[1])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZassenhausTest, "test"))
    suite.addTest(unittest.makeSuite(VanHoeijTest, "test"))
    suite.addTest(unittest.makeSuite(PadicFactorizationTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
