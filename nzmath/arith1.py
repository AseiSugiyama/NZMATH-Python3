import random
import gcd
import factor

#Eulernumber for n 
def euler(n):                    
    f = factor.trialDivision(n)
    p = 1
    for f0, f1 in f:
        p *=pow(f0,f1-1)*(f0-1)
    return p
#Moebius function for n
def moebius(n):
    f = factor.trialDivision(n)
    i=0
    while i < len(f):
        g=f[i]
        if g[1]>1:
            return 0
        i=i+1
    return pow(-1,len(f))

#Legendre symbol (a/m)
def legendre(a,m): #if m is a odd composite then this is Jacobi symbol
    a=a%m
    t=1
    while a!=0:
        while a%2==0:
            a=a/2
            if m%8==3 or m%8==5:
                t=-t
        a,m=m,a
        if a%4==3 and m%4==3:
            t=-t
        a=a%m
    if m==1:
        return t
    return 0

#This is solution for " x**2 = a (mod p)"
def sqroot(a,p): # p is a prime
    if legendre(a,p)==1:
        if p%8==3 or p%8==5 or p%8==7:
            a=a%p
            if p%8==3 or p%8==7:
                x=a**((p+1)/4)%p
                return x 
            else: # p%8==5
                x=a**((p+3)/8)%p
                c= (x**2)%p
                if c%p!=a%p:
                    x=x*(2**((p-1)/4))%p
                return x 
        else: #p%8==1
            d=0
            while legendre(d,p)!=-1:
                d=random.randint(2,p-1)
            s=0
            q=p-1
            while q%2==0:
                q=q/2
                s=s+1
            t=(p-1)/2**s
            A=(a**t)%p
            D=(d**t)%p
            m=0
            for i in range(1,s):
                if ((A*(D**m))**(2**(s-1-i)))%p==(p-1):
                    m=m+2**i
            x=(a**((t+1)/2))*(D**(m/2))%p
            return x
    else:
        print "no solution"

#This is m-adic expansion for n
def expand(n,m):#n>m>0
    k=[]
    while n/m!=0:
        i=n%m
        k.append(i)
        n=n/m
    k.append(n%m)
    return k
#This is inverse of x for modulo p
def inverse(x,p): #x>0 
    if x<0:
        while x<0:
            x=x+p
    y=gcd.extgcd(p,x)
    if y[1]<0:
        r=p+y[1]
        return r
    else:
        return y[1]



    
        
