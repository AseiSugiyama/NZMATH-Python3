import math
import bigrandom
import random
import time
import arith1
import gcd
import trialdivision
import prime

class QS:
    def __init__(self,n,sieverange,factorbase):
        self.number=n
        self.sqrt_n=int(math.sqrt(n))
        for i in [2,3,5,7,11,17,19]:
            if n%i == 0:
                print "This number is divided by ",i
                raise ValueError ;
        i=1
        while 1:
            if self.number > 10**i:
                i+=1
            else :
                self.disit=i
                break

        self.Srange=sieverange
        self.FBN=factorbase

        self.move_range = range(self.sqrt_n-self.Srange,self.sqrt_n+self.Srange+1)

        i=0
        k=0
        factor_base =[-1]
        FB_log =[0]
        while 1:
            ii = primes_table[i]
            if arith1.legendre(self.number,ii) == 1:
                factor_base.append(ii)
                FB_log.append(primes_log_table[i])
                k += 1
                i += 1
                if k==self.FBN:
                    break
            else:
                i += 1

        self.FB =factor_base
        self.FB_log = FB_log
        self.maxFB = factor_base[-1]
        N_sqrt_list =[]
        for i in self.FB:
            if i != 2 and i != -1:
                e = int(math.log(2*self.Srange,i))
                N_sqrt_modp = sqroot_power(self.number,i,e)
                N_sqrt_list.append(N_sqrt_modp)
        self.solution = N_sqrt_list  #This is square roots of N on Z/pZ, p in factor base.
        
        poly_table = [] 
        log_poly = []
        minus_val =[]
        for j in self.move_range:
            jj=(j**2)-self.number
            if jj < 0 :
                jj = -jj
                minus_val.append(j-self.sqrt_n+self.Srange)
            elif jj == 0:
                jj=1
            lj=int((math.log(jj)*30)*0.97)  # 0.97 is an erroe
            poly_table.append(jj)
            log_poly.append(lj)
        self.poly_table =poly_table  # This is Q(x) value , x in [-M+sqrt_n,M+sqrt_n]. 
        self.log_poly =log_poly      # This is log(Q(x)) value.
        self.minus_check = minus_val # This is "x" that Q(x) is minus value.

    def run_sieve(self):
        import pysco
        pysco.full()
        T=time.time()
        M=self.Srange
        start_location=[]
        logp = [0]*(2*M+1)
        j=2
        for i in self.solution:
            k=0
            start_p =[]
            while k < len(i): 
                q = int((self.sqrt_n)/(self.FB[j]**(k+1)))
                s_1=q*(self.FB[j]**(k+1))+i[k][0]
                s_2=q*(self.FB[j]**(k+1))+i[k][1]
                while 1:
                    if s_1 < self.sqrt_n-M :
                        s_1 = s_1+(self.FB[j]**(k+1))
                        break
                    else:
                        s_1 = s_1-(self.FB[j]**(k+1))
                while 1:
                    if s_2 < self.sqrt_n-M :
                        s_2 = s_2+(self.FB[j]**(k+1))
                        break
                    else:
                        s_2 = s_2-(self.FB[j]**(k+1))        
                start_p.append([s_1-self.sqrt_n+M,s_2-self.sqrt_n+M])

                k += 1
            start_location.append(start_p)
            j +=1
        self.start_location=start_location
    
        if self.poly_table[0]%2 == 0:
            i=0
            while i <= 2*M:
                j=1
                while 1:
                    if self.poly_table[i]%(2**(j+1)) == 0:                   
                        j+=1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i += 2
        else:
            i=1
            while i <= 2*M:
                j=1
                while 1:
                    if self.poly_table[i]%(2**(j+1)) == 0:                   
                        j+=1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i += 2
        L=2
        for j in self.start_location:
            k=0
            while k < len(j):
                s_1=j[k][0]
                s_2=j[k][1]
                h_1=0
                h_2=0
                while s_1+h_1 <= 2*M:
                    logp[s_1+h_1] += self.FB_log[L]
                    h_1 += self.FB[L]**(k+1)     
                while s_2+h_2 <= 2*M:
                    logp[s_2+h_2] += self.FB_log[L]
                    h_2 += self.FB[L]**(k+1)
                k += 1
            L += 1
        
        self.logp =logp 
        smooth=[]
        for t in range(0,2*M+1):
            if logp[t] >= self.log_poly[t]:
                poly_val=self.poly_table[t]
                index_vector=[]
                for p in self.FB:
                    if p == -1:
                        if t in self.minus_check:
                            index_vector.append(1)
                        else:
                            index_vector.append(0)
                    else:
                        r=0
                        while poly_val%(p**(r+1)) == 0:
                            r+=1
                        v = r%2
                        index_vector.append(v)
                smooth.append([index_vector,(poly_val,t+self.sqrt_n-M)])
        print " Sieve time is",time.time()-T,"sec"
        print " Found smooth numbers are ", len(smooth),"/",len(self.FB)
        self.smooth=smooth
        return smooth


class MPQS:
    def __init__(self,n,sieverange=0,factorbase=0,multiplier=0):
        self.number=n
        print "The number is ",n, "MPQS starting"

        if prime.primeq(self.number)==1:
            print "This number is Prime Number"
            raise ValueError
        for i in [2,3,5,7,11,13]:
            if n%i == 0:
                print "This number is divided by ",i
                raise ValueError ;

        self.sievingtime = 0
        self.coefficienttime = 0
        self.d_list = []
        self.a_list = []
        self.b_list = []
        
        """
        Decide prameters for each disits

        """
        i=1
        while 1:
            if self.number > 10**i:
                i+=1
            else :
                self.disit=i
                break
            
        if sieverange !=0:
            self.Srange=sieverange
            if factorbase !=0:
                self.FBN=factorbase
            elif self.disit <9:
                self.FBN=parameters_for_mpqs[0][1]
            else:
                self.FBN=parameters_for_mpqs[self.disit-9][1]
        elif factorbase !=0:
            self.FBN=factorbase
            if self.disit <9:
                self.Srange=parameters_for_mpqs[0][0]
            else:
                self.Srange=parameters_for_mpqs[self.disit-9][0]
        elif self.disit < 9:
            self.Srange=parameters_for_mpqs[0][0]
            self.FBN=parameters_for_mpqs[0][1]
        elif self.disit >53:
            self.Srange=parameters_for_mpqs[44][0]
            self.FBN=parameters_for_mpqs[44][1]
        else :
            self.Srange=parameters_for_mpqs[self.disit-9][0]
            self.FBN=parameters_for_mpqs[self.disit-9][1]
        
        self.move_range = range(-self.Srange,self.Srange+1) 

        """
        Decide k such that k*n = 1 (mod4) and k*n has many factor base
        """
        if multiplier == 0:
            sqrt_state=[]
            for i in [3,5,7,11,13]:
                s=arith1.legendre(self.number,i)
                sqrt_state.append(s)
            self.sqrt_state=sqrt_state
            if self.number%8 == 1 :
                j=0
                while 1:
                    if self.sqrt_state == prime_8[0][j][1]:
                        k=prime_8[0][j][0]
                        break
                    else:
                        j+=1
            elif self.number%8 == 3 :
                j=0
                while 1:
                    if self.sqrt_state == prime_8[1][j][1]:
                        k=prime_8[1][j][0]
                        break
                    else:
                        j+=1
            elif self.number%8 == 5 :
                j=0
                while 1:
                    if self.sqrt_state == prime_8[2][j][1]:
                        k=prime_8[2][j][0]
                        break
                    else:
                        j+=1
            elif self.number%8 == 7 :
                j=0
                while 1:
                    if self.sqrt_state == prime_8[3][j][1]:
                        k=prime_8[3][j][0]
                        break
                    else:
                        j+=1
        else:
            if n %4 ==1:
                k=1
            else:
                if multiplier == 1:
                    print "This number is 3 mod 4 "
                    raise ValueError
                else:
                    k= multiplier
        self.number = k*self.number
        self.multiplier = k
       
        print self.disit,"- disits Number"
        print "Multiplier is",self.multiplier

        """
        Table of (log p) , p in FB
        """
        i=0
        k=0
        factor_base =[-1]
        FB_log =[0]
        while 1:
            ii = primes_table[i]
            if arith1.legendre(self.number,ii) == 1:
                factor_base.append(ii)
                FB_log.append(primes_log_table[i])
                k += 1
                i += 1
                if k==self.FBN:
                    break
            else:
                i += 1

        self.FB = factor_base
        self.FB_log = FB_log
        self.maxFB = factor_base[-1]

        """
        Solve x^2 = n (mod p^e) 
        """
        N_sqrt_list =[]
        for i in self.FB:
            if i != 2 and i != -1:
                e = int(math.log(2*self.Srange,i))
                N_sqrt_modp = sqroot_power(self.number,i,e)
                N_sqrt_list.append(N_sqrt_modp)
        self.Nsqrt = N_sqrt_list 
                
    def make_poly(self):
        T=time.time()
        """
        Make coefficients of f(x)= ax^2+b*x+c
        """
        if self.d_list==[]:
            d=int(math.sqrt((math.sqrt(self.number)/(math.sqrt(2)*self.Srange))))    
            if d%2 == 0:
                if (d+1)%4 == 1: #case d=0 mod4
                    d=d+3
                else:
                    d=d+1        #case d=2 mod4
            elif d%4 == 1:       #case d=1 mod4
                d = d+2
                                 #case d=3 mod4
        else:
            d=self.d_list[-1]
            
        i=0
        while 1:
            if d+i not in self.d_list and prime.primeq(d+i) == 1 and arith1.legendre\
                   (self.number,d+i)==1 and d+i not in self.FB :
                break
            else:
                i+= 4
        d = d+i        
        a = d**2
        h_0 = pow(self.number,(d-3)/4,d)
        h_1 = (h_0*self.number)%d
        h_2 = ((arith1.inverse(2,d)*h_0*(self.number - h_1**2))/d)%d
        b = (h_1 + h_2*d)%a
        if b%2 == 0:
            b=b-a

        self.d_list.append(d)   
        self.a_list.append(a)
        self.b_list.append(b)

        """
        Get solution of  F(x) = 0 (mod p^i)

        """
        solution = []
        i=0
        for s in self.Nsqrt:
            k=0
            p_solution=[]
            while k < len(s):
                a_inverse = arith1.inverse(2*self.a_list[-1],self.FB[i+2]**(k+1))
                x_1 = ((-b + s[k][0])*a_inverse)%(self.FB[i+2]**(k+1)) 
                x_2 = ((-b + s[k][1])*a_inverse)%(self.FB[i+2]**(k+1)) 
                p_solution.append([x_1,x_2])
                k+=1
            i += 1
            solution.append(p_solution)
        self.solution = solution
        self.coefficienttime +=time.time()-T
                
    def run_sieve(self):
        self.make_poly()
        T=time.time()
        M=self.Srange
        a=self.a_list[-1]            #
        b=self.b_list[-1]            # These are coefficients of F(x)
        c=(b**2-self.number)/(4*a)   #
        d=self.d_list[-1]            #
        
        poly_table = [] 
        log_poly = []
        minus_val =[]
        for j in self.move_range:
            jj=(a*(j**2)+b*j+c)
            if jj < 0 :
                jj=-jj
                minus_val.append(j+self.Srange)
            elif jj == 0:
                jj=1
            lj=int((math.log(jj)*30)*0.95)  # 0.95 is an erroe
            poly_table.append(jj)
            log_poly.append(lj)
        self.poly_table=poly_table  # This is F(x) value , x in [-M,M]. 
        self.log_poly=log_poly      # This is log(F(x)) value.
        self.minus_check=minus_val  # This is "x" that F(x) is minus value.M=self.Srange
        
        y=arith1.inverse(2*d,self.number)
        start_location = []
        logp = [0]*(2*M+1)
        j=2
        for i in self.solution:
            k=0
            start_p = []
            while k < len(i): 
                q=int(-M/(self.FB[j]**(k+1)))
                s_1=q*(self.FB[j]**(k+1))+i[k][0]
                s_2=q*(self.FB[j]**(k+1))+i[k][1]
                while 1:
                    if s_1 < -M :
                        s_1=s_1+(self.FB[j]**(k+1))
                        break
                    else:
                        s_1=s_1-(self.FB[j]**(k+1))
                while 1:
                    if s_2 < -M :
                        s_2=s_2+(self.FB[j]**(k+1))
                        break
                    else:
                        s_2=s_2-(self.FB[j]**(k+1))        
                start_p.append([s_1+M,s_2+M])
                k+=1
            start_location.append(start_p)
            j+=1
        self.start_location=start_location
    
        if self.poly_table[0]%2 == 0:
            i=0
            while i <= 2*M:
                j=1
                while 1:
                    if self.poly_table[i]%(2**(j+1)) == 0:                   
                        j+=1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i+=2
        else:
            i=1
            while i <= 2*M:
                j=1
                while 1:
                    if self.poly_table[i]%(2**(j+1)) == 0:                   
                        j+=1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i += 2
        L=2
        for j in self.start_location:
            k=0
            while k < len(j):
                s_1=j[k][0]
                s_2=j[k][1]
                h_1=0
                h_2=0
                while s_1+h_1 <=2*M:
                    logp[s_1+h_1]+=self.FB_log[L]
                    h_1+=self.FB[L]**(k+1)     
                while s_2+h_2 <=2*M:
                    logp[s_2+h_2]+=self.FB_log[L]
                    h_2+=self.FB[L]**(k+1)
                k += 1
            L += 1
        
        self.logp=logp 
        smooth=[]
        for t in range(0,2*M+1):
            if logp[t] >= self.log_poly[t]:
                poly_val=self.poly_table[t]
                index_vector = []
                H=(y*(2*a*(t-self.Srange)+b))%self.number
                for p in self.FB:
                    if p == -1:
                        if t in self.minus_check:
                            index_vector.append(1)
                        else:
                            index_vector.append(0)
                    else:
                        r=0
                        while poly_val%(p**(r+1)) == 0:
                            r+=1
                        v=r%2
                        index_vector.append(v)
                smooth.append([index_vector,(poly_val,H)])
        self.sievingtime += time.time()-T
        return smooth
    
    def get_vector(self):
        a=time.time()
        P=len(self.FB)
        if P < 100:
            V=-5
        else:
            V=0
        smooth=[]
        i=0
        while P*1 > V:
            n=self.run_sieve()
            V+=len(n)
            smooth+=n
            i+=1
            if i%50==0:
                if i==50:
                    print "*/","Per 50 times changing poly report","/* "
                print "Time of deciding coefficient =",self.coefficienttime,"sec"
                print "Sieving Time = ",self.sievingtime ,"sec" 
                print "Find smooth numbers are",V,"/",P
        if P<100:
            V+=5
        self.smooth=smooth
        print "*/","Total",i,"times changing poly report","/*"
        print "Time of deciding coefficient =",self.coefficienttime, "sec"
        print "Sieving Time = ",self.sievingtime ,"sec"
        print "Found smooth numbers are",V,"/",P
        print "Total time of getting enough smooth numbers = ",time.time()-a,"sec"
        return smooth


class Elimination:
    def __init__(self,smooth):
        vector=[]
        history=[]
        i=0
        for vec in smooth:
            vector.append(vec[0])
            history.append({i:1})
            i+=1
        self.vector=vector
        self.FB_number=len(vector[0])
        self.row_size=len(vector)
        self.history=history
        self.historytime=0
    def vector_add(self,i,j):
        V_i=self.vector[i]
        V_j=self.vector[j]
        k=0
        while k < len(V_i):
            if V_i[k] == 1:
                if V_j[k] == 1:
                    V_j[k]=0
                else:
                    V_j[k]=1
            k+=1

    def transpose(self):
        Transe_vector = []
        i=0
        while i <self.FB_number:
            j=0
            vector = []
            while j < self.row_size:
                vector.append(self.vector[j][i])
                j+=1
            Transe_vector.append(vector)
            i+=1
        self.Transe=Transe_vector

    def history_add(self,i,j):
        T=time.time()
        H_i=self.history[i].keys()
        H_j=self.history[j].keys()
        for k in H_i:
            if  k in H_j:
                del self.history[j][k]
            else:
                self.history[j][k]=1
        self.historytime+=time.time()-T

    def gaussian(self):
        a=time.time()
        pivot = []
        FBnum=self.FB_number
        Smooth=len(self.vector)
        j=0
        m=0
        while j < FBnum :
            k=0
            while k < Smooth:
                if k not in pivot and self.vector[k][j] == 1 :
                    pivot.append(k)
                    V_k=self.vector[k]
                    h=0
                    while h < Smooth:
                        if h not in pivot and self.vector[h][j] == 1 :
                            self.history_add(k,h)
                            V_h=self.vector[h]
                            q=m
                            while q < FBnum:
                                if V_k[q] == 1:
                                    if V_h[q] == 1:
                                        V_h[q]=0
                                    else:
                                        V_h[q]=1
                                q+=1
                        h+=1
                    break
                else:
                    k+=1
            j+=1    
            m+=1
        self.pivot=pivot

        zero_vector=[]
        check=0
        while check < Smooth:
            if check not in pivot:
                g=0
                while g < FBnum:
                    if self.vector[check][g] == 1:
                        break
                    else:
                        g+=1
                if g == FBnum:
                    zero_vector.append(check)
                check+=1
            else:
                check+=1
        print "Time of Gaussian Elimination = ",time.time()-a,"sec"
        return zero_vector

def qs(n,s,f):
    """
    This is main function of QS
    Arguments are (composite_number, sieve_range, factorbase_size)
    You must input these 3 arguments.
    
    """
    a=time.time()
    Q=QS(n,s,f)
    print "Sieve range is","[",Q.move_range[0],",",Q.move_range[-1],\
    "]",",","Factorbase size =",len(Q.FB),",","Max Factorbase",Q.maxFB
    Q.run_sieve() 
    V=Elimination(Q.smooth)
    A=V.gaussian()
    print "Found",len(A),"liner dependent relations"
    answerX_Y = []
    N_factors = []
    for i in A:
        B=V.history[i].keys()
        X=1
        Y=1
        for j in B:
            X*=Q.smooth[j][1][0]
            Y*=Q.smooth[j][1][1]
            Y=Y%Q.number
        X=sqrt_modn(X,Q.number)
        answerX_Y.append(X-Y)
    for k in answerX_Y:
        if k != 0:
            factor=gcd.gcd(k,Q.number)
            if factor not in N_factors and factor != 1 and factor != Q.number \
            and prime.primeq(factor) == 1:
                N_factors.append(factor)
    N_factors.sort()
    print "Total time =",time.time()-a,"sec"
    print N_factors

def mpqs(n,s=0,f=0,m=0):
    """
    This is main function of MPQS.
    Arguments are (composite_number, sieve_range, factorbase_size, multiplier) 
    You must input composite_number at least.
    
    """
    a=time.time()
    M=MPQS(n,s,f,m)
    print "Sieve range is","[",M.move_range[0],",",M.move_range[-1],\
    "]",",","Factorbase size =",len(M.FB),",","Max Factorbase",M.maxFB
    M.get_vector() 
    N=M.number/M.multiplier
    V=Elimination(M.smooth)
    A=V.gaussian()
    print "Found",len(A),"liner dependent relations"
    answerX_Y = []
    N_prime_factors = []
    N_factors=[]
    output=[]
    for i in A:
        B=V.history[i].keys()
        X=1
        Y=1
        for j in B:
            X*=M.smooth[j][1][0]
            Y*=M.smooth[j][1][1]
            Y=Y%M.number
        X=sqrt_modn(X,M.number)
        answerX_Y.append(X-Y)
    NN=1
    for k in answerX_Y:
        if k != 0:
            factor=gcd.gcd(k,N)
            if factor not in N_factors and factor != 1 and factor != N \
                   and factor not in N_prime_factors:
                if prime.primeq(factor) == 1:
                    NN=NN*factor
                    N_prime_factors.append(factor)
                else:
                    N_factors.append(factor)
    
    print "Total time =",time.time()-a,"sec"

    if NN == N:
        print  "Factored completely!" 
        N_prime_factors.sort()
        for P in N_prime_factors:
            N=N/P
            i=1
            while N%P == 0:
                i+=1
            output.append((P,i))
        return output

    elif NN != 1:
        f=N/NN
        if prime.primeq(f) == 1:
            N_prime_factors.append(f)
            print  "Factored completely !" 
            N_prime_factors.sort()        
            for P in N_prime_factors:
                N=N/P
                i=1
                while N%P == 0:
                    i+=1
                output.append((P,i))
            return output

    for F in N_factors:
        for FF in N_factors:
            if F != FF:
                Q=gcd.gcd(F,FF)
                if prime.primeq(Q)==1 and Q not in N_prime_factors:
                    N_prime_factors.append(Q)
                    NN=NN*Q

    N_prime_factors.sort()        
    for P in N_prime_factors:
        N=N/P
        i=1
        while N%P == 0:
            N=N/P        
            i+=1
        output.append((P,i))

    if  N == 1:
        print  "Factored completely!! " 
        return output
        
    else:
        for F in N_factors:
            g=gcd.gcd(N,F)
            if prime.primeq(g)==1:
                N_prime_factors.append(g)
                N=N/g
                i=1
                while N%g == 0:
                    i+=1
                output.append((g,i))
        if N==1 :
            print  "Factored completely !! " 
            return output
        elif prime.primeq(N)==1:
            output.append((N,1))
            print  "Factored completely!!! " 
            return output
        else:
            N_factors.sort()
            print "Sorry, not factored completely"
            return output,N_factors



########################################################
#                                                      #
# Following functions are subfunction for main progrum #
#                                                      #
########################################################

def eratosthenes(n):
    if n<2:
        raise ValueError,"Input value must be bigger than 1  "
    else:
        primes=[2]
        sieves=[1]*(((n+1)//2)-1)
        k=3
        i=0
        sieves_len=len(sieves)
        while k <= math.sqrt(n):
            if sieves[i]==1:
                j=1
                while i+j*k <= sieves_len-1:
                    sieves[i+j*k]=0
                    j=j+1
                k,i=k+2,i+1
            else:
                k,i=k+2,i+1
        y=3
        for x in sieves:
            if x==1:
                primes.append(y)
                y=y+2
            else:
                y=y+2
        return primes

def prime_mod8(n):

    """
    This is table for choosing multiplier which makes N to have
    factorbase(2,3,5,7,11,13)

    """
    Primes=eratosthenes(n)
    Prime_1,Prime_3,Prime_5,Prime_7=[],[],[],[]
    Prime_1_leg,Prime_3_leg,Prime_5_leg,Prime_7_leg=[],[],[],[]
    sp= [2,3,5,7,11,13]
    sp2=[3,5,7,11,13]
    for i in Primes:
        if i%8 == 1 and i not in sp:
            leg=[]
            for j in sp2:
                a=arith1.legendre(i,j)
                leg.append(a)
            if leg not in Prime_1_leg:
                Prime_1_leg.append(leg)
                Prime_1.append([i,leg])
        elif i%8 == 3 and i not in sp:
            leg=[]
            for j in sp2:
                a=arith1.legendre(i,j)
                leg.append(a)
            if leg not in Prime_3_leg:
                Prime_3_leg.append(leg)
                Prime_3.append([i,leg])
        elif i%8 == 5 and i not in sp:
            leg=[]
            for j in sp2:
                a=arith1.legendre(i,j)
                leg.append(a)
            if leg not in Prime_5_leg:
                Prime_5_leg.append(leg)
                Prime_5.append([i,leg])
        elif i%8 == 7 and i not in sp:
            leg=[]
            for j in sp2:
                a=arith1.legendre(i,j)
                leg.append(a)
            if leg not in Prime_7_leg:
                Prime_7_leg.append(leg)
                Prime_7.append([i,leg])
    return [Prime_1,Prime_3,Prime_5,Prime_7]

def eratosthenes_log(n):
    Primes = eratosthenes(n)
    Primes_log = []
    for i in Primes:
        l=int(math.log(i)*30) #30 is scale
        Primes_log.append(l)
    return Primes_log

def sqrt_modn(n,modn):
    N_factor=trialdivision.trialDivision(n)
    N=1
    for i in N_factor:
        N=N*pow(i[0],i[1]/2,modn)
        N=N%modn
    return N

def sqroot(a,p): # p is a prime

    """
    This returns squareroot of 'a' for mod'p'
    
    """
    if arith1.legendre(a,p)==1:
        if p%8==3 or p%8==5 or p%8==7:
            a=a%p
            if p%8==3 or p%8==7:
                x=pow(a,((p+1)/4),p)
                return [x,p-x]
            else: # p%8==5
                x=pow(a,((p+3)/8),p)
                c= (x**2)%p
                if c%p!=a%p:
                    x=x*(2**((p-1)/4))%p
                return [x,p-x]
        else: #p%8==1
            d=random.randint(2,p-1)
            while arith1.legendre(d,p)!=-1:
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
            return [x,p-x]

def sqroot_power(a,p,n):

    """
    return squareroot of a mod p^n 
    """
    x=sqroot(a,p)
    i=2
    answer=[x]
    while i <= n:
        b_1 =(x[0]**2-a)//(p**(i-1))
        b_2 =(x[1]**2-a)//(p**(i-1))
        x_0_1 = x[0]%p
        x_0_2 = x[1]%p
        x_1=-b_1*(arith1.inverse(2*x_0_1,p))
        x_2=-b_2*(arith1.inverse(2*x_0_2,p))
        X_1=(x[0]+x_1*(p**(i-1))%(p**i))
        X_2=(x[1]+x_2*(p**(i-1))%(p**i))
        x=[X_1,X_2]
        answer.append(x)
        i+=1
    return answer

#################
# Initial items #
#################
primes_table=eratosthenes(10**5)
primes_log_table=eratosthenes_log(10**5)
prime_8=prime_mod8(8090)
parameters_for_mpqs = [[100,20], #9 -disits 
                      [100,21], #10
                      [100,22], #11
                      [100,24], #12
                      [100,26], #13
                      [100,29], #14
                      [100,32], #15
                      [200,35], #16
                      [300,40], #17
                      [300,60], #18
                      [300,80], #19
                      [300,100], #20
                      [300,100], #21
                      [300,120], #22
                      [300,140], #23
                      [600,160], #24
                      [900,180], #25
                      [1200,200], #26
                      [1000,220], #27
                      [2000,240], #28
                      [2000,260], #29
                      [2000,325], #30
                      [2000,355], #31 
                      [2000,375], #32
                      [3000,400], #33
                      [2000,425], #34
                      [2000,550], #35
                      [3000,650], #36
                      [5000,750], #37
                      [4000,850], #38
                      [4000,950], #39
                      [5000,1000], #40
                      [14000,1150], #41
                      [15000,1300], #42
                      [15000,1600], #43
                      [15000,1900], #44
                      [15000,2200], #45
                      [20000,2500], #46
                      [25000,2500], #47
                      [27500,2700], #48
                      [30000,2800], #49
                      [35000,2900], #50
                      [40000,3000], #51 
                      [50000,3200], #52
                      [50000,3500]] #53


