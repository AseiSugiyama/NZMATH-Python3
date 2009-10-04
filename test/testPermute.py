import unittest
from nzmath.permute import *

a1 = Permute([2, 3, 1, 4])
a2 = Permute([1, 3, 2, 0, 4], 0)
a3 = Permute([3, 4, 1, 0, 2], 0)
a4 = Permute(['b', 'c', 'a', 'd', 'e'], 1)
a5 = Permute(['@', '$', '~', '^', '#'], ['#', '$', '@', '^', '~']) 
a6 = Permute({'a':'b', 'b':'c', 'c':'a', 'd':'d', 'e':'e'})

b1 = ExPermute(4, [(1, 2, 3, 4)])
b2 = ExPermute(5, [(1, 2, 3)], 0)
b3 = ExPermute(5, [(2, 3, 4), (0, 1)], 0)
b4 = ExPermute(5, [('a', 'b')], ['a', 'b', 'c', 'd', 'e'])
b5 = ExPermute(5, [('b', 'a')], ['c', 'd', 'b', 'a', 'e'])

c = PermGroup(['a', 'b', 'c', 'd', 'e'])


class PermTest(unittest.TestCase):

    def testInit(self):
        assert(Permute([2, 4, 3, 1, 5], [0, 1, 2, 3, 4], flag=True) == a2)
        assert(Permute([2, 3, 1, 4, 5], ['a', 'b', 'c', 'd', 'e'], flag=True) == a4)
        assert(Permute([3, 2, 5, 4, 1], ['#', '$', '@', '^', '~'], flag=True) == a5)

    def testGetItem(self):
        assert(4 == a1[4])
        assert(4 == a2[4])
        assert('b' == a4['a'])
        assert('@' == a5['#'])
        assert('c' == a6['b'])

    def testMul(self):
        assert(Permute([0, 4, 3, 1, 2], 0) == a2 * a3)

    def testDiv(self):
        assert(Permute([0, 2, 4, 1, 3], 0) == a2 / a3)

    def testPow(self):
        assert(Permute([3, 0, 2, 1, 4], 0) == a2 ** 2)

    def testSetKey(self):
        a6.setKey(['a', 'b', 'c', 'd', 'e'])
        assert(a4 == a6)
        a3.setKey([1, 2, 3, 4, 5])
        assert(Permute([4, 5, 2, 1, 3]) == a3)

    def testGetValue(self):
        assert([3, 4, 1, 0, 2] == a3.getValue())
        a6.setKey(['a', 'b', 'c', 'd', 'e'])
        assert(['b', 'c', 'a', 'd', 'e'] == a6.getValue())

    def testInverse(self):
        assert(Permute([3, 0, 2, 1, 4], 0) == a2.inverse())

    def testNumber(self):
        assert(4 == a1.numbering())

    def testOrder(self):
        assert(3 == a1.order())
    
    def testToTranspose(self):
        assert(ExPermute(5, [(1, 3), (0, 3)], 0) == a2.ToTranspose())

    def testToCyclic(self):
        assert(ExPermute(5, [(1, 3, 0)], 0) == a2.ToCyclic())

    def testSign(self):
        assert(1 == a1.sgn())

    def testTypes(self):
        assert('[3] type' == a1.types())

    def testToMatrix(self):
        from nzmath.matrix import SquareMatrix
        matrices = SquareMatrix(4, 4, [0, 1, 0, 0,  0, 0, 1, 0,  1, 0, 0, 0,  0, 0, 0, 1])
        assert(matrices == a1.ToMatrix())

    def testPermute(self):
        assert(['d', 'a', 'c', 'b', 'e'] == a2.permute(['a', 'b', 'c', 'd', 'e']))

    def testEqual(self):
        assert(a1 == a1)


class ExPermTest(unittest.TestCase):

    def testInit(self):
        assert(ExPermute(5, [(2, 3, 4)], [0, 1, 2, 3, 4], flag=True) == b2)
        assert(ExPermute(5, [(1, 2)], ['a', 'b', 'c', 'd', 'e'], flag=True) == b4)

    def testGetItem(self):
        assert(2 == b1[1])
        assert(0 == b3[1])
        assert('a' == b4['b'])

    def testMul(self):
        assert(ExPermute(5, [(1, 2, 3), (2, 3, 4), (0, 1)], 0) == b2 * b3)

    def testDiv(self):
        assert(ExPermute(5, [(1, 2, 3), (0, 1), (2, 4, 3)], 0) == b2 / b3)

    def testPow(self):
        assert(ExPermute(5, [(1, 3, 2)], 0) == b2 ** 2)

    def testSetKey(self):
        b5.setKey(['a', 'b', 'c', 'd', 'e'])
        assert(b4 == b5)

    def testGetValue(self):
        assert([(2, 3, 4), (0, 1)] == b3.getValue())

    def testInverse(self):
        assert(ExPermute(5, [(1, 3, 2)], 0) == b2.inverse())

    def testOrder(self):
        assert(4 == b1.order())

    def testToNormal(self):
        assert(Permute([2, 3, 4, 1]) == b1.ToNormal())

    def testSimplify(self):
        assert(ExPermute(4, [(1, 2, 3, 4)]) == b1.simplify())

    def testPermute(self):
        assert(['a', 'd', 'b', 'c', 'e'] == b2.permute(['a', 'b', 'c', 'd', 'e']))

    def testEqual(self):
        assert(b1 == b1)

class PermGroupTest(unittest.TestCase):
    def testCreateElement(self):
        assert(a4 == c.createElement(['b', 'c', 'a', 'd', 'e']))
        assert(b4 == c.createElement([('a', 'b')]))

    def testIdentity(self):
        assert(Permute(['a', 'b', 'c', 'd', 'e'], 1) == c.identity())

    def testIdentity_c(self):
        assert(ExPermute(5, [], ['a', 'b', 'c', 'd', 'e']) == c.identity_c())

    def testGroupOrder(self):
        assert(120 == c.grouporder())

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
