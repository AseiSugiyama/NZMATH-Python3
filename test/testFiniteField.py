import unittest
from finitefield import *
from rational import Integer
from rational import Rational

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

    def testGetRing(self):
        elem = FinitePrimeFieldElement(12, 17)
        f17 = elem.getRing()
        self.failUnless(isinstance(f17, FinitePrimeField))
        self.failUnless(elem in f17)

    def testNonzero(self):
        self.failUnless(FinitePrimeFieldElement(12, 17))
        self.failIf(FinitePrimeFieldElement(0, 17))

class FinitePrimeFieldTest(unittest.TestCase):
    def testEq(self):
        self.assertEqual(FinitePrimeField(17), FinitePrimeField(17))

    def testNonZero(self):
        self.failUnless(FinitePrimeField(17))
        self.failUnless(FinitePrimeField(17L))

    def testConst(self):
        F17 = FinitePrimeField(17)
        self.assertEqual(FinitePrimeFieldElement(1, 17), F17.one)
        self.assertEqual(FinitePrimeFieldElement(0, 17), F17.zero)
        self.assertEqual(F17.one, F17.one * F17.one)
        self.assertEqual(F17.one, F17.one + F17.zero)
        self.assertEqual(F17.zero, F17.zero * F17.zero)

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
