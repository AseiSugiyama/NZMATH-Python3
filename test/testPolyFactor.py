import unittest
import nzmath.prime as prime
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil
import nzmath.poly.factor as zassenhaus


Z = rational.theIntegerRing


class ZassenhausTest (unittest.TestCase):
    def testRegular(self):
        f = uniutil.polynomial(enumerate([12, 7, 1]), Z)
        r = zassenhaus.zassenhaus(f)
        self.assert_(isinstance(r, list))
        self.assertEqual(2, len(r), r)
        self.assert_(isinstance(r[0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assert_(isinstance(r[1], uniutil.UniqueFactorizationDomainPolynomial))
        self.assertEqual(f, r[0] * r[1])

    def testIrreducible(self):
        f = uniutil.polynomial(enumerate([12, 6, 1]), Z)
        r = zassenhaus.zassenhaus(f)
        self.assert_(isinstance(r, list), r)
        self.assertEqual(1, len(r))
        self.assert_(isinstance(r[0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assertEqual(f, r[0])


class PadicFactorizationTest (unittest.TestCase):
    def testRegular(self):
        f = uniutil.polynomial(enumerate([12, 7, 1]), Z)
        r = zassenhaus.padic_factorization(f)
        self.assert_(isinstance(r, tuple))
        self.assertEqual(2, len(r))
        self.assert_(prime.primeq(r[0]))
        self.assert_(isinstance(r[1], list))
        self.assertEqual(2, len(r[1]))

    def testIrreducible(self):
        f = uniutil.polynomial(enumerate([12, 6, 1]), Z)
        r = zassenhaus.padic_factorization(f)
        self.assert_(isinstance(r, tuple), r)

class IntegerPolynomialFactorizationTest (unittest.TestCase):
    def testRegular(self):
        f1 = uniutil.polynomial(enumerate([1, 2]), Z)
        f2 = uniutil.polynomial(enumerate([5, 4, 1]), Z)
        f3_1 = uniutil.polynomial(enumerate([-1, 3]), Z)
        f3_2 = uniutil.polynomial(enumerate([1, 3]), Z)
        f = f1**5 * f2**3 * f3_1 * f3_2

        r = zassenhaus.integerpolynomialfactorization(f)
        self.assert_(isinstance(r, list))
        self.assertEqual(4, len(r), r)
        self.assert_(isinstance(r[0][0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assert_(isinstance(r[1][0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assert_(isinstance(r[2][0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assert_(isinstance(r[3][0], uniutil.UniqueFactorizationDomainPolynomial))
        self.assertEqual(f, r[0][0]**r[0][1] * r[1][0]**r[1][1] * r[2][0]**r[2][1] * r[3][0]**r[3][1])

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
