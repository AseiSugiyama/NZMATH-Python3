def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def extgcd(x,y):    # Crandall & Pomerance "PRIME NUMBERS", Algorithm 2.1.4
    x,y = abs(x),abs(y)
    a,b,g,u,v,w = 1,0,x,0,1,y
    while w > 0:
        q = g // w
        a,b,g,u,v,w = u,v,w,a-q*u,b-q*v,g-q*w

    return (a,b,g)

def gcd_of_list(integers):
    the_gcd = 0
    coeff = []
    for next in integers:
        t = extgcd(the_gcd, next)
        the_gcd = t[0]
        for i in range(len(coeff)):
            coeff[i] *= t[1][0]
        coeff += [t[1][1]]
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
