import unittest
from nzmath.permute import *

a1 = Permute([1, 3, 2, 4])
a2 = Permute([2, 3, 1, 4])

b1 = ExPermute(4, [(1, 2, 3, 4)])
b2 = ExPermute(5, [(1, 2, 3)])


class PermTest(unittest.TestCase):

    def testGetItem(self):
        assert(4 == a1[4])

    def testMul(self):
        assert(Permute([3, 2, 1, 4]) == a1 * a2)

    def testDiv(self):
        assert(Permute([2, 1, 3, 4]) == a1 / a2)

    def testPow(self):
        assert(Permute([1, 2, 3, 4]) == a1 ** 2)

    def testInverse(self):
        assert(Permute([1, 3, 2, 4]) == a1.inverse())

    def testIdentity(self):
        assert(Permute([1, 2, 3, 4]) == a1.identify())

    def testNumber(self):
        assert(3 == a1.numbering())

    def testGroupOrder(self):
        assert(24 == a1.grouporder())

    def testOrder(self):
        assert(2 == a1.order())
    
    def testToTranspose(self):
        assert(ExPermute(4, [(1, 3), (1, 2)]) == a2.ToTranspose())

    def testToCyclic(self):
        assert(ExPermute(4, [(1, 2, 3)]) == a2.ToCyclic())

    def testSign(self):
        assert(-1 == a1.sgn())

    def testTypes(self):
        assert('[2] type' == a1.types())

    def testToMatrix(self):
        from nzmath.matrix import Matrix
        assert(Matrix(4, 4, [1, 0, 0, 0,  0, 0, 1, 0,  1, 0, 0, 0,  0, 0, 0, 1]))

    def testEqual(self):
        assert(a1 == a1)


class ExPermTest(unittest.TestCase):

    def TestMul(self):
        assert(ExPermute(4, [(1, 2, 3), (1, 2, 3, 4)]) == b1 * b2)
        
    def TestDiv(self):
        assert(ExPermute(4, [(1, 2, 3, 4), (1, 3, 2)]) == b1 / b2)

    def TestPow(self):
        assert(ExPermute(4, [(1, 3, 2, 4)]) == b2 ** 2)

    def TestInverse(self):
        assert(ExPermute(4, [(1, 4, 3, 2)]) == b1.inverse())

    def TestIdentify(self):
        assert(ExPermute(4, []) == b1.inverse())

    def TestGroupOrder(self):
        assert(24 == b1.inverse())

    def TestOrder(self):
        assert(4 == b1.order())

    def TestToNormal(self):
        assert(Permute([2, 3, 4, 1]) == b1.ToNormal())

    def TestSimplify(self):
        assert(ExPermute(4, [(1, 2, 3, 4)]) == b1.simplify())

    def TestEqual(self):
        assert(b1 == b1)
        

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
