import unittest
import euler

class EulerTest (unittest.TestCase):
    def runTest(self):
        assert euler.euler(101) == 100
        assert euler.euler(480) == 128
        assert euler.euler(43**5*87**2) ==(43**4)*42*6*29*28 
        assert euler.euler(1042387*701) == 701*700*1486 
        assert euler.mebius(1) == 1
        assert euler.mebius(2*3*5*7*11*13) == 1
        assert euler.mebius(8*987654345) == 0 
        assert euler.mebius(999991) == -1        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(EulerTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
