import factor
import gcd
import math
import random

def euler(n):                    
    """
    This program returns Eulernumber for n
    """
    f = factor.trialDivision(n)
    p = 1
    for f0, f1 in f:
        p *=pow(f0,f1-1)*(f0-1)
    return p

def moebius(n):
    """
    This program returns Moebius function for n
    """
    f = factor.trialDivision(n)
    i=0
    while i < len(f):
        g=f[i]
        if g[1]>1:
            return 0
        i=i+1
    return pow(-1,len(f))


def legendre(a,m): 
    """
    This program returns Legendre symbol (a/m)
    If m is a odd composite then this is Jacobi symbol
    """
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


def sqroot(a,p): # p is a prime
    """
    This program returns squareroot of 'a' for mod'p'
    """
    if legendre(a,p)==1:
        if p%8==3 or p%8==5 or p%8==7:
            a=a%p
            if p%8==3 or p%8==7:
                x=pow(a,((p+1)/4),p)
                return x
            else: # p%8==5
                x=pow(a,((p+3)/8),p)
                c= (x**2)%p
                if c%p!=a%p:
                    x=x*(2**((p-1)/4))%p
                return x
        else: #p%8==1
            d=random.randint(2,p-1)
            while legendre(d,p)!=-1:
                d=random.randint(2,p-1)
            s=0
            q=p-1
            while q%2==0:
                q=q/2
                s=s+1
            t=(p-1)/2**s
            A=pow(a,t,p)
            D=pow(d,t,p)
            m=0
            for i in range(1,s):
                if pow((A*(D**m)),(2**(s-1-i)),p) == (p-1):
                    m=m+2**i
            x=(a**((t+1)/2))*(D**(m/2))%p
            return x
    elif legendre(a,p)==0:
        return 0
    else:
        raise ValueError,"There is no solution"


def expand(n,m):#n>m>0
    """
    This program returns m-adic expansion for n
    """
    k=[]
    while n/m!=0:
        i=n%m
        k.append(i)
        n=n/m
    k.append(n%m)
    return k

def inverse(x,p): #x>0 
    """
    This program returns inverse of x for modulo p
    """
    if x<0:
        while x<0:
            x=x+p
    y=gcd.extgcd(p,x)
    if y[1]<0:
        r=p+y[1]
        return r
    else:
        return y[1]


def CRT(list): 
    """
    This program is Chinese Rmainder Theorem using Algorithm 2.1.7 
    of C.Pomerance and R.Crandall's book.
    """
    r=len(list)
    product=[]
    prodinv=[]
    m=1
    i=1
    while i < r:
        m = m*list[i-1][1]
        c = inverse(m,list[i][1])
        product.append(m)
        prodinv.append(c)
        i = i+1

    M=product[r-2]*list[r-1][1]
    n=list[0][0]
    i=1
    while i < r:
        u = ((list[i][0]-n)*prodinv[i-1])%list[i][1]
        n = n + u*product[i-1]
        i = i+1
    n = n%M
    return n

def AGM(a,b):
    x=(a+b)/2.0
    y=math.sqrt(a*b)
    while abs(x-y)>y*1e-15:
        x=(x+y)/2.0
        y=math.sqrt(x*y)
    return x
