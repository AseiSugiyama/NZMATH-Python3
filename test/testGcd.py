import unittest
import doctest
import nzmath.gcd as gcd

class GcdTest (unittest.TestCase):
    def testGcd(self):
        self.assertEqual(1, gcd.gcd(1, 2))
        self.assertEqual(2, gcd.gcd(2, 4))
        self.assertEqual(10, gcd.gcd(0, 10))
        self.assertEqual(10, gcd.gcd(10, 0))
        self.assertEqual(1, gcd.gcd(13, 21))

    def testBinaryGcd(self):
        self.assertEqual(1, gcd.binarygcd(1, 2))
        self.assertEqual(2, gcd.binarygcd(2, 4))
        self.assertEqual(10, gcd.binarygcd(0, 10))
        self.assertEqual(10, gcd.binarygcd(10, 0))
        self.assertEqual(1, gcd.binarygcd(13, 21))

    def testLcm(self):
        self.assertEqual(2, gcd.lcm(1, 2))
        self.assertEqual(4, gcd.lcm(2, 4))
        self.assertEqual(0, gcd.lcm(0, 10))
        self.assertEqual(0, gcd.lcm(10, 0))
        self.assertEqual(273, gcd.lcm(13, 21))

    def testExtgcd(self):
        self.assertEqual((-4,3,1), gcd.extgcd(8, 11))
        extgcd = gcd.extgcd(8, 11)
        self.assert_(8 * extgcd[0] + 11 * extgcd[1] == extgcd[2])
        import nzmath.rational as rational
        self.assertEqual((-4,3,1), gcd.extgcd(rational.Integer(8), 11))

    def testGcdOfList(self):
        self.assertEqual([8, [1]], gcd.gcd_of_list([8]))
        self.assertEqual([1, [-4, 3]], gcd.gcd_of_list([8, 11]))
        self.assertEqual([1, [-4, 3, 0, 0, 0, 0, 0]], gcd.gcd_of_list([8, 11, 10, 9 ,6, 5, 4]))

def suite():
    suite = unittest.makeSuite(GcdTest, "test")
    suite.addTest(doctest.DocTestSuite(gcd))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
