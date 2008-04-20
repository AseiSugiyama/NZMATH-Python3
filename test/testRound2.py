from __future__ import division
import unittest
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil
import nzmath.round2 as round2

import logging
logging.basicConfig(level=logging.WARN)


class Round2UniutilTest (unittest.TestCase):
    """
    Test for the main function round2.
    """
    def setUp(self):
        """
        setup some polynomials.
        """
        self.root2 = [-2, 0, 1]
        self.root1i = [1, 0, 1]
        self.cubic = [1, 9, 0, 1]
        self.sextic = range(7, 0, -1)
        self.septic = range(8, 0, -1)
        self.Z = rational.theIntegerRing
        self.Q = rational.theRationalField

    def testTrivial(self):
        """
	Test trivial errorlessness.

        using Q(sqrt(2)).
	"""
        q2 = round2.round2(self.root2)
        self.assert_(q2)
        self.assertEqual(2, len(q2))
        self.assertEqual(8, q2[1], q2) # disc K = 8

    def testNegativeDisc(self):
        """
	Test negative discriminant.

        using Q(sqrt(-1)).
	"""
        q1i = round2.round2(self.root1i)
        self.assert_(q1i)
        self.assertEqual(2, len(q1i))
        self.assertEqual(-4, q1i[1], q1i) # disc K = -4

    def testCubic(self):
        """
	Test an example: X^3 + 9X + 1
	"""
        poly_disc = uniutil.polynomial(enumerate(self.cubic), self.Z).discriminant()
        self.assertEqual(-3**3 * 109, poly_disc)
        result = round2.round2(self.cubic)
        self.assert_(result)
        self.assertEqual(2, len(result))
        self.assertEqual(-327, result[1], result) # disc K = -327 = -3 * 109

    def testSextic(self):
        """
	Test an example: X^6 + 2X^5 + ... + 6X + 7
	"""
        poly_disc = uniutil.polynomial(enumerate(self.sextic), self.Z).discriminant()
        self.assertEqual(-2**16 * 7**4, poly_disc)
        result = round2.round2(self.sextic)
        self.assert_(result)
        self.assertEqual(2, len(result))
        self.assertEqual(-9834496, result[1], result) # disc K = - 2**12 * 7**4

    def testSeptic(self):
        """
	Test an example: X^7 + 2X^6 + ... + 7X + 8
	"""
        poly_disc = uniutil.polynomial(enumerate(self.septic), self.Z).discriminant()
        self.assertEqual(-2**16 * 3**12, poly_disc)
        result = round2.round2(self.septic)
        self.assert_(result)
        self.assertEqual(2, len(result))
        self.assertEqual(-2**12 * 3**10, result[1], result)


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
