import unittest
from nzmath.integerResidueClass import *
from nzmath.rational import Integer
from nzmath.rational import Rational

class IntegerResidueClassTest(unittest.TestCase):
    def testInit(self):
        residue = IntegerResidueClass(8, 15)
        assert residue
        assert residue.getResidue() == 8
        assert residue.getModulus() == 15
        residue = IntegerResidueClass(Rational(8,15), 11)
        assert residue
        assert residue.getResidue() == 2
        assert residue.getModulus() == 11

    def testMul(self):
        residue1 = IntegerResidueClass(8, 15)
        residue2 = IntegerResidueClass(2, 15)
        assert residue1 * residue2
        assert (residue1 * residue2).getResidue() == 1
        assert (residue1 * residue2).getModulus() == 15
        assert residue1 * 2
        assert (residue1 * 2).getResidue() == 1
        assert (residue1 * 2).getModulus() == 15
        assert 2 * residue1
        assert (2 * residue1).getResidue() == 1
        assert (2 * residue1).getModulus() == 15
        rational2 = Rational(1, 23)
        assert residue1 * rational2
        assert (residue1 * rational2).getResidue() == 1
        assert (residue1 * rational2).getModulus() == 15

    def testDiv(self):
        residue0 = IntegerResidueClass(0, 15)
        residue1 = IntegerResidueClass(8, 15)
        residue2 = IntegerResidueClass(2, 15)
        assert isinstance(residue0 / residue1, IntegerResidueClass)
        assert residue1 / residue2
        assert (residue1 / residue2).getResidue() == 4
        assert (residue1 / residue2).getModulus() == 15
        assert residue1 / 2
        assert (residue1 / 2).getResidue() == 4
        assert (residue1 / 2).getModulus() == 15
        residue3 = IntegerResidueClass(2, 151)
        self.assertRaises(ValueError, residue1.__div__, residue3)

    def testAdd(self):
        residue1 = IntegerResidueClass(8, 15)
        residue2 = IntegerResidueClass(7, 15)
        assert (residue1 + residue2).__class__
        assert not residue1 + residue2
        assert (residue1 + residue2).getResidue() == 0
        assert (residue1 + residue2).getModulus() == 15
        residue3 = IntegerResidueClass(13, 60)
        assert residue1 + residue3
        assert (residue1 + residue3).getResidue() == 6
        assert (residue1 + residue3).getModulus() == 15
        assert residue1 + 2
        assert (residue1 + 2).getResidue() == 10
        assert (residue1 + 2).getModulus() == 15

    def testSub(self):
        residue1 = IntegerResidueClass(8, 15)
        residue2 = IntegerResidueClass(7, 15)
        assert residue1 - residue2
        assert (residue1 - residue2).getResidue() == 1
        assert (residue1 - residue2).getModulus() == 15
        residue3 = IntegerResidueClass(13, 60)
        assert residue1 - residue3
        assert (residue1 - residue3).getResidue() == 10
        assert (residue1 - residue3).getModulus() == 15
        assert residue1 - 2
        assert (residue1 - 2).getResidue() == 6
        assert (residue1 - 2).getModulus() == 15
        assert 2 - residue1
        assert (2 - residue1).getResidue() == 9
        assert (2 - residue1).getModulus() == 15

    def testNeg(self):
        residue1 = IntegerResidueClass(8, 15)
        assert -residue1
        assert (-residue1).getResidue() == 7
        assert (-residue1).getModulus() == 15

    def testPos(self):
        residue1 = IntegerResidueClass(8, 15)
        assert +residue1
        assert (+residue1).getResidue() == 8
        assert (+residue1).getModulus() == 15

    def testPow(self):
        residue1 = IntegerResidueClass(8, 15)
        assert residue1**4
        assert (residue1**4).getResidue() == 1
        assert (residue1**4).getModulus() == 15
        assert (residue1**0).getResidue() == 1

    def testToInteger(self):
        residue = IntegerResidueClass(8, 15)
        assert isinstance(residue.toInteger(), Integer)
        assert residue.toInteger() == 8

    def testGetRing(self):
        residue = IntegerResidueClass(8, 15)
        assert isinstance(residue.getRing(), IntegerResidueClassRing)

    def testEquals(self):
        residue = IntegerResidueClass(0, 15)
        assert residue == IntegerResidueClass(0, 15)
        assert 0 == residue
        assert 1 != IntegerResidueClass(1,15)

class IntegerResidueClassRingTest(unittest.TestCase):
    def testInit(self):
        aRing = IntegerResidueClassRing(73)
        assert aRing

    def testGetInstance(self):
        ring1 = IntegerResidueClassRing.getInstance(7)
        assert ring1
        ring2 = IntegerResidueClassRing.getInstance(7)
        assert ring1 is ring2
        ring3 = IntegerResidueClassRing.getInstance(17)
        assert ring1 is not ring3

    def testCreateElement(self):
        aRing = IntegerResidueClassRing.getInstance(7)
        assert aRing.createElement(3)
        assert isinstance(aRing.createElement(3), IntegerResidueClass)
        assert aRing.createElement(1091L)
        assert isinstance(aRing.createElement(1091L), IntegerResidueClass)
        assert aRing.createElement(IntegerResidueClass(1091,2527))
        assert isinstance(aRing.createElement(IntegerResidueClass(1091,2527)), IntegerResidueClass)
        assert aRing.createElement(Rational(2, 3))
        assert isinstance(aRing.createElement(Rational(2, 3)), IntegerResidueClass)
        self.assertRaises(ValueError, aRing.createElement, Rational(2, 21))

    def testContains(self):
        aRing = IntegerResidueClassRing.getInstance(7)
        assert IntegerResidueClass(1,7) in aRing

    def testProperties(self):
        Zmod3 = IntegerResidueClassRing.getInstance(3)
        assert Zmod3.isfield()
        assert Zmod3.ispid()
        assert Zmod3.isnoetherian()
        assert Zmod3.isdomain()
        Zmod4 = IntegerResidueClassRing.getInstance(4)
        assert not Zmod4.isfield()
        assert not Zmod4.isufd()
        assert not Zmod4.isdomain()

    def testConstants(self):
        Zmod4 = IntegerResidueClassRing.getInstance(4)
        self.assertEqual(IntegerResidueClass(1, 4), Zmod4.one)
        self.assertEqual(IntegerResidueClass(0, 4), Zmod4.zero)

    def testHash(self):
        dictionary = {}
        Zmod4 = IntegerResidueClassRing.getInstance(4)
        dictionary[Zmod4] = 4
        self.assertEqual(4, dictionary[IntegerResidueClassRing(4)])
        self.assertRaises(KeyError, dictionary.__getitem__, IntegerResidueClassRing.getInstance(4 + 0xFFFFFFFF))


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

