from sandbox.poly.array_poly import *
from nzmath import *
import math

def aks( n ):
    """
    AKS ( Cyclotomic Conguence Test ) primality test for a nutural number.
    
    Input: a natural number n ( n > 1 ).
    Output: n is prime => Print " n is prime " and return True
            n is not prime => Print " n is not prime " and return False.
    """

    def aks_mod( polynomial , r ):
        """
        This function is used in aks.
        polynomial modulo ( x^r - 1 )
        """
        aks_mod = polynomial.coefficients
        total = aks_mod[ : r ]
        aks_mod = aks_mod[ r : ]
        while len(aks_mod) - 1 >= r :
            for i in range(r):
                total[i] += aks_mod[i]
            aks_mod = aks_mod[ r : ]
        for i in range(len(aks_mod)):
            total[i] += aks_mod[i]
        return array_poly_mod( total , polynomial.mod )

    lg = math.log( n , 2 )
    k = int( lg * lg )

    if arith1.powerDetection( n )[ 1 ] != 1: #Power Detection
        print " n is not prime "
        return False

    start = 3
    while 1:
        d = arith1.gcd.gcd( start , n )
        if 1 < d < n:
            print "n is not prime"
            return False
        x = n % start
        N = x
        for i in range( 1 , k + 1 ):
            if N == 1:
                break
            N = ( N * x ) % start
        if i == k:
            r = start
            break
        start += 1
    d = arith1.gcd.gcd( r , n )
    if 1 < d < n:
        print " n is not prime "
        return False
    if n <= r:
        print " n is prime "
        return True

    e = multiplicative.euler( r ) #Cyclotomic Conguence
    e = math.sqrt( e )
    e = int( e * lg )
    for b in range( 1 , e+1 ):
        f = array_poly_mod( [ b , 1 ] , n )
        total = array_poly_mod( [ 1 ] , n )
        count = n
        while count > 0:
            if count & 1:
                total = total * f
                total = aks_mod( total , r )
            f = f.power()
            f = aks_mod( f , r )
            count = count >> 1
        total_poly = total.coefficients_to_dict()
        if total_poly != { 0 : b , n % r : 1 }:
            print  " n is not prime "
            return False
    print " n is prime "
    return True


def testAks( self ):
    self.assertEqual( True , prime.aks( 521 ))
    self.assertEqual( False , prime.aks( 525 ))
