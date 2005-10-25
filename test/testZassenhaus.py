import unittest
import nzmath.zassenhaus as zassenhaus
import nzmath.polynomial as polynomial

class ZassenhausTest (unittest.TestCase):
    def testRegular(self):
        f = polynomial.OneVariableDensePolynomial([12,7,1],'X')
        r = zassenhaus.zassenhaus(f)
        assert isinstance(r, list)
        assert 2 == len(r), r
        assert f == r[0] * r[1]

    def testIrreducible(self):
        f = polynomial.OneVariableDensePolynomial([12,6,1],'X')
        r = zassenhaus.zassenhaus(f)
        assert isinstance(r, list), r
        assert 1 == len(r)
        assert f == r[0]


class VanHoeijTest (unittest.TestCase):
    def testRegular(self):
        f = polynomial.OneVariableDensePolynomial([12,7,1],'X')
        r = zassenhaus.vanHoeij(f)
        assert isinstance(r, list)
        assert 2 == len(r), r
        assert f == r[0] * r[1]


class PadicFactorizationTest (unittest.TestCase):
    def testRegular(self):
        r = zassenhaus.padicFactorization(polynomial.OneVariableDensePolynomial([12,7,1],'X'))
        assert isinstance(r, tuple)
        assert 2 == len(r)
        import nzmath.prime as prime
        assert prime.primeq(r[0])
        assert isinstance(r[1], list)
        assert 2 == len(r[1])

    def testIrreducible(self):
        f = polynomial.OneVariableDensePolynomial([12,6,1],'X')
        r = zassenhaus.padicFactorization(f)
        assert isinstance(r, tuple), r


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZassenhausTest, "test"))
    suite.addTest(unittest.makeSuite(VanHoeijTest, "test"))
    suite.addTest(unittest.makeSuite(PadicFactorizationTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
