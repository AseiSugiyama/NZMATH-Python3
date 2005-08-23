import math
import nzmath.arith1 as arith1
import nzmath.bigrandom as bigrandom
import nzmath.gcd as gcd
import nzmath.prime as prime
import trialdivision

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

    This function returns factorization of arbitrary natural numbers 

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

def ord(p, n):
    """

    ord(p, n) returns the power of the prime p which divides the non-zero integer n.

    """ 
    result = 0
    while n % p == 0:
        n /= p
        result += 1
    return result

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
        kk = kk+ Numfact
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

## 
## defs for MPQS
##
class FactorFound:
    def __init__(self,factors):
        self.value=factors

class F2MatrixWithTwoVectors:
    def __init__(self):
        self.rows=[]
        self.cols=[]
        self.u=[]
        self.v=[]
    def extendrow(self,vector,u0,v0):
        rownum=self.rowsize()
        self.rows.append(vector)
        for pi in vector:
            while pi>=len(self.cols):
                self.cols.append([])
            self.cols[pi].append(rownum)
        self.u.append(u0)
        self.v.append(v0)
    def compact(self):
        isdeleted=1 # pass first test
        while isdeleted:
            isdeleted=0
            for j in self.cols:
                if j and len(j)==1:
                    k=j[0]
                    for i in self.rows[k]:
                        if k in self.cols[i]:
                            self.cols[i].remove(k)
                    self.rows[k]=[]
                    self.u[k]=self.v[k]=0
                    isdeleted=1
                elif j and len(j)==2:
                    k0,k1 = j[0],j[1]
                    for i in self.rows[k1]:
                        if i in self.rows[k0]:
                            self.cols[i].remove(k0)
                            self.cols[i].remove(k1)
                            self.rows[k0].remove(i)
                        elif self.cols[i]:
                            self.cols[i][self.cols[i].index(k1)]=k0
                            self.rows[k0].append(i)
                    self.rows[k1]=[]
                    self.u[k0],self.u[k1]=self.u[k0]*self.u[k1],0
                    self.v[k0],self.v[k1]=self.v[k0]*self.v[k1],0
                    isdeleted=1
        while self.cols.count([]):
            j=self.cols.index([])
            for i in range(self.rowsize()):
                for k in range(len(self.rows[i])):
                    if self.rows[i][k]>j:
                        self.rows[i][k]=self.rows[i][k]-1
            del self.cols[j]
        while self.rows.count([]):
            i=self.rows.index([])
            for j in range(self.colsize()):
                for k in range(len(self.cols[j])):
                    if self.cols[j][k]>i:
                        self.cols[j][k]=self.cols[j][k]-1
            del self.rows[i],self.u[i],self.v[i]
    def transpose(self):
        self.rows,self.cols=self.cols,self.rows
    def colsize(self):
        return len(self.cols)
    def rowsize(self):
        return len(self.rows)
    def xorrow(self,i,j):
        lc=self.rows[i][:]
        for n in self.rows[j]:
            if n in lc:
                lc.remove(n)
            else:
                lc.append(n)
        lc.sort()
        return lc
    def kernel(self,n):
        c,d={},{}
        for k in range(self.colsize()):
            for j in range(self.rowsize()):
                if c.has_key(j):
                    continue
                if k in self.rows[j]:
                    for i in range(self.rowsize()):
                        if i!=j and k in self.rows[i]:
                            self.rows[i]=self.xorrow(i,j)
                    c[j],d[k]=k,j
                    break
        del c

        for i in range(self.colsize()):
            if d.has_key(i):
                continue
            x=[i]
            for k in d.keys():
                if i in self.rows[d[k]]:
                    x.append(k)
            confirm(x,self.u,self.v,n)

class QuadraticPolynomial:
    def __init__(self,a,b,c):
        assert b%2==0
        self._a, self._b, self._c = a,b,c
        self._d=(b/2)**2-a*c
    def __call__(self, m):
        return (self._a*m-self._b)*m+self._c
    def root_modp(self,p):
        if not self._a%p and self._b%p:
            return (self._c* arith1.inverse(self._b,p))%p
        elif self._a%p:
            y1=mod_sqrt(self._d,p)
            y2 = arith1.inverse(self._a,p)
            x = [((y1+self._b/2)*y2)%p, ((-y1+self._b/2)*y2)%p]
            x.sort()
            return tuple(x)

class MPQS:
    def __init__(self, n):
        self.N=n
    def run(self, sizeofFB=300, halfWidth=65535, C3=10, C4=10):
        """
        extra primes can be C3 times as big as the biggest of factor base.
        C4 is for plenty of linear relations
        """
        try:
            self.make_factor_base(sizeofFB)
            self.bl = math.log(self.factor_base[-1]*C3)
            self.mat = F2MatrixWithTwoVectors()
            a = prime.sqrt(2L*self.N)//halfWidth
            if a&1 == 0:
                a -= 1
            self.wanted = len(self.factor_base)+C4
            while self.wanted>0:
                while not prime.primeq(a) or arith1.legendre(self.N,a)!=1:
                    a += 2
                b = arith1.sqroot(self.N,a)
                c = (b**2-self.N)/a
                self.sieve(a,b+b,c,halfWidth)
                a += 2
            self.eliminate()
        except FactorFound,r:
            return [(p,e) for p,e in r.value.iteritems()]
        else:
            return self.run(sizeofFB,halfWidth, C3, C4*2)
    def make_factor_base(self,size):
        self.factor_base = []
        q = 3
        while len(self.factor_base)<size:
            if prime.primeq(q):
                qr = arith1.legendre(self.N,q)
                if qr == 1:
                    self.factor_base.append(q)
                elif qr == 0: # very rare case
                    raise FactorFound({q:1, self.N//q:1})
            q += 2
        self.factor_base[:0] = [-1,2L]
        self.small_factor = self.factor_base[:size//10]
    def sieve(self,a,b,c,rangeHalfWidth):
        assert b%2 == 0
        rangeMin = (b/2)//a-rangeHalfWidth
        rangeMax = (b/2)//a+rangeHalfWidth
        t = {}
        sieve_prime = self.factor_base[len(self.small_factor):]
        f = QuadraticPolynomial(a,b,c)
        if a in sieve_prime:
            l = math.log(a)
            if b%a:
                x = f.root_modp(a)
                i = rangeMin//a*a+x
                while i<rangeMax:
                    t[i] = l
                    i += a
            sieve_prime.remove(a)
        for p in sieve_prime:
            l = math.log(p)
            x0,x1 = f.root_modp(p)
            d = x1-x0
            i = rangeMin//p*p+x0
            while i<rangeMax:
                t[i] = t.get(i,0)+l
                t[i+d] = t.get(i+d,0)+l
                i += p
        if a not in self.factor_base:
            self.factor_base.append(a)
            self.wanted += 1
        for i in t.keys():
            if math.log(abs(f(i)))-t[i]<=self.bl:
                ui=f(i)
                if ui<0:
                    factors = {-1:1}
                    for p,e in trialdivision.trialDivision(-ui):
                        factors[p] = e
                else:
                    factors = {}
                    for p,e in trialdivision.trialDivision(ui):
                        factors[p] = e
                factors[a] = factors.get(a,0)+1
                ti = []
                for p in factors.keys():
                    if factors[p]&1:
                        try:
                            ti.append(self.factor_base.index(p))
                        except ValueError:
                            self.factor_base.append(p)
                            self.wanted=self.wanted+1
                            ti.append(self.factor_base.index(p))
                ti.sort()
                self.mat.extendrow(ti,a*ui,a*i-b/2)
                self.wanted -= 1
                if self.wanted<=0:
                    return

    def eliminate(self):
        self.mat.compact()
        self.mat.transpose()
        self.mat.kernel(self.N)
        # failed to factor if this line is reached

def confirm(dep,u,v,n):
    r1 = r2 = 1
    for i in dep:
        r1 *= u[i]
        r2 *= v[i]%n
    assert (r1-r2**2)%n == 0
    r1 = arith1.floorsqrt(r1) % n
    sum, dif = (r1+r2)%n, (r1-r2)%n
    if sum != 0 and dif != 0:
        g = gcd.gcd(sum,n)
        if 1 < g < n:
            raise FactorFound({g:1, n//g:1})

class Issquare:
    q64 = [0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57]
    q63 = [0, 1, 4, 7, 9, 16, 18, 22, 25, 28, 36, 37, 43, 46, 49, 58]
    q65 = [0, 1, 4, 9, 10, 14, 16, 25, 26, 29, 30, 35, 36, 39, 40, 49, 51, 55, 56, 61, 64]
    q11 = [0, 1, 3, 4, 5, 9]
    def __call__(self, a):
        if a&63 in self.q64:
            r = a%45045
            if r%63 in self.q63 and r%65 in self.q65 and r%11 in self.q11:
                q = prime.sqrt(a)
                if q*q == a:
                    return q
        return 0

issquare = Issquare()

def mod_sqrt(a, m):
    """
    Return a square root of 'a' mod 'm'.
    """
    if m < 0:
        raise ValueError, 'negative modulus.'
    if not m:
        raise ZeroDivisionError
    if m == 1:
        return 0

    am = a % m
    if (not am) or am == 1:
        return am
    p = issquare(am)
    if p:
        return p
    if prime.primeq(m):
        return _modp_sqrt(am, m)
    if m&3 == 0:
        if am&3 == 2 or am&3 == 3:
            raise ValueError, "There is no square root of %s mod %s" % (a, m)
        else:
            t, step = am&3, 4
    else:
        t, step = 0, 1
    p = 3
    while p < m:
        if prime.isprime(p) and not (m % p):
            if not (am % p):
                while t % p:
                    t += step
                step *= p
                p += 2
                continue
            s = _modp_sqrt(am, p)
            if s:
                while t % p != s:
                    t += step
                step *= p
            else:
                raise ValueError, "There is no square root of %s mod %s" % (a, m)
        p += 2
    for i in range(t, m, step):
        if (i*i) % m == am:
            return i
    raise ValueError, "There is no square root of %s mod %s" % (a, m)

def _modp_sqrt(a, p):
    """
    Return a square root of 'a' mod 'p' where 'p' is a prime.
    This function is intended to be called from modp_sqrt only.
    """
    if arith1.legendre(a, p) == 1:
        if p & 3 == 3:
            return pow(a, (p+1)//4, p)
        elif p & 7 == 5:
            if pow(a, (p-1)//4, p) == 1:
                return pow(a, (p+3)//8, p)
            else:
                return (2*a*pow(4*a, (p-5)//8, p)) % p
        else:
            r, q = prime.vp((p-1)//8, 2, 3)
            n = 2
            while arith1.legendre(n, p) == 1:
                n += 1
            y = pow(n, q, p)
            x = pow(a, (q-1)//2, p)
            b = (a*x*x) % p
            x = (a*x) % p
            while b != 1:
                s, m = b, 0
                while s != 1:
                    s, m = (s*s)%p, m+1
                y = pow(y, pow(2, r-m-1, p-1), p)
                r = m
                x = (x*y) % p
                y = (y**2) % p
                b = (b*y) % p
            return x
    else:
        raise ValueError, "There is no square root of %s mod %s" % (a, p)

def PrimePowerTest(n):
    """
    This program using Algo. 1.7.5 in Cohen's book judges whether
    n is of the form p**k with p or not.
    If it is True, then return is (p,k)
    If it is False, then return is (n,0)
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
                    return n,0
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

def mpqs(N):
    return MPQS(N).run()
