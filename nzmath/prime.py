#prime.py
import string
import bigrandom
boundary_p = 20000000000

def primeq(z):
    """Judge the integer which you input.
return 1 if the integer belongs prime numbers.
return 0 in the case of others."""
    import math
    import prime
    if long(z) != z:
        raise ValueError, "non-integer for primeq()"
    elif z <= 1:
        return 0
    elif z == 2:
        return 1
#    elif z >= boundary_p:
#        return prime.bigprimeq(z)
    else:
        f_1 = open("primes.txt","r")
        line=f_1.readline()
        v = 2
        while line:
            x=string.split(line)
            if z % long(x[0]) == 0:
                return 0
                break
            elif long(x[0])**2 > z:
                return 1
                break
            line=f_1.readline()
        f_1.close()
        if v == 2:
            prime.produce(long(math.sqrt(2*z)))
        return prime.primeq(z)

def produce(n):
    """Produce prime numbers to the integer which you input."""
    if n != long(n):
        raise ValueError, "non-integer for produce()"
    import prime
    f_2 = open("primes.txt","r")
    line=f_2.readline()
    while line:
        x=string.split(line)
        max = long(x[0])
        line=f_2.readline()
    f_2.close()
    p = max + 2
    while p < n+1:
        while prime.primeq(p) == 0:
            p += 2 
        f_3 = open("primes.txt","r")
        plist = f_3.readlines()
        plist.append(str(p))
        plist.append("\n")
        f_3.close()
        f_3 = open("primes.txt","w")
        f_3.writelines(plist)
        f_3.close()
        p += 2

def prime(s):
    """Return the prime number in the number which you input."""
    import prime
    import math
    if s != long(s):
        raise ValueError, "non-integer for prime()"
    elif s <= 0:
        raise ValueError, "non-positive-integer for prime()" 
    f_4 = open("primes.txt","r")
    line = f_4.readline()
    i=0
    t=0
    while i+1 != s:
        i += 1
        line = f_4.readline()
        if not line:
            t = 1
            break
    f_4.close() 
    if t == 1:
        prime.produce(s*(long(math.log(s)/math.log(2))))
        return prime.prime(s)
    else:
        return long(line[:-1])

def bigprimeq(n):
    """Judge the integer which you input.
return 1 if the integer belongs prime numbers.
return 0 in the case of others."""
    import bigrandom
    times_of_test = 20
    if n != long(n):
        raise ValueError, "non-integer for bigprimeq()"
    elif n < 0:
        return 0
    elif n == 2:
        return 1
    elif n == 1:
        return 0
    elif n % 2 == 0:
        return 0
    else :
        s = 0
        t = n-1
        while t % 2 == 0:
            t = t / 2
            s=s+1
        for i in range(times_of_test):
            b = bigrandom.randrange(1,n-1)
            if pow(b,t,n) != 1 and pow(b,t,n) !=  n-1:
                j = 0
                z = pow(b,t,n)
                while j < s+1:
                    j=j+1
                    z = pow(z,2,n)
                    if z == n-1:
                        break
                else:
                    return 0
        return 1

          