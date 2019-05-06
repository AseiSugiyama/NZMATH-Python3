import unittest
import nzmath.arith1 as arith1


class Arith1Test (unittest.TestCase):
    def testLegendre(self):
        self.assertEqual(1, arith1.legendre(4, 13))
        self.assertEqual(1, arith1.legendre(396685310, 2**31-1))
        self.assertEqual(-1, arith1.legendre(2, 11**1293))
        self.assertEqual(1, arith1.legendre(1, 3))
        self.assertEqual(0, arith1.legendre(13*(2**107-1), 2**107-1))

    def testModsqrt(self):
        self.assertTrue(arith1.modsqrt(2, 17) in (6, 11))
        self.assertTrue(arith1.modsqrt(124413, 2**17-1) in (3998, 127073))
        self.assertEqual(1, arith1.modsqrt(1, 2**13-1))
        self.assertTrue(arith1.modsqrt(2, 7, 2) in (10, 39))
        self.assertTrue(arith1.modsqrt(12, 97, 3) in (448799, 463874))

    def testExpand(self):
        self.assertEqual([0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1,1,1],
                         arith1.expand(10**6, 2))
        self.assertEqual([1,1,3,3,3,3,1,1], arith1.expand(10**6, 7))

    def testInverse(self):
        self.assertEqual(205, arith1.inverse(160, 841))
        self.assertEqual(1, arith1.inverse(1, 2**19-1))
        self.assertRaises(ZeroDivisionError, arith1.inverse, 0, 3)

    def testFloorsqrt(self):
        self.assertEqual(0, arith1.floorsqrt(0))
        self.assertEqual(1, arith1.floorsqrt(1))
        self.assertEqual(1, arith1.floorsqrt(3))
        self.assertEqual(2, arith1.floorsqrt(4))
        self.assertEqual(3, arith1.floorsqrt(10))
        self.assertEqual(arith1.floorsqrt(400000000000000000000), 20000000000)
        self.assertEqual(arith1.floorsqrt(400000000000000000000 - 1), 19999999999)
        self.assertTrue(arith1.floorsqrt(2**60 - 1) ** 2 <= 2**60 - 1)
        self.assertTrue(arith1.floorsqrt(2**59 - 1) ** 2 <= 2**59 - 1)

    def testFloorpowerroot(self):
        self.assertEqual(0, arith1.floorpowerroot(0, 1))
        self.assertEqual(0, arith1.floorpowerroot(0, 4))
        self.assertEqual(0, arith1.floorpowerroot(0, 7))
        self.assertEqual(1, arith1.floorpowerroot(1, 2))
        self.assertEqual(1, arith1.floorpowerroot(1, 6))
        self.assertEqual(1, arith1.floorpowerroot(1, 9))
        self.assertEqual(1, arith1.floorpowerroot(2, 3))
        self.assertEqual(1, arith1.floorpowerroot(2, 7))
        self.assertEqual(2, arith1.floorpowerroot(8, 3))
        self.assertEqual(2, arith1.floorpowerroot(128, 7))
        self.assertEqual((5, 5), arith1.floorpowerroot(5, 1, True))
        self.assertEqual((5, 25), arith1.floorpowerroot(27, 2, True))
        self.assertEqual((0, 0), arith1.floorpowerroot(0, 7, True))
        self.assertEqual((3, 243), arith1.floorpowerroot(245, 5, True))
        self.assertEqual((-3, -243), arith1.floorpowerroot(-245, 5, True))
        for j in range(3,100,10):
            k = 5**j
            self.assertEqual(4, arith1.floorpowerroot(k - 1, j))
            self.assertEqual(5, arith1.floorpowerroot(k, j))
            self.assertEqual(5, arith1.floorpowerroot(k + 1, j))
        self.assertEqual(arith1.floorpowerroot(400000000000000000000, 4),
                         arith1.floorsqrt(20000000000))

    def testVp(self):
        self.assertEqual((3, 1), arith1.vp(8, 2))
        self.assertEqual((0, 10), arith1.vp(10, 3))
        self.assertEqual((1, 10), arith1.vp(10, 3, 1))
        self.assertEqual((3, 10), arith1.vp(270, 3))

    def testLog(self):
        self.assertEqual(3, arith1.log(8, 2))
        self.assertEqual(3, arith1.log(15, 2))
        self.assertEqual(3, arith1.log(1000, 10))
        self.assertEqual(9, arith1.log(1000000001, 10))
        self.assertTrue(10 ** arith1.log(1000000001, 10) <= 1000000001)

    def testIssquare(self):
        self.assertTrue(arith1.issquare(1))
        self.assertEqual(1, arith1.issquare(1))
        self.assertTrue(arith1.issquare(289))
        self.assertEqual(17, arith1.issquare(289))
        self.assertFalse(arith1.issquare(2))
        self.assertEqual(0, arith1.issquare(2))
        self.assertFalse(arith1.issquare(0))
        self.assertEqual(0, arith1.issquare(0))

    def testAGM(self):
        self.assertAlmostEqual(1.4567910310469068692, arith1.AGM(1, 2))
        self.assertAlmostEqual(1.8636167832448965424, arith1.AGM(1, 3))

    def testProduct(self):
        self.assertEqual(1, arith1.product([]))
        self.assertEqual(120, arith1.product(range(1, 6)))
        self.assertEqual(14400, arith1.product(i**2 for i in range(1, 6)))
    
    def testPowerDetection(self):
        self.assertEqual((1, 1), arith1.powerDetection(1))
        self.assertEqual((2, 1), arith1.powerDetection(2))
        self.assertEqual((3, 1), arith1.powerDetection(3))
        self.assertEqual((2, 2), arith1.powerDetection(4))
        self.assertEqual((3, 2), arith1.powerDetection(9))
        self.assertEqual((4, 2), arith1.powerDetection(16))
        self.assertEqual((2, 4), arith1.powerDetection(16, True))
        self.assertEqual((97, 1), arith1.powerDetection(97))
        self.assertEqual((16, 2), arith1.powerDetection(256))
        self.assertEqual((2, 8), arith1.powerDetection(256, True))


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
