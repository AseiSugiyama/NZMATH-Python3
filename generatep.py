#generatep.py
import primeq

def generate_over(a):
    """Return the smallest prime number which is over your input integer."""
    if a <= 2:
        return 2
    elif a % 2 == 0:
        a = a + 1
    while primeq.primeQ(a) == 0:
        a = a + 2
    return a

def generate_mod(a,b,c):
    """Return P which belongs prime numbers over a.
And mod(P,b) = c."""
    while a % b != c:
        a = a + 1
    while primeq.primeQ(a) == 0:
        a = a + b
    return a