from __future__ import division
import nzmath.arith1 as arith1
import nzmath.prime as prime
import nzmath.rational as rational
import nzmath.combinatorial as combinatorial
import nzmath.intresidue as intresidue
import nzmath.finitefield as finitefield
import nzmath.poly.uniutil as uniutil
import nzmath.poly.ring as poly_ring

# requirement: polynomial factor for numberfield(FIXME)
import nzmath.gcd as gcd
import nzmath.algfield as algfield
import nzmath.sandbox.poly.multiutil as multiutil

def zassenhaus(f):
    """
    zassenhaus(f) -> list of factors of f.

    Factor a squarefree monic integer coefficient polynomial f with
    Berlekamp-Zassenhaus method.
    """
    p, fp_factors = padic_factorization(f)
    if len(fp_factors) == 1:
        return [f]
    # lift to Mignotte bound
    blm = upper_bound_of_coefficient(f)
    q = p
    while q < 2*f.leading_coefficient()*blm:
        fp_factors = padic_lift_list(f, fp_factors, p, q)
        q *= p
    print fp_factors
    return brute_force_search(f, fp_factors, q)

def padic_factorization(f):
    """
    padic_factorization(f) -> p, factors

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
        fmodp = uniutil.polynomial(
            f.terms(),
            finitefield.FinitePrimeField.getInstance(p))
        if f.degree() > fmodp.degree():
            continue
        g = fmodp.getRing().gcd(fmodp,
                                fmodp.differentiate())
        if g.degree() == 0:
            fp_factors = fmodp.factor()
            if (not stock) or num_factors > len(fp_factors):
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
        fp_factors.append(minimum_absolute_injection(fp_factor))
    return (p, fp_factors)

def brute_force_search(f, fp_factors, q):
    """
    brute_force_search(f, fp_factors, q) -> [factors]

    Find the factorization of f by searching a factor which is a
    product of some combination in fp_factors.  The combination is
    searched by brute force.
    """
    factors = []
    d, r = 1, len(fp_factors)
    while 2*d <= r:
        found, combination = find_combination(f, d, fp_factors, q)
        if found:
            factors.append(found)
            for picked in combination:
                fp_factors.remove(picked)
            f = f.pseudo_floordiv(found)
            r -= d
        else:
            d += 1
    factors.append(f.primitive_part())
    return factors

def padic_lift_list(f, factors, p, q):
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
    ZpZx = poly_ring.PolynomialRing(
        intresidue.IntegerResidueClassRing.getInstance(p))
    gg = arith1.product(factors)
    h = ZpZx.createElement([(d, c // q) for (d, c) in (f - gg).iterterms()])
    lifted = []
    for g in factors:
        gg = gg.pseudo_floordiv(g)
        g_mod = ZpZx.createElement(g)
        if gg.degree() == 0:
            break
        u, v, w = extgcdp(g, gg, p)
        if w.degree() > 0:
            raise ValueError("factors must be pairwise coprime.")
        v_mod = ZpZx.createElement(v)
        t = v_mod * h // g_mod
        lifted.append(g + minimum_absolute_injection(v_mod * h - g_mod * t)*q)
        u_mod = ZpZx.createElement(u)
        gg_mod = ZpZx.createElement(gg)
        h = u_mod * h + gg_mod * t
    lifted.append(g + minimum_absolute_injection(h)*q)
    return lifted

def extgcdp(f, g, p):
    """
    extgcdp(f,g,p) -> u,v,w

    Find u,v,w such that f*u + g*v = w = gcd(f,g) mod p.
    """
    zpz = intresidue.IntegerResidueClassRing.getInstance(p)
    f_zpz = uniutil.polynomial(f, zpz)
    g_zpz = uniutil.polynomial(g, zpz)
    zero, one = f_zpz.getRing().zero, f_zpz.getRing().one
    u, v, w, x, y, z = one, zero, f_zpz, zero, one, g_zpz
    while z:
        q = w // z
        u, v, w, x, y, z = x, y, z, u - q*x, v - q*y, w - q*z
    if w.degree() == 0 and w[0] != zpz.one:
        u = u.scalar_exact_division(w[0]) # u / w
        v = v.scalar_exact_division(w[0]) # v / w
        w = w.getRing().one # w / w
    u = minimum_absolute_injection(u)
    v = minimum_absolute_injection(v)
    w = minimum_absolute_injection(w)
    return u, v, w

def minimum_absolute_injection(f):
    """
    minimum_absolute_injection(f) -> F

    Return an integer coefficient polynomial F by injection of a Z/pZ
    coefficient polynomial f with sending each coefficient to minimum
    absolute representatives.
    """
    coefficientRing = f.getCoefficientRing()
    if isinstance(coefficientRing, intresidue.IntegerResidueClassRing):
        p = coefficientRing.m
    elif isinstance(coefficientRing, finitefield.FinitePrimeField):
        p = coefficientRing.getCharacteristic()
    else:
        raise TypeError("unknown ring (%s)" % repr(coefficientRing))
    half = p // 2
    g = {}
    for i, c in f.iterterms():
        if c.n > half:
            g[i] = c.n - p
        else:
            g[i] = c.n
    return uniutil.polynomial(g, rational.theIntegerRing)


def upper_bound_of_coefficient(f):
    """
    upper_bound_of_coefficient(polynomial) -> int

    Compute Landau-Mignotte bound of coefficients of factors, whose
    degree is no greater than half of the given polynomial.  The given
    polynomial must have integer coefficients.
    """
    weight = 0
    for c in f.itercoefficients():
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

def find_combination(f, d, factors, q):
    """
    find_combination(f, d, factors, q) -> g, list

    Find a combination of d factors which divides f (or its
    complement).  The returned values are: the product g of the
    combination and a list consisting of the combination itself.
    If there is no combination, return (0,[]).
    """
    if d == 1:
        for g in factors:
            if divisibility_test(f.leading_coefficient()*f, g):
                return (g.primitive_part(), [g])
    else:
        ZqZ = intresidue.IntegerResidueClassRing.getInstance(q)
        ZqZX = uniutil.PolynomialRingAnonymousVariable.getInstance(ZqZ)
        for idx in combinatorial.combinationIndexGenerator(len(factors), d):
            picked = [factors[i] for i in idx]
            product = arith1.product(picked)
            product = minimum_absolute_injection(ZqZX.createElement(product))
            if divisibility_test(f.leading_coefficient()*f, product):
                return (product.primitive_part(), picked)
    return 0, [] # nothing found

def divisibility_test(f, g):
    """
    Return boolean value whether f is divisible by g or not, for polynomials.
    """
    if g[0] and f[0] % g[0]:
        return False
    if isinstance(f, uniutil.FieldPolynomial) and f % g:
        return False
    elif isinstance(f, uniutil.UniqueFactorizationDomainPolynomial) and f.pseudo_mod(g):
        return False
    return True

def integerpolynomialfactorization(f):
    """
    integerpolynomialfactorization -> list of (factors,index) of f.

    Factor a integer coefficient polynomial f with
    Berlekamp-Zassenhaus method.
    """
    F = [f]
    G = f
    c = 0
    one = G.getRing().one
    while (G.differentiate() and F[c] != one):
        c = c + 1
        deriv = G.differentiate()
        F.append(F[c-1].subresultant_gcd(deriv))
        G = G.pseudo_floordiv(F[c])
    sqfree_part = F[0].pseudo_floordiv(F[0].subresultant_gcd(F[1]))
    N = zassenhaus(sqfree_part)
    result = [()] * len(N)

    F.reverse()
    e = len(F)-1    
    for deg, deriv in enumerate(F):
        part = sqfree_part.pseudo_floordiv(sqfree_part.subresultant_gcd(deriv))
        for index,factor in enumerate(N):
            if (factor.pseudo_mod(part)):
                pass
            else:
                result[index]=(factor,deg)
    return result

def polyfactorizationNF(f):
    """
    NFPolynomialFactorization(f) -> factors

    Return a number field factorization of given number field
    coefficient squarefree polynomial f. The result factors have
    number field coefficients, its minimum absolute representation.
    """
    # initialize
    Q = rational.RationalField() # Q as RationalField
    K = f.getCoefficientRing()              # K as NumberField
    
    # to squarefree
    u = f/f.gcd(f.differentiate())

    # partition each degree.
    degree = g.degree()    
    Gcoeffs = {}   # Gcoeffs as coefficient as G (TBA)
    for i in range(degree+1):
        U[i] = u[i]
        if not isinstance(U[i], algfield.BasicAlgNumber):
            raise NotImplementError("FIXME: support only BasicAlgNumber .")
        g[i] = uniutil.OneVariableDensePolynomial(U[i].coeff,"Y",Q) / U[i].denom
        for j in range(g[i].degree()+1):
            Gcoeffs[(i,j)] = g[i][j]
    G = multiutil.polynomial(Gcoeffs,Q) # G as partition form of u

    # search for squarefree polynomial norm
    k = 0
    # FIXME: symbolic computation, but also slower.
    x = multiutil.polynomial((1,0),Q)
    y = multiutil.polynomial((0,1),Q)
    while True:
        N = T(y).resultant(G(x-k*y,y),2)
        if (N == N/N.gcd(N.differentiate())):
            break
        k = k + 1

    # Now, here N is squarefree.
    # assume all the coefficients of N is rational.Rational .
    denom = 1
    for coeff in N.coefficients():
        denom = gcd.lcm(denom, coeff.denominator)
    Nz = N * denom # NZ be a integer, but probably not monic.
    for index,coeff in Nz.terms():
        V[index] = coeff.numerator
    NZ = uniutil.polynomial(V,rational.IntegerRing())
    
    F = integerpolynomialfactorization(NZ)
    
    
