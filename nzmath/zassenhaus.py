from __future__ import division
import random

import arith1
import prime
import rational
import combinatorial
import matrix
import lattice
import vector
import integerResidueClass
import polynomial
import finitefield


def zassenhaus(f):
    """
    zassenhaus(f) -> list of factors of f.

    Factor a squarefree monic integer coefficient polynomial f with
    Berlekamp-Zassenhaus method.
    """
    p, fp_factors = padicFactorization(f)
    if len(fp_factors) == 1:
        return [f]
    # lift to Mignotte bound
    blm = upperBoundOfCoefficient(f)
    q = p
    while q < 2*blm:
        fp_factors = padicLiftList(f, fp_factors, p, q)
        q *= p
    return bruteForceSearch(f, fp_factors, q)

def vanHoeij(f):
    """
    vanHoeij(f) -> list of factors of f.

    Factor a squarefree monic integer coefficient polynomial f with
    van Hoeij's knapsack method.
    """
    # precomputations
    p, fp_factors = padicFactorization(f)
    if len(fp_factors) == 1:
        return [f]
    # lift to Mignotte bound
    blm = upperBoundOfCoefficient(f)
    q = p
    while q < 2*blm:
        fp_factors = padicLiftList(f, fp_factors, p, q)
        q *= p
    if len(fp_factors) < 15:
        return bruteForceSearch(f, fp_factors, q)
    factors = []
    bfbound = 4
    for d in range(1, bfbound):
        found, combination = findCombination(f, d, fp_factors, q)
        if found:
            factors.append(found)
            for picked in combination:
                fp_factors.remove(picked)
            f = f / found
    if len(fp_factors) < 2*bfbound:
        factors.append(f)
        return factors

    # knapsack factorization
    n = len(fp_factors)
    brt = complexRootAbsoluteUpperBound(f)
    fp_degrees = [g.degree() for g in fp_factors]
    Base = matrix.unitMatrix(n)
    s, d = 5, 5
    while True:
        A = newMatrix(s, d)

        # determine bound (and sometimes Hensel lift)
        B = [0] * s
        pa, pb = [], []
        for i in range(s):
            for j in range(d):
                if A[i, j]:
                    B[i] += A[i, j] * fp_degrees[j] * brt**j
            while 2*p*B[i] > q:
                # more Hensel lift
                q *= p
                fp_factors = padicLiftList(f, fp_factors, p, q)
            pa.append(q)
            pb.append(q // p)
            while pb[i] > 2*B[i]*p:
                pb[i] = pb[i] // p

        # make lattice
        preF = []
        for j in range(n):
            preF.extend(tri(fp_factors[j]))
        F = matrix.Matrix(d, n, preF)
        C = (A * F).transpose()
        c = arith1.floorsqrt(s * n) // 2
        M = c ** 2 * n + s * n ** 2 // 4
        extBase = matrix.Matrix(Base.row + s, n + s)
        for i in range(Base.row):
            for j in range(n):
                if Base[i, j]:
                    extBase[i, j] = c * Base[i, j]
        BC = Base * C
        for i in range(Base.row):
            for j in range(s):
                extBase[i, n + j] = BC[i, j]
        for i in range(s):
            extBase[Base.row + i, n + i] = pa[i] // pb[i]
        extBase = extBase.transpose()

        # LLL
        L = lattice.Lattice(extBase, matrix.unitMatrix(extBase.row))
        transform = L.LLL()
        newBase = extBase * transform
        # Gram-Schmidt
        V = [(newBase[0], vector.innerProduct(newBase[0], newBase[0]))]
        for i in range(1, newBase.column):
            w = newBase[i]
            for v, b in V:
                mu = vector.innerProduct(v, newBase[i]) / b
                w -= mu * v
            V.append((w, vector.innerProduct(w, w)))
        while V[-1][1] > M:
            V.pop()
        r = Base.row
        Base = matrix.Matrix(n, len(V))
        for i in range(n):
            for j in range(len(V)):
                Base[i, j] = newBase[i, j] / c
        if Base.column == r:
            # dimension of bases is not decreased.
            q *= p
            fp_factors = padicLiftList(f, fp_factors, p, q)
            s += 1
            d += 1
            continue
        if Base.column == 1:
            # f is irreducible
            factors.append(f)
            return factors
        echelonForm = Base.columnEchelonForm()
        Base = Base.transpose()
        # check whether problem is solved or not
        for i in range(echelonForm.row):
            weight = 0
            for j in range(echelonForm.column):
                if echelonForm[i, j] < 0 or echelonForm[i, j] > 1:
                    break
                weight += echelonForm[i, j]
            else:
                if weight != 1:
                    break
        else:
            ZqZ = integerResidueClass.IntegerResidueClassRing.getInstance(q)
            ZqZX = polynomial.PolynomialRing(ZqZ, f.getVariable())
            for j in range(echelonForm.column):
                gj = 0
                for i in range(echelonForm.row):
                    if echelonForm[i, j]:
                        if gj:
                            gj = gj * fp_factors[i]
                        else:
                            gj = fp_factors[i]
                gj = minimumAbsoluteInjection(ZqZX.createElement(gj))
                if not divisibilityTest(gj, f):
                    factors.append(gj)
                else:
                    break
            else:
                # factorization is finished
                return factors
        s += 1
        d += 1
        # haven't yet finished, continue.

def padicFactorization(f):
    """
    padicFactorization(f) -> p, factors

    Return a prime p and a p-adic factorization of given integer
    coefficient squarefree polynomial f. The result factors have
    integer coefficients, injected from F_p to its minimum absolute
    representation. The prime is chosen to be 1) f is still squarefree
    mod p, 2) the number of factors is not greater than with the
    successive prime.
    """
    num_factors = f.degree()
    stock = None
    for p in prime.generator():
        fmodp = polynomial.OneVariableSparsePolynomial(
            f.coefficient.getAsDict(),
            f.getVariable(),
            finitefield.FinitePrimeField.getInstance(p))
        g = fmodp.getRing().gcd(fmodp,
                                fmodp.differentiate(fmodp.getVariable()))
        if g.degree() == 0:
            fp_factors = fmodp.factor()
            if not stock or num_factors > len(fp_factors):
                stock = (p, fp_factors)
                if len(fp_factors) == 1:
                    return stock
                num_factors = len(fp_factors)
            else:
                break
    p = stock[0]
    fp_factors = []
    for (fp_factor, m) in stock[1]:
        assert m == 1 # since squarefree
        fp_factors.append(minimumAbsoluteInjection(fp_factor))
    return (p, fp_factors)

def bruteForceSearch(f, fp_factors, q):
    """
    bruteForceSearch(f, fp_factors, q) -> [factors]

    Find the factorization of f by searching a factor which is a
    product of some combination in fp_factors.  The combination is
    searched by brute force.
    """
    factors = []
    d, r = 1, len(fp_factors)
    while 2*d <= r:
        found, combination = findCombination(f, d, fp_factors, q)
        if found:
            factors.append(found)
            for picked in combination:
                fp_factors.remove(picked)
            f = f / found
            r -= d
        else:
            d += 1
    factors.append(f)
    return factors

def padicLiftList(f, factors, p, q):
    """
    padicLift(f, factors, p, q) -> lifted_factors

    Find a lifted integer coefficient polynomials such that:
      f = G1*G2*...*Gm (mod q*p),
      Gi = gi (mod q),
    from f and gi's of integer coefficient polynomials such that:
      f = g1*g2*...*gm (mod q),
      gi's are pairwise coprime
    with positive integers p dividing q.
    """
    ZpZx = polynomial.PolynomialRing(
        integerResidueClass.IntegerResidueClassRing.getInstance(p),
        f.getVariable())
    gg = reduce(lambda x, y: x*y, factors, 1)
    h = ZpZx.createElement((f - gg) / q)
    lifted = []
    for g in factors:
        gg = gg / g
        g_mod = ZpZx.createElement(g)
        if gg.degree() == 0:
            break
        u, v, w = extgcdp(g, gg, p)
        if w.degree() > 0:
            raise ValueError, "factors must be pairwise coprime."
        v_mod = ZpZx.createElement(v)
        t = v_mod * h // g_mod
        lifted.append(g + minimumAbsoluteInjection(v_mod * h - g_mod * t)*q)
        u_mod = ZpZx.createElement(u)
        gg_mod = ZpZx.createElement(gg)
        h = u_mod * h + gg_mod * t
    lifted.append(g + minimumAbsoluteInjection(h)*q)
    return lifted

def extgcdp(f, g, p):
    """
    extgcdp(f,g,p) -> u,v,w

    Find u,v,w such that f*u + g*v = w = gcd(f,g) mod p.
    """
    zpz = integerResidueClass.IntegerResidueClassRing.getInstance(p)
    f_coeff = f.coefficient.getAsDict()
    f_zpz = polynomial.OneVariableSparsePolynomial(f_coeff, "x", zpz)
    g_coeff = g.coefficient.getAsDict()
    g_zpz = polynomial.OneVariableSparsePolynomial(g_coeff, "x", zpz)
    u, v, w, x, y, z = (zpz.createElement(1), zpz.createElement(0), f_zpz,
                        zpz.createElement(0), zpz.createElement(1), g_zpz,)
    while z:
        q = w // z
        u, v, w, x, y, z = x, y, z, u - q*x, v - q*y, w - q*z
    if w.degree() == 0 and w != zpz.createElement(1):
        u = u / w
        v = v / w
        w = w / w
    if isinstance(u, polynomial.OneVariablePolynomial):
        u = minimumAbsoluteInjection(u)
    if isinstance(v, polynomial.OneVariablePolynomial):
        v = minimumAbsoluteInjection(v)
    if isinstance(w, polynomial.OneVariablePolynomial):
        w = minimumAbsoluteInjection(w)
    return u, v, w

def minimumAbsoluteInjection(f):
    """
    minimumAbsoluteInjection(f) -> F

    Return an integer coefficient polynomial F by injection of a Z/pZ
    coefficient polynomial f with sending each coefficient to minimum
    absolute representatives.

    """
    coefficientRing = f.getCoefficientRing()
    if isinstance(coefficientRing, integerResidueClass.IntegerResidueClassRing):
        p = coefficientRing.m
    elif isinstance(coefficientRing, finitefield.FinitePrimeField):
        p = coefficientRing.getCharacteristic()
    else:
        raise TypeError, "unknown ring (%s)" % repr(coefficientRing)
    half = p // 2
    g = polynomial.OneVariableSparsePolynomial({}, f.getVariable(), rational.theIntegerRing)
    for i, c in f.coefficient.iteritems():
        if c.n > half:
            g[i] = c.n - p
        else:
            g[i] = c.n
    return g


def upperBoundOfCoefficient(f):
    """
    upperBoundOfCoefficient(polynomial) -> long

    Compute Landau-Mignotte bound of coefficients of factors, whose
    degree is no greater than half of the given polynomial.  The given
    polynomial must have integer coefficients.
    """
    weight = 0
    for c in f.coefficient.itercoeffs():
        weight += abs(c)**2
    weight = arith1.floorsqrt(weight) + 1
    degree = f.degree()
    lc = f[degree]
    m = degree // 2 + 1
    bound = 1
    for i in range(1, m):
        b = combinatorial.binomial(m - 1, i) * weight + \
            combinatorial.binomial(m - 1, i - 1) * lc
        if bound < b:
            bound = b
    return bound

def findCombination(f, d, factors, q):
    """
    findCombination(f, d, factors, q) -> g, list

    Find a combination of d factors which divides f (or its
    complement).  The returned values are: the product g of the
    combination and a list consisting of the combination itself.
    If there is no combination, return (0,[]).

    """
    if d == 1:
        for g in factors:
            if divisibilityTest(f, g):
                return (g, [g])
    else:
        ZqZ = integerResidueClass.IntegerResidueClassRing.getInstance(q)
        ZqZX = polynomial.PolynomialRing(ZqZ, f.getVariable())
        for idx in combinatorial.combinationIndexGenerator(len(factors), d):
            picked = [factors[i] for i in idx]
            product = reduce(lambda x, y: x*y, picked, 1)
            product = minimumAbsoluteInjection(ZqZX.createElement(product))
            if divisibilityTest(f, product):
                return (product, picked)
    return 0, [] # nothing found

def divisibilityTest(f, g):
    """
    Return boolean value whether f is divisible by g or not, for polynomials.
    """
    if g[0] and f[0] % g[0]:
        return False
    if f % g:
        return False
    return True

def complexRootAbsoluteUpperBound(f):
    """
    complexRootAbsoluteUpperBound(f) -> m

    Return an upper bound of absolute value of complex root of given
    (complex coefficient) polynomial f.
    """
    n = 0
    for i, c in f.coefficient.iteritems():
        if i == f.degree():
            d = abs(c)
        elif n < abs(c):
            n = abs(c)
    return int(2 + n/d)

def newMatrix(s, d):
    """
    create a random s by d matrix.
    """
    if s == d:
        return matrix.unitMatrix(s)
    elif s > d:
        rand_list = []
        for i in range(s):
            for j in range(d):
                rand_list.append(random.randrange(d))
        return matrix.Matrix(s, d, rand_list)
    raise ValueError, "s must not be smaller than d."

def tri(f):
    """
    tr(f) -> list of Tr_i(f)

    Return the list of Tr_i(f) for a monic integer coefficient
    polynomial f in range 0 < i <= deg(f).  Tr_i(f) is defined as the
    sum of i-th powered roots of f.
    """
    deg = f.degree()
    plist = [f[deg - 1]]
    for i in range(2, deg + 1):
        p = i*f[deg - i]
        for k in range(1, i):
            p += plist[k] * f[deg - i + k]
        plist.append(p)
    return plist

# for backward compatibility
combinationIndexGenerator = combinatorial.combinationIndexGenerator
