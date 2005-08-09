def gcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b.
    """
    while b:
        a, b = b, a%b
    return a

def binarygcd(a, b):
    """
    Return the greatest common divisor of 2 integers a and b
    by binary gcd algorithm.
    """
    if a < b:
        tmp = a
        a = b
        b =tmp
    if b == 0:
        return a
    tmp = a % b
    a = b
    b = tmp
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
    a,b,g,u,v,w = 1,0,abs(x),0,1,abs(y)
    while w > 0:
        q = g // w
        a,b,g,u,v,w = u,v,w,a-q*u,b-q*v,g-q*w

    return (a,b,g)

def gcd_of_list(integers):
    """
    Return a list [d, [c1, ..., cn]] for a list of integers [x1, ..., xn]
    such that d = c1 * x1 + ... + cn * xn.
    """
    the_gcd = 0
    coeff = []
    for next in integers:
        t = extgcd(the_gcd, next)
        for i in range(len(coeff)):
            coeff[i] *= t[0]
        coeff.append(t[1])
        the_gcd = t[2]
    return [the_gcd, coeff]

def lcm(a, b):
    """

    lcm returns the lowest common multiple of given 2 integers.
    If both are zero, it raises an exception.

    """
    return a // gcd(a, b) * b 
