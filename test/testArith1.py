
import unittest
import arith1

class Arith1Test (unittest.TestCase):
    def testLgendre(self):
        assert arith1.legendre(4,13) == 1
        assert arith1.legendre(396685310,2**31-1) == 1
        assert arith1.legendre(2,11**1293) == -1
        assert arith1.legendre(1,3) == 1
        assert arith1.legendre(13*(2**107-1),2**107-1) == 0

    def testSqroot(self):
        assert arith1.sqroot(2,17) == 6 or 11
        assert arith1.sqroot(124413,2**17-1) == 3988 or 127083
        assert arith1.sqroot(1,2**13-1) == 1 
        
    def testExpand(self):
        assert arith1.expand(10**6,2) == [0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1,1,1]
        assert arith1.expand(10**6,7) == [1,1,3,3,3,3,1,1]

    def testInverse(self):
        assert arith1.inverse(160,841) == 205
        assert arith1.inverse(1,2**19-1) == 1

    def testEuler(self):
        assert arith1.euler(101) == 100
        assert arith1.euler(480) == 128
        assert arith1.euler(3**2 * 29**3 * 43**5) == 2*3 * 28*29**2 * 42*43**4 
        assert arith1.euler(701**2 * 1487) == 700*701 * 1486

    def testMoebius(self):
        assert arith1.moebius(1) == 1
        assert arith1.moebius(2*3*5*7*11*13) == 1
        assert arith1.moebius(8*987654345) == 0
        assert arith1.moebius(999991) == -1
        
def suite():
    suite = unittest.makeSuite(Arith1Test, "test")
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
