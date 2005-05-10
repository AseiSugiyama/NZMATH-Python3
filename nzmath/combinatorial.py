"""

Combinatorial functions

"""

from rational import Integer, Rational

def binomial(n, m):
    """

    The binomial coefficient.
    binomial(n, m) returns n ! / ((n - m) ! * m !).

    n must be a positive integer and m must be a non-negative integer.
    For convinience, binomial(n, n+i) = 0 for positive i, and
    binomial(0,0) = 1.

    In other cases, it raises an exception.

    """
    if not isinstance(n, (int, long)):
        raise TypeError, "integer is expected, %s detected." % n.__class__
    if not isinstance(m, (int, long)):
        raise TypeError, "integer is expected, %s detected." % m.__class__
    if n == m or m == 0:
        return 1
    if n <= 0:
        raise ValueError, "non-positive number: %d" % n
    if m < 0:
        raise ValueError, "negative number: %d" % m
    if n < m:
        return 0
    if m*2 > n:
        m = n - m
    retval = n
    for i in range(1, m):
        retval *= (n - i)
        retval /= (i + 1)
    return Integer(retval)

def factorial(n):
    """

    Return n! for non negative integer n.

    """
    if not isinstance(n, (int, long)):
        raise TypeError, "integer is expected, %s detected." % n.__class__
    elif n < 0:
        raise ValueError, "argument must not be a negative integer."
    elif n == 0 or n == 1:
        return Integer(1)
    l = range(1, n+1)
    while len(l) > 1:
        for i in range(len(l)//2):
            l[i] *= l.pop()
    return Integer(l.pop())

def bernoulli(n):
    """

    Return n-th Bernoulli number.

    """
    if n != 1 and n & 1:
        return 0
    B = {0:Integer(1),
         1:Rational(-1, 2)}
    for i in range(2, n+1, 2):
        a = B[0] + (i+1)*B[1]
        for j in range(2, i, 2):
            a += binomial(i+1, j) * B[j]
        B[i] = -a / (i+1)
    return B[n]

def catalan(n):
    """

    Return n-th Catalan number.

    """
    return binomial(2*n, n) // (n+1)
