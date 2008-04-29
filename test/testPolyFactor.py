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
