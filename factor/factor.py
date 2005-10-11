import math
import nzmath.arith1 as arith1
import nzmath.bigrandom as bigrandom
import nzmath.gcd as gcd
import nzmath.prime as prime
import trialdivision

# Pollard's rho method
class FactoringIntegerForRhoMethod:
    """
    An instance of the class has three attributes:
      number -- the factoring integer,
      factors -- list of tuples (composite,valuation) and
      primefactors -- list of tuples (prime, valuation).

    The target integer n, which is given as the argument of
    constructor and the attributes keep satisfying:
      n = number * product(factors) * product(primefactors)
    where product() multiplies all tuples (d, e) as d**e.
    """
    def __init__(self, number):
        self.number = number
        self.factors = []
        self.primefactors = []

    def register(self, divisor, isprime=False):
        """
        Register a divisor of the number, if the divisor is a true
        divisor of the number.  The number is divided by the divisor
        as many times as possible.

        If 'isprime' argument is True, then 'divisor' is registered
        into primedivisors list, otherwise into factors list.
        """
        valuation = 0
        while not (self.number % divisor):
            self.number //= divisor
            valuation += 1
        if valuation:
            if isprime:
                self.primefactors.append((divisor, valuation))
            else:
                self.factors.append((divisor, valuation))

    def getPrimeFactors(self):
        """
        Return all prime factors.
        Composite factors are factored by trial division.
        """
        if self.factors:
            for (composite, exponent) in self.factors:
                factorization = trialdivision.trialDivision(composite)
                for (divisor, valuation) in factorization:
                    self.primefactors.append((divisor, valuation * exponent))
        return self.sortPrimefactors()

    def sortPrimefactors(self):
        """
        Sort primefactors list and return it.
        """
        if len(self.primefactors) != 1:
            temp = []
            while self.primefactors:
                p0, e0 = self.primefactors.pop()
                waste = []
                for p, e in self.primefactors:
                    if p == p0:
                        e0 += e
                        waste.apend((p,e))
                for dust in waste:
                    self.primefactors.remove(dust)
                temp.append((p0,e0))
            self.primefactors = temp
            self.primefactors.sort()
        return self.primefactors

def subrhomethod(n):
    """

    This function is to find a non-trivial factor of n using
    algorithm of C.Pomerance's book.

    """
    if n <= 3:
        return n
    g = n
    while g == n:
        a = bigrandom.randrange(1, n-3)
        s = bigrandom.randrange(0, n-1)
        u = s
        v = s
        g = gcd.gcd((v**2+v+a)%n-u, n)
        while g == 1:
            u = (u**2+a)%n
            v = (v**2+a)%n
            v = (v**2+a)%n
            g = gcd.gcd(v-u, n)
    return g

def rhomethod(n):
    """

    This function returns factorization of arbitrary natural numbers.

    """
    target = FactoringIntegerForRhoMethod(n)
    if not (n % 2):
        target.register(2, isprime = True)
    while target.number != 1 and prime.primeq(target.number) == 0:
        g = subrhomethod(target.number)
        target.register(g, isprime = prime.primeq(g))
    if target.number != 1:
        target.register(target.number, isprime = True)
    return target.getPrimeFactors()

# p-1 method
def pmom(nn):
    f = []
    factors = []
    ii = nn
    while ii > 1 and not prime.primeq(ii):
        ff = subpmom(ii)
        if ff != -1 :
            f.append(ff)
            ii = ii//ff
        else:
            f.append(ii)
            break
    else :
        if ii != 1:
            f.append(ii)
    f.sort()
    kk = 0
    while kk < len(f) :
        fact = f[kk]
        Numfact = f.count(fact)
        factors.append((fact,Numfact))
        kk = kk + Numfact
    return factors

def subpmom(N):
    """

    This program tries to find a non-trivial factor of N using
    Algorithm 8.8.2 (p-1 first stage) of Cohen's book. In case of N =
    pow(2,i), this program will not terminate.

    """

    # initialize
    x , B = 2 , 10000001
    y = x
    primes = []

    for q in prime.generator():
        primes.append(q)
        if q > B:
            if gcd.gcd(x-1,N) != 1:
                x = y
                break
            else:
                return -1
        else:
            q1 = q
            l = B//q
            while q1 <= l:
                q1 *= q
            x = pow(x,q1,N)
            if len(primes) >= 20:
                if gcd.gcd(x-1,N) == 1:
                    primes, y = [], x
                else:
                    x = y
                    break

    for q in primes:
        q1 = q
        while q1 <= B:
            x = pow(x,q,N)
            g = gcd.gcd(x-1,N)
            if g != 1:
                if g == N:
                    return -1
                return g
            q1 *= q

# misc functions
def PrimePowerTest(n):
    """
    This program using Algo. 1.7.5 in Cohen's book judges whether
    n is of the form p**k with prime p or not.
    If it is True, then (p,k) will be returned,
    otherwise (n,0).
    """
    if n % 2 == 1:
        q = n
        while True:
            if not prime.primeq(q):
                a = 2
                while prime.spsp(n, a):
                    a += 1
                d = gcd.gcd(pow(a,q,q) - a, q)
                if d == 1 or d == q:
                    return (n, 0)
                else:
                    q = d
            else:
                p = q
                break
    else:
        p = 2

    k, q = arith1.vp(n, p)
    if q == 1:
        return (p, k)
    else:
        return (n, 0)

def AllDivisors(n):
    """
    this returns all factors divide n
    """
    divisors = [1]
    for p, e in rhomethod(n):
        p_part = [p**j for j in range(1, e+1)]
        divisors += [n*q for n in divisors for q in p_part]
    divisors.sort()
    return divisors

def primeDivisors(n):
    """

    primeDivisors(n) returns the list of primes that divides n.

    """
    result = []
    for d,e in rhomethod(n):
        result.append(d)
    return result

def squarePart(n):
    """

    squarePart(n) returns the largest integer whose
    square divides n.

    """
    factors = rhomethod(n)
    result = 1
    for d, e in factors:
        if e >= 2:
            result *= d ** (e//2)
    return result
