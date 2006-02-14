"""
funtions related to the greatest common divisor of integers.
"""

def gcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b.
    """
    while b:
        a, b = b, a % b
    return a

def binarygcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b
    by binary gcd algorithm.
    """
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    a, b = b, a % b
    if b == 0:
        return a
    k = 0
    while not a & 1 and not b & 1:
        k += 1
        a >>= 1
        b >>= 1
    while not a & 1:
        a >>= 1
    while not b & 1:
        b >>= 1
    t = (a - b) >> 1
    while t:
        while not t & 1:
            t >>= 1
        if t > 0:
            a = t
        else:
            b = -t
        t = (a - b) >> 1
    return a << k

def extgcd(x, y):
    """
    Return a tuple (u, v, d); they are the greatest common divisor d
    of two integers x and y and u, v such that d = x * u + y * v.
    """
    # Crandall & Pomerance "PRIME NUMBERS", Algorithm 2.1.4
    a, b, g, u, v, w = 1, 0, abs(x), 0, 1, abs(y)
    while w > 0:
        q = g // w
        a, b, g, u, v, w = u, v, w, a-q*u, b-q*v, g-q*w
    return (a, b, g)

def gcd_of_list(integers):
    """
    Return a list [d, [c1, ..., cn]] for a list of integers [x1, ..., xn]
    such that d = c1 * x1 + ... + cn * xn.
    """
    the_gcd = 0
    total_length = len(integers)
    coeffs = []
    coeffs_length = 0
    for integer in integers:
        multiplier, new_coeff, the_gcd = extgcd(the_gcd, integer)
        if multiplier != 1:
            for i in range(coeffs_length):
                coeffs[i] *= multiplier
        coeffs.append(new_coeff)
        coeffs_length += 1
        if the_gcd == 1:
            coeffs.extend([0] * (total_length - coeffs_length))
            break
    return [the_gcd, coeffs]

def lcm(a, b):
    """
    lcm returns the lowest common multiple of given 2 integers.
    If both are zero, it raises an exception.
    """
    return a // gcd(a, b) * b

def coprime(a, b):
    """
    Return True if a and b are coprime, False otherwise.

    For Example:
    >>> coprime(8, 5)
    True
    >>> coprime(-15, -27)
    False
    >>>
    """
    return abs(gcd(a, b)) == 1

def pairwise_coprime(int_list):
    """
    Return True if all integers in int_list are pairwise coprime,
    False otherwise.

    For example:
    >>> pairwise_coprime([1, 2, 3])
    True
    >>> pairwise_coprime([1, 2, 3, 4])
    False
    >>>
    """
    int_iter = iter(int_list)
    product = int_iter.next()
    for n in int_iter:
        if not coprime(product, n):
            return False
        product *= n
    return True
