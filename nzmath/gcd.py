def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def binarygcd(a, b):
    if a < b:
        tmp = a
        a = b
        b =tmp
    if b == 0:
        return a
    r = a % b
    a = b
    b = r
    if b == 0:
        return a
    k = 0
    while not a & 1 and not b & 1:
        k = k + 1
        a = a / 2
        b = b / 2
    while not a & 1:
        a = a / 2
    while not b & 1:
        b = b / 2
    t = (a - b) / 2
    while t != 0:
        while not t & 1:
            t = t / 2
        if t > 0:
            a = t
        else:
            b = -t
        t = (a - b)/2
    return (2**k)*a

def extgcd(x,y):    # Crandall & Pomerance "PRIME NUMBERS", Algorithm 2.1.4
    a,b,g,u,v,w = 1,0,abs(x),0,1,abs(y)
    while w > 0:
        q = g // w
        a,b,g,u,v,w = u,v,w,a-q*u,b-q*v,g-q*w

    return (a,b,g)

def gcd_of_list(integers):
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

if __name__ == "__main__":
    doc = """calculate the G.C.D. of some integers
usage: gcd integer1 integer2 [integer3 ...]"""

    import sys
    if len(sys.argv) < 3:
        print doc
        sys.exit()
    integers = []
    for i in sys.argv[1:]:
        integers += [int(i)]
    print gcd_of_list(integers)
