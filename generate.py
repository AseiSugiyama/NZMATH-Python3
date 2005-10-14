#from math import*
import sets
import random
import arith1
import gcd
import function
import prime
import combinatorial
import time 

def norm(x,s,D):
    """
    x = [i,j]
    """
    return x[0]**2+s*x[0]*x[1]+(x[1]**2)*(s-D)/4

def para(n,k,m):
    #Determine the generator "omega" of Z_K as a Z-module
    #omega=function.powering(m,[0,1],1)

    #Determine discriminant of field K=Q(sqrt(m)).
    starttime = time.clock()
    if m%4==1:
        s=1
    else:
        s=0
    D=(4**(1-s))*m    

    #Select a prime number s.t. (p) is prime ideal of Z_K.
    if m%4==1:
        pi=prime.nextPrime(n*k*abs(m))
    else:
        pi=prime.nextPrime(2*n*k*abs(m))
        
    while True:
        while True:
            p=pi
            if D%2==0:
                if p%2==1:
                    u=8-(D%8)
                    w=(((p-1)*(4*p+D+4-u)/(2*u)+1)%4)
                    if w==3:
                        j=-1
                    else:
                        j=w
                    t=j*arith1.legendre(p,abs(D/u))
                else:
                    t=0
            else:
                t=arith1.legendre(p,abs(D))
            if t==-1:
                break
            pi=prime.nextPrime(p)
              
        #Determine a generator g of (O_K/(p))*
        for i in range(1,p):
            for j in range(1,p):
                h=function.generator(m,[i,j],p)
                if h==True:
                    Base=[i,j]
                    w=0
                    while w == 0:
                        rnd = random.randint(2,p**2-2)
                        if gcd.gcd(rnd,p**2-1) == 1:
                            w = 1 
                            g = function.powering_mod(m,Base,rnd,p)
                        else:
                            w = 0
                    break
                  
        #Check if norm of S[i] are coprime.
        LIst=[]
        for i in range(-n,n):
            for j in range(-n,n):
                LIst.append([i,j])
                
        #Remove units and zero from LIst.
        LIst.remove([0,0])
        LIst.remove([1,0])
        LIst.remove([-1,0])
        if m == -1:
            LIst.remove([0,1])
            LIst.remove([0,-1])
        if m == -3:
            LIst.remove([1,-1])
            LIst.remove([-1,1])
            LIst.remove([0,-1])
            LIst.remove([0,1])
            
        t=1
        while t<=18:
            S=random.sample(LIst,n)  #Input n random elements in (O_K/(P))*
            list=[]
            snorm=[norm(Si,s,D) for Si in S] 
            for i in range(n):
                for j in range(i+1,n):
                    if gcd.gcd(snorm[i],snorm[j])==1:
                        list.append([S[i],S[j]])
            if len(list)!=combinatorial.binomial(n, 2):
                continue
            listcopy=snorm
            listcopy.sort()
            
            #Check if the set S[i] is collect.
            N=listcopy[n-k]
            for l in range(n-k+1,n):
                N=N*listcopy[l]
            if D%4 == 0:
                if N < (p**2)/4:
                    break
            else :
                if N <(((p-1)**2)*(-D))/(4*(1-D)):
                    break
            t=t+1
        else:
            pi=prime.nextPrime(pi)
            continue
        break        
    stoptime = time.clock()
    print "time estim(select) =",stoptime-starttime
    #Generate secret key.
    d=random.randint(1,p**2-2)


    #Generate public key.
    a=[]
    b=[]
    for i in range(n):
        a.append(function.Bsgs(m,p,g,S[i]))
        b.append((a[i]+d)%(p**2-1))
            
    return [[m,g,d,p,S],[n,k,b]]
