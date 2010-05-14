import unittest
import logging

import testAlgfield
import testArith1
import testArygcd
import testBigrandom
import testBigrange
import testCombinatorial
import testCompatibility
import testCubic_root
import testElliptic
import testEquation
import testGcd
import testGroup
import testImaginary
import testIntresidue
#import testIntegerResidueClass deprecated
import testLattice
import testMatrix
import testMultiplicative
import testPermute
#import testPolynomial deprecated
import testPrime
import testQuad
import testRational
#import testRationalFunction deprecated
import testReal
import testRing
import testRound2
import testSquarefree
import testVector
#import testZassenhaus deprecated
# nzmath.factor
import testFactorUtil
import testFactorMpqs
import testFactorEcm
import testFactorMethods
import testFactorMisc
import testFiniteField
# nzmath.poly
import testFormalsum
import testTermOrder
import testUnivar
import testUniutil
import testMultivar
import testMultiutil
import testPolyFactor
import testPolyRing
import testRatfunc

def suite():
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.startswith("test"):
            suite.addTest(all_names[name].suite())
    return suite

if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
