import unittest
import euler

class EulerTest (unittest.TestCase):
    def runTest(self):
        assert euler.euler(101) == 100
        assert euler.euler(480) == 128
        assert euler.euler(43**5*87**2) ==(43**4)*42*6*29*28 
        assert euler.euler(1042387*701) == 701*700*1486 
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(EulerTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
