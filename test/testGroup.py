import unittest
from nzmath.group import *
from nzmath.finitefield import FinitePrimeFieldElement, FinitePrimeField
from nzmath.integerResidueClass import *
from nzmath.permute import Permute

a1 = GroupElement(Permute([2, 4, 1, 3])) #Multiplication Group
a2 = GroupElement(Permute([3, 1, 4, 2]))
aa1 = a1.getGroup()

b1 = GroupElement(IntegerResidueClass(4, 30)) #additive Group
b2 = GroupElement(IntegerResidueClass(8, 30))
bb1 = b1.getGroup()

c1_a = GroupElement(FinitePrimeFieldElement(20, 37)) #Field
cc1_a = c1_a.getGroup()
c2 = GroupElement(FinitePrimeFieldElement(15, 37))
c1_m = GroupElement(c1_a.element)
cc1_m = c1_m.getGroup()
c1_m.setmain(1)
cc1_m.setmain(1)

bg = AbelianGenerate([b1, b2])

class GroupTest (unittest.TestCase):
    def testEqual(self):
        assert(aa1 == Group(Permute([2, 4, 1, 3]), 1))
        assert(bb1 == Group(IntegerResidueClassRing(30)))
        assert(cc1_a == Group(FinitePrimeField(37)))
        assert(cc1_m == Group(FinitePrimeField(37), 1))

    def testidentity(self):
        assert(GroupElement(Permute([1, 2, 3, 4]), 1) == aa1.identity())
        assert(GroupElement(IntegerResidueClass(0, 30)) == bb1.identity())
        assert(GroupElement(FinitePrimeFieldElement(0, 37)) == cc1_a.identity())
        assert(GroupElement(FinitePrimeFieldElement(1, 37), 1) == cc1_m.identity())

    def testGroupOrder(self):
        assert(24 == aa1.grouporder())
        assert(30 == bb1.grouporder())
        assert(37 == cc1_a.grouporder())
        assert(36 == cc1_m.grouporder())


class GroupElementTest(unittest.TestCase):
    def testEqual(self):
        assert(a1 == GroupElement(Permute([2, 4, 1, 3]), 1))
        assert(b1 == GroupElement(IntegerResidueClass(4, 30)))
        assert(c1_a == GroupElement(FinitePrimeFieldElement(20, 37)))
        assert(c1_m == GroupElement(FinitePrimeFieldElement(20, 37), 1))

    def testOpe(self):
        assert(GroupElement(Permute([1, 2, 3, 4]), 1) == a1.ope(a2))
        assert(GroupElement(IntegerResidueClass(12, 30)) == b1.ope(b2))
        assert(GroupElement(FinitePrimeFieldElement(35, 37)) == c1_a.ope(c2))
        assert(GroupElement(FinitePrimeFieldElement(4, 37), 1) == c1_m.ope(c2))

    def testOpe2(self):
        assert(GroupElement(Permute([3, 1, 4, 2]), 1) == a1.ope2(3))
        assert(GroupElement(IntegerResidueClass(2, 30)) == b1.ope2(8))
        assert(GroupElement(FinitePrimeFieldElement(3, 37)) == c1_a.ope2(2))
        assert(GroupElement(FinitePrimeFieldElement(30, 37), 1) == c1_m.ope2(2))
        
    def testInverse(self):
        assert(GroupElement(Permute([3, 1, 4, 2]), 1) == a1.inverse())
        assert(GroupElement(IntegerResidueClass(26, 30)) == b1.inverse())
        assert(GroupElement(FinitePrimeFieldElement(17, 37)) == c1_a.inverse())
        assert(GroupElement(FinitePrimeFieldElement(13, 37), 1) == c1_m.inverse())

    def testOrder(self):
        assert(4 == a1.order())
        assert(15 == b1.order())
        assert(37 == c1_a.order())
        assert(36 == c1_m.order())

    def testT_Order(self):
        assert(4 == a1.t_order())
        assert(15 == b1.order())
        assert(37 == c1_a.t_order())
        assert(36 == c1_m.t_order())

    def testGetGroup(self):
        assert(Group(Permute([2, 4, 1, 3]), 1) == a1.getGroup())
        assert(Group(IntegerResidueClassRing(30)) == b1.getGroup())
        assert(Group(FinitePrimeField(37)) == c1_a.getGroup())
        assert(Group(FinitePrimeField(37), 1) == c1_m.getGroup())


class AbelianGenerateTest(unittest.TestCase):
    def testRelationLattice(self):
        result = bg.relationLattice()
        assert(((4 * result[1, 1] + 8 * result[2, 1]) % 30) == 0)
        assert(((4 * result[1, 2] + 8 * result[2, 2]) % 30) == 0)
        
    def testComputeStructure(self):
        assert([IntegerResidueClass(4, 30)], 15 == bg.computeStructure())


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
