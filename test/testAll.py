import unittest
import testBigrandom
import testEuler
import testFactor
import testGcd
import testImaginary
import testIntegerResidueClass
import testMatrix
import testPolynomial
import testPrime
import testRational
import testRationalFunction
import testReal
import testVector

def suite():
    suite = unittest.TestSuite()
    suite.addTest(testBigrandom.suite())
    suite.addTest(testEuler.suite())
    suite.addTest(testFactor.suite())
    suite.addTest(testGcd.suite())
    suite.addTest(testImaginary.suite())
    suite.addTest(testIntegerResidueClass.suite())
    suite.addTest(testMatrix.suite())
    suite.addTest(testPolynomial.suite())
    suite.addTest(testPrime.suite())
    suite.addTest(testRational.suite())
    suite.addTest(testRationalFunction.suite())
    suite.addTest(testReal.suite())
    suite.addTest(testVector.suite())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
