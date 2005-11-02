import unittest
import doctest
import nzmath.gcd as gcd

class GcdTest (unittest.TestCase):
    def testGcd(self):
        assert gcd.gcd(1, 2) == 1
        assert gcd.gcd(2, 4) == 2
        assert gcd.gcd(0, 10) == 10
        assert gcd.gcd(10, 0) == 10
        assert gcd.gcd(13, 21) == 1

    def testBinaryGcd(self):
        assert gcd.binarygcd(1, 2) == 1
        assert gcd.binarygcd(2, 4) == 2
        assert gcd.binarygcd(0, 10) == 10
        assert gcd.binarygcd(10, 0) == 10
        assert gcd.binarygcd(13, 21) == 1

    def testLcm(self):
        assert gcd.lcm(1, 2) == 2
        assert gcd.lcm(2, 4) == 4
        assert gcd.lcm(0, 10) == 0
        assert gcd.lcm(10, 0) == 0
        assert gcd.lcm(13, 21) == 273

    def testExtgcd(self):
        assert (-4,3,1) == gcd.extgcd(8, 11)
        extgcd = gcd.extgcd(8, 11)
        assert 8 * extgcd[0] + 11 * extgcd[1] == extgcd[2]
        import nzmath.rational as rational
        assert (-4,3,1) == gcd.extgcd(rational.Integer(8), 11)

    def testGcdOfList(self):
        assert [1, [-4, 3]] == gcd.gcd_of_list([8, 11])

def suite():
    suite = unittest.makeSuite(GcdTest, "test")
    suite.addTest(doctest.DocTestSuite(gcd))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
