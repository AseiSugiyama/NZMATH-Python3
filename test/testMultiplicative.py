import unittest
import multiplicative

class MultiplicativeTest (unittest.TestCase):
    def testEuler(self):
        assert multiplicative.euler(101) == 100
        assert multiplicative.euler(480) == 128
        assert multiplicative.euler(3**2 * 29**3 * 43**5) == 2*3 * 28*29**2 * 42*43**4 
        assert multiplicative.euler(701**2 * 1487) == 700*701 * 1486

    def testMoebius(self):
        assert multiplicative.moebius(1) == 1
        assert multiplicative.moebius(2*3*5*7*11*13) == 1
        assert multiplicative.moebius(8*987654345) == 0
        assert multiplicative.moebius(999991) == -1
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MultiplicativeTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
