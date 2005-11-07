
import unittest
import nzmath.arith1 as arith1

class Arith1Test (unittest.TestCase):
    def testLegendre(self):
        assert arith1.legendre(4,13) == 1
        assert arith1.legendre(396685310,2**31-1) == 1
        assert arith1.legendre(2,11**1293) == -1
        assert arith1.legendre(1,3) == 1
        assert arith1.legendre(13*(2**107-1),2**107-1) == 0

    def testModsqrt(self):
        assert arith1.modsqrt(2,17) in (6, 11)
        assert arith1.modsqrt(124413,2**17-1) in (3988, 127073)
        assert arith1.modsqrt(1,2**13-1) == 1 

    def testExpand(self):
        assert arith1.expand(10**6,2) == [0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1,1,1]
        assert arith1.expand(10**6,7) == [1,1,3,3,3,3,1,1]

    def testInverse(self):
        assert arith1.inverse(160,841) == 205
        assert arith1.inverse(1,2**19-1) == 1
        self.assertRaises(ZeroDivisionError, arith1.inverse, 0, 3)

    def testFloorsqrt(self):
        self.assertEqual(0, arith1.floorsqrt(0))
        self.assertEqual(1, arith1.floorsqrt(1))
        self.assertEqual(1, arith1.floorsqrt(3))
        self.assertEqual(2, arith1.floorsqrt(4))
        self.assertEqual(3, arith1.floorsqrt(10))
        self.assertEqual(arith1.floorsqrt(400000000000000000000), 20000000000)
        self.assertEqual(arith1.floorsqrt(400000000000000000000 - 1), 19999999999)
        self.assert_(arith1.floorsqrt(2**60 - 1) ** 2 <= 2**60 - 1)
        self.assert_(arith1.floorsqrt(2**59 - 1) ** 2 <= 2**59 - 1)

    def testFloorpowerroot(self):
        assert arith1.floorpowerroot(0,1) == 0
        assert arith1.floorpowerroot(0,4) == 0
        assert arith1.floorpowerroot(0,7) == 0
        assert arith1.floorpowerroot(1,2) == 1
        assert arith1.floorpowerroot(1,6) == 1
        assert arith1.floorpowerroot(1,9) == 1
        assert arith1.floorpowerroot(2,3) == 1
        assert arith1.floorpowerroot(2,7) == 1
        assert arith1.floorpowerroot(8,3) == 2
        assert arith1.floorpowerroot(128,7) == 2
        for j in range(3,100,10):
            k = 5**j
            assert arith1.floorpowerroot(k - 1, j) == 4
            assert arith1.floorpowerroot(k, j) == 5
            assert arith1.floorpowerroot(k + 1, j) == 5
        assert arith1.floorpowerroot(400000000000000000000, 4) == arith1.floorsqrt(20000000000)

    def testVp(self):
        assert (3, 1) == arith1.vp(8, 2)
        assert (0, 10) == arith1.vp(10, 3)
        assert (1, 10) == arith1.vp(10, 3, 1)
        assert (3, 10) == arith1.vp(270, 3)

    def testLog(self):
        self.assertEqual(3, arith1.log(8, 2))
        self.assertEqual(3, arith1.log(15, 2))
        self.assertEqual(3, arith1.log(1000, 10))
        self.assertEqual(9, arith1.log(1000000001, 10))
        self.assert_(10 ** arith1.log(1000000001, 10) <= 1000000001)


def suite():
    suite = unittest.makeSuite(Arith1Test, "test")
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
