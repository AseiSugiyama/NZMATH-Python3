"""
Power Detection

perfect_power_detection:
   Given a positive integer n (>=2), returm a pair of integers (m, k) such
   that n == m**k where k is not 1 if n is a perfect power.


REFERENCE:
* Bernstein, Daniel J., Detecting Perfect Powers in Essentially Linear Time.
  Math. Comp. 67(223) pp 1253--1283, 1998.
"""

import nzmath.arith1 as arith1
import nzmath.prime as prime


def perfect_power_detection(n):
    """
    Return (m, k) if n = m**k.

    Note that k is the smallest possible and m still can be a perfect
    power; if n is not a perfect power, it returns (n, 1).
    """
    f = arith1.log(n) + 1
    y = DyadicRational(0, n).nroot(1, 3 + (f - 1) // 2 + 1)
    for p in prime.generator_eratosthenes(f):
        x = _is_kth_power(n, p, y, f)
        if x != 0:
            return (x, p)
    return (n, 1)

def _is_kth_power(n, k, y, f):
    """
    Return kth power root of n iff n is a kth power, 0 otherwise.

    y is a precomputed approximation of inverse of n; it is a
    DyadicRational instance.
    f = floor(lg(2*n)).
    """
    # b = 3 + ceil(f / k)
    b = 3 + (f - 1) // k + 1

    r = y.nroot(k, b)
    x = int(r)
    rint = DyadicRational(0, x)
    five_eighth = DyadicRational(-3, 5)
    assert r >= rint
    diffr = r.sub(rint)
    if diffr > five_eighth:
        rint += DyadicRational(0, 1)
        x += 1
        assert r <= rint and rint.sub(r) <= five_eighth
        diffr = rint.sub(r)

    if rint.abscissa == 0 or DyadicRational(-2, 1) <= diffr:
        return 0

    return 0 if _power_sign(n, x, k, f) else x


def _power_sign(n, x, k, f):
    """
    Return the sign of n - x**k.  All of n, x, and k are positive
    integers.
    """
    lg8k = arith1.log(k) + 3
    if 2 ** lg8k < 8 * k:
        lg8k += 1
    bound = 1
    drn = DyadicRational(0, n)

    while True:
        r = DyadicRational(0, x).power(k, bound + lg8k)
        if drn < r:
            return -1
        elif r * (DyadicRational(0, 1) + DyadicRational(-bound, 1)) <= drn:
            return 1
        elif bound >= f:
            return 0
        bound = min(2 * bound, f)


class DyadicRational(object):
    """
    Just like floating point numbers, a dyadic rational number is a pair
    (a, n) which represents 2**a * n, where a is an integer and n is a
    positive integer.
    """
    def __init__(self, exponent, abscissa):
        self.exponent = exponent
        self.abscissa = abscissa
        if self.abscissa:
            while not (self.abscissa & 1):
                self.exponent += 1
                self.abscissa >>= 1
        # f - 1 <= lg abscissa < f
        self.log_absc = arith1.log(self.abscissa)
        if 2 ** self.log_absc <= self.abscissa:
            self.log_absc += 1

    def __int__(self):
        """
        Return the integer part of a dyadic rational.
        If exponent is negative, some information will be lost.
        """
        if self.exponent < 0:
            return self.abscissa >> (-self.exponent)
        return self.abscissa << self.exponent

    def __lt__(self, other):
        if self.exponent < other.exponent:
            exponent = other.exponent - self.exponent
            return self.abscissa < (other.abscissa << exponent)
        elif self.exponent > other.exponent:
            exponent = self.exponent - other.exponent
            return (self.abscissa << exponent) < other.abscissa
        else:
            return self.abscissa < other.abscissa

    def __le__(self, other):
        if self.exponent < other.exponent:
            exponent = other.exponent - self.exponent
            return self.abscissa <= (other.abscissa << exponent)
        elif self.exponent > other.exponent:
            exponent = self.exponent - other.exponent
            return (self.abscissa << exponent) <= other.abscissa
        else:
            return self.abscissa <= other.abscissa

    def __gt__(self, other):
        if self.exponent < other.exponent:
            exponent = other.exponent - self.exponent
            return self.abscissa > (other.abscissa << exponent)
        elif self.exponent > other.exponent:
            exponent = self.exponent - other.exponent
            return (self.abscissa << exponent) > other.abscissa
        else:
            return self.abscissa > other.abscissa

    def __add__(self, other):
        """
        Add two dyadic rationals and return the result.
        """
        min_expo = min(self.exponent, other.exponent)
        return DyadicRational(min_expo,
                              (self.abscissa << self.exponent - min_expo) +
                              (other.abscissa << other.exponent - min_expo))

    def sub(self, other):
        """
        Subtract a dyadic rational from another dyadic rational and
        return the result.  If the subtractee is less than subtracter
        then raise ValueError.
        """
        if self < other:
            raise ValueError("subtraction a - b is defined only for a >= b")
        min_expo = min(self.exponent, other.exponent)
        return DyadicRational(min_expo,
                              (self.abscissa << self.exponent - min_expo) -
                              (other.abscissa << other.exponent - min_expo))

    def div(self, divisor, bits):
        """
        Divide a dyadic rational by a positive integer divisor within
        precision bits and return the result.
        """
        # lgd - 1 < lg divisor <= lgd
        lgd = arith1.log(divisor)
        if 2 ** lgd < divisor:
            lgd += 1
        offset = self.log_absc - lgd - bits
        if offset < 0:
            abscissa = (self.abscissa << -offset) // divisor
        else:
            abscissa = self.abscissa // (divisor << offset)
        return DyadicRational(self.exponent + offset, abscissa)

    def trunc(self, bits):
        """
        Truncate a dyadic rational within precision bits and return
        the result.
        """
        return self.div(1, bits)

    def mul(self, multiplier):
        """
        Multiply a dyadic rational by an integer multiplier and return
        the result.
        """
        return DyadicRational(self.exponent, self.abscissa * multiplier)

    def __mul__(self, other):
        """
        Multiply two dyadic rationals and return the result.
        """
        return DyadicRational(self.exponent + other.exponent,
                              self.abscissa * other.abscissa)

    def power(self, index, bits):
        """
        Return a dyadic rational to the index-th power, approximated to
        bits.
        """
        if index == 1:
            return self.trunc(bits)
        if index & 1:
            pred = self.power(index - 1, bits)
            return (pred * self.trunc(bits)).trunc(bits)
        else:
            half = self.power(index // 2, bits)
            return (half * half).trunc(bits)

    def nrootb(self, index, bits):
        """
        Approximately compute the inverse of index-th root and return it.

        b stands for binary search. It should be used for:
          1 <= bits <= ceil(lg(8 * index))
        """
        # lgy - 1 < lg self <= lgy
        lgy = arith1.log(self.abscissa) + self.exponent
        if DyadicRational(lgy, 1) < self:
            lgy += 1
        assert DyadicRational(lgy - 1, 1) < self <= DyadicRational(lgy, 1)
        lgr = -lgy // index
        ebound = 66 * (2 * index + 1)
        bound = arith1.log(ebound)
        if 2 ** bound < ebound:
            bound += 1
        rbound = DyadicRational(-10, 993)
        one = DyadicRational(0, 1)

        z = DyadicRational(lgr, 1) + DyadicRational(lgr - 1, 1)
        for j in range(1, bits):
            r = (z.power(index, bound) * self.trunc(bound)).trunc(bound)
            if r <= rbound:
                z += DyadicRational(lgr - j - 1, 1)
            if r > one:
                z = z.sub(DyadicRational(lgr - j - 1, 1))

        return z

    def nrootn(self, index, bits):
        """
        Approximately compute the inverse of index-th root and return it.

        n stands for Newton's method. It should be used for:
          bits > ceil(lg(8 * index))
        """
        lgk = arith1.log(index)
        if 2 ** lgk < index:
            lgk += 1
        lg2k = lgk + 1
        lg8k = lgk + 3
        smallbits = lg2k + (bits - lg2k - 1) // 2 + 1
        bound = 2 * smallbits + 4 - lgk

        if smallbits <= lg8k:
            z = self.nrootb(index, smallbits)
        else:
            z = self.nrootn(index, smallbits)

        r2 = z.trunc(bound).mul(index + 1)
        r3 = (z.power(index + 1, bound) * self.trunc(bound)).trunc(bound)
        r4 = r2.sub(r3).div(index, bound)
        return r4

    def nroot(self, index, bits):
        lg8k = arith1.log(8 * index)
        if 2 ** lg8k < 8 * index:
            lg8k += 1

        if bits <= lg8k:
            return self.nrootb(index, bits)
        else:
            return self.nrootn(index, bits)
