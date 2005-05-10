import unittest
import testArith1
import testBigrandom
import testCombinatorial
import testElliptic
import testEquation
import testFactor
import testFiniteField
import testGcd
import testImaginary
import testIntegerResidueClass
import testLattice
import testMatrix
import testPolynomial
import testPrime
import testRational
import testRationalFunction
import testReal
import testRing
import testVector
import testMultiplicative

def suite():
    suite = unittest.TestSuite()
    suite.addTest(testArith1.suite())
    suite.addTest(testBigrandom.suite())
    suite.addTest(testCombinatorial.suite())
    suite.addTest(testElliptic.suite())
    suite.addTest(testEquation.suite())
    suite.addTest(testFactor.suite())
    suite.addTest(testFiniteField.suite())
    suite.addTest(testGcd.suite())
    suite.addTest(testImaginary.suite())
    suite.addTest(testIntegerResidueClass.suite())
    suite.addTest(testLattice.suite())
    suite.addTest(testMultiplicative.suite())
    suite.addTest(testMatrix.suite())
    suite.addTest(testPolynomial.suite())
    suite.addTest(testPrime.suite())
    suite.addTest(testRational.suite())
    suite.addTest(testRationalFunction.suite())
    suite.addTest(testReal.suite())
    suite.addTest(testRing.suite())
    suite.addTest(testVector.suite())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
