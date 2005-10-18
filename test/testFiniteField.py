import unittest
from finitefield import *
from rational import Integer, Rational, theRationalField


class FinitePrimeFieldElementTest(unittest.TestCase):
    def testInit(self):
        elem = FinitePrimeFieldElement(12, 17)
        self.failUnless(elem)
        self.assertEqual(12, elem.toInteger())
        self.assertEqual(17, elem.getModulus())
        residue = FinitePrimeFieldElement(Rational(8,15), 11)
        self.failUnless(residue)
        self.assertEqual(2, residue.toInteger())
        self.assertEqual(11, residue.getModulus())

    def testMul(self):
        residue1 = FinitePrimeFieldElement(8, 151)
        residue2 = FinitePrimeFieldElement(2, 151)
        self.failUnless(residue1 * residue2)
        self.failUnless(isinstance(residue1 * residue2, FinitePrimeFieldElement))
        self.assertEqual(16, (residue1 * residue2).toInteger())
        self.assertEqual(151, (residue1 * residue2).getModulus())
        self.failUnless(residue1 * 2)
        self.assertEqual(16, (residue1 * 2).toInteger())
        self.assertEqual(151, (residue1 * 2).getModulus())
        self.failUnless(2 * residue1)
        self.assertEqual(16, (2 * residue1).toInteger())
        self.assertEqual(151, (2 * residue1).getModulus())
        self.failUnless(residue1 * Rational(1, 76))
        self.assertEqual(16, (residue1 * Rational(1, 76)).toInteger())
        self.assertEqual(151, (residue1 * Rational(1, 76)).getModulus())
        self.failUnless(Rational(1, 76) * residue1)
        self.assertEqual(16, (Rational(1, 76) * residue1).toInteger())
        self.assertEqual(151, (Rational(1, 76) * residue1).getModulus())

    def testDiv(self):
        zero = FinitePrimeFieldElement(0, 5)
        one = FinitePrimeFieldElement(1, 5)
        self.failUnless(isinstance(zero.__div__(one), FinitePrimeFieldElement))
        self.failUnless(isinstance(zero.__truediv__(one), FinitePrimeFieldElement))
        self.assertEqual(zero, zero / one)

    def testAdd(self):
        residue1 = FinitePrimeFieldElement(8, 151)
        residue2 = FinitePrimeFieldElement(2, 151)
        self.failUnless(isinstance(residue1 + residue2, FinitePrimeFieldElement))

    def testSub(self):
        residue1 = FinitePrimeFieldElement(8, 151)
        residue2 = FinitePrimeFieldElement(2, 151)
        self.failUnless(isinstance(residue1 - residue2, FinitePrimeFieldElement))
        # the followings are possible now. are they correct?
        self.failUnless(isinstance(residue1 - 2, FinitePrimeFieldElement))
        self.failUnless(isinstance(1 - residue2, FinitePrimeFieldElement))

    def testInverse(self):
        residue1 = FinitePrimeFieldElement(8, 151)
        self.failUnless(isinstance(residue1.inverse(), FinitePrimeFieldElement))

    def testGetRing(self):
        elem = FinitePrimeFieldElement(12, 17)
        f17 = elem.getRing()
        self.failUnless(isinstance(f17, FinitePrimeField))
        self.failUnless(elem in f17)

    def testNonzero(self):
        self.failUnless(FinitePrimeFieldElement(12, 17))
        self.failIf(FinitePrimeFieldElement(0, 17))

    def testOrder(self):
        zero = FinitePrimeFieldElement(0, 5)
        one = FinitePrimeFieldElement(1, 541)
        minusone = FinitePrimeFieldElement(3910, 3911)
        elem = FinitePrimeFieldElement(12, 17)
        self.assertRaises(ValueError, zero.order)
        self.assertEqual(1, one.order())
        self.assertEqual(2, minusone.order())
        self.assertEqual(16, elem.order())


class FinitePrimeFieldTest(unittest.TestCase):
    def setUp(self):
        self.F17 = FinitePrimeField(17)
    
    def testEq(self):
        self.assertEqual(self.F17, self.F17)

    def testNonZero(self):
        self.failUnless(self.F17)
        self.failUnless(FinitePrimeField(17L))

    def testConst(self):
        self.assertEqual(FinitePrimeFieldElement(1, 17), self.F17.one)
        self.assertEqual(FinitePrimeFieldElement(0, 17), self.F17.zero)
        self.assertEqual(self.F17.one, self.F17.one * self.F17.one)
        self.assertEqual(self.F17.one, self.F17.one + self.F17.zero)
        self.assertEqual(self.F17.zero, self.F17.zero * self.F17.zero)

    def testGetInstance(self):
        self.assertEqual(self.F17, FinitePrimeField.getInstance(17))
        self.failUnless(FinitePrimeField.getInstance(17) is FinitePrimeField.getInstance(17))

    def testStrings(self):
        self.assertEqual("F_17", str(self.F17))
        self.assertEqual("FinitePrimeField(17)", repr(self.F17))

    def testSubring(self):
        self.assert_(self.F17.issubring(self.F17))
        self.assert_(self.F17.issuperring(self.F17))
        # polynomial ring
        import polynomial
        F17X = polynomial.PolynomialRing(self.F17, 'X')
        self.assert_(self.F17.issubring(F17X))
        self.failIf(self.F17.issuperring(F17X))
        # rational field
        self.failIf(self.F17.issuperring(theRationalField))
        self.failIf(self.F17.issubring(theRationalField))
        

def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name[-len(suffix):] == suffix:
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
