from __future__ import division
import arith1
import cmath
import factor
import finitefield
#import imaginary
import integerResidueClass
import math
import polynomial 
import prime
import random
import rational

def Element_p(a,p):
    """
    a is (rational,int,long) number
    this returns a in F_p
    """
    return int(finitefield.FinitePrimeFieldElement(a,p).n)#.createElement(a).n

def PolyMod(f,g):
    """
    return f (mod g)
    """
    if isinstance(g,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
        return 0
    elif isinstance(f,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
        return f
    else:
        return f%g

def GCD(f,g):
    if f==0 and g!=0:
        return g
    elif g==0 and f!=0:
        return f
    elif isinstance(f,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
        return 1
    elif isinstance(g,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
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
        elif isinstance(list[i],(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
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
        if isinstance(POLY,(int,long,finitefield.FinitePrimeFieldElement,integerResidueClass.IntegerResidueClass)): ##
            pass
        else:
            if POLY.degree()>=poly.degree():
                POLY=PolyMod(POLY,poly)
                if POLY==0:
                    return 0
        i=i+1
    return POLY

# t=imaginary.Complex(a,b)
#
#def q(t):
#    """
#    this returns exp(2*pi*j*t)
#    t is complex and h.imag>0
#    """
#    Return cmath.exp(2*cmath.pi*1j*t)
#
#def delta(t,x):
#    """
#    """
#    qt=q(t)
#    def a(i):
#        if i%2==0:
#            return qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2)
#        else:
#            return (-1)*(qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2))
#    i=1
#    b=0
#    while abs(a(i+1))>x: #syuusoku
#       b=a(i)+b
#       print i #
#       i=i+1
#    return qt*(1+b)**24
#
#def h(t,x):
#    """
#    """
#    return delta(2*t,x)/delta(t,x)
#
#def j(t,x):
#    """
#    """
#    return (256*h(t,x)+1)**3/h(t,x)
#    
#def nu(t,x):
#    """
#    """
#    qt=q(t)
#    qq=cmath.exp(cmath.pi*1j/12)
#    def a(i):
#        if i%2==0:
#            return qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2)
#        else:
#            return (-1)*(qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2))
#    i=1
#    b=0
#    while abs(a(i+1))>x: # one time we caluculate a(i+1),so waste more time??
#       b=a(k)+b #### miss ,if k==i !
#       i=i+1
#    return qq*(1+b)
        
class EC:
    """
    Elliptic curves over Q and Fp.
    # If you wanna use over other fields, just a moment please :-)
    """
    def __init__(self,coefficient,character,index=None):
        """
        Initialize an elliptic curve. If coefficient has 5 elements,
        it represents E:y**2+a1*x*y+a3*y=x**3+a2*x**2+a4*x+a6 or 2
        elements, E:y*2=x*3+a*x+b.
        """
        if isinstance(coefficient,list):
            self.coefficient=coefficient
            self.ch=character 
            if self.ch==0: #complex
                pass
                #self.coeffField=
            else:
                if not index: #field=F_p
                    self.coeffField=finitefield.FinitePrimeField(character)
                    self.index=1
                elif index==0:
                    raise ValueError,"you must input(index \in Z>0) (-_-;)"
                elif index==1:
                    self.coeffField=finitefield.FinitePrimeField(character)
                    self.index=1
                else: #field=F_q,q=p^r
                    self.coeffField=finitefield.FinitePrimeField(character) ##
                    self.index=index
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
                    if not isinstance(coefficient[i],(int,long)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if len(self)==5:
                    if coefficient[0]%2==1 and coefficient[2]%2==coefficient[3]%2==0:
                        self.a1=finitefield.FinitePrimeFieldElement(1,2) 
                        self.a2=finitefield.FinitePrimeFieldElement(coefficient[1],2)
                        self.a3=finitefield.FinitePrimeFieldElement(0,2) 
                        self.a4=finitefield.FinitePrimeFieldElement(0,2) 
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],2)
                        self.disc=self.a6
                        if self.disc.n!=0:
                            self.j=a6.inverse()
                    elif coefficient[0]%2==coefficient[1]%2==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,2)
                        self.a2=finitefield.FinitePrimeFieldElement(0,2)
                        self.a3=finitefield.FinitePrimeFieldElement(coefficient[2],2)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[3],2)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],2)
                        self.disc=self.a3**4%2
                        self.j=finitefield.FinitePrimeFieldElement(0,2)
                    else:
                        raise ValueError, "can't defined EC (-_-;)"
                    if self.disc.n==0:
                        raise ValueError, "singular curve (@_@)"
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
            elif self.ch==3: # y^2=x^3+a2*x^2+a6 or y^2=x^3+a4*x+a6
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if len(self)==5:
                    if coefficient[0]%3==coefficient[2]%3==coefficient[3]%3==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,3)
                        self.a2=finitefield.FinitePrimeFieldElement(coefficient[1],3)
                        self.a3=finitefield.FinitePrimeFieldElement(0,3)
                        self.a4=finitefield.FinitePrimeFieldElement(0,3)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],3)
                        self.disc=-self.a2**3*self.a6
                        if self.disc.n!=0:
                            self.j=(-self.a2**3)*self.a6.inverse()
                    elif coefficient[0]==coefficient[1]==coefficient[2]==0:
                        self.a1=finitefield.FinitePrimeFieldElement(0,3)
                        self.a2=finitefield.FinitePrimeFieldElement(0,3)
                        self.a3=finitefield.FinitePrimeFieldElement(0,3)
                        self.a4=finitefield.FinitePrimeFieldElement(coefficient[3],3)
                        self.a6=finitefield.FinitePrimeFieldElement(coefficient[4],3)
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
                    if not isinstance(coefficient[i],(int,long)):
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
                            raise ValueError, "singuler curve (@_@)"
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
                            raise ValueError, "singuler curve (@_@)"
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
            raise ValueError, "you must input (,list) m(__)m"

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
                    t=s**3+self.a4*s+self.a6
                return [s,arith1.sqroot(t,self.ch)]
            elif self.ch!=2 and self.ch!=3:
                other=self.simple()
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) 
                    t=s**3+other.a*s+other.b
                x=(s-3*self.b2)/36
                y=(rational.Rational(arith1.sqroot(t,self.ch),108)-self.a1*x-self.a3)/2
                return [x.n,y.n]
            elif self.ch==3:
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) 
                    t=s**3+self.a2*s**2+self.a4*s+self.a6
                return [s,arith1.sqroot(t,self.ch)]
            else: 
                s=0
                while self.coordinateX(s) is ValueError:
                    s=random.randrange(0,self.ch)
                return [s,self.coordinateX(s)]
        else: 
            w=int(random.random()*10**3)
            s=random.randrange(1,w)
            return [s,self.coordinateX(s)]

    def coordinateX(self,x):
        """ 
        this returns the y(P)>0,x(P)==x
        """
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
            if y1**2+4*y2>=0:
                return rational.Rational((-1)*y1+math.sqrt(y1**2+4*y2),2)
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
                        return False
                else:
                    if self.index!=1:
                        raise NotImplementError,"Now making (>_<)"
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
                            raise NotImplementError,"Now making (>_<)"
                        if P[0]==Q[0]:
                            if P[1]+Q[1]+self.a1*Q[0]+self.a3==0:
                                return [0]
                            else:
                                s=(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                                t=(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                        else:
                            P0=finitefield.FinitePrimeFieldElement(P[0],self.ch).inverse()
                            P1=finitefield.FinitePrimeFieldElement(P[1],self.ch).inverse()
                            s=(Q[1]-P[1])/(Q[0]-P[0])
                            t=(P[1]*Q[0]-Q[1]*P[0])/(Q[0]-P[0])
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

    def lattice(self):
        raise NotImplementedError,"Now making (>_<)"

    def divPoly(self,default=0,Number=None):
        if self.ch==0:
            x=polynomial.OneVariableSparsePolynomial({1:1},['x'])
            y=polynomial.OneVariableSparsePolynomial({1:1},['y'])
        else:
            x=polynomial.OneVariableSparsePolynomial({1:1},['x'],finitefield.FinitePrimeField(self.ch))
            y=polynomial.OneVariableSparsePolynomial({1:1},['y'],finitefield.FinitePrimeField(self.ch))
        def change(poly,i,e,p):
            """
            poly is multi
            """
            L=poly.coefficient.items()
            if i%2==0:
                t=0
                if self.ch==0:
                    poly=0
                else:
                    poly=finitefield.FinitePrimeFieldElement(0,p)
                while t<len(L): # y^2->e
                    k=L[t][0][1]
                    if k%2==0:
                        k=k//2
                        poly=poly+e**k*L[t][1]*x**L[t][0][0]
                    else:
                        k=(k-1)//2
                        poly=poly+y*e**k*L[t][1]*x**L[t][0][0]
                    t=t+1
                L=poly.coefficient.items()
                t=0
                dict={}
                while t<len(L):
                    dict[(L[t][0][0],L[t][0][1]-1)]=L[t][1]
                    t=t+1
                poly.coefficient=dict
            else: #y^2->e
                t=0
                if self.ch==0:
                    poly=0
                else:
                    poly=finitefield.FinitePrimeFieldElement(0,p)
                while t<len(L):
                    k=L[t][0][1]//2
                    poly=poly+e**k*L[t][1]*x**L[t][0][0]
                    t=t+1
            return poly.toOneVariableSparsePolynomial()
        if not Number:
            def heart(q):
                l=[]
                i=3
                j=1
                while j<=4*int(math.sqrt(q)):
                    if prime.primeq(i):
                        l.append(i)
                        j=j*i
                    i=i+2
                return l
            if self.ch==0 and self.ch==3:
                raise ValueError,"You must imput (Nunber)"
            elif self.ch==2: 
                f={}
                M={}
                f[-1]=finitefield.FinitePrimeFieldElement(-1,2)
                M[-1]=finitefield.FinitePrimeFieldElement(-1,2)
                f[0]=finitefield.FinitePrimeFieldElement(0,2)
                M[0]=finitefield.FinitePrimeFieldElement(0,2)
                if default==0:
                    H=heart(self.ch)
                else:
                    H=heart(self.ch**self.index)
                i=1
                while i<=H[-1]+1:
                    if i==1:
                        f[1]=finitefield.FinitePrimeFieldElement(1,2)
                        M[1]=finitefield.FinitePrimeFieldElement(1,2)
                    elif i==2:
                        f[2]=x
                        M[2]=x
                    elif i==3:
                        f[3]=x**4+x**3+self.a6
                        M[3]=x**4+x**3+self.a6
                    elif i==4:
                        f[4]=x**6+self.a6*x**2
                        M[4]=x**6+self.a6*x**2
                    else:
                        if i%2!=0:
                            j=(i-1)//2
                            f[i]=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                            M[i]=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                        else:
                            j=i//2
                            g=(f[j+2]*f[j-1]*f[j-1]+f[j-2]*f[j+1]*f[j+1])*f[j]
                            L=g.coefficient.getAsDict().items()
                            t=0
                            dict={}
                            while t<len(L):
                                dict[L[t][0][0]-1]=finitefield.FinitePrimeFieldElement(L[t][1],2)
                                t=t+1
                            g.coefficient=dict
                            f[i]=g
                            M[i]=g
                    i=i+1
                return M,H
            else:
                f={}
                M={}
                f[-1]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(-1,self.ch)},["x","y"])
                M[-1]=polynomial.OneVariableSparsePolynomial({0:-1},['x'],finitefield.FinitePrimeField(self.ch))
                f[0]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(0,self.ch)},["x","y"])
                M[0]=polynomial.OneVariableSparsePolynomial({},["x"],finitefield.FinitePrimeField(self.ch))
                if default==0: 
                    H=heart(self.ch) 
                else: 
                    H=heart(self.ch**self.index) 
                E=self.simple()
                e=x**3+E.a*x+finitefield.FinitePrimeFieldElement(E.b,E.ch)
                i=1
                while i<=H[-1]+1:
                    if i==1:
                        f[1]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(1,self.ch)},["x","y"])
                        M[1]=polynomial.OneVariableSparsePolynomial({0:1},['x'],finitefield.FinitePrimeField(E.ch))
                    elif i==2:
                        f[2]=2*y
                        M[2]=polynomial.OneVariableSparsePolynomial({0:2},['x'],finitefield.FinitePrimeField(E.ch))
                    elif i==3:
                        g=3*x**4+6*E.a*x**2+12*E.b*x-finitefield.FinitePrimeFieldElement(E.a,E.ch)**2
                        f[3]=g
                        M[3]=g.toOneVariableSparsePolynomial()
                    elif i==4:
                        g=4*y*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-finitefield.FinitePrimeFieldElement(E.a,E.ch)**3-finitefield.FinitePrimeFieldElement(8,E.ch)*E.b**2)
                        f[4]=g
                        g=change(g,i,e,E.ch)
                        M[4]=polynomial.OneVariableSparsePolynomial(g.coefficient.getAsDict(),["x"],finitefield.FinitePrimeField(E.ch))
                    else:
                        if i%2!=0: 
                            j=(i-1)//2
                            g=f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                            f[i]=g
                            g=change(g,i,e,E.ch)
                            M[i]=polynomial.OneVariableSparsePolynomial(g.coefficient.getAsDict(),["x"],finitefield.FinitePrimeField(E.ch))
                        else: 
                            j=i//2
                            g=(f[j+2]*(f[j-1]**2)-f[j-2]*(f[j+1]**2))*f[j] 
                            L=g.coefficient.items()
                            t=0
                            dict={}
                            while t<len(L): #div2*y
                                dict[(L[t][0][0],L[t][0][1]-1)]=L[t][1]*finitefield.FinitePrimeFieldElement(2,E.ch).inverse()
                                t=t+1
                            g.coefficient=dict
                            f[i]=g
                            g=change(g,i,e,E.ch)
                            M[i]=polynomial.OneVariableSparsePolynomial(g.coefficient.getAsDict(),["x"],finitefield.FinitePrimeField(E.ch))
                    i=i+1
                return M,H
        else: 
            f={}
            M={}
            if self.ch==0:
                f[-1]=-1
                M[-1]=-1
                f[0]=0
                M[0]=0
                E=self.simple()
                e=x**3+E.a*x+E.b
                i=1
                while i<=Number:
                    if i==1:
                        f[1]=1
                        M[1]=1
                    elif i==2:
                        f[2]=2*y
                        M[2]=1
                    elif i==3:
                        f[3]=3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                        M[3]=3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                    elif i==4:
                        f[4]=4*y*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
                    elif i%2!=0:
                        j=(i-1)//2
                        f[i]=f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                    else: #i%2==0
                        j=i//2
                        g=(f[j+2]*(f[j-1]**2)-f[j-2]*(f[j+1]**2))*f[j] 
                        L=g.coefficient.items()
                        t=0
                        dict={}
                        while t<len(L): #div2*y
                            dict[(L[t][0][0],L[t][0][1]-1)]=L[t][1]//2
                            t=t+1
                        g.coefficient=dict
                        f[i]=g
                    i=i+1
                if Number<=3:
                    i=Number
                    return M[i]
                else:
                    if Number%2==0:
                        return change(f[Number],Number,e,0)/2
                    else:
                        return change(f[Number],Number,e,0)
            elif self.ch==2:
                f[-1]=finitefield.FinitePrimeFieldElement(-1,2)
                f[0]=finitefield.FinitePrimeFieldElement(0,2)
                i=1
                while i<=Number:
                    if i==1:
                        f[1]=finitefield.FinitePrimeFieldElement(1,2)
                    elif i==2:
                        f[2]=x
                    elif i==3:
                        f[3]=x**4+x**3+self.a6
                    elif i==4:
                        f[4]=x**6+self.a6*x**2
                    else:
                        if i%2!=0:
                            j=(i-1)//2
                            f[i]=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                        else:
                            j=i//2
                            g=(f[j+2]*f[j-1]*f[j-1]+f[j-2]*f[j+1]*f[j+1])*f[j]
                            L=g.coefficient.getAsDict().items()
                            t=0
                            dict={}
                            while t<len(L):
                                dict[L[t][0][0]-1]=finitefield.FinitePrimeFieldElement(L[t][1],2)
                                t=t+1
                            g.coefficient=dict
                            f[i]=g
                    i=i+1
                return f[Number]
            elif self.ch==3:
                raise NotImplementedError,"Now making (>_<)"
            else:
                f[-1]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(-1,self.ch)},["x","y"])
                f[0]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(0,self.ch)},["x","y"])
                E=self.simple()
                e=x**3+E.a*x+finitefield.FinitePrimeFieldElement(E.b,E.ch)
                i=1
                while i<=Number:
                    if i==1:
                        f[1]=polynomial.MultiVariableSparsePolynomial({(0,0):finitefield.FinitePrimeFieldElement(1,self.ch)},["x","y"])
                    elif i==2:
                        f[2]=2*y
                        M[2]=1
                    elif i==3:
                        g=3*x**4+6*E.a*x**2+12*E.b*x-finitefield.FinitePrimeFieldElement(E.a,E.ch)**2
                        f[3]=g
                        M[3]=g
                    elif i==4:
                        g=4*y*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-finitefield.FinitePrimeFieldElement(E.a,E.ch)**3-finitefield.FinitePrimeFieldElement(8,E.ch)*E.b**2)
                        f[4]=g
                    else:
                        if i%2!=0: 
                            j=(i-1)//2
                            g=f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                            f[i]=g
                        else: 
                            j=i//2
                            g=(f[j+2]*(f[j-1]**2)-f[j-2]*(f[j+1]**2))*f[j] 
                            L=g.coefficient.items()
                            t=0
                            dict={}
                            while t<len(L): #div2*y
                                dict[(L[t][0][0],L[t][0][1]-1)]=L[t][1]*finitefield.FinitePrimeFieldElement(2,E.ch).inverse()
                                t=t+1
                            g.coefficient=dict
                            f[i]=g
                    i=i+1
                if Number==2:
                    return M[2]
                elif Number==3:
                    return M[3]
                else:
                    if Number%2==0:
                        return change(f[Number],Number,e,self.ch)/2
                    else:
                        return change(f[Number],Number,e,self.ch)

    def order(self,default=0): 
        """
        this returns #E(Fp)
        """
        """
        a=3
        b=1043498151013573141076033119958062900890
        p=2**130+169
        #E=1361129467683753853808807784495688874237
        polynomial can use p<2*10**9
        """
        def schoof(self,default=0):
            if self.ch>3:
                if len(self)!=2:
                    other=self.simple()
                else:
                    other=self 
                E=polynomial.OneVariableSparsePolynomial({0:other.b,1:other.a,3:1},['x'],finitefield.FinitePrimeField(other.ch))
                x=polynomial.OneVariableSparsePolynomial({1:1},["x"],finitefield.FinitePrimeField(other.ch)) 
                T=[]
                D=other.divPoly(default)
                L=D[1]
                D=D[0]
                i=0
                M=1
                while i<len(L):
                    j=L[i]
                    M=M*j
                    u=PolyPow(x,other.ch,D[j]) #u=x^q
                    v=PolyPow(u,other.ch,D[j]) #v=x^{q^2}
                    g0=PolyPow(E,int((other.ch-1)/2),D[j])#y^(q-1)
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
                return other.ch+1-tau
            else:
                raise NotImplementedError, "Now making (>_<)"
        
        def Shanks_Mestre(self):
            import sets
            """
            This program is using
            Algorithm 7.5.3(Shanks-Mestre assessment of curve order)
            Crandall & Pomerance ,PRIME NUMBERS
            self.ch<=10**5+o(1)
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
                    return other.ch+1+k
                else: #E.ch>229
                    def BSGS(E,P,W):
                        L=[]
                        A=[]
                        B=[]
                        i=0
                        Q=E.mul(E.ch+1,P)
                        while i<W:
                            A.append(Q[0])
                            Q=E.add(Q,P)
                            i=i+1
                        L.append(A)
                        j=0
                        Q=[0]
                        R=E.mul(W,P)
                        while j<=W:
                            B.append(Q[0])
                            Q=E.add(Q,R)
                            j=j+1
                        L.append(B)
                        L.append(sets.Set(A).intersection(sets.Set(B)))
                        return L
                    
                    if len(self)!=2:
                        other=self.simple()
                    else:
                        other=self
                    g=0
                    while arith1.legendre(g,other.ch)!=-1:
                        g=random.randint(2,other.ch-1)
                    W=int(math.sqrt(math.sqrt(other.ch))*math.sqrt(2))+1
                    c,d=g**2*other.a,g**3*other.b
                    f=polynomial.OneVariableDensePolynomial([other.b,other.a,0,1],"X")
                    BOX=[]
                    i=0
                    while i<other.ch:
                        BOX.append(1)
                        i=i+1
                    k=0
                    while k==0:
                        x=random.randint(0,other.ch-1)
                        while BOX[x]==0 or arith1.legendre(f(x),other.ch)==0:
                            BOX[x]=0
                            x=random.randint(0,other.ch-1)
                        BOX[x]=0
                        if arith1.legendre(f(x),other.ch)==1:
                            E=other
                            cg=1
                        else: #arith1.legendre(f(cg),other.ch)==-1
                            E=EC([c,d],other.ch)
                            cg=-1
                            x=g*x%E.ch
                        P=[x,E.coordinateX(x)]
                        L=BSGS(E,P,W)
                        A=L[0]
                        B=L[1]
                        S=L[2]
                        if len(S)==1:
                            k=1
                    s=S.pop()
                    aa=A.index(s)
                    bb=B.index(s)
                    t=aa-bb*W
                    if E.mul(E.ch+1+t,P)==[0]:
                        return E.ch+1+cg*t
                    else:
                        t=aa+bb*W
                        return E.ch+1+cg*t
            else:
                raise NotImplementedError,"Now making m(__)m"

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
        
        if self.ch<=3:
            if self.index!=1:
                raise NotImplementedError,"Now making m(__)m"
            else:
                raise NotImplementedError,"Now making m(__)m"
        elif self.ch<10**6:
            if self.index!=1:
                return pow(self.ch,self.index)+1-powOrd(-Shanks_Mestre(self)+self.ch+1,self.index,self.ch)
            else:
                return Shanks_Mestre(self)
        else: # self.ch>=10**6
            if self.index!=1:
                if default==0:
                    raise  self.ch**self.index+1-powOrd(-schoof(self)+self.ch+1,self.index,self.ch)
                else:
                    return schoof(self,default)
            else:
                return schoof(self)

    # Cremona's book p.66
    def tatesAlgorithm(self):
        """
        tatesAlgorithm()

        returns [Kp, fp, cp]

        Kp : Kodaira symbol
        fp : Exponent of p in conductor
        cp : Local index
        """

        p = self.ch
        c4 = self.c4
        c6 = self.c6
        b2 = self.b2
        b4 = self.b4
        b6 = self.b6
        b8 = self.b8
        a1 = self.a1
        a2 = self.a2
        a3 = self.a3
        a4 = self.a4
        a6 = self.a6

        n = factor.ord(self.ch, self.disc)

        if n == 0:
            Kp = "IO"
            fp = 0
            cp = 1

        if p == 2:
            if b2 % p == 0:
                r = a4 % p
                t = (r * (1+a2+a4) + a6) % p
            else:
                r= a3 % p
                t = (r+a4) % p
        elif p == 3:
            if b2 % p == 0:
                r = -b6 % p
            else:
                r = -b2*b4 % p
            t = (a1*r+a3) % p
        else:
            if c4 % p == 0:
                r = -inv(12, p) * b2
            else:
                r = -inv(12*c4, p) * (c6+b2*c4)
            t = -inv(12, p)*(a1*r+a3)
            r = r % p
            t = t % p

        self.changeCurve([r, 0, t, 1])

        if c4 % p != 0:
            if quadroots(1, a1, -a2, p):
                cp = n
            elif n % 2 == 0:
                cp = 2
            else:
                cp = 1
        if a6 % (p**2) != 0:
            Kp = "II"
            fp = n
            cp = 1
            return [Kp, fp, cp]
        if b8 % (p**3) != 0:
            Kp = "III"
            fp = n-1
            cp = 2
            return [Kp, fp, cp]
        if b6 % (p**3) != 0:
            if quadroots(1, a3/p, -a6/(p**2), p):
                cp = 3
            else:
                cp = 1
            Kp = "IV"
            fp = n-2
            return [Kp, fp, cp]
        if p == 2:
            s = a2 % 2
            t = 2*(a6/4 % 2)
        else:
            s = -a1*inv(2,p)
            t = -a3*inv(2, p)
        changeCurve(0, s, t, 1)
        b = a2/p
        c = a4/(p**2)
        d = a6/(p**3)
        w = 27*(d**2) - (b**2)*(c**2) + 4*(b**3)*d - 18*b*c*d + 4*(c**3)
        x = 3*c - b**2
        if w % p != 0:
            Kp = "I*O"
            fp = n-4
            cp = 1 + nrootscubic(b, c, d, p)
            return [Kp, fp, cp]
        elif x % p != 0:
            if p == 2:
                r = c
            elif p == 3:
                r = b*c
            else:
                r = (b*c-9*d)*inv(2*x, p)
            r = p*(r % p -p/2+1)
            changeCurve(r, 0, 0, 1)
            m = 1
            mx = p*p
            my = p*p
            cp = 0 
            while cp == 0:
                xa2 = a2/p
                xa3 = a3/my
                xa4 = a4/(p*mx)
                xa6 = a6/(my*my)
                if (xa3**2+4*xa6) % p != 0:
                    if quadroots(1, xa3, -xa6, p):
                        cp = 4
                    else:
                        cp = 2
                else:
                    if p == 2:
                        t = my*xa6
                    else:
                        t = my*((-xa3*inv(2, p)) % p -p/2+1)
                    changeCurve(0, 0, t, 1)
                    my = my*p
                    m = m + 1
                    xa2 = a2/p
                    xa3 = a3/my
                    xa4 = a4/(p*mx)
                    xa6 = a6(mx*my)
                    if (xa4**2-4*xa2*xa6) % p != 0:
                        if quadroots(xa2, xa4, xa6, p):
                            cp = 4
                        else:
                            cp = 2
                    else:
                        if p == 2:
                            r = mx*(xa6*xa2 % 2)
                        else:
                            r = mx*(-xa4*inv(2*xa2, p) % p -p/2+1)
                        changeCurve(r, 0, 0, 1)
                        mx = mx*p
                        m = m + 1

            fp = n-m-4
            Kp = "I*m"
            return [Kp, fp, cp]
        else:
            if p == 3:
                rp = -d
            else:
                rp = -b*inv(3, p)
            r = p*(rp % p -p/2+1)
            changeCurve(r, 0, 0, 1)
            x3 = a3/(p*p)
            x6 = a6/(p**4)
            if (x3**2+4*x6) % p != 0:
                if quadroots(1, x3, -x6, p):
                    cp = 3
                else:
                    cp = 1
                Kp = "IV*"
                fp = n-6
                return [Kp, fp, cp]
            else:
                if p == 2:
                    t = x6
                else:
                    t = x3*inv(2, p)
                t = -(p**2)*(t % p -p/2+1)
                changeCurve(0, 0, t, 1)
                if a4 % (p**4) != 0:
                    Kp = "III*"
                    fp = n-7
                    cp = 2
                    return [Kp, fp, cp]
                elif a6 % (p**6) != 0:
                    Lp = "II*"
                    fp = n-8
                    cp = 1
                    return [Kp, fp, cp]
                else:
                    self.changeCurve(0, 0, 0, p)
                    self.tatesAlgorithm()

# necessary for tatesAlgorithm ---------------------------------------

def quadroots(a, b, c, p):
    """

    returns True if the congruence ax**2+bx+c = 0 (mod p)
    has a solution.
    else False.
    """

    if len(roots(polynomial.OneVariableDensePolynomial([1, b, a], "x"), p)) == 0:
        return True
    else:
        return False

def roots(f, mod):
    """
    f.roots(m) 

    returns a list of f's roots in modulus m
    """

    result = []

    for i in range(mod):
        if f(i) % mod == 0:
            result.append(i)
    return result

def nrootscubic(b, c, d, p):
    f = roots(polynomial.OneVariableDensePolynomial([d, c, b, 1], "x"), p)
    print polynomial.OneVariableDensePolynomial([d, c, b, 1], "x")
    return len(f)


import integerResidueClass 
def inv(a, p):
    c = integerResidueClass.IntegerResidueClass(a, p)
    return c.inverse().n

# --------------------------------------------------------------------

