import unittest
import gcd

class GcdTest (unittest.TestCase):
    def runTest(self):
        assert gcd.gcd(1, 2) == 1
        assert gcd.gcd(2, 4) == 2
        assert gcd.gcd(0, 10) == 10
        assert gcd.gcd(10, 0) == 10
        assert gcd.gcd(13, 21) == 1

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GcdTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
