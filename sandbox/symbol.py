"""
define short symbols (for user friendly initialization)
usage: python -i symbol.py
"""
nzmath_version = '0.90.0'
nzmath_year = '2008'

############## for startup file
import os
startupfile = os.environ.get('PYTHONSTARTUP')
if startupfile and os.path.isfile(startupfile):
    execfile(startupfile)

del os
del startupfile

############## print copyright
print "  N  Z  M  A  T  H"
print "Version " + nzmath_version
print "Python based number theory oriented calculation system"
print "Developed at Tokyo Metropolitan University"
print ""
print "Copyright (c) 2003-" + nzmath_year + ", NZMATH development group"
print "All rights reserved."
print "Please read LICENSE.txt for detail."
print ""
print ""
print "NZMATH is provided as a Python library package named 'nzmath'"
print "(Use just as a usual package)"
print ""

del nzmath_year, nzmath_version

############## import nzmath module
import nzmath
from nzmath import *
# import nzmath.compatibility

############## define constant symbol
Q = nzmath.rational.RationalField()
Z = nzmath.rational.IntegerRing()
R = nzmath.real.RealField()
pi = nzmath.real.pi
e = nzmath.real.e
C = nzmath.imaginary.ComplexField()

# X = nzmath.poly.uniutil({0:1},Q)
#Q[X] = nzmath.rational.rationalFunctionField()

############## define method symbol
GF = lambda p: nzmath.finitefield.FinitePrimeField(p)

M = lambda n, R: nzmath.matrix.MatrixRing(n, R)

frac = lambda a, b: nzmath.rational.Rational(a, b)


factorize = lambda n: nzmath.factor.methods.factor(n)
isprime = lambda n: nzmath.prime.primeq(n)
nextP = lambda n: nzmath.prime.nextPrime(n)
randP = lambda n: nzmath.prime.randPrime(n)
