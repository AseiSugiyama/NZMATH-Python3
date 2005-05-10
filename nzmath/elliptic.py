from __future__ import division
import math
import random
import sets

import arith1
import factor
import finitefield
import gcd
import integerResidueClass
import polynomial 
import prime
import rational

def divi(n):
    """
    this returns all factors divide n
    """
    D=factor.rhomethod(n)
    N=[]
    i=0
    while i<len(D):
        j=0
        list=[]
        while j<=D[i][1]:
            list.append(D[i][0]**j)
            j=j+1
        if i==0:
            l=0
            while l<len(list):
                N.append(list[l])
                l=l+1
        else:
            x=len(N)
            k=0
            while k<x:
                l=1
                while l<len(list):
                    N.append(N[k]*list[l])
                    l=l+1
                k=k+1
        i=i+1
    N.sort()
    return N

def Element_p(a,p):
    """
    a is (rational,int,long) number
    this returns a in F_p
    """
    return int(finitefield.FinitePrimeFieldElement(a,p).n)

def PolyMod(f,g):
    """
    return f (mod g)
    """
    if isinstance(g,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
        return 0
    elif isinstance(f,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
        return f
    else:
        return f%g

def GCD(f,g):
    if f==0 and g!=0:
        return g
    elif g==0 and f!=0:
        return f
    elif isinstance(f,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
        return 1
    elif isinstance(g,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
        return 1
    else:
        p=f.getRing().gcd(f,g)
        if p.degree()==0:
            return 1
        else:
            return p

def PolyPow(f,d,g):
    """
    this returns (f^d)%g
    """
    l=arith1.expand(d,2)
    poly=1
    for i in range(len(l)-1,-1,-1):
        poly=poly*poly
        poly=PolyMod(poly,g)
        if l[i]==1:
            poly=poly*f
            poly=PolyMod(poly,g)
    return poly

def PolyMulRed(list,poly):
    """
    list[*] is (OneSparsePoly,int,long)
    poly is OneSparsePoly
    """
    if poly.degree()<1:
        return 0 
    i=0
    while i<len(list):
        if list[i]==0:
            return 0 
        elif isinstance(list[i],(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
            pass
        elif list[i].degree()>=poly.degree():
            list[i]=PolyMod(list[i],poly)
            if list[i]==0:
                return 0
        i=i+1
    POLY=polynomial.OneVariableSparsePolynomial({0:1},['x'],poly.coefficientRing)
    i=0
    while i<len(list):
        POLY=POLY*list[i]
        if isinstance(POLY,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)):
            pass
        else:
            if POLY.degree()>=poly.degree():
                POLY=PolyMod(POLY,poly)
                if POLY==0:
                    return 0
        i=i+1
    return POLY

def heart(q):
    """
    this is for Schoof's
    """
    l=[]
    i=3
    j=1
    while j<=4*int(math.sqrt(q)):
        if prime.primeq(i):
            l.append(i)
            j=j*i
        i=i+2
    return l

def powOrd(x,y,z):
    """
    x=-#E(F_p)+p+1
    y=self.index >1
    z=self.ch
    """
    C={}
    C[1]=x
    i=2
    C[-1]=x
    C[-2]=2
    while i<=y:
        C[0]=C[1]*C[-1]-z*C[-2]
        C[-1],C[-2]=C[0],C[-1]
        i=i+1
    return C[0]

class EC:
    """
    Elliptic curves over Q and Fp.
    # If you wanna use over other fields, just a moment please :-)
    """
    def __init__(self,coefficient,character=None,index=None):
        """
        Initialize an elliptic curve. If coefficient has 5 elements,
        it represents E:y**2+a1*x*y+a3*y=x**3+a2*x**2+a4*x+a6 or 2
        elements, E:y*2=x*3+a*x+b.
        """
        if isinstance(coefficient,list):
            self.coefficient=coefficient
            if not character:
                self.ch=0
            else:
                self.ch=character
            if self.ch==0: 
                pass
            else:
                if not index: #field=F_p
                    self.coeffField=finitefield.FinitePrimeField(character)
                    self.index=1
                elif index==0:
                    raise ValueError,"you must input(index \in Z>0) (-_-;)"
                elif index==1:
                    self.coeffField=finitefield.FinitePrimeField(character)
                    self.index=1
                else: #field=F_q,q=(character)^r
                    """
                    index is irred polynomial in F_p,deg=r
                    To add this, we must exchange field and element.
                    """
                    raise NotImplementedError,"Now making (>_<),now we can use only over finite prime fields"
            self.PointAtInfinity=[0] 
            if self.ch==0:
                if len(self)==5:
                    self.a1=coefficient[0]
                    self.a2=coefficient[1]
                    self.a3=coefficient[2]
                    self.a4=coefficient[3]
                    self.a6=coefficient[4]
                    self.b2=self.a1**2+4*self.a2
                    self.b4=self.a1*self.a3+2*self.a4
                    self.b6=self.a3**2+4*self.a6
                    self.b8=self.a1**2*self.a6+4*self.a2*self.a6-self.a1*self.a3*self.a4+self.a2*self.a3**2-self.a4**2
                    self.c4=self.b2**2-24*self.b4
                    self.c6=-self.b2**3+36*self.b2*self.b4-216*self.b6
                    self.disc=-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6
                elif len(self)==2:
                    self.a=coefficient[0]
                    self.b=coefficient[1]
                    self.a1=0
                    self.a2=0
                    self.a3=0
                    self.a4=coefficient[0]
                    self.a6=coefficient[1]
                    self.b2=0
                    self.b4=2*self.a
                    self.b6=4*self.b
                    self.b8=-self.a**2
                    self.c4=-48*self.a
                    self.c6=-864*self.b
                    self.disc=rational.IntegerIfIntOrLong(self.c4**3-self.c6**2)/1728
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
                if self.disc==0:
                    raise ValueError, "singular curve (@_@)"
                self.j=rational.IntegerIfIntOrLong(self.c4**3)/rational.IntegerIfIntOrLong(self.disc)
            elif self.ch==1:
                raise ValueError, "characteristic must be 0 or prime (-_-;)"
            elif self.ch==2: # y^2+x*y=x^3+a2*x^2+a6 or y^2+a3*y=x^3+a4*x+a6
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long,finitefield.FinitePrimeFieldElement)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if len(self)==5:
                    if coefficient[0]%2==1 and coefficient[2]%2==coefficient[3]%2==0:
                        self.a1=finitefield.FinitePrimeFieldElement(1,2) 
                        self.a2=finitefield.FinitePrimeFieldElement(coefficient[1],2)
                        self.a3=finitefield.FinitePrimeFieldElement(0,2) 
                        self.a4=finitefield.FinitePrimeFieldElement(0,2) 
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],2)
                        self.b2=finitefield.FinitePrimeFieldElement(1,2)
                        self.b4=finitefield.FinitePrimeFieldElement(0,2)
                        self.b6=finitefield.FinitePrimeFieldElement(0,2)
                        self.b8=self.a6
                        self.c4=finitefield.FinitePrimeFieldElement(1,2)
                        self.c6=finitefield.FinitePrimeFieldElement(1,2)
                        self.disc=self.a6
                        if self.disc.n!=0:
                            self.j=self.a6.inverse()
                    elif coefficient[0]%2==coefficient[1]%2==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,2)
                        self.a2=finitefield.FinitePrimeFieldElement(0,2)
                        self.a3=finitefield.FinitePrimeFieldElement(coefficient[2],2)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[3],2)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],2)
                        self.b2=finitefield.FinitePrimeFieldElement(0,2)
                        self.b4=finitefield.FinitePrimeFieldElement(0,2)
                        self.b6=self.a3**2
                        self.b8=self.a4**2
                        self.c4=finitefield.FinitePrimeFieldElement(0,2)
                        self.c6=finitefield.FinitePrimeFieldElement(0,2)
                        self.disc=self.a3**4
                        self.j=finitefield.FinitePrimeFieldElement(0,2)
                    else:
                        raise ValueError, "can't defined EC (-_-;)"
                    if self.disc.n==0:
                        raise ValueError, "singular curve (@_@)"
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
            elif self.ch==3: # y^2=x^3+a2*x^2+a6 or y^2=x^3+a4*x+a6
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long,finitefield.FinitePrimeFieldElement)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if len(self)==5:
                    if coefficient[0]%3==coefficient[2]%3==coefficient[3]%3==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,3)
                        self.a2=finitefield.FinitePrimeFieldElement(coefficient[1],3)
                        self.a3=finitefield.FinitePrimeFieldElement(0,3)
                        self.a4=finitefield.FinitePrimeFieldElement(0,3)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],3)
                        self.b2=self.a2
                        self.b4=finitefield.FinitePrimeFieldElement(0,3)
                        self.b6=self.a6
                        self.b8=self.a2*self.a6
                        self.c4=self.b2**2
                        self.c6=2*self.b2**3
                        self.disc=-self.a2**3*self.a6
                        if self.disc.n!=0:
                            self.j=(-self.a2**3)*self.a6.inverse()
                    elif coefficient[0]==coefficient[1]==coefficient[2]==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,3)
                        self.a2=finitefield.FinitePrimeFieldElement(0,3)
                        self.a3=finitefield.FinitePrimeFieldElement(0,3)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[3],3)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],3)
                        self.b2=finitefield.FinitePrimeFieldElement(0,3)
                        self.b4=2*self.a4
                        self.b6=self.a6
                        self.b8=2*self.a4**2
                        self.c4=finitefield.FinitePrimeFieldElement(0,3)
                        self.c6=finitefield.FinitePrimeFieldElement(0,3)
                        self.disc=-self.a4**3
                        self.j=finitefield.FinitePrimeFieldElement(0,3)
                    else:
                        raise ValueError, "can't defined EC (-_-;)"
                    if self.disc.n==0:
                        raise ValueError, "singular curve (@_@)"
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
            else:
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long,finitefield.FinitePrimeFieldElement)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if prime.millerRabin(self.ch)==1:
                    if len(self)==5:
                        self.a1=finitefield.FinitePrimeFieldElement(coefficient[0],self.ch)
                        self.a2=finitefield.FinitePrimeFieldElement(coefficient[1],self.ch)
                        self.a3=finitefield.FinitePrimeFieldElement(coefficient[2],self.ch)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[3],self.ch)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],self.ch)
                        self.b2=self.a1**2+4*self.a2
                        self.b4=self.a1*self.a3+2*self.a4
                        self.b6=self.a3**2+4*self.a6
                        self.b8=self.a1**2*self.a6+4*self.a2*self.a6-self.a1*self.a3*self.a4+self.a2*self.a3**2-self.a4**2
                        self.c4=self.b2**2-24*self.b4
                        self.c6=-self.b2**3+36*self.b2*self.b4-216*self.b6
                        self.disc=-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6
                        if self.disc.n==0:
                            raise ValueError, "singular curve (@_@)"
                        self.j=self.c4**3*self.disc.inverse()
                    elif len(self)==2:
                        self.a=finitefield.FinitePrimeFieldElement(coefficient[0],self.ch)
                        self.b=finitefield.FinitePrimeFieldElement(coefficient[1],self.ch)
                        self.a1=finitefield.FinitePrimeFieldElement(0,self.ch)
                        self.a2=finitefield.FinitePrimeFieldElement(0,self.ch)
                        self.a3=finitefield.FinitePrimeFieldElement(0,self.ch)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[0],self.ch)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[1],self.ch)
                        self.b2=finitefield.FinitePrimeFieldElement(0,self.ch)
                        self.b4=2*self.a
                        self.b6=4*self.b
                        self.b8=-self.a**2
                        self.c4=-48*self.a
                        self.c6=-864*self.b
                        self.disc=-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6
                        if self.disc.n==0:
                            raise ValueError, "singular curve (@_@)"
                        self.j=self.c4**3*self.disc.inverse()
                    else:
                        raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
                else:
                    raise ValueError, "characteristic must be 0 or prime (-_-;)"
        else:
            raise ValueError, "you must input (coefficient,list) m(__)m"
           
    def __len__(self):
        return len(self.coefficient)

    def __repr__(self):
        if self.ch==0:
            if len(self)==2 or self.a1==self.a2==self.a3==0:
                return "EC(["+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")" 
            else:
                return "EC(["+repr(self.a1)+","+repr(self.a2)+","+repr(self.a3)+","+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")"   
        else:
            if len(self)==2 or self.a1.n==self.a2.n==self.a3.n==0:
                return "EC(["+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"
            else:
                return "EC(["+repr(self.a1.n)+","+repr(self.a2.n)+","+repr(self.a3.n)+","+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"

    def __str__(self):
        if self.ch==0:
            return str(polynomial.MultiVariableSparsePolynomial({(0,2):1,(1,1):self.a1,(0,1):self.a3},["x","y"]))+"="+str(polynomial.MultiVariableSparsePolynomial({(3,0):1,(2,0):self.a2,(1,0):self.a4,(0,0):self.a6},["x","y"]))
        else:
            return str(polynomial.MultiVariableSparsePolynomial({(0,2):1,(1,1):self.a1.n,(0,1):self.a3.n},["x","y"]))+"="+str(polynomial.MultiVariableSparsePolynomial({(3,0):1,(2,0):self.a2.n,(1,0):self.a4.n,(0,0):self.a6.n},["x","y"]))

    def simple(self):
        """
        this transforms E:y^2+a1*x*y+a3*y=x^3+a2*x^2+a4*x+a6 to E':Y^2=X^3+(-27*c4)*X+(-54*c6),
        if ch is not 2 or 3
        """
        if self.ch==0:
            if len(self)==2 or (self.a1==self.a2==self.a3==0):
                return self
            else:
                other=EC([-27*self.c4,-54*self.c6],self.ch)
                return other
        else:
            if len(self)==2 or (self.a1.n==self.a2.n==self.a3.n==0):
                return self
            else:
                if self.ch==2 or self.ch==3:
                    return self
                else:
                    other=EC([-27*self.c4.n,-54*self.c6.n],self.ch)
                    return other

    def changeCurve(self,V):
        """
        this transforms E to E' by V=[u,r,s,t] ; x->u^2*x'+r,y->u^3*y'+s*u^2*x'+t 
        """
        if isinstance(V,list): 
            if len(V)==4:
                if V[0]!=0:
                    if self.ch==0:
                        other=EC([rational.Rational(self.a1+2*V[2],V[0]),
                              rational.Rational(self.a2-V[2]*self.a1+3*V[1]-V[2]**2,V[0]**2),
                              rational.Rational(self.a3+V[1]*self.a1+2*V[3],V[0]**3),
                              rational.Rational(self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4),
                              rational.Rational(self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1,V[0]**6)],0) 
                        return other
                    else:
                        for v in V:
                            if not isinstance(v,(int,long)):
                                raise ValueError, "you must input integer m(__)m"
                        v=finitefield.FinitePrimeFieldElement(V[0],self.ch).inverse()
                        other=EC([(self.a1+2*V[2])*v.n,
                                  ((self.a2-V[2]*self.a1+3*V[1]-V[2]**2)*v**2).n,
                                  ((self.a3+V[1]*self.a1+2*V[3])*v**3).n,
                                  ((self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3])*v**4).n,
                                  ((self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1)*v**6).n],self.ch)
                        return other
                else: 
                    raise ValueError, "you must input nonzero u (-_-;)"
            else:        
                raise ValueError, "you must input (-_-;)"
        else:
            raise ValueError, "you must input (change,list) m(__)m"

    def changePoint(self,P,V):
        """
        this transforms P to P' by V=[u,r,s,t] ; x->u^2*x'+r,y->u^3*y'+s*u^2*x'+t
        """
        if isinstance(P,list) and isinstance(V,list):
            if len(P)==2 and len(V)==4 and V[0]!=0:
                if self.ch==0:
                    Q0=rational.IntegerIfIntOrLong(P[0]-V[1])/rational.IntegerIfIntOrLong(V[0]**2)
                    Q1=rational.IntegerIfIntOrLong(P[1]-V[2]*(P[0]-V[1])-V[3])/rational.IntegerIfIntOrLong(V[0]**3)
                else:
                    if self.index!=1:
                        raise NotImplementedError,"Now making (>_<)"
                    v=finitefield.FinitePrimeFieldElement(V[0],self.ch).inverse()
                    Q0=((P[0]-V[1])*v**2).n
                    Q1=((P[1]-V[2]*(P[0]-V[1])-V[3])*v**3).n
                Q=[Q0,Q1]
                return Q
            else:
                raise ValueError, "(-_-;)"
        else:
            raise ValueError, "m(__)m"

    def point(self): 
        """
        this returns a random point on eliiptic curve over ch(field)>3
        """
        if self.ch!=0:
            if self.index!=1:
                raise NotImplementedError,"Now making (>_<)"
            if len(self)==2 or (self.a1.n==self.a2.n==self.a3.n==0):    
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) 
                    t=(s**3+self.a4*s+self.a6).n
                return [s,arith1.sqroot(t,self.ch)]
            elif self.ch!=2 and self.ch!=3:
                other=self.simple()
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) 
                    t=(s**3+other.a*s+other.b).n
                x=(s-3*self.b2)/36
                y=(rational.Rational(arith1.sqroot(t,self.ch),108)-self.a1*x-self.a3)/2
                return [x.n,y.n]
            elif self.ch==3:
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) 
                    t=(s**3+self.a2*s**2+self.a4*s+self.a6).n
                return [s,arith1.sqroot(t,self.ch)]
            else: 
                s=0
                while self.coordinateY(s) is ValueError:
                    s=random.randrange(0,self.ch)
                return [s,self.coordinateY(s)]
        else:
            i=0
            while i<100:
                w=int(random.random()*10**3)
                s=random.randrange(1,w)
                t=random.randrange(1,w)
                y=self.coordinateY(rational.Rational(s,t))
                if y!=False:
                    return [s,self.coordinateY(s)]
                i=i+1
            raise ValueError,"I can't find m(__)m"

    def coordinateY(self,x):
        """ 
        this returns the y(P)>0,x(P)==x
        """
        if self.ch==0:
            y1=self.a1*x+self.a3
            y2=x**3+self.a2*x**2+self.a4*x+self.a6
        else:
            y1=self.a1.n*x+self.a3.n
            y2=x**3+self.a2.n*x**2+self.a4.n*x+self.a6.n
        if self.ch!=0 and self.ch!=2:
            if len(self)==2 or (self.a1.n==self.a2.n==self.a3.n==0):
                if arith1.legendre(y2,self.ch)>=0:
                    return arith1.sqroot(y2,self.ch)
                else:
                    return False
            else:
                if y1**2+4*y2>=0:
                    d=arith1.sqroot(y1**2+4*y2,self.ch)
                    return Element_p(rational.Rational(-y1-d,2),self.ch)
                else:
                    return False
        elif self.ch==2:
            raise NotImplementedError, "Now making (>_<)"
        else: 
            Y=y1**2+4*y2
            if Y>=0:
                if isinstance(Y,rational.Rational):
                    yn=Y.numerator
                    yn=math.sqrt(yn)
                    yd=Y.denominator
                    yd=math.sqrt(yd)
                    if int(yn)==yn and int(yd)==yd:
                        return rational.Rational((-1)*y1+rational.Rational(yn,yd),2)
                    else:
                        return False
                else: 
                    Z=math.sqrt(Y)
                    if int(Z)==Z:
                        return rational.Rational((-1)*y1+int(Z),2)
                    else:
                        return False
            else:
                return False

    def whetherOn(self,P):
        """
        Determine whether P is on curve or not.
        Return 1 if P is on, return 0 otherwise.
        """
        if isinstance(P,list):
            if len(P)==2:
                if self.ch==0:
                    if P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]==P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6:
                        return True
                    else:
                        print P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]
                        print P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6
                        return False
                else:
                    if self.index!=1:
                        raise NotImplementedError,"Now making (>_<)"
                    if P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]==P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6:
                        return True
                    else:
                        return False
            elif P==[0]:
                return True
            else:
                raise ValueError, "you must input (len(point)==2) (-_-;)"
        else:
            raise ValueError, "you must input (point,list) m(__)m"

    def add(self,P,Q):
        """
        this returns P+Q
        """
        if isinstance(P,list) and isinstance(Q,list):
            if self.whetherOn(P) and self.whetherOn(Q):
                if len(P)==len(Q)==2:
                    if self.ch==0:
                        if P[0]==Q[0]:
                            if P[1]+Q[1]+self.a1*Q[0]+self.a3==0:
                                return [0]
                            else: 
                                s=rational.IntegerIfIntOrLong(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1])/rational.IntegerIfIntOrLong(2*P[1]+self.a1*P[0]+self.a3)
                                t=rational.IntegerIfIntOrLong(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1])/rational.IntegerIfIntOrLong(2*P[1]+self.a1*P[0]+self.a3)
                        else: 
                            s=rational.IntegerIfIntOrLong(Q[1]-P[1])/rational.IntegerIfIntOrLong(Q[0]-P[0])
                            t=rational.IntegerIfIntOrLong(P[1]*Q[0]-Q[1]*P[0])/rational.IntegerIfIntOrLong(Q[0]-P[0])
                        x3=s**2+self.a1*s-self.a2-P[0]-Q[0]
                        y3=-(s+self.a1)*x3-t-self.a3
                        R=[x3,y3]
                        return R
                    else:
                        if self.index!=1:
                            raise NotImplementedError,"Now making (>_<)"
                        if P[0]==Q[0]:
                            if P[1]+Q[1]+self.a1*Q[0]+self.a3==0:
                                return [0]
                            else:
                                s=(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                                t=(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                        else:
                            s=(Q[1]-P[1]*finitefield.FinitePrimeFieldElement(1,self.ch))/(Q[0]-P[0])
                            t=(P[1]*Q[0]-Q[1]*P[0]*finitefield.FinitePrimeFieldElement(1,self.ch))/(Q[0]-P[0])
                        x3=s**2+self.a1*s-self.a2-P[0]-Q[0]
                        y3=-(s+self.a1)*x3-t-self.a3
                        R=[x3.n,y3.n]
                        return R
                elif (P==[0]) and (Q!=[0]):
                    return Q
                elif (P!=[0]) and (Q==[0]):
                    return P
                elif (P==[0]) and (Q==[0]):
                    return [0]
                else:
                    raise ValueError, "you must input (len(point)==2) (-_-;)"
            else:
                raise ValueError, "you must input point on curve (-_-;)"
        else:
            raise ValueError, "you must input (point,list) m(__)m"

    def sub(self,P,Q): 
        """
        this retuens P-Q
        """
        if isinstance(P,list) and isinstance(Q,list):
            if self.whetherOn(P) and self.whetherOn(Q):
                if len(P)==len(Q)==2:
                    x=Q[0]
                    if self.ch==0:
                        y=-Q[1]-self.a1*Q[0]-self.a3
                    else:
                        y=-Q[1]-self.a1.n*Q[0]-self.a3.n
                    R=[x,y] 
                    return self.add(P,R) 
                elif (P==[0]) and (Q!=[0]):
                    x=Q[0]
                    if self.ch==0:
                        y=-Q[1]-self.a1*Q[0]-self.a3
                    else:
                        y=-Q[1]-self.a1.n*Q[0]-self.a3.n
                    R=[x,y]
                    return R
                elif (P!=[0]) and (Q==[0]):
                    return P
                elif (P==[0]) and (Q==[0]):
                    return [0]
                else:
                    raise ValueError, "you must input (len(point)==2) (-_-;)"
            else:
                raise ValueError, "you must input point on curve (-_-;)"
        else:
            raise ValueError, "you must input (point,list) m(__)m"

    def mul(self,k,P):
        """
        this returns [k]*P
        """
        if k>=0:
            l=arith1.expand(k,2)
            Q=[0]
            for j in range(len(l)-1,-1,-1):
                Q=self.add(Q,Q)
                if l[j]==1:
                    Q=self.add(Q,P)
            return Q
        else:
            l=arith1.expand(-k,2)
            Q=[0]
            for j in range(len(l)-1,-1,-1):
                Q=self.add(Q,Q)
                if l[j]==1:
                    Q=self.add(Q,P)
            return self.sub([0],Q)

    def divPoly(self,Number=None):
        if self.ch==0:
            x=polynomial.OneVariableSparsePolynomial({1:1},['x'])
            y=polynomial.OneVariableSparsePolynomial({1:1},['y'])
        else:
            x=polynomial.OneVariableSparsePolynomial({1:1},['x'],finitefield.FinitePrimeField(self.ch))
            y=polynomial.OneVariableSparsePolynomial({1:1},['y'],finitefield.FinitePrimeField(self.ch))
        if not Number:
            if self.ch<=3:
                raise ValueError,"You must input (Number)"
            else:
                f={}
                f[-1]=polynomial.OneVariableSparsePolynomial({0:-1},['x'],finitefield.FinitePrimeField(self.ch))
                f[0]=polynomial.OneVariableSparsePolynomial({},["x"],finitefield.FinitePrimeField(self.ch))
                H=heart(self.ch**self.index)
                E=self.simple()
                e=4*(x**3+E.a*x+E.b)
                i=1
                while i<=H[-1]+1:
                    if i==1:
                        f[1]=polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(E.ch))
                    elif i==2:
                        f[2]=polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(E.ch))
                    elif i==3:
                        f[3]=3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                    elif i==4:
                        f[4]=2*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
                    else:
                        if i%2!=0:
                            j=(i-1)//2
                            if j%2!=0:
                                f[i]=f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                            else:
                                f[i]=e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                        else:
                            j=i//2
                            f[i]=(f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                    i=i+1
                i=-1
                while i<=H[-1]+1:
                    if i>1 and i%2==0:
                        f[i]=2*f[i]
                    i=i+1
                return f,H
        else: 
            f={}
            if self.ch==0:
                f[-1]=-1
                f[0]=0
                E=self.simple()
                e=x**3+E.a*x+E.b
                i=1
                while i<=Number:
                    if i==1:
                        f[1]=1
                    elif i==2:
                        f[2]=1
                    elif i==3:
                        f[3]=3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                    elif i==4:
                        f[4]=2*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
                    else:
                        if i%2!=0:
                            j=(i-1)//2
                            if j%2!=0:
                                f[i]=f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                            else:
                                f[i]=e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                        else:
                            j=i//2
                            f[i]=(f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                    i=i+1
                return f[Number]
            else:
                f[-1]=polynomial.OneVariableSparsePolynomial({0:-1},['x'],finitefield.FinitePrimeField(self.ch))
                f[0]=polynomial.OneVariableSparsePolynomial({},["x"],finitefield.FinitePrimeField(self.ch))
                e=4*x**3+self.b2*x**2+2*self.b4*x+self.b6
                i=1
                while i<=Number:
                    if i==1:
                        f[1]=polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(self.ch))
                    elif i==2:
                        f[2]=polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(self.ch))
                    elif i==3:
                        f[3]=3*x**4+self.b2*x**3+3*self.b4*x**2+3*self.b6*x+self.b8
                    elif i==4:
                        f[4]=2*x**6+self.b2*x**5+5*self.b4*x**4+10*self.b6*x**3+10*self.b8*x**2+(self.b2*self.b8-self.b4*self.b6)*x+self.b4*self.b8-self.b6**2
                    else:
                        if i%2!=0:
                            j=(i-1)//2
                            if j%2!=0:
                                f[i]=f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                            else:
                                f[i]=e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                        else:
                            j=i//2
                            f[i]=(f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                    i=i+1
                return f[Number]

    def Schoof(self):
        """
        this return t=p+1-#E(F_p)
        """
        if self.ch>3:
            if len(self)!=2:
                other=self.simple()
            else:
                other=self 
            E=polynomial.OneVariableSparsePolynomial({0:other.b,1:other.a,3:1},['x'],finitefield.FinitePrimeField(other.ch))
            x=polynomial.OneVariableSparsePolynomial({1:1},["x"],finitefield.FinitePrimeField(other.ch)) 
            T=[]
            D=other.divPoly()
            L=D[1]
            D=D[0]
            i=0
            M=1
            while i<len(L):
                j=L[i]
                M=M*j
                u=PolyPow(x,other.ch,D[j]) #u=x^q
                v=PolyPow(u,other.ch,D[j]) #v=x^{q^2}
                g0=PolyPow(E,int((other.ch-1)/2),D[j]) #y^(q-1)
                k=other.ch%j
                f0=PolyMulRed([D[k-1],D[k+1]],D[j])
                f3=PolyMulRed([D[k],D[k]],D[j])
                if k%2==0:
                    f=v-x
                    P=GCD(PolyMulRed([f,E,f3],D[j])+f0,D[j])
                else:
                    f=v-x
                    P=GCD(PolyMulRed([f,f3],D[j])+PolyMulRed([f0,E],D[j]),D[j])
                if P!=1:
                    if arith1.legendre(other.ch,j)==-1:
                        T.append((0,j))
                        print T,"$"
                    else:
                        w=arith1.sqroot(k,j)
                        if w%2==0:
                            P=GCD(PolyMulRed([u-x,D[w],D[w],E],D[j])+PolyMulRed([D[w-1],D[w+1]],D[j]),D[j])
                        else:
                            P=GCD(PolyMulRed([u-x,D[w],D[w]],D[j])+PolyMulRed([D[w-1],D[w+1],E],D[j]),D[j])
                        if P!=1:
                            if w%2==0:
                                P=GCD(PolyMulRed([4,PolyMulRed([g0,E],D[j]),PolyPow(D[w],3,D[j])],D[j])-PolyMulRed([D[w-1],D[w-1],D[w+2]],D[j])+PolyMulRed([D[w-2],D[w+1],D[w+1]],D[j]),D[j])
                            else: 
                                P=GCD(PolyMulRed([4,g0,PolyPow(D[w],3,D[j])],D[j])-PolyMulRed([D[w-1],D[w-1],D[w+2]],D[j])+PolyMulRed([D[w-2],D[w+1],D[w+1]],D[j]),D[j])
                            if P!=1:
                                T.append((2*w,j))
                                print T,"$$"
                            else:
                                T.append((-2*w,j))
                                print T,"$$$"
                        else:
                            T.append((0,j))
                            print T,"$$$$"
                else:
                    X=v+u+x
                    Y=x-v
                    Z=-2*v-x
                    f1=PolyMulRed([D[k-1],D[k-1],D[k+2]],D[j])
                    f2=PolyMulRed([D[k-2],D[k+1],D[k+1]],D[j])
                    g1=PolyPow(g0,int(other.ch+1),D[j]) #y^(q^2-1)
                    if k%2==0:
                        g2=PolyMulRed([g1,E,E],D[j])
                        f=f1-f2-4*PolyMulRed([g2,f3,D[k]],D[j])
                        g=(PolyMulRed([Y,E,f3],D[j])-f0)*4
                        h0=PolyMulRed([g,g],D[j])
                        h1=PolyMulRed([f,f],D[j])
                        X_d=PolyMulRed([E,f3,h0],D[j])
                        X_n=PolyMulRed([X_d,X],D[j])-PolyMulRed([f0,h0],D[j])-h1
                    else:
                        f=f1-f2-4*PolyMulRed([g1,f3,D[k]],D[j])
                        g=(PolyMulRed([Y,f3],D[j])-PolyMulRed([E,f0],D[j]))*4
                        h0=PolyMulRed([g,g],D[j])
                        h1=PolyMulRed([f,f],D[j])
                        X_d=PolyMulRed([f3,h0],D[j])
                        X_n=PolyMulRed([X_d,X],D[j])-PolyMulRed([E,f0,h0],D[j])-PolyMulRed([E,h1],D[j])
                    t=1
                    while t<=(j-1)/2:
                        if t%2==0:
                            Z_d_x=PolyPow(PolyMulRed([E,D[t],D[t]],D[j]),other.ch,D[j])
                            Z_n_x=PolyPow(PolyMulRed([D[t-1],D[t+1]],D[j]),other.ch,D[j])
                        else:
                            Z_d_x=PolyPow(PolyMulRed([D[t],D[t]],D[j]),other.ch,D[j])
                            Z_n_x=PolyPow(PolyMulRed([E,D[t-1],D[t+1]],D[j]),other.ch,D[j])
                        P=PolyMulRed([X_n,Z_d_x],D[j])-PolyMulRed([X_d,Z_n_x],D[j])
                        if P==0:
                            if k%2==0:
                                Y_d=PolyMulRed([E,D[k],g,X_d],D[j])
                                y0=PolyMulRed([Z,X_d],D[j])+PolyMulRed([f0,h0],D[j])+h1
                                Y_n=-PolyMulRed([g1,Y_d],D[j])-PolyMulRed([f,y0],D[j])
                                if t%2==0:
                                    Z_d_y=PolyPow(PolyMulRed([4,E,E,D[t],D[t],D[t]],D[j]),other.ch,D[j])
                                    z0=PolyPow(PolyMulRed([D[t-1],D[t-1],D[t+2]],D[j])-PolyMulRed([D[t-2],D[t+1],D[t+1]],D[j]),other.ch,D[j])
                                    Z_n_y=PolyMulRed([g0,z0],D[j])
                                else:
                                    Z_d_y=PolyPow(PolyMulRed([4,D[t],D[t],D[t]],D[j]),other.ch,D[j])
                                    z0=PolyPow(PolyMulRed([D[t-1],D[t-1],D[t+2]],D[j])-PolyMulRed([D[t-2],D[t+1],D[t+1]],D[j]),other.ch,D[j])
                                    Z_n_y=PolyMulRed([g0,z0],D[j])
                            else:
                                Y_d=PolyMulRed([D[k],g,X_d],D[j])
                                y0=PolyMulRed([Z,X_d],D[j])+PolyMulRed([E,f0,h0],D[j])+PolyMulRed([E,h1],D[j])
                                Y_n=-PolyMulRed([g1,Y_d],D[j])-PolyMulRed([f,y0],D[j])
                                if t%2==0:
                                    Z_d_y=PolyPow(PolyMulRed([4,E,E,D[t],D[t],D[t]],D[j]),other.ch,D[j])
                                    z0=PolyPow(PolyMulRed([D[t-1],D[t-1],D[t+2]],D[j])-PolyMulRed([D[t-2],D[t+1],D[t+1]],D[j]),other.ch,D[j])
                                    Z_n_y=PolyMulRed([g0,z0],D[j])
                                else:
                                    Z_d_y=PolyPow(PolyMulRed([4,D[t],D[t],D[t]],D[j]),other.ch,D[j])
                                    z0=PolyPow(PolyMulRed([D[t-1],D[t-1],D[t+2]],D[j])-PolyMulRed([D[t-2],D[t+1],D[t+1]],D[j]),other.ch,D[j])
                                    Z_n_y=PolyMulRed([g0,z0],D[j])
                            Q=PolyMulRed([Y_n,Z_d_y],D[j])-PolyMulRed([Y_d,Z_n_y],D[j])
                            if Q==0:
                                T.append((t,j))
                                print T,"@"
                                break
                            else:
                                T.append((j-t,j))
                                print T,"@@"
                                break
                        t=t+1
                        if t>(j-1)/2:
                            T.append((0,j))
                            print T,"@@@"
                i=i+1
            tau=arith1.CRT(T)
            if tau>M/2:
                tau=tau-M
            return tau
        elif self.ch==2:
            raise NotImplementedError, "Now making (>_<)"
        else:
            raise NotImplementedError, "Now making (>_<)"

    def step(self,P,W):
        """
        this use only for Shanks_Mestre,
        """
        L=[]
        A=[]
        B=[]
        i=0
        Q=self.mul(self.ch+1,P)
        while i<W:
            A.append(Q[0])
            Q=self.add(Q,P)
            i=i+1
        L.append(A)
        j=0
        Q=[0]
        R=self.mul(W,P)
        while j<=W:
            B.append(Q[0])
            Q=self.add(Q,R)
            j=j+1
        L.append(B)
        L.append(sets.Set(A).intersection(sets.Set(B)))
        return L
            
    def Shanks_Mestre(self):
        import sets
        """
        This program is using
        Algorithm 7.5.3(Shanks-Mestre assessment of curve order)
        Crandall & Pomerance ,PRIME NUMBERS
        self.ch<=10**5+o(1)
        This returns t=self.ch+1-#E(F_p)
        """
        if self.ch>3:
            if self.ch<=229:
                if len(self)!=2:
                    other=self.simple()
                else:
                    other=self
                k=0
                for i in range(0,other.ch):
                    k=k+arith1.legendre(i*(i**2+other.a.n)+other.b.n,other.ch)
                return -k
            else: #E.ch>229
                if len(self)!=2:
                    other=self.simple()
                else:
                    other=self
                g=0
                while arith1.legendre(g,other.ch)!=-1:
                    g=random.randint(2,other.ch-1)
                W=int(math.sqrt(math.sqrt(other.ch))*math.sqrt(2))+1
                c,d=g**2*other.a,g**3*other.b
                f=polynomial.OneVariableDensePolynomial([other.b,other.a,0,1],"X",finitefield.FinitePrimeField(other.ch))
                BOX=[]
                i=0
                while i<other.ch:
                    BOX.append(1)
                    i=i+1
                k=0
                while k==0:
                    x=random.randint(0,other.ch-1)
                    while BOX[x]==0 or arith1.legendre(f(x).n,other.ch)==0:
                        BOX[x]=0
                        x=random.randint(0,other.ch-1)
                    BOX[x]=0
                    if arith1.legendre(f(x).n,other.ch)==1:
                        E=other
                        cg=1
                    else: #arith1.legendre(f(cg),other.ch)==-1
                        E=EC([c.n,d.n],other.ch)
                        cg=-1
                        x=g*x%E.ch
                    P=[x,E.coordinateY(x)]
                    L=E.step(P,W)
                    A=L[0]
                    B=L[1]
                    S=L[2]
                    if len(S)==1:
                        s=S.pop()
                        if B.count(s)<=2:
                            k=1
                aa=A.index(s)
                bb=B.index(s)
                t=aa-bb*W
                if E.mul(E.ch+1+t,P)==[0]:
                    return -cg*t
                else:
                    t=aa+bb*W
                    return -cg*t
        else:
            raise NotImplementedError,"Now making m(__)m"

    def naive(self):
        if self.ch>3:
            other=self.simple()
            k=0
            for i in range(0,other.ch):
                k=k+arith1.legendre(i*(i**2+other.a.n)+other.b.n,other.ch)
            return -k
        else:
            raise NotImplementedError,"Now making m(__)m"

    def order(self,flag=None):
        """
        this returns #E(Fp)
        if flag==0: #E/F_p
        else:#E/F_{p^r}, E is defind over F_p
        """
        if self.ch<=3:
            raise NotImplementedError,"Now making m(__)m"
        elif self.ch<10**4:
            if not flag:
                return self.ch+1-self.naive()
            else:
                return pow(self.ch,flag)+1-powOrd(self.naive(),flag,self.ch)
        elif self.ch<10**30:
            if not flag:
                return self.ch+1-self.Shanks_Mestre()
            else:
                return pow(self.ch,flag)+1-powOrd(self.Shanks_Mestre(),flag,self.ch)
        else: # self.ch>=10**30
            if not flag:
                return self.ch+1-self.Schoof()
            else:
                return pow(self.ch,flag)+1-powOrd(self.Schoof(),flag,self.ch)

    def line(self,P,Q=None):
        """
        this use to compute weil pairing
        isinstance((P,Q),list),P,Q \in E
        over F_p
        self is E_{a,b}
        """
        p=self.ch
        if p>3:
            if self.index==1:
                x=polynomial.OneVariableSparsePolynomial({1:1},["x"],finitefield.FinitePrimeField(p))
                y=polynomial.OneVariableSparsePolynomial({1:1},["y"],finitefield.FinitePrimeField(p))
                if not Q:
                    if P!=[0]:
                        return 1,x-finitefield.FinitePrimeFieldElement(P[0],p)
                    else:
                        return 0,x(1)
                else:
                    if P==Q:
                        if P==[0]:
                            return 0,x(1)
                        s=finitefield.FinitePrimeFieldElement(P[0],p)
                        t=finitefield.FinitePrimeFieldElement(P[1],p)
                        f=(3*s**2+self.a)*(x-s)-2*t*(y-t)
                        if isinstance(f,(int,finitefield.FinitePrimeFieldElement)):
                            return 0,f
                        elif len(f.variable)==2:
                            return 2,f
                        elif 'x' in f.variable:
                            return 1,f
                        else:
                            return -1,f
                    elif P==[0] or Q==[0]:
                        if P==[0]:
                            return 1,x-finitefield.FinitePrimeFieldElement(Q[0],p)
                        else:
                            return 1,x-finitefield.FinitePrimeFieldElement(P[0],p)
                    elif P[0]==Q[0]:
                        f=x-finitefield.FinitePrimeFieldElement(P[0],p)
                        return 1,f
                    else:
                        Q=finitefield.FinitePrimeFieldElement(Q[0],p),finitefield.FinitePrimeFieldElement(Q[1],p)
                        s=finitefield.FinitePrimeFieldElement(P[0],p)
                        t=finitefield.FinitePrimeFieldElement(P[1],p)
                        f=(Q[0]-s)*(x-s)+(Q[1]-t)-(y-t)*(Q[0]-s)
                        if isinstance(f,(int,finitefield.FinitePrimeFieldElement)):#
                            return 0,f
                        elif len(f.variable)==2:
                            return 2,f
                        elif 'x' in f.variable:
                            return 1,f
                        else:
                            return -1,f
            else:
                raise NotImplementedError,"Now making m(__)m"
        else:
            raise NotImplementedError,"Now making m(__)m"

    def Miller(self,P,m,Q):
        """
        this returns value of function
        with divisor f_p(Q)
        this use for compute Weil/Tate pairing
        self is E_{a,b}
        """
        if self.ch>3 and self.index==1:
            if P==Q==[0] or Q==[0]:
                raise ValueError,"You must input not [0]"
            m=arith1.expand(m,2)
            f=finitefield.FinitePrimeFieldElement(1,self.ch)
            V=P
            i=len(m)-1
            while i>=0:
                l=self.line(V,V)
                if l[0]==0:
                    f_n=l[1]
                elif l[0]==1:
                    f_n=l[1](Q[0])
                elif l[0]==-1:
                    f_n=l[1](Q[1])
                else:
                    f_n=l[1](x=Q[0],y=Q[1])
                V=self.mul(2,V)
                l=self.line(V)
                if l[0]==0:
                    f_d=l[1]
                else:
                    f_d=l[1](Q[0])
                if f_d==0:
                    return False
                f=f**2*f_n/f_d
                if m[i]==1:
                    l=self.line(V,P)
                    if l[0]==0:
                        f_n=l[1]
                    elif l[0]==1:
                        f_n=l[1](Q[0])
                    elif l[0]==-1:
                        f_n=l[1](Q[1])
                    else:
                        f_n=l[1](x=Q[0],y=Q[1])
                    V=self.add(V,P)
                    l=self.line(V)
                    if l[0]==0:
                        f_d=l[1]
                    else:
                        f_d=l[1](Q[0])
                    if f_d==0:
                        return False
                    f=f*f_n/f_d
                i=i-1
            return f

    def WeilPairing(self,m,P,Q):
        i=1
        while i<math.log(self.ch,2):
            T=[0]
            U=[0]
            A=[0]
            B=[0]
            while T==[0] or U==[0] or A==[0] or B==[0]: 
                T,U=self.point(),self.point()
                A=self.add(P,T) 
                B=self.add(Q,U)
            g=self.Miller(P,m,B)
            if g!=False and g!=0:
                G=self.Miller(Q,m,T)
                if G!=False and G!=0:
                    h=self.Miller(Q,m,A)
                    if h!=False and h!=0:
                        H=self.Miller(P,m,U)
                        if H!=False and H!=0:
                            return g*G/h*H
            i=i+1
        return False

    def BSGS(self,n,P,Q):
        """
        retruns k such that Q=kP
        P,Q is the elements of the same group
        """
        B=[]
        m=int(math.sqrt(n))+1
        R=Q
        B.append(Q)
        i=1
        while i<=m:
            R=self.sub(R,P)
            if R==[0]:
                return i
            B.append(R)
            i=i+1
        R=self.mul(m,P)
        P=R
        if R in B:
            return m+B.index(R)
        else:
            i=2
            while i<=m:
                R=self.add(R,P)
                if R in B:
                    return i*m+B.index(R)
                i=i+1
            if self.mul(n,P)==Q:
                return n
            else:
                return False

    def allPoint(self,O):
        if self.ch>3 and self.index==1:
            p=self.ch
            x=polynomial.OneVariableSparsePolynomial({1:1},["x"],finitefield.FinitePrimeField(p))
            other=self.simple()
            Y=x**3+other.a*x+other.b
            L=[]
            i=0
            while i<p:
                y=Y(i).n
                if arith1.legendre(y,p)==1:
                    Q=[i,arith1.sqroot(y,p)]
                    R=[i,p-Q[1]]
                    q=other.BSGS(O,Q,[0])
                    r=other.BSGS(O,R,[0])
                    if q==O or r==O:
                        return (O,1)
                    else:
                        L.append(q)
                        L.append(r)
                i=i+1
            L=max(L)
            return (L,O//L)
    
    def structure(self):
        if self.ch>3:
            if self.index==1:
                other=self.simple()
                N=other.order()
                if prime.primeq(N):
                    return (1,N)
                N0=gcd.gcd(other.ch-1,N)
                if N0==N:
                    return (1,N)
                N1,N2=N0,N//N0
                N0=gcd.gcd(N1,N2)
                N1,N2=N1*N0,N2//N0
                P1=[0]
                P2=[0]
                k=1
                while k<=10:
                    while P1==[0] or P2==[0]:
                        P1,P2=other.point(),other.point()
                    P1,P2=other.mul(N2,P1),other.mul(N2,P2)
                    if P1==P2==[0]:
                        ord1=1
                        ord2=1
                    elif P1==[0] and P2!=[0]:
                        ord1=1
                        ord2=other.BSGS(N,P2,[0])
                    elif P1!=[0] and P2==[0]:
                        ord1=other.BSGS(N,P1,[0])
                        ord2=1
                    else:
                        ord1=other.BSGS(N,P1,[0])
                        ord2=other.BSGS(N,P2,[0])
                    r=gcd.lcm(ord1,ord2)
                    e=other.WeilPairing(r,P1,P2)
                    if e==False:
                        pass
                    else:
                        s=1
                        if e!=finitefield.FinitePrimeFieldElement(1,self.ch):
                            D=divi(self.ch-1)
                            j=e
                            i=0
                            while j!=finitefield.FinitePrimeFieldElement(1,self.ch):
                                j=e
                                i=i+1
                                j=pow(j,D[i])
                            s=D[i]
                        if r*s==N1: 
                            return (r*N2,s)
                    k=k+1
                return self.allPoint(N)
            else:
                raise NotImplementedError,"Now making m(__)m"
        else:
            raise NotImplementedError,"Now making m(__)m"
        
