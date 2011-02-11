import unittest
import nzmath.finitefield as finitefield
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil
# the test target:
import sandbox.linrec as linrec


class MinpolyTest(unittest.TestCase):
    def testAtti(self):
        """
	This test case is taken from the paper of Atti et al.
	"""
        Q = rational.theRationalField
        rat = rational.Rational
        ann = uniutil.polynomial(enumerate([0, 1, 1, 1]), Q)
	self.assertEqual(ann, linrec.minpoly(map(rat, [1, 2, 7, -9, 2, 7])))

    def testAtti_19(self):
        """
	testAtti on F19
	"""
        F19 = finitefield.FinitePrimeField.getInstance(19)
        f19 = F19.createElement
        ann = uniutil.polynomial(enumerate([0, 1, 1, 1]), F19)
	self.assertEqual(ann, linrec.minpoly(map(f19, [1, 2, 7, -9, 2, 7])))

    def testShortSeq(self):
        """
        sequence has less dimension
        """
        F5 = finitefield.FinitePrimeField.getInstance(5)
        f5 = F5.createElement
        ann = uniutil.polynomial({1:1}, F5)
        self.assertEqual(ann, linrec.minpoly(map(f5, [3, 0, 0, 0, 0, 0])))
        ann = uniutil.polynomial({2:1}, F5)
        self.assertEqual(ann, linrec.minpoly(map(f5, [3, 1, 0, 0, 0, 0])))


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
