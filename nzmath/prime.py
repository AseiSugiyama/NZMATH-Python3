"""
A module for generating primes and testing primality.
"""

import gcd
import bigrandom
from arith1 import floorsqrt, vp


def trialDivision(n, bound = 0):
    """

    Trial division primality test for an odd natural number.
    Optional second argument is a search bound of primes.
    If the bound is given and less than the sqaure root of n
    and True is returned, it only means there is no prime factor
    less than the bound.

    """

    if bound:
        m = min((bound, floorsqrt(n)))
    else:
        m = floorsqrt(n)
    p = 3
    while p <= m:
        if not (n % p):
            return False
        p += 2
    return True

def spsp(n, base, s=None, t=None):
    """

    Strong Pseudo-Prime test.  Optional third and fourth argument
    s and t are the numbers such that n-1 = 2**s * t and t is odd.

    """
    if not s or not t:
        s, t = vp(n-1, 2)
    z = pow(base, t, n)
    if z != 1 and z != n-1:
        j = 0
        while j < s:
            j += 1
            z = pow(z, 2, n)
            if z == n-1:
                break
        else:
            return False
    return True

def millerRabin(n, times = 20):
    """

    Miller-Rabin pseudo-primality test.  Optional second argument
    times (default to 20) is the number of repetition.  The error
    probability is at most 4**(-times).

    """
    s, t = vp(n-1, 2)
    for i in range(times):
        b = bigrandom.randrange(2, n-1)
        if not spsp(n, b, s, t):
            return False
    return True

def bigprimeq(z):
    if long(z) != z:
        raise ValueError, "non-integer for primeq()"
    elif z <= 1:
        return False
    elif gcd.gcd(z, 510510) > 1:
        return (z in (2, 3, 5, 7, 11, 13, 17))
    return millerRabin(z)

def prime(s):
    """prime(n) returns the n-th prime number."""
    if s != long(s):
        raise ValueError, "non-integer for prime()"
    elif s <= 0:
        raise ValueError, "non-positive-integer for prime()"
    i = 1
    for p in generator():
        if i == s:
            return p
        i += 1
    # The following line should not be reached:
    raise ValueError, "Too big number %d for prime(i)." % s

def generator():
    """

    Generate primes from 2 to infinity.

    """
    yield 2
    yield 3
    yield 5
    coprimeTo30 = (7, 11, 13, 17, 19, 23, 29, 31)
    times30 = 0
    while True:
        for i in coprimeTo30:
            if primeq(i + times30):
                yield i + times30
        times30 += 30

def generator_eratosthenes(n):
    """
    Generate primes up to n using Eratosthenes sieve.
    """
    if n < 2:
        raise StopIteration
    yield 2
    sieve = [1]*(((n+1)//2)-1)
    k = 3
    i = 0
    sieve_len = len(sieve)
    while k*k <= n:
        if sieve[i]:
            yield k
            j = i + k
            while j < sieve_len:
                sieve[j] = 0
                j += k
        k, i = k+2, i+1
    while k <= n:
        if sieve[i]:
            yield k
        k, i = k+2, i+1

def nextPrime(n):
    """

    returns the smallest prime bigger than the given integer.

    """
    if n <= 1:
        return 2
    if n == 2:
        return 3
    n += (1 + (n & 1)) # make n be odd.
    while not primeq(n):
        n += 2
    return n

def randPrime(n):
    """
    returns a random n-digits prime
    """
    if n <= 0 :
        raise ValueError,"input number must be natural number"
    else:
        p = bigrandom.randrange(10**(n-1), (10**n)-1)
        if not (p % 2):
            p += 1
        i = 0
        while True:
            if primeq(p+i):
                break
            else:
                i += 2
    if p+i >= 10**n:
        return randPrime(n) # very rare case or n is too small case
    return p+i

def smallSpsp(n):
    """

    4 spsp tests are sufficient to determine whether an integer less
    than 10**12 is prime or not.

    """
    for p in [2, 13, 23, 1662803]:
        if not spsp(n, p):
            return False
    return True

def primeq(n):
    """
    A convinient function for primatilty test. It uses one of
    trialDivision, smallSpsp or apr depending on the size of n.
    """
    if long(n) != n:
        raise ValueError, "non-integer for primeq()"
    if n <= 1:
        return False

    if gcd.gcd(n, 510510) > 1:
        return (n in (2, 3, 5, 7, 11, 13, 17))
    if n < 2000000:
        return trialDivision(n)
    if not smallSpsp(n):
        return False
    if n < 10000000000000:
        return True
    return apr(n)

# defs for APR algorithm

def _isprime(n):
    if gcd.gcd(n, 510510) > 1:
        return (n in (2, 3, 5, 7, 11, 13, 17))
    for p in [2, 13, 23, 1662803]:
        if not spsp(n, p):
            return False
    return True

def properDivisors(n):
    """
    Return proper divisors of n (divisors of n excluding 1 and n).

    It is only useful for a product of small primes.
    """
    if n in (2,3,5,7,11,13,17,19,23):
        return []
    else:
        l = [1]
        d = _factor(n)
        for (p,e) in d:
            for j in range(1, e+1):
                l += [k*pow(p,j) for k in l if k % p != 0]
        l.remove(1)
        l.remove(n)
        l.sort()
        return l

def _factor(n, bound = 0):
    """
    Trial division factorization for a natural number.
    Optional second argument is a search bound of primes.
    If the bound is given and less than the sqaure root of n,
    result is not proved to be a prime factorization.
    """

    factors = []
    if not (n % 2):
        v2, n = vp(n, 2)
        factors.append((2, v2))
    m = _calc_bound(n, bound)
    p = 3
    while p <= m:
        if not (n % p):
            v, n = vp(n, p)
            factors.append((p, v))
            m = _calc_bound(n, bound)
        p += 2
    if n > 1:
        factors.append((n, 1))
    return factors

def _calc_bound(n, bound = 0):
    if bound:
        m = min((bound, floorsqrt(n)))
    else:
        m = floorsqrt(n)
    return m

def primitive_root(p):
    """
    Return a primitive root of Z/pZ.
    """
    i = 2
    pd = properDivisors(p-1)
    while i < p:
        for d in pd:
            if pow(i, (p-1)//d, p) == 1:
                break
        else:
            return i
        i += 1

class Zeta:
    """
    Represent linear combinations of roots of unity.
    """
    def __init__(self, size, pos=None, val=1):
        self.size = size
        self.z = [0]*self.size
        if pos != None:
            self.z[pos%self.size] = val

    def __add__(self, other):
        if self.size == other.size:
            m = self.size
            zr_a = Zeta(m)
            for i in range(m):
                zr_a.z[i] = self.z[i] + other.z[i]
            return zr_a
        else:
            m = gcd.lcm(self.size,other.size)
            return self.promote(m) + other.promote(m)

    def __mul__(self,other):
        if not isinstance(other, Zeta):
            zr_m = Zeta(self.size)
            zr_m.z = [x*other for x in self.z]
            return zr_m
        elif self.size == other.size:
            zr_m = Zeta(self.size)
            other = +other
            for k in range(other.size):
                if not other.z[k]:
                    continue
                elif other.z[k] == 1:
                    zr_m = zr_m + (self<<k)
                else:
                    zr_m = zr_m + (self<<k)*other.z[k]
            return zr_m
        else:
            m = gcd.lcm(self.size,other.size)
            return self.promote(m)*other.promote(m)

    __rmul__ = __mul__

    def __lshift__(self, offset):
        """The name is shift but the meaning of function is rotation."""
        new = Zeta(self.size)
        new.z = self.z[-offset:] + self.z[:-offset]
        return new

    def __pow__(self, e, mod=0):
        r = Zeta(self.size, 0)
        if e == 0:
            return r
        if mod:
            z = self % mod
        else:
            z = +self
        while True:
            if e&1 == 1:
                r = z*r
                if mod:
                    r = r % mod
                if e == 1:
                    return r
            e //= 2
            z = z.square(mod)

    def square(self, mod=0):
        zr_sq = self*self
        if mod:
            zr_sq = zr_sq % mod
        return zr_sq

    def __pos__(self):
        m = self.size
        z_p = Zeta(m)
        if m % 2 == 0:
            mp = m//2
            for i in range(mp):
                if self.z[i] > self.z[i+mp]:
                    z_p.z[i] = self.z[i] - self.z[i+mp]
                else:
                    z_p.z[i+mp] = self.z[i+mp] - self.z[i]
        else:
            p = 3
            while m%p:
                p += 2
            mp = m//p
            for i in range(mp):
                min = self.z[i]
                for j in range(mp+i, m, mp):
                    if min > self.z[j]:
                        min = self.z[j]
                for j in range(i,m,mp):
                    z_p.z[j] = self.z[j] - min
        return z_p

    def __mod__(self, mod):
        new = Zeta(self.size)
        new.z = [x%mod for x in self.z]
        return new

    def __setitem__(self, position, value):
        self.z[position % self.size] = value

    def __getitem__(self, position):
        return self.z[position % self.size]

    def promote(self, size):
        if size == self.size:
            return +self
        new = Zeta(size)
        r = size // self.size
        for i in range(self.size):
            new.z[i*r] = self.z[i]
        return new

    def __len__(self):
        return self.size

    def __eq__(self, other):
        for i in range(self.size):
            if self.z[i] != other.z[i]:
                return False
        return True

    def weight(self):
        return len(filter(None,self.z))

    def mass(self):
        return sum(self.z)

class FactoredInteger:
    def __init__(self, other):
        if isinstance(other, FactoredInteger):
            self.integer = other.integer
            self.factors = other.factors.copy()
        else:
            self.integer = long(other)
            self.factors = {}
            for (p, e) in _factor(self.integer):
                self.factors[p] = e

    def __mul__(self, other):
        if isinstance(other, FactoredInteger):
            new = +self
            for p in other.factors:
                new.factors[p] = new.factors.get(p, 0) + other.factors[p]
            new.integer *= other.integer
            return new
        else:
            return self * FactoredInteger(other)

    __rmul__ = __mul__

    def __pow__(self, other, mod=None):
        new = +self
        new.integer = new.integer**other
        for p in new.factors:
            new.factors[p] *= other
        return new

    def __pos__(self):
        return self.__class__(self)

    def __str__(self):
        return str(self.integer)

    def __mod__(self, other):
        return self.integer%other

    def __cmp__(self, other):
        return cmp(long(self), long(other))

    def __long__(self):
        return long(self.integer)

class TestPrime:
    primes = [2,3,5,7,11,13,17,19,23,29,31]

    def __init__(self, t=12):
        self.t = FactoredInteger(t)
        self.et = FactoredInteger(4)*(2**self.t.factors[2])
        smoothp = [1]
        for p in self.t.factors:
            temp = smoothp[:]
            pp = 1
            for i in range(self.t.factors[p]):
                pp *= p
                smoothp += [x*pp for x in temp]
        for p in [x+1 for x in smoothp]:
            if p&1 and _isprime(p):
                self.et = self.et*p
                if p in self.t.factors:
                    self.et = self.et*(p**self.t.factors[p])
        del smoothp

    def next(self):
        eu = []
        for p in self.primes:
            if self.t.factors.has_key(p):
                eu.append((p-1)*(p**(self.t.factors[p]-1)))
            else:
                eu.append(p-1)
        return self.__class__(self.t*self.primes[eu.index(min(eu))])

class Status:
    """
    status collector for apr.
    """
    def __init__(self):
        self.d = {}

    def yet(self, key):
        self.d[key] = 0

    def done(self, key):
        self.d[key] = 1

    def yet_keys(self):
        l = [k for k in self.d.keys() if not self.d[k]]
        return l

    def isDone(self, key):
        return self.d[key]

    def subodd(self,p,q,n,J):
        s = J.get(1,p,q)
        Jpq = J.get(1,p,q)
        m = s.size
        for x in range(2,m):
            if x % p == 0:
                continue
            sx = Zeta(m)
            i = x
            j = 1
            while i>0:
                sx[j] = Jpq[i]
                i = (i+x)%m
                j += 1
            sx[0] = Jpq[0]
            sx = pow(sx, x, n)
            s = s*sx%n
        s = pow(s, n//m, n)
        r = n%m
        t = 1
        for x in range(1, m):
            if x % p == 0:
                continue
            c = (r*x) // m
            if c:
                tx = Zeta(m)
                i = x
                j = 1
                while i > 0:
                    tx[j] = Jpq[i]
                    i = (i+x)%m
                    j += 1
                tx[0] = Jpq[0]
                tx = pow(tx, c, n)
                t = t*tx%n
        s = +(t*s%n)
        if s.weight() == 1 and s.mass() == 1:
            for i in range(1,m):
                if gcd.gcd(m,s.z.index(1)) == 1:
                    self.done(p)
                return True
        return False

    def sub8(self,q,k,n,J):
        s = J.get(3,q)
        J3 = J.get(3,q)
        m = len(s)
        sx_z = {1:s}
        x = 3
        step = 2
        while m > x:
            z_4b = Zeta(m)
            i = x
            j = 1
            while i != 0:
                z_4b[j] = J3[i]
                i = (i+x)%m
                j += 1
            z_4b[0] = J3[0]
            sx_z[x] = z_4b
            s = pow(sx_z[x], x, n) * s
            step = 8 - step
            x += step

        s = pow(s, n//m, n)

        r = n%m
        step = 2
        x = 3
        while m > x:
            c = r*x
            if c > m:
                s = pow(sx_z[x], c//m, n) * s
            step = 8 - step
            x += step
        r = r%8
        if r == 5 or r == 7:
            s = J.get(2,q).promote(m) * s
        s = +(s%n)

        if s.weight() == 1 and s.mass() == 1:
            if gcd.gcd(m, s.z.index(1)) == 1 and pow(q, (n-1)//2, n) == n-1:
                self.done(2)
            return True
        elif s.weight() == 1 and s.mass() == n-1:
            if gcd.gcd(m, s.z.index(n-1)) == 1 and pow(q, (n-1)//2, n) == n-1:
                self.done(2)
            return True
        return False

    def sub4(self,q,n,J):
        j2 = J.get(1,2,q)**2
        s = q*j2%n
        s = pow(s, n//4, n)
        if n%4 == 3:
            s = s*j2%n
        s = +(s%n)
        if s.weight() == 1 and s.mass() == 1:
            i = s.z.index(1)
            if (i == 1 or i == 3) and pow(q, (n-1)//2, n) == n-1:
                self.done(2)
            return True
        return False

    def sub2(self,q,n):
        s = pow(n-q, (n-1)//2, n)
        if s == n-1:
            if n%4 == 1:
                self.done(2)
        elif s != 1:
            return False
        return True

    def subrest(self,p,n,et,J,ub=200):
        if p == 2:
            q = 5
            c = 0
            while c < ub:
                q += 2
                if not _isprime(q) or et%q == 0:
                    continue
                if n%q == 0:
                    sys.stderr.write("%s divides %s.\n" % (q,n))
                    return False
                k = vp(q-1,2)[0]
                if k == 1:
                    if n%4 == 1 and not self.sub2(q,n):
                        return False
                elif k == 2:
                    if not self.sub4(q,n,J):
                        return False
                else:
                    if not self.sub8(q,k,n,J):
                        return False
                if self.isDone(p):
                    return True
                c += 1
            else:
                raise ImplementLimit
        else:
            step = p*2
            q = 1
            c = 0
            while c < ub:
                q += step
                if not _isprime(q) or et % q == 0:
                    continue
                if n % q == 0:
                    import sys
                    sys.stderr.write("%s divides %s.\n" % (q,n))
                    return False
                if not self.subodd(p,q,n,J):
                    return False
                if self.isDone(p):
                    return True
                c += 1
            else:
                raise ImplementLimit

class JacobiSum:
    def __init__(self):
        self.shelve = {}
    def get(self, group, p, q=None):
        if q:
            assert group == 1
            if not self.shelve.has_key(str((group,long(p),long(q)))):
                self.make(q)
            return self.shelve[str((group,long(p),long(q)))]
        else:
            assert group == 2 or group == 3
            if not self.shelve.has_key(str((group,long(p)))):
                self.make(p)
            return self.shelve[str((group,long(p)))]

    def make(self,q):
        fx = self.makefx(q)
        qpred = q-1
        qt = _factor(qpred)
        qt2 = [k for (p, k) in qt if p == 2][0]
        k, pk = qt2, 2**qt2
        if k >= 2:
            J2q = Zeta(pk, 1+fx[1])
            for j in range(2, qpred):
                J2q[j+fx[j]] = J2q[j+fx[j]]+1
            self.shelve[str((1,2L,long(q)))] = +J2q
            if k >= 3:
                J2 = Zeta(8, 3+fx[1])
                J3 = Zeta(pk, 2+fx[1])
                for j in range(2,qpred):
                    J2[j*3+fx[j]] = J2[j*3+fx[j]]+1
                    J3[j*2+fx[j]] = J3[j*2+fx[j]]+1
                self.shelve[str((3,long(q)))] = +(self.shelve[str((1,2L,long(q)))]*J3)
                self.shelve[str((2,long(q)))] = +(J2*J2)
        else:
            self.shelve[str((1,2L,long(q)))] = 1
        for (p, k) in qt:
            if p == 2:
                continue
            pk = p**k
            Jpq = Zeta(pk,1+fx[1])
            for j in range(2,qpred):
                Jpq[j+fx[j]] = Jpq[j+fx[j]]+1
            self.shelve[str((1,long(p),long(q)))] = +Jpq
        del fx

    def makefx(self, q):
        g = primitive_root(q)
        qpred = q-1
        qd2 = qpred//2
        g_mf = [0,g]
        for i in range(2,qpred):
            g_mf.append((g_mf[-1]*g)%q)
        fx = {}
        for i in range(1,qpred):
            if fx.has_key(i):
                continue
            j = 1
            while g_mf[j]+g_mf[i]-1 != q:
                j += 1
            fx[i] = j
            fx[j] = i
            fx[qpred-i] = (j-i+qd2)%qpred
            fx[fx[qpred-i]] = qpred-i
            fx[qpred-j] = (i-j+qd2)%qpred
            fx[fx[qpred-j]] = qpred-j
        del g_mf
        return fx

def apr(n):
    """

    apr is the main function for Adleman-Pomerance-Rumery primality test.
    Assuming n has no prime factors less than 32.
    Assuming n is spsp for several bases.

    """
    L = Status()

    rb = floorsqrt(n) + 1
    el = TestPrime()
    while el.et <= rb:
        el = el.next()

    plist = el.t.factors.keys()
    plist.remove(2)
    L.yet(2)
    for p in plist:
        if pow(n, p-1, p*p) != 1:
            L.done(p)
        else:
            L.yet(p)
    qlist = el.et.factors.keys()
    qlist.remove(2)
    J = JacobiSum()
    for q in qlist:
        for p in plist:
            if (q-1) % p != 0:
                continue
            if not L.subodd(p,q,n,J):
                return False
        k = vp(q-1,2)[0]
        if k == 1:
            if not L.sub2(q,n):
                return False
        elif k == 2:
            if not L.sub4(q,n,J):
                return False
        else:
            if not L.sub8(q,k,n,J):
                return False
    for p in L.yet_keys():
        if not L.subrest(p,n,el.et,J):
            return False
    r = long(n)
    i = 1
    while i < el.t.integer:
        r = (r*n) % el.et.integer
        if n % r == 0 and r != 1 and r != n:
            import sys
            sys.stderr.write("%s divide %s.\n" %(r,n))
            return False
        i += 1
    return True

class ImplementLimit (Exception):
    """
    Exception throwed when the execution hits the implementation limit.
    """
    pass
