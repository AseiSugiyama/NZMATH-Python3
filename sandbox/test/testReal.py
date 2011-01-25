from __future__ import division
import unittest
import nzmath.rational as rational
import sandbox.imaginary as imaginary
import sandbox.real as real


class RealFieldTest (unittest.TestCase):
    def testConstants(self):
        self.assertEqual(1, real.theRealField.one)
        self.assertEqual(0, real.theRealField.zero)

    def testStrings(self):
        self.assertEqual("R", str(real.theRealField))
        self.assertEqual("RealField()", repr(real.theRealField))

    def testSubring(self):
        R = real.theRealField
        self.failUnless(R.issubring(R), 'trivial')
        self.failUnless(R.issuperring(R), 'trivial')
        self.failUnless(R.issuperring(rational.theRationalField), 'R > Q')
        self.failUnless(R.issubring(imaginary.theComplexField), 'R < C')
        self.failIf(R.issubring(rational.theRationalField), 'R < Q')

    def testHash(self):
        dictionary = {}
        dictionary[real.theRealField] = 1
        self.assertEqual(1, dictionary[real.RealField()])


def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
