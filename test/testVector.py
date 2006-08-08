import unittest
import nzmath.vector as vector

class VectorTest(unittest.TestCase):

    def testAdd(self):
        v1 = vector.Vector([1,2,3])
        v2 = vector.Vector([0,-2,2])
        assert v1+v2 == vector.Vector([1,0,5])

    def testGetItem(self):
        v1 = vector.Vector([1,2,3])
        assert v1[1] == 1

    def testSetItem(self):
        v1 = vector.Vector([1,2,3])
        v1[3] = 99
        assert v1[3] == 99

    def testLen(self):
        v1 = vector.Vector([1,2,3])
        assert len(v1) == 3

    def testMul(self):
        v1 = vector.Vector([1,2,3])
        import nzmath.matrix as matrix
        m1 = matrix.createMatrix(2,3,[1,0,1,0,1,0])
        assert m1*v1 == vector.Vector([4,2])

    def testRMul(self):
        v1 = vector.Vector([1,2,3])
        import nzmath.matrix as matrix
        m1 = matrix.createMatrix(3,2,[1,1,0,1,0,1])
        assert v1*m1 == vector.Vector([1,6])

    def testIndexOfNoneZero(self):
        v = vector.Vector([0,2,0])
##         print v.indexOfNoneZero()
        assert v.indexOfNoneZero() == 2

def suite():
    suite = unittest.makeSuite(VectorTest, 'test')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
