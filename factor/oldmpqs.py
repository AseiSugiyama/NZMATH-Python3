## 
## defs for MPQS
##
from nzmath.factor.factor import *

class FactorFound:
    def __init__(self, factors):
        self.value = factors

class F2MatrixWithTwoVectors:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.u = []
        self.v = []

    def extendrow(self, vector, u0, v0):
        rownum = self.rowsize()
        self.rows.append(vector)
        for pi in vector:
            while pi >= len(self.cols):
                self.cols.append([])
            self.cols[pi].append(rownum)
        self.u.append(u0)
        self.v.append(v0)

    def compact(self):
        isdeleted = 1 # pass first test
        while isdeleted:
            isdeleted = 0
            for j in self.cols:
                if j and len(j) == 1:
                    k = j[0]
                    for i in self.rows[k]:
                        if k in self.cols[i]:
                            self.cols[i].remove(k)
                    self.rows[k] = []
                    self.u[k] = self.v[k] = 0
                    isdeleted = 1
                elif j and len(j) == 2:
                    k0, k1 = j[0], j[1]
                    for i in self.rows[k1]:
                        if i in self.rows[k0]:
                            self.cols[i].remove(k0)
                            self.cols[i].remove(k1)
                            self.rows[k0].remove(i)
                        elif self.cols[i]:
                            self.cols[i][self.cols[i].index(k1)] = k0
                            self.rows[k0].append(i)
                    self.rows[k1] = []
                    self.u[k0], self.u[k1] = self.u[k0]*self.u[k1], 0
                    self.v[k0], self.v[k1] = self.v[k0]*self.v[k1], 0
                    isdeleted = 1
        while self.cols.count([]):
            j = self.cols.index([])
            for i in range(self.rowsize()):
                for k in range(len(self.rows[i])):
                    if self.rows[i][k] > j:
                        self.rows[i][k] = self.rows[i][k] - 1
            del self.cols[j]
        while self.rows.count([]):
            i = self.rows.index([])
            for j in range(self.colsize()):
                for k in range(len(self.cols[j])):
                    if self.cols[j][k] > i:
                        self.cols[j][k] = self.cols[j][k] - 1
            del self.rows[i], self.u[i], self.v[i]

    def transpose(self):
        self.rows, self.cols = self.cols, self.rows

    def colsize(self):
        return len(self.cols)

    def rowsize(self):
        return len(self.rows)

    def xorrow(self, i, j):
        lc = self.rows[i][:]
        for n in self.rows[j]:
            if n in lc:
                lc.remove(n)
            else:
                lc.append(n)
        lc.sort()
        return lc

    def kernel(self, n):
        c, d = {}, {}
        for k in range(self.colsize()):
            for j in range(self.rowsize()):
                if c.has_key(j):
                    continue
                if k in self.rows[j]:
                    for i in range(self.rowsize()):
                        if i != j and k in self.rows[i]:
                            self.rows[i] = self.xorrow(i, j)
                    c[j], d[k] = k, j
                    break
        del c

        for i in range(self.colsize()):
            if d.has_key(i):
                continue
            x = [i]
            for k in d.keys():
                if i in self.rows[d[k]]:
                    x.append(k)
            confirm(x, self.u, self.v, n)

class QuadraticPolynomial:
    def __init__(self, a, b, c):
        assert b%2 == 0
        self._a, self._b, self._c = a, b, c
        self._d = (b/2)**2 - a*c

    def __call__(self, m):
        return (self._a*m - self._b) * m + self._c

    def root_modp(self,p):
        if not self._a % p and self._b % p:
            return (self._c* arith1.inverse(self._b, p)) % p
        elif self._a % p:
            y1 = mod_sqrt(self._d, p)
            y2 = arith1.inverse(self._a, p)
            x = [((y1 + self._b/2)*y2) % p, ((-y1 + self._b/2)*y2) % p]
            x.sort()
            return tuple(x)

class MPQS:
    def __init__(self, n):
        self.N = n

    def run(self, sizeofFB=300, halfWidth=65535, C3=10, C4=10):
        """
        extra primes can be C3 times as big as the biggest of factor base.
        C4 is for plenty of linear relations
        """
        try:
            self.make_factor_base(sizeofFB)
            self.bl = math.log(self.factor_base[-1] * C3)
            self.mat = F2MatrixWithTwoVectors()
            a = arith1.floorsqrt(2L*self.N) // halfWidth
            if a&1 == 0:
                a -= 1
            self.wanted = len(self.factor_base) + C4
            while self.wanted > 0:
                while not prime.primeq(a) or arith1.legendre(self.N, a) != 1:
                    a += 2
                b = arith1.modsqrt(self.N,a)
                c = (b**2-self.N) / a
                self.sieve(a, b+b, c, halfWidth)
                a += 2
            self.eliminate()
        except FactorFound, r:
            return [item for item in r.value.iteritems()]
        else:
            return self.run(sizeofFB, halfWidth, C3, C4*2)

    def make_factor_base(self, size):
        self.factor_base = []
        q = 3
        while len(self.factor_base) < size:
            if prime.primeq(q):
                qr = arith1.legendre(self.N, q)
                if qr == 1:
                    self.factor_base.append(q)
                elif qr == 0: # very rare case
                    raise FactorFound({q:1, self.N // q:1})
            q += 2
        self.factor_base[:0] = [-1, 2L]
        self.small_factor = self.factor_base[:size//10]

    def sieve(self, a, b, c, rangeHalfWidth):
        assert b % 2 == 0
        rangeMin = (b/2)//a - rangeHalfWidth
        rangeMax = (b/2)//a + rangeHalfWidth
        t = {}
        sieve_prime = self.factor_base[len(self.small_factor):]
        f = QuadraticPolynomial(a, b, c)
        if a in sieve_prime:
            l = math.log(a)
            if b % a:
                x = f.root_modp(a)
                i = rangeMin//a*a + x
                while i < rangeMax:
                    t[i] = l
                    i += a
            sieve_prime.remove(a)
        for p in sieve_prime:
            l = math.log(p)
            x0, x1 = f.root_modp(p)
            d = x1-x0
            i = rangeMin//p*p + x0
            while i < rangeMax:
                t[i] = t.get(i, 0) + l
                t[i+d] = t.get(i+d, 0) + l
                i += p
        if a not in self.factor_base:
            self.factor_base.append(a)
            self.wanted += 1
        for i in t.keys():
            if math.log(abs(f(i))) - t[i] <= self.bl:
                ui = f(i)
                if ui<0:
                    factors = {-1:1}
                    for p, e in trialdivision.trialDivision(-ui):
                        factors[p] = e
                else:
                    factors = {}
                    for p, e in trialdivision.trialDivision(ui):
                        factors[p] = e
                factors[a] = factors.get(a, 0) + 1
                ti = []
                for p in factors.keys():
                    if factors[p] & 1:
                        try:
                            ti.append(self.factor_base.index(p))
                        except ValueError:
                            self.factor_base.append(p)
                            self.wanted = self.wanted + 1
                            ti.append(self.factor_base.index(p))
                ti.sort()
                self.mat.extendrow(ti, a*ui, a*i - b/2)
                self.wanted -= 1
                if self.wanted <= 0:
                    return

    def eliminate(self):
        self.mat.compact()
        self.mat.transpose()
        self.mat.kernel(self.N)
        # failed to factor if this line is reached

def confirm(dep, u, v, n):
    r1 = r2 = 1
    for i in dep:
        r1 *= u[i]
        r2 *= v[i] % n
    assert (r1-r2**2) % n == 0
    r1 = arith1.floorsqrt(r1) % n
    plus, minus = (r1 + r2) % n, (r1 - r2) % n
    if plus != 0 and minus != 0:
        g = gcd.gcd(plus, n)
        if 1 < g < n:
            raise FactorFound({g:1, n//g:1})

def mpqs(N):
    return MPQS(N).run()

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
    p = arith1.issquare(am)
    if p:
        return p
    if prime.primeq(m):
        return arith1.modsqrt(am, m)
    if m&3 == 0:
        if am&3 == 2 or am&3 == 3:
            raise ValueError, "There is no square root of %s mod %s" % (a, m)
        else:
            t, step = am&3, 4
    else:
        t, step = 0, 1
    p = 3
    while p < m:
        if prime.primeq(p) and not (m % p):
            if not (am % p):
                while t % p:
                    t += step
                step *= p
                p += 2
                continue
            s = arith1.modsqrt(am, p)
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
