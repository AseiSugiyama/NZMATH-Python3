from __future__ import division
import unittest
import logging
from nzmath.config import HAVE_MPMATH
import nzmath.ecpp as ecpp


logging.basicConfig(level=logging.INFO)


class NextDiscTest(unittest.TestCase):
    """
    test for ecpp.next_disc
    """
    def testFalse(self):
        result = ecpp.next_disc(-4, 7)
        self.assertEqual(False, result)

    def testBig(self):
        result = ecpp.next_disc(-215591, 300000)
        self.assertEqual(-215592, result)


class ECPPTest(unittest.TestCase):
    """
    test for ecpp.ecpp
    """
    def testPrime(self):
        #import nzmath.prime as prime
        p = 300000000000000000053 # prime.nextPrime(3*10**20)
        #p = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000267 #prime.nextPrime(10**100)
        self.assertTrue(ecpp.ecpp(p))

    def testComposite(self):
        n = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000139
        self.assertFalse(ecpp.ecpp(n))


class CMMethodTest(unittest.TestCase):
    """
    cmm, cmm_order
    """
    def test_cmm(self):
        result = ecpp.cmm(7)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(2, len(result[0]))

    def test_cmm_order(self):
        result = ecpp.cmm_order(7)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(3, len(result[0]))

    def test_param_gen(self):
        """param_gen"""
        result3 = [param for param in ecpp.param_gen(-3, 13, 2)]
        self.assertEqual(6, len(result3))
        result4 = [param for param in ecpp.param_gen(-4, 17, 3)]
        self.assertEqual(4, len(result4))
        resultg = [param for param in ecpp.param_gen(-7, 29, 2)]
        self.assertEqual(2, len(resultg))


if HAVE_MPMATH:
    import mpmath

    def q(tau):
        return mpmath.exp(mpmath.pi*1j*tau)

    # the following test is only runnable when there is mpmath
    class DedekindEtaTest(unittest.TestCase):
        def testSpecialValue(self):
            # eta at i
            self.assertAlmostEqual(0.7682254, abs(ecpp.dedekind(1j, 10)))

        def testIdentity1(self):
            """eta(t) = 1/sqrt(3) * theta_2(pi/6, q(t/3))"""
            # eta at omega, a third root of unity
            omega = (-1+mpmath.sqrt(3)*1j) / 2
            eta3 = ecpp.dedekind(omega, 18)
            theta3 = mpmath.jtheta(2, mpmath.pi/6, q(omega/3))/mpmath.sqrt(3)
            self.assertTrue(mpmath.almosteq(theta3, eta3), eta3 - theta3)

        def testIdentity2(self):
            """eta(t)**3 = theta_2(0,q(t))theta_3(0,q(t))theta_4(0,q(t))/2"""
            # eta at omega, a third root of unity
            omega = (-1+mpmath.sqrt(3)*1j) / 2
            eta3cubed = ecpp.dedekind(omega, 15)**3
            triple = (mpmath.jtheta(2, 0, q(omega))
                      * mpmath.jtheta(3, 0, q(omega))
                      * mpmath.jtheta(4, 0, q(omega))
                      / 2)
            self.assertTrue(mpmath.almosteq(triple, eta3cubed), triple - eta3cubed)


# The following part is always unedited.
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
