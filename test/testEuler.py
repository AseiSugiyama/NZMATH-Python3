import unittest
import euler

class EulerTest (unittest.TestCase):
    def runTest(self):
        assert euler.euler(101) == 100
        assert euler.euler(480) == 128
        assert euler.euler(3**2 * 29**3 * 43**5) == 2*3 * 28*29**2 * 42*43**4 
        assert euler.euler(701**2 * 1487) == 700*701 * 1486
        assert euler.moebius(1) == 1
        assert euler.moebius(2*3*5*7*11*13) == 1
        assert euler.moebius(8*987654345) == 0
        assert euler.moebius(999991) == -1

def suite():
    suite = unittest.TestSuite()
    suite.addTest(EulerTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
