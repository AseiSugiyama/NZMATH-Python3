#prime.py
boundary_p = 4000000000000

def primeq(z):
    """Judge the integer which you input.
return 1 if the integer belongs prime numbers.
return 0 in the case of others."""
    import math
    if long(z) != z:
        raise ValueError, "non-integer for primeq()"
    elif z <= 1:
        return 0
    elif z == 2:
        return 1
#    elif z >= boundary_p:
#        return bigprimeq(z)
#        return isprimeq(z)
    else:
        primes = open("primes.txt","r")
#        line=primes.readlines() 
        line=primes.readline()
#        for i in line:
#            if z % long(i) == 0:
#                return 0
#            elif long(i)**2 > z:
#                return 1
        while line:
            if z % long(line) == 0:
                return 0
            elif long(line)**2 > z:
                return 1
            line=primes.readline()
        primes.close()
        produce(long(math.sqrt(2*z)))
        return prime.primeq(z)

def produce(n):
    """Produce prime numbers to the integer which you input."""
    if n != long(n):
        raise ValueError, "non-integer for produce()"
    primes = open("primes.txt","r")
    line=primes.readline()
#    line = primes.readlines()
#    max = long(line[-1:][0])
    while line:
        max = long(line)
        line=primes.readline()
    primes.close()
    p = max + 2
    while p < n+1:
        while primeq(p) == 0:
            p += 2 
        primes = open("primes.txt","r")
        plist = primes.readlines()
        plist.append(str(p))
        plist.append("\n")
        primes.close()
        primes = open("primes.txt","w")
        primes.writelines(plist)
        primes.close()
        p += 2

def prime(s):
    """Return the prime number in the number which you input."""
    import math
    if s != long(s):
        raise ValueError, "non-integer for prime()"
    elif s <= 0:
        raise ValueError, "non-positive-integer for prime()" 
    primes = open("primes.txt","r")
#    line = primes.readlines()
    line = primes.readline()
#    l = len(line) 
#    if l < s:
#        produce(s*(long(math.log(s)/math.log(2))))
#        return prime(s)
    i=0
    t=0
    while i+1 != s:
        i += 1
        line = primes.readline()
        if not line:
            t = 1
            break
    primes.close() 
#    return long(line[s-1:s][0])

    if t == 1:
        produce(s*(long(math.log(s)/math.log(2))))
        return prime(s)
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

def isprime(a):
    if a<10000000:
        return trial_division(a,'i')
    elif gcd(a,510510)>1:
        return 0
    for p in [2, 13, 23, 1662803]:
        if not spsp(a,p):
            return 0
    if a<1000000000000: # 10^12
        return 1
    f=trial_division(a-1,'f',32)
    fk=f.keys()
    fk.sort()
    r=fk[-1]
    if isprime(r):
        i=2
        while 1:
            if not psp(a,i):
                return 0
            for p in fk:
                if pow(i,(a-1)//p,a)==1:
                    break
            else:
                return 1
            i=i+1
    elif r*r<a:
        del f[r]
        fk=fk[:-1]
        i=2
        while 1:
            if not psp(a,i):
                return 0
            for p in fk:
                if pow(i,(a-1)//p,a)!=1:
                    fk.remove(p)
                    if len(fk)==0:
                        return 1
            i=i+1
    else:
        return apr(a)
          