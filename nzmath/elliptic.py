from __future__ import division
import arith1
import cmath
import factor
import finitefield
import imaginary
import math
import polynomial 
import prime
import random
import rational

"""
f=polynomial.OneVariableSparsePolynomial({1:-1,10201:1}, ['x']) 
g=polynomial.OneVariableSparsePolynomial({(0,):48,(1,):58,(2,):53,(3,):60,( 4,):28,(5,):93,(6,):79,(7,):52,(8,):65,(9,):5,(10,):85,(12,):5}, ['x']) 
h=polynomial.OneVariableSparsePolynomial({0:1,2:17,3:1,4:13,5:71,6:36,7:59,8:46,9:12,10:51,11:52,12:50},["x"])

"""
def Element_p(a,p):
    """
    a is (rational,int,long) number
    this returns a in F_p
    """
    return int(finitefield.FinitePrimeField(p).createElement(a).n)

def Mod(poly,d):
    """
    this returns poly%(x^d)
    """
    if isinstance(poly,(int,long)):
        return polynomial.OneVariableDensePolynomial([int(poly)],"x").toOneVariableSparsePolynomial()
    elif isinstance(poly,(polynomial.OneVariableDensePolynomial,polynomial.OneVariableSparsePolynomial)):
        if poly.degree()>=d:
            if isinstance(poly,polynomial.OneVariableSparsePolynomial):
                poly=poly.toOneVariableDensePolynomial()
            P=poly.coefficient.getAsDict().items()
            dict={}
            i=0
            while i<len(P):
                if P[i][0]<d:
                    dict[P[i][0]]=P[i][1]
                i=i+1
            if len(dict)!=0:
                return polynomial.OneVariableSparsePolynomial(dict,["x"])
            else:
                return polynomial.OneVariableDensePolynomial([0],"x").toOneVariableSparsePolynomial()
        else:
            return poly.toOneVariableSparsePolynomial()
    else:
        raise ValueError,"you must imput (poly,OneVariable{Dense,Sparese}Polynomial)"

def Div(poly,d):
    """
    this returns poly//(x^d)
    """
    if d==0:
        return poly.toOneVariableSparsePolynomial()
    elif isinstance(poly,(polynomial.OneVariableDensePolynomial,polynomial.OneVariableSparsePolynomial)):
        if isinstance(poly,polynomial.OneVariableSparsePolynomial):
            poly=poly.toOneVariableDensePolynomial()
        P=poly.coefficient.getAsDict()
        if min(P)>=d:
            P=P.items()
            i=0
            dict={}
            while i<len(P):
                dict[P[i][0]-d]=P[i][1]
                i=i+1
            return polynomial.OneVariableSparsePolynomial(dict,["x"])
        else:
            raise ValueError,"*/x^"
    else:
        raise ValueError,"*/x^"

def Evaluate(poly,t):
    """
    use Horner's rule
    """
    if poly.degree()<1:
        return poly
    poly=poly.toOneVariableSparsePolynomial()
    d=poly.degree()
    P=poly.coefficient
    v=P[d]*t+P[d-1]
    i=d-2
    while i>=0:
        v=v*t+P[i]
        i=i-1
    return v

def Mul(f,g):
    """
    all coefficient are nonnegative integer
    """
    if isinstance(f,(int,long)) or isinstance(g,(int,long)):
        return f*g
    elif f.degree()<1 or g.degree()<1:
        return f*g
    else:
        pass
    F=f.toOneVariableDensePolynomial()
    G=g.toOneVariableDensePolynomial()
    if len(F.coefficient.getAsDict())*len(G.coefficient.getAsDict())<f.degree()+g.degree():
        return f*g
    f=f.toOneVariableSparsePolynomial()
    g=g.toOneVariableSparsePolynomial()
    F=f.degree()
    G=g.degree()
    v=max(F+1,G+1)*max(f.coefficient)*max(g.coefficient)
    i=2
    while i<=v:
        i=i*2
    X=Evaluate(f,i)
    Y=Evaluate(g,i)
    u=X*Y
    L=[]
    j=0
    k=1
    while j<F+G+1:
        u=int(u/k)
        L.append(u%i)
        k=i
        j=j+1
    return polynomial.OneVariableDensePolynomial(L,"x").toOneVariableSparsePolynomial()

def Inver_p(poly,d,p):
    """
    this returns poly inversion mod x^d /F_p
    """
    poly=poly%p
    poly=poly.toOneVariableDensePolynomial()
    L=poly.coefficient.getAsList()
    if len(L)==1:
        return polynomial.OneVariableSparsePolynomial({(0,):Element_p(rational.Rational(1,L[0]),p)},["x"]) 
    if L[0]!=1:
        poly=poly*Element_p(rational.Rational(1,L[0]),p)%p
    poly=poly.toOneVariableSparsePolynomial()
    f=polynomial.OneVariableSparsePolynomial({0:1},["x"])
    n=1
    while n<d+1:
        n=2*n
        if n>d+1:
            n=d+1
        g=Mod(poly,n)%p
        g=Mod(f*g%p,n)%p #
        f=Mod(f*(2-g)%p,n)%p #
        print n ,d+1,"*" ###
    if L[0]==1:
        return f%p
    else:
        return f*Element_p(rational.Rational(1,L[0]),p)%p

def PolyMod_p(f,g,p):
    """
    return f (mod g)/F_p
    """
    def rev(poly,d):
        poly=poly.toOneVariableDensePolynomial()
        L=poly.coefficient.getAsList()
        if len(L)<=d:
            i=0
            while len(L)<=d:
                L.append(0)
                i=i+1
        f=0
        i=0
        while i<=d:
            if L[d-i]!=0:
                f=f+polynomial.OneVariableSparsePolynomial({i:L[d-i]},["x"])
            i=i+1
        return f
    def ind(poly,d):
        if isinstance(poly,(int,long)):
            return 0
        else:
            if poly.degree()<d:
                return 0
            poly=poly.toOneVariableDensePolynomial()
            L=poly.coefficient.getAsList()
            i=d
            while i<len(L):
                if L[i]!=0:
                    break
                i=i+1
            return i        
    f=f%p
    g=g%p
    f=f.toOneVariableSparsePolynomial()
    g=g.toOneVariableSparsePolynomial()
    a=g.coefficient[g.degree()]
    if a!=1:
        g=g*Element_p(rational.Rational(1,a),p)%p
    d=f.degree()-g.degree()
    if g.degree()<=0:
        return 0
    elif d<0:
        return f
    else:
        F=rev(f,f.degree())
        G=rev(g,g.degree())
        q=Inver_p(G,d,p)# time wastes 
        q=Mod(q*F%p,d+1) #
        r=(F-q*G)%p #
        i=ind(r,d+1)
        r=Div(r,i)
        return rev(r,f.degree()-i)

def GCD(f,g,p):
    f=f%p
    g=g%p
    if isinstance(f,(int,long)):
        return 1
    elif isinstance(g,(int,long)):
        return 1
    else:
        f=f.toOneVariableSparsePolynomial()
        g=g.toOneVariableSparsePolynomial()
        if f.degree()<1 or g.degree()<1:
            return 1
        else:
            if f.degree()>g.degree():
                f,g=f,g
            elif f.degree()<g.degree():
                f,g=g,f
            else: 
                F=f.coefficient
                G=g.coefficient
                if F[f.degree()]>=G[g.degree()]:
                    f,g=f,g
                else:
                    f,g=g,f
            while g:
                f,g=g,PolyMod_p(f,g,p)
                if isinstance(g,(int,long)) and g!=0:
                    return 1
                elif isinstance(g,(polynomial.OneVariableDensePolynomial,polynomial.OneVariableSparsePolynomial)) and g.degree()==1:
                    return 1
                else:
                    pass
            return f

def PolyMulRed(list,poly,p):
    """
    list[*] is OneSparsePoly
    poly is OneSparsePoly
    """
    poly=poly%p
    if len(poly.coefficient)==1: 
        return 0 
    i=0
    while i<len(list):
        if list[i]==0:
            return 0 
        elif list[i].degree()>=poly.degree():
            list[i]=PolyMod_p(list[i],poly,p)
        i=i+1
    POLY=polynomial.OneVariableSparsePolynomial({0:1},['x'])
    i=0
    while i<len(list):
        POLY=Mul(POLY,list[i])
        if isinstance(POLY,(int,long)):
            pass
        else:
            if POLY.degree()>=poly.degree():
                POLY=PolyMod_p(POLY,poly,p)
        i=i+1
    return POLY

# t=imaginary.Complex(a,b)

def q(t):
    """
    this returns exp(2*pi*j*t)
    t is complex and h.imag>0
    """
    return cmath.exp(2*cmath.pi*1j*t)

def delta(t,x):
    """
    """
    qt=q(t)
    def a(i):
        if i%2==0:
            return qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2)
        else:
            return (-1)*(qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2))
    i=1
    b=0
    while abs(a(i+1))>x: #syuusoku
       b=a(i)+b
       print i #
       i=i+1
    return qt*(1+b)**24

def h(t,x):
    """
    """
    return delta(2*t,x)/delta(t,x)

def j(t,x):
    """
    """
    return (256*h(t,x)+1)**3/h(t,x)
    
def nu(t,x):
    """
    """
    qt=q(t)
    qq=cmath.exp(cmath.pi*1j/12)
    def a(i):
        if i%2==0:
            return qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2)
        else:
            return (-1)*(qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2))
    i=1
    b=0
    while abs(a(i+1))>x: # one time we caluculate a(i+1),so waste more time??
       b=a(k)+b #### miss ,if k==i !
       i=i+1
    return qq*(1+b)
        
class EC:
    """
    Elliptic curves over Q and Fp.
    # If you wanna use over other fields, just a moment please :-)
    """
    def __init__(self,coefficient,character):
        """
        Initialize an elliptic curve. If coefficient has 5 elements,
        it represents E:y**2+a1*x*y+a3*y=x**3+a2*x**2+a4*x+a6 or 2
        elements, E:y*2=x*3+a*x+b.
        """
        if isinstance(coefficient,list):
            self.coefficient=coefficient
            self.ch=character
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
                    if coefficient[0]%2==1 and coefficient[2]==coefficient[3]==0:
                        self.a1=1
                        self.a2=coefficient[1]%2
                        self.a3=0
                        self.a4=0
                        self.a6=coefficient[4]%2
                        self.disc=self.a6
                        if self.disc!=0:
                            self.j=arith1.inverse(self.a6,2)%2
                    elif coefficient[0]==coefficient[1]==0:
                        self.a1=0
                        self.a2=0
                        self.a3=Element_p(coefficient[2],2)
                        self.a4=Element_p(coefficient[3],2)
                        self.a6=Element_p(coefficient[4],2)
                        self.disc=Element_p(self.a3**4,2)
                        self.j=0
                    else:
                        raise ValueError, "can't defined EC (-_-;)"
                    if self.disc==0:
                        raise ValueError, "singular curve (@_@)"
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
            elif self.ch==3: # y^2=x^3+a2*x^2+a6 or y^2=x^3+a4*x+a6
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if len(self)==5:
                    if coefficient[0]==coefficient[2]==coefficient[3]==0:
                        self.a1=0
                        self.a2=Element_p(coefficient[1],3)
                        self.a3=0
                        self.a4=0
                        self.a6=Element_p(coefficient[4],3)
                        self.disc=Element_p(-self.a2**3*self.a6,3)
                        if self.disc!=0:
                            j=rational.Rational(-self.a2**3,self.a6)
                            self.j=Elemant(j,3)
                    elif coefficient[0]==coefficient[1]==coefficient[2]==0:
                        self.a1=0
                        self.a2=0
                        self.a3=0
                        self.a4=Element_p(coefficient[3],3)
                        self.a6=Element_p(coefficient[4],3)
                        self.disc=Element_p(-self.a4**3,3)
                        self.j=0
                    else:
                        raise ValueError, "can't defined EC (-_-;)"
                    if self.disc==0:
                        raise ValueError, "singular curve (@_@)"
                else:
                    raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
            else:
                for i in range(0,len(self)):
                    if not isinstance(coefficient[i],(int,long)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
                if prime.millerRabin(self.ch)==1:
                    if len(self)==5:
                        self.a1=Element_p(coefficient[0],self.ch)
                        self.a2=Element_p(coefficient[1],self.ch)
                        self.a3=Element_p(coefficient[2],self.ch)
                        self.a4=(coefficient[3],self.ch)
                        self.a6=Element_p(coefficient[4],self.ch)
                        self.b2=Element_p(self.a1**2+4*self.a2,self.ch)
                        self.b4=Element_p(self.a1*self.a3+2*self.a4,self.ch)
                        self.b6=Element_p(self.a3**2+4*self.a6,self.ch)
                        self.b8=Element_p(self.a1**2*self.a6+4*self.a2*self.a6-self.a1*self.a3*self.a4+self.a2*self.a3**2-self.a4**2,self.ch)
                        self.c4=Element_p(self.b2**2-24*self.b4,self.ch)
                        self.c6=Element_p(-self.b2**3+36*self.b2*self.b4-216*self.b6,self.ch)
                        self.disc=Element_p(-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6,self.ch)
                        if self.disc==0:
                            raise ValueError, "singuler curve (@_@)"
                        j=rational.Rational(self.c4**3,self.disc)
                        self.j=Element_p(j,self.ch)
                    elif len(self)==2:
                        self.a=Element_p(coefficient[0],self.ch)
                        self.b=Element_p(coefficient[1],self.ch)
                        self.a1=0
                        self.a2=0
                        self.a3=0
                        self.a4=Element_p(coefficient[0],self.ch)
                        self.a6=Element_p(coefficient[1],self.ch)
                        self.b2=0
                        self.b4=Element_p(2*self.a,self.ch)
                        self.b6=Element_p(4*self.b,self.ch)
                        self.b8=Element_p(-self.a**2,self.ch)
                        self.c4=Element_p(-48*self.a,self.ch)
                        self.c6=Element_p(-864*self.b,self.ch)
                        self.disc=Element_p(-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6,self.ch)
                        if self.disc==0:
                            raise ValueError, "singuler curve (@_@)"
                        j=rational.Rational(self.c4**3,self.disc)
                        self.j=Element_p(j,self.ch)
                    else:
                        raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
                else:
                    raise ValueError, "characteristic must be 0 or prime (-_-;)"
        else:
            raise ValueError, "you must input (coefficient,list) m(__)m"
           
    def __len__(self):
        return len(self.coefficient)

    def __repr__(self):
        if len(self)==2 or self.a1==self.a2==self.a3==0:
            return "EC(["+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")"
        else:
            return "EC(["+repr(self.a1)+","+repr(self.a2)+","+repr(self.a3)+","+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")"

    def __str__(self):
        return str(polynomial.MultiVariableSparsePolynomial({(0,2):1,(1,1):self.a1,(0,1):self.a3,(3,0):-1,(2,0):-self.a2,(1,0):-self.a4,(0,0):-self.a6},["x","y"]))

    def simple(self):
        """
        this transforms E:y^2+a1*x*y+a3*y=x^3+a2*x^2+a4*x+a6 to E':Y^2=X^3+(-27*c4)*X+(-54*c6),
        if ch is not 2 or 3
        """
        if len(self)==2 or (self.a1==self.a2==self.a3==0):
            return self
        else:
            if self.ch==0:
                other=EC([-27*self.c4,-54*self.c6],self.ch)
                return other   
            elif self.ch==2 or self.ch==3:
                return self
            else:
                other=EC([Element_p(-27*self.c4,self.ch),Element_p(-54*self.c6,self.ch)],self.ch)
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
                        A=[rational.Rational(self.a1+2*V[2],V[0]),
                           rational.Rational(self.a2-V[2]*self.a1+3*V[1]-V[2]**2,V[0]**2),
                           rational.Rational(self.a3+V[1]*self.a1+2*V[3],V[0]**3),
                           rational.Rational(self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4),
                           rational.Rational(self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1,V[0]**6)]
                        other=EC([Element_p(A[0],self.ch),
                                  Element_p(A[1],self.ch),
                                  Element_p(A[2],self.ch),
                                  Element_p(A[3],self.ch),
                                  Element_p(A[4],self.ch),],self.ch)
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
                    qx=rational.Rational(P[0]-V[1],V[0]**2)
                    Q0=Element_p(qx,self.ch)
                    qy=rational.Rational(P[1]-V[2]*(P[0]-V[1])-V[3],V[0]**3)
                    Q1=Element_p(qy,self.ch)
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
            if len(self)==2 or (self.a1==self.a2==self.a3==0):    
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
                x=rational.Rational(s-3*self.b2,36)
                x=Element_p(x,self.ch)
                y=rational.Rational(1,2)*(rational.Rational(arith1.sqroot(t,self.ch),108)-self.a1*x-self.a3)
                y=Element_p(y,self.ch)
                return [x,y]
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
        y1=self.a1*x+self.a3
        y2=x**3+self.a2*x**2+self.a4*x+self.a6
        if self.ch!=0 and self.ch!=2:
            if len(self)==2 or (self.a1==self.a2==self.a3==0):
                if arith1.legendre(y2,self.ch)>=0:
                    return arith1.sqroot(y2,self.ch)
                else:
                    raise ValueError, "(-_-;)"
            else:
                if y1**2+4*y2>=0:
                    d=arith1.sqroot(y1**2+4*y2,self.ch)
                    return (-y1-d)*arith1.inverse(2,self.ch)%self.ch
                else:
                    raise ValueError, "(-_-;)" 
        elif self.ch==2:
            raise NotImplementedError, "Now making (>_<)"
        else: 
            if y1**2+4*y2>=0:
                return rational.Rational((-1)*y1+math.sqrt(y1**2+4*y2),2)
            else:
                raise ValueError, "(-_-;)"
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
                    if (P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1])%self.ch==(P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6)%self.ch:
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
                        if P[0]==Q[0]:
                            if (P[1]+Q[1]+self.a1*Q[0]+self.a3)%self.ch==0:
                                return [0]
                            else:
                                s=rational.Rational(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1],2*P[1]+self.a1*P[0]+self.a3)
                                t=rational.Rational(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1],2*P[1]+self.a1*P[0]+self.a3)
                        else: 
                            s=rational.Rational(Q[1]-P[1],Q[0]-P[0])
                            t=rational.Rational(P[1]*Q[0]-Q[1]*P[0],Q[0]-P[0])
                        x3=s**2+self.a1*s-self.a2-P[0]-Q[0]
                        x3=Element_p(x3,self.ch)
                        y3=-(s+self.a1)*x3-t-self.a3
                        y3=Element_p(y3,self.ch)
                        R=[x3,y3]
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
                    y=-Q[1]-self.a1*Q[0]-self.a3
                    R=[x,y] 
                    return self.add(P,R) 
                elif (P==[0]) and (Q!=[0]):
                    x=Q[0]
                    y=-Q[1]-self.a1*Q[0]-self.a3
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

    def divPoly(self):
        x=polynomial.OneVariableSparsePolynomial({(1,):1},['x'])
        y=polynomial.OneVariableSparsePolynomial({(1,):1},['y'])
        def heart(q):
            l=[]
            i=3
            j=1
            while j<=4*int(math.sqrt(q)):
                if prime.primeq(i):
                    l.append(i)
                    j=j*i
                i=i+1
            return l
        def change(poly,i,e,p):#y^2->e=x^3+a*x+b and if i%2,div y
            """
            poly is multi 
            """
            L=poly.coefficient.items()
            if i%2==0:
                t=0
                poly=0
                while t<len(L):
                    k=L[t][0][1]
                    if k%2==0:
                        k=k//2
                        poly=poly+e**k*L[t][1]*x**L[t][0][0]
                    else:
                        k=(k-1)//2
                        poly=poly+y*e**k*L[t][1]*x**L[t][0][0]
                    t=t+1
                poly=poly%p
                L=poly.coefficient.items()
                t=0
                dict={}
                while t<len(L): #div y
                    dict[(L[t][0][0],L[t][0][1]-1)]=L[t][1]
                    t=t+1
                poly.coefficient=dict
            else: #y^2->e
                t=0
                poly=0
                while t<len(L):
                    k=L[t][0][1]//2
                    poly=poly+e**k*L[t][1]*x**L[t][0][0]
                    t=t+1
                poly=poly%p 
            return poly.toOneVariableSparsePolynomial()
        f=[]
        M=[]
        f.append(0)
        M.append(0) #
        H=heart(self.ch)
        if self.ch!=2 and self.ch!=3: 
            E=self.simple()
            e=x**3+E.a*x+E.b
            i=1
            for i in xrange(1,H[-1]+1):
                if i==1:
                    f.append(1)
                    M.append(polynomial.OneVariableSparsePolynomial({0:1},['x']))
                elif i==2:
                    f.append(2*y)
                    M.append(polynomial.OneVariableSparsePolynomial({0:2},['x']))
                elif i==3:
                    g=3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                    g=g%E.ch
                    f.append(g)
                    M.append(g)
                elif i==4:
                    g=4*y*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
                    g=g%E.ch
                    f.append(g)
                    M.append(change(g,i,e,E.ch))#div y
                else:
                    if i%2!=0: 
                        j=(i-1)//2
                        g=f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                        g=g%E.ch
                        f.append(g)
                        M.append(change(g,i,e,E.ch)) # y^2->e
                    else: 
                        j=i//2
                        g=(f[j+2]*(f[j-1]**2)-f[j-2]*(f[j+1]**2))*f[j] 
                        L=g.coefficient.items()
                        t=0
                        dict={}
                        while t<len(L): #div 2y
                            dict[(L[t][0][0],L[t][0][1]-1)]=(L[t][1]%E.ch)//2
                            t=t+1
                        g.coefficient=dict
                        f.append(g)
                        M.append(change(g,i,e,E.ch)) # y^2->e and div y
        elif self.ch==2:#E(ch=2):y^2+x*y=x^3+a2*x^2+a6
            for i in xrange(1,H[-1]+1):
                if i==1:
                    f.append(1)
                    M.append(1) #
                elif i==2:
                    f.append(x)
                    M.append(x)
                elif i==3:
                    g=x**4+x**3+self.a6
                    G=g.coefficient
                    L=G.items()
                    t=0
                    dict={}
                    while t<len(L):
                        dict[L[t][0]]=Element_p(L[t][1],2)
                        t=t+1
                    g.coefficient=dict
                    f.append(g)
                    M.append(g)
                elif i==4:
                    g=x**6+self.a6*x**2
                    L=g.coefficient.items()
                    t=0
                    dict={}
                    while t<len(L):
                        dict[L[t][0]]=Element_p(L[t][1],2)
                        t=t+1
                    g.coefficient=dict
                    f.append(g)
                    M.append(g)
                else:
                    if i%2!=0:
                        j=(i-1)//2
                        g=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                        L=g.coefficient.items()
                        t=0
                        dict={}
                        while t<len(L):
                            dict[L[t][0]]=Element_p(L[t][1],2)
                            t=t+1
                        g.coefficient=dict
                        f.append(g)
                        M.append(g)
                    else:
                        j=i//2
                        g=(f[j+2]*f[j-1]*f[j-1]+f[j-2]*f[j+1]*f[j+1])*f[j]
                        L=g.coefficient.items()
                        t=0
                        dict={}
                        while t<len(L): # div x
                            dict[(L[t][0][0]-1,)]=Element_p(L[t][1],2)
                            t=t+1
                        g.coefficient=dict
                        f.append(g)
                        M.append(g)
        else: #self.ch==3 
            raise NotImplementedError, "Now making (>_<)"
        return M,H

    def order(self): 
        """
        this returns #E(Fp)
        """
        def schoof(self):
            if self.ch>3:
                if len(self)!=2:
                    other=self.simple()
                else:
                    other=self 
                T=[]
                D=other.divPoly()
                L=D[1]
                D=D[0]
                E=polynomial.OneVariableSparsePolynomial({0:other.b,1:other.a,3:1},['x'])
                f=polynomial.OneVariableSparsePolynomial({1:-1,other.ch**2:1},['x'])
                i=0
                while i<len(L):
                    j=L[i]
                    k=self.ch%j
                    if k%2==0:
                        P=GCD(PolyMulRed([f,E,D[k],D[k]],D[j],j)+PolyMulRed([D[k-1],D[k+1]],D[j],j),D[j],j)
                        if P==1:
                            F=0 
                        else:
                            F=1
                            P=equation.solve_Fp(P,j) #now making
                            P=(P,other.coordinateX(P))# P in E[j]
                    else:
                        P=GCD(PolyMulRed([f,D[k],D[k]],D[j],j)+PolyMulRed([D[k-1],D[k+1],E],D[j],j),D[j],j)
                        if P==1:
                            F=0
                        else:
                            F=1
                            P=equation.solve_Fp(P,j) #now making
                            P=(P,other.coordinateX(P))# P in E[j]
                    if F==1: #GCD!=1
                        if arith1.legendre(other.ch,j)==-1:
                            T.append((0,j))
                            #print T,"@" ### 
                        else:
                            w=arith1.sqroot(k,j)
                            #print P ###
#                            if : #
#                                T.append((2*w,j))
#                            elif : #
#                                T.append((-2*w,j))
#                            else: #
#                                T.append((0,j))
                            #T.append(P)###
                            pass
                    else: #GCD==1
                        l=1
                        while l<k:
                            #P=GCD(,,)#
                            if P==1:
                                T.append((0,j))
                                print T,"@@"
                            else:
                                T.append((l,j))
                                print T,"@@@"
                            l=l+1
                    i=i+1
                    print i,len(L),"#"###
                return T
            else:
                raise NotImplementedError, "Now making (>_<)"
        
        return schoof(self)###

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
                        k=k+arith1.legendre(i*(i**2+other.a)+other.b,other.ch)
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

        #def SEA(self):
        if self.ch<=3:
            raise NotImplementedError,"Now making m(__)m"
        elif self.ch<10**6:
            return Shanks_Mestre(self)
        else: # self.ch>=10**6
            raise NotImplementedError,"Now making m(__)m"

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

