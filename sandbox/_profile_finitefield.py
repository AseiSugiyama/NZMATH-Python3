import profile
from sandbox.finitefield import *
F=FiniteExtendedField(3, FinitePrimeFieldPolynomial([(0, FinitePrimeFieldElement(2, 3)), (1, FinitePrimeFieldElement(1, 3)), (2, FinitePrimeFieldElement(1, 3))], FinitePrimeField(3)))
XX=F.createElement(4)
def test(X):
    i=0
    while i<10:
        N=X**65536
        i=i+1
    return N

def test2(X):
    i = 0
    while i<10:
        j = 0
        N = X
        while j<16:
            N = N * N
            j = j+1
        i= i+1
    return N

print test2(XX) == test(XX)
profile.run("test(XX)")
profile.run("test2(XX)")