import unittest
from nzmath.group import *
from nzmath.finitefield import FinitePrimeFieldElement
from nzmath.permute import Permute

a1 = GroupElement(Permute([2, 4, 1, 3])) #Multiplication Group
a2 = GroupElement(Permute([3, 1, 4, 2]))
aa1 = a1.getGroup()

c1_a = GroupElement(FinitePrimeFieldElement(20, 37)) #Field
cc1_a = c1_a.getGroup()
c2 = GroupElement(FinitePrimeFieldElement(15, 37))
c1_m = GroupElement(c1_a.element)
cc1_m = c1_m.getGroup()
c1_m.setmain(1)
cc1_m.setmain(1)


class GroupTest (unittest.TestCase):

    def testidentity(self):
        assert(GroupElement(Permute([1, 2, 3, 4])) == aa1.identity())
        assert(GroupElement(FinitePrimeFieldElement(0, 37)) == cc1_a.identity())
        assert(GroupElement(FinitePrimeFieldElement(1, 37)) == cc1_m.identity())

    def testGroupOrder(self):
        assert(24 == aa1.grouporder())
        assert(37 == cc1_a.grouporder())
        assert(36 == cc1_m.grouporder())


class GroupElementTest(unittest.TestCase):
    def testEqual(self):
        assert(a1 == GroupElement(Permute([2, 4, 1, 3])))
        assert(c1_a == GroupElement(FinitePrimeFieldElement(20, 37)))
        assert(c1_m == GroupElement(FinitePrimeFieldElement(20, 37)))

    def testOpe1(self):
        assert(GroupElement(Permute([1, 2, 3, 4])) == a1.ope(a2))
        assert(GroupElement(FinitePrimeFieldElement(35, 37)) == c1_a.ope(c2))
        assert(GroupElement(FinitePrimeFieldElement(4, 37)) == c1_m.ope(c2))

    def testOpe2(self):
        assert(GroupElement(Permute([3, 1, 4, 2])) == a1.ope2(3))
        assert(GroupElement(FinitePrimeFieldElement(3, 37)) == c1_a.ope2(2))
        assert(GroupElement(FinitePrimeFieldElement(30, 37)) == c1_m.ope2(2))

    def testOrder(self):
        assert(4 == a1.order())
        assert(37 == c1_a.order())
        assert(36 == c1_m.order())

    def testT_Order(self):
        assert(4 == a1.t_order())
        assert(37 == c1_a.t_order())
        assert(36 == c1_m.t_order())


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
