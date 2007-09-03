"""
Combinatorial functions
"""

import itertools
from nzmath.rational import Integer, Rational


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
        raise TypeError("integer is expected, %s detected." % n.__class__)
    if not isinstance(m, (int, long)):
        raise TypeError("integer is expected, %s detected." % m.__class__)
    if n == m >= 0 or m == 0 and n > 0:
        return 1
    if n <= 0:
        raise ValueError("non-positive number: %d" % n)
    if m < 0:
        raise ValueError("negative number: %d" % m)
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
        raise TypeError("integer is expected, %s detected." % n.__class__)
    elif n < 0:
        raise ValueError("argument must not be a negative integer.")
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

def combinationIndexGenerator(n, m):
    """
    Generate indeces of m elment subsets of n element set.

    For example:
    >>> for idx in combinationIndexGenerator(5,3):
    ...     print idx
    ...
    [0, 1, 2]
    [0, 1, 3]
    [0, 1, 4]
    [0, 2, 3]
    [0, 2, 4]
    [0, 3, 4]
    [1, 2, 3]
    [1, 2, 4]
    [1, 3, 4]
    [2, 3, 4]
    >>>
    """
    assert n >= m > 0
    idx = range(m)
    while True:
        yield idx
        for i in range(1, m+1):
            if idx[-i] != n-i:
                idx[-i] += 1
                for j in range(i-1, 0, -1):
                    idx[-j] = idx[-j-1] + 1
                break
        else:
            raise StopIteration

def fallingfactorial(n, m):
    """
    Return the falling factorial; n to the m falling, i.e. n(n-1)..(n-m+1).

    For Example:
    >>> fallingfactorial(7, 3)
    210
    """
    r = 1
    for i in range(n, n-m, -1):
        r *= i
    return r

def risingfactorial(n, m):
    """
    Return the rising factorial; n to the m rising, i.e. n(n+1)..(n+m-1).

    For example:
    >>> risingfactorial(7, 3)
    504
    """
    r = 1
    for i in range(n, n+m):
        r *= i
    return r

def multinomial(n, parts):
    """
    Return multinomial coefficient.

    parts MUST be a sequence of natural numbers and n==sum(parts) holds.
    """
    if n != sum(parts):
        raise ValueError("sum of parts must be equal to n.")
    for part in parts:
        if not isinstance(part, (int, long)) or part < 0:
            raise ValueError("parts must be a sequence of natural numbers.")
    # binomial case
    if len(parts) == 2:
        return binomial(n, parts[0])
    # other cases
    result = factorial(n)
    for part in parts:
        if part >= 2: # 0! = 1! = 1 are negligible
            result //= factorial(part)
    return result

def stirling1(n, m):
    """
    Stirling number of the first kind.

    Let s denote the Stirling number, (x)_n falling factorial, then
      (x)_n = \sum_{i=0}^{n} s(n, i) * x**i
    and s satisfies the recurrence relation:
      s(n, m) = s(n-1, m-1) - (n-1)*S(n-1, m)
    """
    if n == m:
        return 1
    elif n < m or n*m < 0:
        return 0
    elif m == 0:
        return 0
    elif m == 1:
        if n % 2:
            sign = 1
        else:
            sign = -1
        return sign * factorial(n - 1)
    elif m == n - 1:
        return -binomial(n, 2)
    else:
        # recursively calculate by s(n, m) = s(n-1, m-1) - (n-1)*S(n-1, m)
        slist = (1,) # S(1, 1) = 1
        for i in range(1, n):
            l, u = max(1, m - n + i + 1), min(i + 2, m + 1)
            if l == 1 and len(slist) < n - l:
                nlist = [-i * slist[0]]
            else:
                nlist = []
            for j in range(len(slist) - 1):
                nlist.append(slist[j] - i * slist[j + 1])
            if len(slist) <= u - l:
                nlist.append(slist[-1])
            slist = tuple(nlist)
        return slist[0]

def stirling2(n, m):
    """
    Stirling number of the second kind.

    Let S denote the Stirling number, (x)_i falling factorial, then:
      x**n = \sum_{i=0}^{n} S(n, i) * (x)_i
    S satisfies:
      S(n, m) = S(n-1, m-1) + m*S(n-1, m)
    """
    if n == m:
        return 1
    elif n < m or n * m <= 0:
        return 0
    elif n < 0:
        return stirling2_negative(-m, -n)
    elif m == 1:
        return 1
    elif m == 2:
        return 2**(n - 1) - 1
    elif m == n - 1:
        return n * m // 2
    else:
        r = 0
        b = m
        l = 1
        while 1:
            if l & 1:
                r -= b * l**n
            else:
                r += b * l**n
            if l == m:
                break
            b = (b * (m - l)) // (l + 1)
            l += 1
        if m & 1:
            r = -r
        return r // factorial(m)

def stirling2_negative(n, m):
    """
    Stiring number of the second kind extended to negative numbers.

    Let S# denote the extended Stirling number, S the original, then
    S#(n, m) = S(-m, -n) and extended by the recurrence relation:
      S#(n, m) = S#(n-1, m-1) + (n-1)*S#(n-1, m)
    """
    if n == m:
        return 1
    elif n < m or n * m <= 0:
        return 0
    elif n < 0:
        return stirling2(-m, -n)
    elif m == 1:
        return factorial(n - 1)
    else: # return S(n-1,m-1)+(n-1)*S(n-1,m)
        slist = [1]
        i = 1
        while i < n:
            l, u = max(1, m - n + i + 1), min(i + 2, m + 1)
            if len(slist) < u - l:
                nlist = [i * slist[0]]
            else:
                nlist = []
            for j in range(len(slist) - 1):
                nlist.append(slist[j] + i * slist[j + 1])
            if len(slist) <= u - l:
                nlist.append(slist[-1])
            slist = nlist
            i += 1
        return slist[-1]

def bell(n):
    """
    Bell number.

    The Bell number b is defined by:
      b(n) = \sum_{i=0}^{n} S(n, i)
    where S denotes Stirling number of the second kind.
    """
    return sum([stirling2(n, i) for i in range(n + 1)])

def partitionGenerator(n, maxi=None):
    """
    Generate partitions of n.
    If maxi is given, then addends are limited to at most maxi.
    """
    if maxi is None or maxi > n:
        maxi = n
    partition = [maxi]
    rest = n - maxi
    while True:
        key = partition[-1]
        q, r = divmod(rest, key)
        if q:
            partition.extend([key] * q)
        if r:
            partition.append(r)
        rest = 0

        yield tuple(partition)

        try:
            # wind up all 1's.
            first_one = partition.index(1)
            rest = len(partition) - first_one
            del partition[first_one:]
            level = first_one -1
        except ValueError:
            # 1 is not found
            level = len(partition) - 1
        if level >= 0:
            partition[level] -= 1
            rest += 1
        else:
            # partition==[1]*n: it means all partitions have been generated.
            raise StopIteration

def _pentagonal():
    """
    Generates pentagonal and skew pentagonal numbers.
    (1, 2, 5, 7, 12, 15, ...)
    """
    j = 1
    while True:
        yield j*(3*j - 1)//2
        yield j*(3*j + 1)//2
        j += 1

def partition_numbers_upto(n):
    """
    Return the partition numbers for 0 to '''n''' (inclusive).
    """
    penta = list(itertools.izip(
        itertools.takewhile(lambda k: k <= n, _pentagonal()),
        itertools.cycle((1, 1, -1, -1))))                 
    p = [1]
    for i in range(1, n + 1):
        s = 0
        for k, sign in penta:
            if k > i:
                break
            s += sign * p[i - k]
        p.append(s)
    return p

def partition_number(n):
    """
    Return the partition number for '''n'''.
    """
    return partition_numbers_upto(n)[-1]
