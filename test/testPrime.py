import unittest
import prime

class PrimeTest(unittest.TestCase):
    def testComposite(self):
        assert not prime.primeq(1)
        assert not prime.primeq(2 ** 2)
        assert not prime.primeq(2 * 7)
        assert not prime.primeq(3 * 5)
        assert not prime.primeq(11 * 31)
        assert not prime.primeq(1111111111111111111 * 11111111111111111111111)

    def testPrime(self):
        assert prime.primeq(2)
        assert prime.primeq(3)
        assert prime.primeq(1111111111111111111)
        assert prime.primeq(9127065170209166627512577049835050786319879175417462565489372634726057)

    def testBigprimeq(self):
        assert prime.bigprimeq(1111111111111111111)
        assert prime.bigprimeq(9127065170209166627512577049835050786319879175417462565489372634726057)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PrimeTest("testComposite"))
    suite.addTest(PrimeTest("testPrime"))
    suite.addTest(PrimeTest("testBigprimeq"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
     

 
   
 
