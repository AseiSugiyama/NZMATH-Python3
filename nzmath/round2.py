"""
Round 2 method

The method is for obtaining the maximal order of a number field from a
subring generated by a root of a defining polynomial of the field.

- H.Cohen CCANT Algorithm 6.1.8
- Kida Y. LN Chapter 3
"""

from __future__ import division
import logging
import nzmath.arith1 as arith1
import nzmath.finitefield as finitefield
import nzmath.factor.methods as factormethods
import nzmath.gcd as gcd
import nzmath.integerResidueClass as integerresidueclass
import nzmath.matrix as matrix
import nzmath.poly.uniutil as uniutil
import nzmath.rational as rational
import nzmath.vector as vector
import nzmath.squarefree as squarefree


_log = logging.getLogger('nzmath.round2')

uniutil.special_ring_table[finitefield.FinitePrimeField] = uniutil.FinitePrimeFieldPolynomial

Z = rational.theIntegerRing
Q = rational.theRationalField

def round2(minpoly_coeff):
    """
    Return integral basis of the ring of integers of a field with its
    discriminant.  The field is given by a list of integers, which is
    a polynomial of generating element theta.  The polynomial ought to
    be monic, in other word, the generating element ought to be an
    algebraic integer.

    The integral basis will be given as a list of rational vectors
    with respect to theta.  (In other functions, bases are returned in
    the same fashion.)
    """
    minpoly_int = uniutil.polynomial(enumerate(minpoly_coeff), Z)
    d = minpoly_int.discriminant()
    squarefactors = _prepare_squarefactors(d)
    omega = _default_omega(minpoly_int.degree())
    for p, e in squarefactors:
        _log.debug("p = %d" % p)
        omega = omega + _p_maximal(p, e, minpoly_coeff)

    G = omega.determinant()
    return omega.get_rationals(), d * G**2

def _prepare_squarefactors(disc):
    """
    Return a list of square factors of disc (=discriminant).

    PRECOND: d is integer
    """
    squarefactors = []
    if disc < 0:
        fund_disc, absd = -1, -disc
    else:
        fund_disc, absd = 1, disc
    v2, absd = arith1.vp(absd, 2)
    if squarefree.trivial_test_ternary(absd):
        fund_disc *= absd
    else:
        for p, e in factormethods.factor(absd):
            if e > 1:
                squareness, oddity = divmod(e, 2)
                squarefactors.append((p, squareness))
                if oddity:
                    fund_disc *= p
            else:
                fund_disc *= p
    if fund_disc % 4 == 1:
        if v2 % 2:
            squareness, oddity = divmod(v2, 2)
            squarefactors.append((2, squareness))
            if oddity:
                fund_disc *= 2
        else:
            squarefactors.append((2, v2 // 2))
    else: # fund_disc % 4 == 3
        assert v2 >= 2
        fund_disc *= 4
        if v2 > 2:
            squarefactors.append((2, (v2 - 2) // 2))
    return squarefactors

def _p_maximal(p, e, minpoly_coeff):
    """
    Return p-maximal basis with some related informations.

    The arguments:
      p: the prime
      e: the exponent
      minpoly_coeff: (intefer) list of coefficients of the minimal
        polynomial of theta
    """
    # Apply the Dedekind criterion
    finished, omega = Dedekind(minpoly_coeff, p, e)
    if finished:
        _log.info("Dedekind(%d)" % p)
        return omega

    # main loop to construct p-maximal order
    minpoly = uniutil.polynomial(enumerate(minpoly_coeff), Z)
    theminpoly = minpoly.to_field_polynomial()
    n = theminpoly.degree()
    q = p ** (arith1.log(n, p) + 1)
    while True:
        # Ip: radical of pO
        # Ip = <alpha>, l = dim Ip/pO (essential part of Ip)
        alpha, l = _p_radical(omega, p, q, minpoly, n)

        # instead of step 9 big matrix,
        # Kida's LN section 2.2
        # Up = {x in Ip | xIp \subset pIp} = <zeta> + p<omega>
        zeta = _p_module(alpha, l, p, theminpoly)
        if zeta.rank == 0:
            # no new basis is found
            break

        # new order
        # 1/p Up = 1/p<zeta> + <omega>
        omega2 = zeta / p + omega
        if all(o1 == o2 for o1, o2 in zip(omega.basis, omega2.basis)):
            break
        omega = omega2

    # now <omega> is p-maximal.
    return omega

def _p_radical(omega, p, q, minpoly, n):
    """
    Return module Ip with dimension of Ip/pO.

    Ip is the radical of pO, or
    Ip = {x in O | ~x in kernel f},
    where ~x is x mod pO, f is q(=p^e > n)-th powering, which in fact an
    Fp-linear map.
    """
    # Ip/pO = kernel of q-th powering.
    # omega_j^q = \sum a_i_j omega_i
    base_p = _kernel_of_qpow(omega, q, p, minpoly, n)
    l = base_p.column

    # expand basis of Ip/pO to O/pO
    base_p.toSubspace()
    beta_p = base_p.supplementBasis()

    # basis of Ip
    # pulled back from bases of Ip/pO and O/pO
    omega_poly = omega.get_polynomials()
    alpha_basis = []
    for j in range(1, l + 1):
        alpha_basis.append(omega.linear_combination([_pull_back(c, p) for c in beta_p[j]]))
    for j in range(l + 1, n + 1):
        alpha_basis.append(omega.linear_combination([_pull_back(c, p) * p for c in beta_p[j]]))
    alpha = ModuleWithDenominator(alpha_basis, omega.denominator)
    return alpha, l

def _kernel_of_qpow(omega, q, p, minpoly, n):
    """
    Return the kernel of q-th powering, which is a linear map over Fp.
    q is a power of p which exceeds n.

    (omega_j^q (mod theminpoly) = \sum a_i_j omega_i   a_i_j in Fp)
    """
    omega_poly = omega.get_polynomials()
    denom = omega.denominator
    theminpoly = minpoly.to_field_polynomial()
    field_p = finitefield.FinitePrimeField.getInstance(p)
    zero = field_p.zero
    qpow = matrix.zeroMatrix(n, n, field_p) # Fp matrix
    for j in range(n):
        a_j = [zero] * n
        omega_poly_j = uniutil.polynomial(enumerate(omega.basis[j]), Z)
        omega_j_qpow = pow(omega_poly_j, q, minpoly)
        redundancy = gcd.gcd(omega_j_qpow.content(), denom ** q)
        omega_j_qpow = omega_j_qpow.coefficients_map(lambda c: c // redundancy)
        essential = denom ** q // redundancy
        while omega_j_qpow:
            i = omega_j_qpow.degree()
            a_ji = int(omega_j_qpow[i] / (omega_poly[i][i] * essential))
            omega_j_qpow -= a_ji * (omega_poly[i] * essential)
            if omega_j_qpow.degree() < i:
                a_j[i] = field_p.createElement(a_ji)
            else:
                _log.debug("%s / %d" % (str(omega_j_qpow), essential))
                _log.debug("j = %d, a_ji = %s" % (j, a_ji))
                raise ValueError("omega is not a basis")
        qpow.setColumn(j + 1, a_j)

    return qpow.kernel()

def _p_module(alpha, l, p, theminpoly):
    """
    Return basis of Up/pO, where Up = {x in Ip | xIp \subset pIp}.
    """
    zeta = alpha.get_polynomials()[:l]
    for j in range(l):
        # refine zeta so that zeta * alpha[j] (mod theminpoly) = 0 (mod pIp)
        kernel = _null_linear_combination(zeta, alpha, j, p, theminpoly)
        if kernel is None:
            zeta = []
            break
        newzeta = []
        for k in range(1, kernel.column + 1):
            newzeta.append(sum(_pull_back(c, p) * z for (c, z) in zip(kernel[k], zeta)))
        zeta = newzeta
    n = theminpoly.degree()
    denominator = 1
    zeta_list = []
    for z in zeta:
        while True:
            try:
                zeta_list.append([_normalize_int(c * denominator) for c in _coeff_list(z, n)])
                break
            except ValueError:
                for i in range(len(zeta_list)):
                    zeta_list[i] = [c * p for c in zeta_list[i]]
                denominator *= p
                _log.debug("denominator = %d" % denominator)
    # since zeta may be empty, a hint 'dimension' is necessary
    return ModuleWithDenominator(zeta_list, denominator, dimension=n)

def _null_linear_combination(zeta, alpha, j, p, theminpoly):
    """
    Return linear combination coefficients of tau_i = z_i * alpha[j],
    which is congruent to 0 modulo theminpoly and pIp.

    alpha is a module.
    
    zeta_{j+1} = {z in zeta_j | z * alpha[j] (mod theminpoly) = 0 (mod pIp)}
    """
    n = theminpoly.degree()
    l = len(zeta)
    assert n == len(alpha.basis)
    alpha_basis = [tuple(b) for b in alpha.get_rationals()]
    alpha_mat = matrix.createMatrix(n, alpha_basis, coeff_ring=Q)
    alpha_poly = alpha.get_polynomials()

    taus = []
    for i in range(l):
        tau_i = zeta[i] * alpha_poly[j] % theminpoly
        taus.append(tuple(_coeff_list(tau_i, n)))
    tau_mat = matrix.createMatrix(n, l, taus, coeff_ring=Q)

    xi = alpha_mat.inverseImage(tau_mat)

    field_p = finitefield.FinitePrimeField.getInstance(p)
    xi_p = xi.map(field_p.createElement)
    return xi_p.kernel() # linear combination of tau_i's

def Dedekind(minpoly_coeff, p, e):
    """
    Return (finished or not, an order)

    the Dedekind criterion

    Arguments:
    - minpoly_coeff: (integer) list of the minimal polynomial of theta.
    - p, e: p**e divides the discriminant of the minimal polynomial.
    """
    n = len(minpoly_coeff) - 1  # degree of the minimal polynomial

    m, uniq = _factor_minpoly_modp(minpoly_coeff, p)
    omega = _default_omega(n)

    if m == 0:
        return True, omega

    minpoly = uniutil.polynomial(enumerate(minpoly_coeff), Z)
    v = [_coeff_list(uniq, n)]
    shift = uniq
    for i in range(1, m):
        shift = shift.upshift_degree(1).pseudo_mod(minpoly)
        v.append(_coeff_list(shift, n))
    updater = ModuleWithDenominator(v, p)

    return (m + 1 > e), updater + omega

def _factor_minpoly_modp(minpoly_coeff, p):
    """
    Factor theminpoly modulo p, and return two values in a tuple.
    We call gcd(square factors mod p, difference of minpoly and its modp) Z.
    1) degree of Z
    2) (minpoly mod p) / Z
    """
    Fp = finitefield.FinitePrimeField.getInstance(p)
    theminpoly_p = uniutil.polynomial([(d, Fp.createElement(c)) for (d, c) in enumerate(minpoly_coeff)], Fp)
    modpfactors = theminpoly_p.factor()
    mini_p = arith1.product([t for (t, e) in modpfactors])
    quot_p = theminpoly_p.exact_division(mini_p)
    mini = _min_abs_poly(mini_p)
    quot = _min_abs_poly(quot_p)
    minpoly = uniutil.polynomial(enumerate(minpoly_coeff), Z)
    f_p = _mod_p((mini * quot - minpoly).scalar_exact_division(p), p)
    gcd = f_p.getRing().gcd
    common_p = gcd(gcd(mini_p, quot_p), f_p) # called Z
    uniq_p = theminpoly_p // common_p
    uniq = _min_abs_poly(uniq_p)

    return common_p.degree(), uniq

def _mod_p(poly, p):
    """
    Return modulo p reduction of given integer coefficient polynomial.
    """
    coeff = {}
    for d, c in poly:
        coeff[d] = finitefield.FinitePrimeFieldElement(c, p)
    return uniutil.polynomial(poly, finitefield.FinitePrimeField.getInstance(p))

def _min_abs_poly(poly_p):
    """
    Return minimal absolute mapping of given F_p coefficient polynomial.
    """
    coeff = {}
    p = poly_p.getCoefficientRing().char
    for d, c in poly_p:
        coeff[d] = _pull_back(c, p)
    return uniutil.polynomial(coeff, Z)

def _coeff_list(upoly, size):
    """
    Return a list of given size consisting of coefficients of upoly
    and possibly zeros padded.
    """
    return [upoly[i] for i in range(size)]

def _pull_back(elem, p):
    """
    Return an integer which is a pull back of elem in Fp.
    """
    if not isinstance(elem, finitefield.FinitePrimeFieldElement):
        if isinstance(elem, integerresidueclass.IntegerResidueClass):
            # expecting Z/(p^2 Z)
            result = finitefield.FinitePrimeFieldElement(elem.n, p).n
        else:
            # expecting Z or Q
            result = finitefield.FinitePrimeFieldElement(elem, p).n
    else:
        result = elem.n
    if result > p // 2: # minimum absolute
        result -= p
    return result

def _normalize_int(elem):
    """
    Return integer object, which is equal to given elem, whose type is
    either integer or rational number.
    """
    if isinstance(elem, (int, long)):
        return elem
    elif elem.denominator == 1:
        return elem.numerator
    else:
        raise ValueError("non integer: %s" % str(elem))

def _default_omega(degree):
    """
    Return the default omega
    """
    # omega is initialized to basis of Z[theta]
    return ModuleWithDenominator([_standard_base(degree, i) for i in range(degree)], 1)

def _standard_base(degree, i):
    """
    Return i-th standard unit base
    """
    base = [0] * degree
    base[i] = 1
    return base

def _rational_polynomial(coeffs):
    """
    Return rational polynomial with given coefficients in ascending
    order.
    """
    return uniutil.polynomial(enumerate(coeffs), Q)


class ModuleWithDenominator (object):
    """
    Represent basis of Z-module with denominator
    """
    def __init__(self, basis, denominator, **hints):
        """
        basis is a list of integer sequences.
        denominator is a common denominator of all bases.

        Example:
        ModuleWithDenominator([[1, 2], [4, 6]], 2) represents a module
        <[1/2, 1], [2, 3]>.
        """
        self.basis = basis
        self.denominator = denominator
        self.rank = len(self.basis)
        if self.rank:
            self.dimension = len(self.basis[0])
        else:
            self.dimension = hints['dimension']
        self.rational_basis = None
        self.poly_basis = None

    def get_rationals(self):
        """
        Return a list of rational list, which is basis divided by
        denominator.
        """
        if self.rational_basis is None:
            self.rational_basis = []
            for base in self.basis:
                self.rational_basis.append([rational.Rational(c, self.denominator) for c in base])
        return self.rational_basis

    def get_polynomials(self):
        """
        Return a list of rational polynomials, which is made from basis
        divided by denominator.
        """
        if self.poly_basis is None:
            self.poly_basis = []
            for base in self.basis:
                self.poly_basis.append(_rational_polynomial([rational.Rational(c, self.denominator) for c in base]))

        return self.poly_basis

    def __add__(self, other):
        """
        Return sum of two modules.
        """
        denominator = gcd.lcm(self.denominator, other.denominator)
        row = self.dimension
        assert row == other.dimension
        column = self.rank + other.rank
        mat = matrix.createMatrix(row, column)
        adjust = denominator // self.denominator
        for i, base in enumerate(self.basis):
            mat.setColumn(i + 1, [c * adjust for c in base])
        adjust = denominator // other.denominator
        for i, base in enumerate(other.basis):
            mat.setColumn(self.rank + i + 1, [c * adjust for c in base])

        # Hermite normal form
        hnf = mat.hermiteNormalForm()
        # The hnf returned by the hermiteNormalForm method may have columns
        # of zeros, and they are not needed.
        zerovec = vector.Vector([0] * hnf.row)
        while hnf.row < hnf.column or hnf[1] == zerovec:
            hnf.deleteColumn(1)

        omega = []
        for j in range(1, hnf.column + 1):
            omega.append(list(hnf[j]))
        return ModuleWithDenominator(omega, denominator)

    def __mul__(self, scale):
        """
        scalar multiplication.
        """
        if not (self.denominator % scale):
            return ModuleWithDenominator(self.basis, self.denominator // scale)
        else:
            muled = [[c * scale for c in base] for base in self.basis]
            return ModuleWithDenominator(muled, self.denominator)

    __rmul__ = __mul__

    def __truediv__(self, divisor):
        return ModuleWithDenominator(self.basis, self.denominator * divisor)

    def determinant(self):
        """
        Return determinant of the basis (basis ought to be of full
        rank and in Hermite normal form).
        """
        return arith1.product([rational.Rational(self.basis[i][i], self.denominator) for i in range(self.rank)])

    def linear_combination(self, coefficients):
        """
        Return a list corresponding a linear combination of basis with
        given coefficients.  The denominator is ignored.
        """
        new_basis = [0] * self.dimension
        for c, base in zip(coefficients, self.basis):
            for i in range(self.dimension):
                new_basis[i] += c * base[i]
        return new_basis
