"""
pseudoprime

Pseudoprime is a composite which satisfies some properties all primes
satisfy.  A predicate on integer characterizing such a property is
called pseudoprimality test, and an integer the predicate returns True
is called probable prime.  Thus, a probable prime can be either prime
or composite.  It is, however, true that those predicates may give
precise "erro probability"; therefore an integer mapped to True by
the predicate is "probably" a prime.
"""

import nzmath.arith1 as arith1
import nzmath.bigrandom as bigrandom
import nzmath.gcd as gcd


def spsp(n, base, s=None, t=None):
    """
    Strong PSeudo-Prime test.
    A composite can pass this test with probability at most 1/4.

    Optional third and fourth argument s and t are the numbers such
    that n-1 = 2**s * t and t is odd.
    """
    nminus1 = n - 1
    if s is None or t is None:
        s, t = arith1.vp(nminus1, 2)
    z = pow(base, t, n)
    if z != 1 and z != nminus1:
        j = 0
        while j < s:
            j += 1
            z = pow(z, 2, n)
            if z == nminus1:
                break
        else:
            return False
    return True


def miller_rabin(n, times=20):
    """
    Miller-Rabin pseudo-primality test.
    The error probability is at most 4**(-times).

    Optional second argument times (default to 20) is the number of
    repetition.  The testee 'n' is required to be much bigger than
    'times'.
    """
    nminus1 = n - 1
    s, t = arith1.vp(nminus1, 2)
    randrange = bigrandom.randrange
    return all(spsp(n, randrange(i + 2, nminus1), s, t) for i in range(times))


def _lucas_chain(n, f, g, x_0, x_1):
    """
    Given an integer n, two functions f and g, and initial value (x_0, x_1),
    compute (x_n, x_{n+1}), where the sequence {x_i} is defined as:
      x_{2i} = f(x_i)
      x_{2i+1} = g(x_i, x_{i+1})
    """
    binary = arith1.expand(n, 2)
    u = x_0
    v = x_1
    while binary:
        if 1 == binary.pop():
            u, v = g(u, v), f(v)
        else:
            u, v = f(u), g(u, v)
    return u, v


def _lucas_test_sequence(n, a, b):
    """
    Return x_0, x_1, x_m, x_{m+1} of Lucas sequence of parameter a, b,
    where m = (n - (a**2 - 4*b / n)) // 2.
    """
    d = a**2 - 4*b
    if (d >= 0 and arith1.issquare(d)
        or not(gcd.coprime(n, 2*a*b*d))):
        raise ValueError("Choose another parameters.")

    x_0 = 2
    inv_b = arith1.inverse(b, n)
    x_1 = ((a ** 2) * inv_b - 2) % n

    # Chain functions
    def even_step(u):
        """
        'double' u.
        """
        return (u**2 - x_0) % n

    def odd_step(u, v):
        """
        'add' u and v.
        """
        return (u*v - x_1) % n

    m = (n - arith1.legendre(d, n)) // 2
    x_m, x_mplus1 = _lucas_chain(m, even_step, odd_step, x_0, x_1)

    return x_0, x_1, x_m, x_mplus1


def lpsp(n, a, b):
    """
    Lucas test.
    Return True if n is a Lucas pseudoprime of parameters a, b,
    i.e. with respect to x**2-a*x+b.
    """
    x_0, x_1, x_m, x_mplus1 = _lucas_test_sequence(n, a, b)

    return (x_1 * x_m - x_0 * x_mplus1) % n == 0


def fpsp(n, a, b):
    """
    Frobenius test.
    Return True if n is a Frobenius pseudoprime of parameters a, b,
    i.e. with respect to x**2-a*x+b.
    """
    x_0, x_1, x_m, x_mplus1 = _lucas_test_sequence(n, a, b)

    if (x_1 * x_m - x_0 * x_mplus1) % n == 0:
        euler_pow = pow(b, (n-1)//2, n)
        return (euler_pow * x_m) % n == 2
    else:
        return False


# utilities 

def next_probable_prime(n, times=20):
    """
    Return the smallest probable prime bigger than the given integer.
    n ought to be greater than, say, 1000.  There is no penalty to use
    prime.nextPrime(n) for n less than 10**12.

    This implementation uses miller_rabin to determine the
    pseudoprimality, and 'times' parameter can be specified.
    """
    n += (1 + (n & 1)) # make n be odd.
    while not gcd.coprime(n, 510510) or not miller_rabin(n, times):
        n += 2
    return n


def rand_probable_prime(minimum, maximum, times=20):
    """
    Return a random probable prime in range(minimum, maximum)
    """
    p = next_probable_prime(bigrandom.randrange(minimum, maximum), times)
    if p < maximum:
        return p

    # in very rare case or n is too small case,
    # search continues from the lower bound.
    return next_probable_prime(minimum, times)
