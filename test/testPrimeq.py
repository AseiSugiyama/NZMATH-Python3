import unittest
import primeq

class PrimeqTest(unittest.TestCase):
    def testComposite(self):
        assert primeq.primeQ(1) == 0
        assert primeq.primeQ(2 ** 2) == 0
        assert primeq.primeQ(2 * 7) == 0
        assert primeq.primeQ(3 * 5) == 0
        assert primeq.primeQ(11 * 31) == 0
        assert primeq.primeQ(1111111111111111111 * 11111111111111111111111) == 0

    def testPrime(self):
        assert primeq.primeQ(2)
        assert primeq.primeQ(3)
        assert primeq.primeQ(9127065170209166627512577049835050786319879175417462565489372634726057) == 1
        assert primeq.primeQ(4891379345109868851790779024240568865616378588791632639038053751715559) == 1
        assert primeq.primeQ(2363858618621131491522909922855848947505660583231660184604997989181799) == 1
        assert primeq.primeQ(4863823651998692364632113443650710053965475364018056831834088668072143) == 1
        assert primeq.primeQ(8520974761250017240680501273660048802742313617854066886979477558755123) == 1
        assert primeq.primeQ(5333328454311749563135260012013022290652354664978333312255798095476751) == 1
        assert primeq.primeQ(6979118229619441705140745622685486689402511156029709500112279644097451) == 1
        assert primeq.primeQ(6940050835173448128559468350422822677962492227281659500452999249203611) == 1
        assert primeq.primeQ(9096999911112296151294175170592524902405362373930931784293209773275589) == 1
        assert primeq.primeQ(2408251454834202887967294940107459015531157887991446227268133398163643) == 1

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PrimeqTest("testComposite"))
    suite.addTest(PrimeqTest("testPrime"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
     

 
   
 
