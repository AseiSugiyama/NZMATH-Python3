def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
 
def extgcd(a, b):
    from matrix import Matrix
    tmp = Matrix(2,2)
    tmp.set([1,0,0,1])
    q = []
    while b:
        q += [a/b]
        a,b = b, a%b
    m = Matrix(2,2)
    for i in range(len(q)):
        m.set([0,1,1,-q[i]])
        tmp = m * tmp
    return [a, [tmp.compo[0][0], tmp.compo[0][1]]]

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
