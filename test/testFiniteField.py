import unittest
from finitefield import *
from rational import Integer
from rational import Rational

class FinitePrimeFieldElementTest(unittest.TestCase):
    def testInit(self):
        elem = FinitePrimeFieldElement(12, 17)
        assert elem
        assert elem.toInteger() == 12
        assert elem.getModulus() == 17
        residue = FinitePrimeFieldElement(Rational(8,15), 11)
        assert residue
        assert residue.toInteger() == 2
        assert residue.getModulus() == 11

    def testMul(self):
        residue1 = FinitePrimeFieldElement(8, 151)
        residue2 = FinitePrimeFieldElement(2, 151)
        assert residue1 * residue2
        assert (residue1 * residue2).toInteger() == 16
        assert (residue1 * residue2).getModulus() == 151
        assert residue1 * 2
        assert (residue1 * 2).toInteger() == 16
        assert (residue1 * 2).getModulus() == 151
        assert 2 * residue1
        assert (2 * residue1).toInteger() == 16
        assert (2 * residue1).getModulus() == 151
        assert residue1 * Rational(1, 76)
        assert (residue1 * Rational(1, 76)).toInteger() == 16
        assert (residue1 * Rational(1, 76)).getModulus() == 151
        assert Rational(1, 76) * residue1
        assert (Rational(1, 76) * residue1).toInteger() == 16
        assert (Rational(1, 76) * residue1).getModulus() == 151

    def testGetRing(self):
        elem = FinitePrimeFieldElement(12, 17)
        f17 = elem.getRing()
        assert isinstance(f17, FinitePrimeField)
        assert elem in f17

class FinitePrimeFieldTest(unittest.TestCase):
    def testEq(self):
        assert FinitePrimeField(17) == FinitePrimeField(17)

    def testNonZero(self):
        assert FinitePrimeField(17)
        assert FinitePrimeField(17L)

def suite():
    suite = unittest.TestSuite((
        unittest.makeSuite(FinitePrimeFieldElementTest, 'test'),
        unittest.makeSuite(FinitePrimeFieldTest, 'test'),
        ))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
