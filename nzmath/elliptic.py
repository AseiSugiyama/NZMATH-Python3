from __future__ import division
import math
import random
import sets
import logging

import nzmath.arith1 as arith1
import nzmath.finitefield as finitefield
import nzmath.gcd as gcd
import nzmath.integerResidueClass as integerResidueClass
import nzmath.polynomial as polynomial
import nzmath.prime as prime
import nzmath.rational as rational
import nzmath.ring as ring
import nzmath.factor.methods as factor_methods

_log = logging.getLogger('nzmath.elliptic')


def Element_p(a,p):
    """
    a is (rational,int,long) number
    this returns a in F_p
    """
    return int(finitefield.FinitePrimeFieldElement(a,p).n)

def PolyMod(f, g):
    """
    return f (mod g)
    """
    if _isscalar(g):
        return 0
    elif _isscalar(f):
        return f
    else:
        return f % g

def GCD(f, g):
    # trivial cases
    if f == 0 and g != 0:
        return g
    elif g == 0 and f != 0:
        return f
    elif _isscalar(f) or _isscalar(g):
        return 1
    # other cases
    p = f.getRing().gcd(f, g)
    if p.degree() == 0:
        return 1
    else:
        return p

def PolyPow(f, d, g):
    """
    this returns (f^d)%g
    """
    l = arith1.expand(d,2)
    l.reverse()
    poly = ring.getRing(f).one
    for i in range(len(l)):
        poly = poly*poly
        poly = PolyMod(poly, g)
        if l[i]:
            poly = poly*f
            poly = PolyMod(poly, g)
    return poly

def PolyMulRed(multipliees, poly):
    """
    multipliees[*] is (OneSparsePoly,int,long)
    poly is OneSparsePoly
    """
    if poly.degree() < 1:
        return 0
    product = polynomial.PolynomialRing(poly.coefficientRing, 'x').one
    for factor in multipliees:
        if not _isscalar(factor) and factor.degree() >= poly.degree():
            factor = PolyMod(factor, poly)
        if factor == 0:
            return 0
        product = product * factor
        if not _isscalar(product) and product.degree() >= poly.degree():
            product = PolyMod(product, poly)
            if product == 0:
                return 0
    return product

def _isscalar(elem):
    """
    test whether 'elem' is scalar or not.
    """
    return isinstance(elem, (int,
                             long,
                             finitefield.FinitePrimeFieldElement,
                             integerResidueClass.IntegerResidueClass))

def heart(q):
    """
    this is for Schoof's
    """
    l = []
    i = 3
    j = 1
    bound = 4 * arith1.floorsqrt(q)
    while j <= bound:
        if i != q and prime.primeq(i):
            l.append(i)
            j *= i
        i += 2
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


class ECGeneric:
    """
    Elliptic curves for generic field.
    this class is fundamental class, normally only called sub class.
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
            elif character == 1:
                raise ValueError("characteristic must be 0 or prime.")
            else:
                self.ch=character
                if not index or index == 1: #field=F_p
                    self.field = finitefield.FinitePrimeField.getInstance(self.ch)
                    self.index = 1
                else: #field=F_q,q=(character)^r
                    """
                    index is irred polynomial in F_p,deg=r
                    To add this, we must exchange field and element.
                    """
                    raise NotImplementedError("now we can use only over finite prime fields.")
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
                    raise ValueError("coefficient is less or more, can't defined EC.")
                if self.disc==0:
                    raise ValueError("this curve is singular.")
                self.j=rational.IntegerIfIntOrLong(self.c4**3)/self.disc
        else:
            raise ValueError("you must input (coefficient, character, index)")

    def __len__(self):
        return len(self.coefficient)

    def __repr__(self):
        """
        return represantation form.
        only defined generic representation.
        """
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
                                raise ValueError("you must input integer m(__)m")
                        v=finitefield.FinitePrimeFieldElement(V[0],self.ch).inverse()
                        other=EC([(self.a1+2*V[2])*v.n,
                                  ((self.a2-V[2]*self.a1+3*V[1]-V[2]**2)*v**2).n,
                                  ((self.a3+V[1]*self.a1+2*V[3])*v**3).n,
                                  ((self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3])*v**4).n,
                                  ((self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1)*v**6).n],self.ch)
                        return other
                else:
                    raise ValueError("you must input ([u, r, s, t]) with u != 0.")
            else:
                raise ValueError("you must input ([u, r, s, t]) with u != 0.")
        else:
            raise ValueError("you must input ([u, r, s, t]) with u != 0.")

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
                        raise NotImplementedError("Now making (>_<)")
                    v=finitefield.FinitePrimeFieldElement(V[0],self.ch).inverse()
                    Q0=((P[0]-V[1])*v**2).n
                    Q1=((P[1]-V[2]*(P[0]-V[1])-V[3])*v**3).n
                Q=[Q0,Q1]
                return Q
            else:
                raise ValueError("you must input ([px, py], [u, r, s, t]) with u != 0.")
        else:
            raise ValueError("you must input ([px, py], [u, r, s, t]) with u != 0.")



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
                    return arith1.modsqrt(y2,self.ch)
                else:
                    return False
            else:
                if y1**2+4*y2>=0:
                    d=arith1.modsqrt(y1**2+4*y2,self.ch)
                    return Element_p(rational.Rational(-y1-d,2),self.ch)
                else:
                    return False
        elif self.ch==2:
            raise NotImplementedError("This is not implemented.")
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
        Return True if P is on, return False otherwise.
        """
        if isinstance(P,list):
            if len(P)==2:
                if self.ch==0:
                    if P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]==P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6:
                        return True
                    else:
                        _log.debug(str(P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]))
                        _log.debug(str(P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6))
                        return False
                else:
                    if self.index!=1:
                        raise NotImplementedError("Now making (>_<)")
                    if P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]==P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6:
                        return True
                    else:
                        return False
            elif P==[0]:
                return True
            else:
                raise ValueError("input must not be point on curve.")
        else:
            raise ValueError("you must input ([px, py])")

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
                            raise NotImplementedError("Now making (>_<)")
                        if P[0]==Q[0]:
                            if P[1]+Q[1]+self.a1*Q[0]+self.a3==0:
                                return [0]
                            else:
                                s=(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                                t=(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1])/(2*P[1]+self.a1*P[0]+self.a3)
                        else:
                            s=(Q[1]-P[1]*self.field.one)/(Q[0]-P[0])
                            t=(P[1]*Q[0]-Q[1]*P[0]*self.field.one)/(Q[0]-P[0])
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
                    raise ValueError("you must input ([px, py], [qx, qy])")
            else:
                raise ValueError("input must not be point on curve.")
        else:
            raise ValueError("you must input ([px, py], [qx, qy])")

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
                    raise ValueError("you must input ([px, py], [qx, qy])")
            else:
                raise ValueError("input must not be point on curve.")
        else:
            raise ValueError("you must input ([px, py], [qx, qy])")

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
        if self.ch == 0:
            x = polynomial.OneVariableMonomial('x')
        else:
            x = polynomial.OneVariableMonomial('x', coeffring=self.field)
        if not Number:
            if self.ch <= 3:
                raise ValueError("You must input (Number)")
            Kx = x.getRing()
            f = {-1: -Kx.one, 0: Kx.zero}
            H = heart(self.ch**self.index)
            E = self.simple()
            e = 4*(x**3+E.a*x+E.b)
            if 1 <= H[-1]+1:
                f[1] = Kx.one
            if 2 <= H[-1]+1:
                f[2] = Kx.one
            if 3 <= H[-1]+1:
                f[3] = 3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
            if 4 <= H[-1]+1:
                f[4] = 2*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
            i = 5
            while i <= H[-1]+1:
                if i % 2 != 0:
                    j = (i-1)//2
                    if j % 2 != 0:
                        f[i] = f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                    else:
                        f[i] = e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                else:
                    j = i//2
                    f[i] = (f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                i += 1
            i = -1
            while i <= H[-1]+1:
                if i > 1 and i % 2 == 0:
                    f[i] = 2*f[i]
                i += 1
            return (f, H)
        else:
            f = {}
            if self.ch == 0:
                f[-1] = -1
                f[0] = 0
                E = self.simple()
                e = x**3+E.a*x+E.b
                if 1 <= Number:
                    f[1] = 1
                if 2 <= Number:
                    f[2] = 1
                if 3 <= Number:
                    f[3] = 3*x**4+6*E.a*x**2+12*E.b*x-E.a**2
                if 4 <= Number:
                    f[4] = 2*(x**6+5*E.a*x**4+20*E.b*x**3-5*E.a**2*x**2-4*E.a*E.b*x-E.a**3-8*E.b**2)
                i = 5
                while i <= Number:
                    if i % 2 != 0:
                        j = (i-1)//2
                        if j % 2 != 0:
                            f[i] = f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                        else:
                            f[i] = e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                    else:
                        j = i//2
                        f[i] = (f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                    i += 1
                return f[Number]
            else:
                Kx = x.getRing()
                f[-1] = -Kx.one
                f[0] = Kx.zero
                e = 4*x**3 + self.b2*x**2 + 2*self.b4*x + self.b6
                if 1 <= Number:
                    f[1] = Kx.one
                if 2 <= Number:
                    f[2] = Kx.one
                if 3 <= Number:
                    f[3] = 3*x**4+self.b2*x**3+3*self.b4*x**2+3*self.b6*x+self.b8
                if 4 <= Number:
                    f[4] = 2*x**6+self.b2*x**5+5*self.b4*x**4+10*self.b6*x**3+10*self.b8*x**2+(self.b2*self.b8-self.b4*self.b6)*x+self.b4*self.b8-self.b6**2
                i = 5
                while i <= Number:
                    if i % 2 != 0:
                        j = (i-1)//2
                        if j % 2 != 0:
                            f[i]=f[j+2]*f[j]**3-e**2*f[j-1]*f[j+1]**3
                        else:
                            f[i]=e**2*f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                    else:
                        j = i//2
                        f[i] = (f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j]
                    i += 1
                return f[Number]

   

class ECoverQ(ECGeneric):
    """
    Elliptic curves over Q.
    """
    def __init__(self,coefficient):
        ECGeneric.__init__(self,coefficient,0)
    def __repr__(self):
        if len(self)==2 or self.a1==self.a2==self.a3==0:
            return "ECoverQ(["+repr(self.a4)+","+repr(self.a6)+"])"
        else:
            return "ECoverQ(["+repr(self.a1)+","+repr(self.a2)+","+repr(self.a3)+","+repr(self.a4)+","+repr(self.a6)+"])"

    def point(self, limit = 1000):
        """
        this returns a random point on eliiptic curve over Q.
        limit set maximal find time.
        """
        i=9
        while i<limit:
            s=random.randrange(1,i)
            t=random.randrange(1,i)
            y=self.coordinateY(rational.Rational(s,t))
            if y!=False:
                return [s,self.coordinateY(s)]
            i=i+10
        raise ValueError("Times exceeded for limit.")

class ECoverFp(ECGeneric):
    """
    Elliptic curves over Fp, p>2 .
    """
    def __init__(self,coefficient,character=None,index=None):
        if character<3:
            raise ValueError("ECoverFp accepts character > 2.")
        ECGeneric.__init__(self,coefficient,character,index)
        if self.ch==3: # y^2=x^3+a2*x^2+a6 or y^2=x^3+a4*x+a6
            for c in coefficient:
                if not isinstance(c, (int,long,finitefield.FinitePrimeFieldElement)):
                    raise ValueError("you must input integer coefficients.")
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
                    if self.disc.n:
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
                    raise ValueError("can't defined EC.")
                if self.disc.n==0:
                    raise ValueError("this curve is singular.")
            else:
                raise ValueError("coefficient is less or more, can't defined EC.")
        else:
            for c in coefficient:
                if not isinstance(c, (int,long,finitefield.FinitePrimeFieldElement)):
                    raise ValueError("you must input integer coefficients.")
            if prime.primeq(self.ch):
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
                    if self.disc:
                        self.j=self.c4**3*self.disc.inverse()
                    else:
                        raise ValueError("singular curve (@_@)")
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
                    if self.disc:
                        self.j=self.c4**3*self.disc.inverse()
                    else:
                        raise ValueError("this curve is singular.")
                else:
                    raise ValueError("coefficient is less or more, can't defined EC.")
            else:
                raise ValueError("characteristic must be prime.")
        self.o = False
        self.abelian = False
        
    def __repr__(self):
        if len(self)==2 or self.a1.n==self.a2.n==self.a3.n==0:
            return "ECoverFp(["+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"
        else:
            return "ECoverFp(["+repr(self.a1.n)+","+repr(self.a2.n)+","+repr(self.a3.n)+","+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"

    def point(self):
        """
        this returns a random point on eliiptic curve over ch(field)>3
        """
        if self.index!=1:
            raise NotImplementedError("This is not implemented.")
        if len(self)==2 or (self.a1.n==self.a2.n==self.a3.n==0):
            t=0
            while arith1.legendre(t,self.ch)!=1:
                s=random.randrange(0,self.ch)
                t=(s**3+self.a4*s+self.a6).n
            t=arith1.modsqrt(t,self.ch)
            r=random.randint(0,1)
            if r:
                return [s,self.ch-t]
            else:
                return [s,t]
        elif self.ch!=2 and self.ch!=3:
            other=self.simple()
            t=0
            while arith1.legendre(t,self.ch)!=1:
                s=random.randrange(0,self.ch)
                t=(s**3+other.a*s+other.b).n
            x=(s-3*self.b2)/36
            y=(rational.Rational(arith1.modsqrt(t,self.ch),108)-self.a1*x-self.a3)/2
            return [x.n,y.n]
        elif self.ch==3:
            t=0
            while arith1.legendre(t,self.ch)!=1:
                s=random.randrange(0,self.ch)
                t=(s**3+self.a2*s**2+self.a4*s+self.a6).n
            return [s,arith1.modsqrt(t,self.ch)]
        else:
            s=0
            while self.coordinateY(s) is ValueError:
                s=random.randrange(0,self.ch)
            return [s,self.coordinateY(s)]

    def Schoof(self):
        """
        this return t=p+1-#E(F_p)
        """
        if len(self)!=2:
            other=self.simple()
        else:
            other=self
        E = polynomial.OneVariableSparsePolynomial({0:other.b,1:other.a,3:1}, 'x', other.field)
        x = polynomial.OneVariableMonomial("x", coeffring=other.field)
        T = []
        D, L = other.divPoly()
        i=0
        M=1
        while i<len(L):
            j=L[i]
            M=M*j
            u=PolyPow(x,other.ch,D[j]) #u=x^q
            v=PolyPow(u,other.ch,D[j]) #v=x^{q^2}
            g0=PolyPow(E,(other.ch-1)//2,D[j]) #y^(q-1)
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
                    _log.debug("%s $" % str(T))
                else:
                    w=arith1.modsqrt(k,j)
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
                            _log.debug("%s $$" % str(T))
                        else:
                            T.append((-2*w,j))
                            _log.debug("%s $$$" % str(T))
                    else:
                        T.append((0,j))
                        _log.debug("%s $$$$" % str(T))
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
                            _log.debug("%s @" % str(T))
                            break
                        else:
                            T.append((j-t,j))
                            _log.debug("%s @@" % str(T))
                            break
                    t=t+1
                    if t>(j-1)/2:
                        T.append((0,j))
                        _log.debug("%s @@@" % str(T))
            i=i+1
        tau=arith1.CRT(T)
        if tau>M/2:
            tau=tau-M
        return tau

    def _step(self,P,W):
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
        """
        This program is using
        Algorithm 7.5.3(Shanks-Mestre assessment of curve order)
        Crandall & Pomerance ,PRIME NUMBERS
        self.ch<=10**5+o(1)
        This returns t=self.ch+1-#E(F_p)
        """
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
            f=polynomial.OneVariableDensePolynomial([other.b,other.a,0,1],"X",other.field)
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
                L=E._step(P,W)
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

    def naive(self):
        other=self.simple()
        k=0
        for i in range(0,other.ch):
            k=k+arith1.legendre(i*(i**2+other.a.n)+other.b.n,other.ch)
        return -k

    def order(self,flag=None):
        """
        this returns #E(Fp)
        if flag==False : #E/F_p
        else:#E/F_{p^r}, E is defined over F_p
        """
        if self.ch<=3:
            raise NotImplementedError("this is not implemented.")
        if self.ch<10**4:
            if flag:
                return pow(self.ch,flag)+1-powOrd(self.naive(),flag,self.ch)
            if not self.o:
                self.o=self.ch+1-self.naive()
        elif self.ch<10**30:
            if flag:
                return pow(self.ch,flag)+1-powOrd(self.Shanks_Mestre(),flag,self.ch)
            if not self.o:
                self.o=self.ch+1-self.Shanks_Mestre()
        else: # self.ch>=10**30
            if flag:
                return pow(self.ch,flag)+1-powOrd(self.Schoof(),flag,self.ch)
            if not self.o:
                self.o=self.ch+1-self.Schoof()
        return self.o

    def line(self,P,Q=None):
        """
        this use to compute weil pairing
        isinstance((P,Q),list),P,Q \in E
        over F_p
        self is E_{a,b}
        """
        p=self.ch
        x = polynomial.OneVariableMonomial("x", coeffring=self.field)
        y = polynomial.OneVariableMonomial("y", coeffring=self.field)
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
                f=(3*s**2+2*self.a2*s+self.a4-self.a1*t)*x-(2*t+self.a1*s+self.a3)*y
                f=f-(s**3)+self.a4*s+2*self.a6-self.a3*t
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
                Q = [self.field.createElement(e) for e in Q]
                P = [self.field.createElement(e) for e in P]
                f=(Q[1]-P[1])*(x-P[0])-(Q[0]-P[0])*(y-P[1])
                if isinstance(f,(int,finitefield.FinitePrimeFieldElement)):#
                    return 0,f
                elif len(f.variable)==2:
                    return 2,f
                elif 'x' in f.variable:
                    return 1,f
                else:
                    return -1,f

    def pointorder(self,P,ord=None,f=None):
        """
        find point order of P and return order.
        """
        # parameter ord and f are extension for structre.
        if ord:
            N = ord
        else:
            N = self.order()
        if f:
            l = f
        else:
            l = factor_methods.factor(N)
        o=1
        for p,e in l:
            B=self.mul(N//(p**e),P)
            while B!=[0]:
                o=o*p
                B=self.mul(p,B)
        return o

    def findpoint(self,m):
        """
        returns point P in E/F_p s.t mP == [0] .
        """
        if self.order()%m:
            raise ValueError("point order does not divide group order.")
        else:
            while 1:
                P=self.point()
                if self.mul(m,P)==[0]:
                    return P

    def _divisor(self,k,j,P,R,S):
        """
        returns divisor value of function
        use for compute Miller's Algorithm.
        """
        kP=self.mul(k,P)
        jP=self.mul(j,P)
        l=self.line(kP,jP)
        if l[0]==0:
            f_n1=l[1]
            f_d2=l[1]
        elif l[0]==1:
            f_n1=l[1](S[0])
            f_d2=l[1](R[0])
        elif l[0]==-1:
            f_n1=l[1](S[1])
            f_d2=l[1](R[1])
        else:
            f_n1=l[1](x=S[0],y=S[1])
            f_d2=l[1](x=R[0],y=R[1])
        l=self.line(self.add(kP,jP))
        if l[0]==0:
            f_n2=l[1]
            f_d1=l[1]
        else:
            f_n2=l[1](R[0])
            f_d1=l[1](S[0])
        if not f_d1*f_d2:
            return False
        return (f_n1*f_n2)/(f_d1*f_d2)

    def Miller(self,P,m,Q,R):
        """
        this returns value of function
        with divisor f_P(D_Q)
        this use for only compute Weil-Tate pairing
        """
        # check order
        if m<2 or not (self.ch%m):
            raise ValueError("order more than 1 and divisible characteristic")

        # check points are not infinity point
        if P==Q==[0] or Q==[0]:
            raise ValueError("You must input not [0]")
        
        # initialize
        S=self.add(R,Q)
        if S==[0]:
            return False

        f0=self.field.one
        f1=self.field.one
        f=f1

        M=m
        j=0
        k=1
        vj=f0
        vk=f1
        while M>0:
            if not (M%2):
                f=self._divisor(k,k,P,R,S)
                if not f:
                    return False
                vk=vk**2*f
                k=k*2
                M=M//2
            if M%2:
                f=self._divisor(k,j,P,R,S)
                if not f:
                    return False
                vj=vj*vk*f
                j=j+k
                M=M-1
                        
        return vj

    def TatePairing(self,m,P,Q):
        """
        computing the Tate-Lichetenbaum pairing with Miller's algorithm.
        """
        if m%self.BSGS(P) or m%self.BSGS(Q):
            raise ValueError("sorry, not mP=[0] or mQ=[0].")

        if P==[0] or Q==[0]:
            return self.field.one
        T=False
        while (not T) or (T.order()==1):
            R=[0]
            while R==P or R==Q or R==[0] or R==self.sub(Q,P):
                R=self.point()
            T=self.Miller(P,m,Q,R)
        return T

    def TatePairing_Extend(self,m,P,Q):
        """
        computing the Tate-Lichtenbaum pairing extended original Tate Pairing.
        """
        if P==[0] or Q==[0]:
            return self.field.one

        return self.TatePairing(m,P,Q)**((self.ch-1)//m)

    def WeilPairing(self,m,P,Q):
        """
        computing the Weil pairing with Miller's algorithm.
        """
        if m%self.BSGS(P) or m%self.BSGS(Q):
            raise ValueError("sorry, not mP=[0] or mQ=[0].")

        if P==[0] or Q==[0] or P==Q:
            return self.field.one
  
        while 1:
            T=U=False
            while (not T) or (not U):
                R=[0]
                while R==P or R==Q or R==[0] or R==self.sub(Q,P):
                    R=self.point()
                S=self.add(P,R)
                if S==[0]:
                    continue
                T=self.Miller(Q,m,P,R)
                S=self.sub(Q,R)
                if S==[0]:
                    continue
                U=self.Miller(P,m,Q,self.mul(-1,R))
            F=T/U
            return F

    def BSGS(self, P):
        """
        returns order of P such that kP=[0]
        refered to Washington 4.3.4.
        """
        if P==[0]:
            return 1

        Q = self.mul(self.ch+1, P)
        m = int(math.sqrt(math.sqrt(self.ch)))+1
        Plist = [[0]]
        R = P
        j = 1
        while j <= m:
            Plist.append(R)
            R = self.add(R, P)
            j = j+1
        R = self.mul(2*m, P)
        k = -m
        Plist_rev = map(self.mul,[-1]*(m+1), Plist) # make reverse point mapping
        j = 0
        while k <= m:
            S = self.add(Q, self.mul(k, R))
            if S!=[0]:
                if S in Plist:
                    j = Plist.index(S)
                    break
                elif S in Plist_rev:
                    j = -Plist_rev.index(S)
                    break
            k = k+1
        M = self.ch+1+2*m*k-j
        Flist = factor_methods.factor(M)
        for p,e in Flist:
            for i in range(e):
                if self.mul(M//p, P) == [0]:
                    M = M//p
        return M
            
    def DLP_BSGS(self,n,P,Q):
        """
        returns k such that Q=kP
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
        p=self.ch
        x = polynomial.OneVariableMonomial("x", coeffring=self.field)
        other=self.simple()
        Y=x**3+other.a*x+other.b
        L=[]
        i=0
        while i<p:
            y=Y(i).n
            if arith1.legendre(y,p)==1:
                Q=[i,arith1.modsqrt(y,p)]
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
        """
        returns group structure E(K)=Z_d x Z_m with d|m|#E(K)
        """
        if self.abelian:
            return self.abelian
        
        # step 1. find order E/F_p.
        simplified=self.simple()
        N=simplified.order()
        if prime.primeq(N):
            return (1,N)
        if simplified.issupersingular() and simplified.ch%4==1:
            return (1,N)
        
        # step 2. decompose N.
        r = gcd.gcd(simplified.ch - 1, N)
        r_factor = factor_methods.factor(r)
        N0 = r
        N1,N2 = 1,N
        for p,e in r_factor:
            while gcd.gcd(p,N2) > 1:
                N1,N2 = N1*p, N2//p
        
        while 1:
            P1 = [0]
            while P1 == [0]:
                P1 = simplified.point()
            P2 = [0]
            while P2 == [0]:
                P2 = simplified.point()
            P1,P2=simplified.mul(N2,P1), simplified.mul(N2,P2)
            s=simplified.pointorder(P1,r,r_factor)
            t=simplified.pointorder(P2,r,r_factor)
            m=gcd.lcm(s,t)
            if m>1:
                e=simplified.WeilPairing(m,P1,P2)
                if e!=self.field.one:
                    d=e.order()
                else:
                    d=1
                #print m,d
                if m*d==N1:
                    self.abelian = (d,N//d)
                    return self.abelian

    def issupersingular(self):
        """
        returns supersingularities.
        """
        if self.order()==self.ch+1:
            return True
        else:
            return False
    

class ECoverF2(ECoverFp):
    """
    Elliptic curves over F2.
    """
    def __init__(self,coefficient, index=None):
        ECGeneric.__init__(self, coefficient, 2, index)
        for c in coefficient:
            if not isinstance(c, (int,long,finitefield.FinitePrimeFieldElement)):
                raise ValueError("you must input integer coefficients.")
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
                    if self.disc:
                        self.j=self.disc.inverse()
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
                    raise ValueError("can't defined EC.")
                if self.disc.n==0:
                    raise ValueError("this curve is singular.")
            else:
                raise ValueError("coefficient is less or more, can't defined EC.")
    def __repr__(self):
        if len(self)==2 or self.a1.n==self.a2.n==self.a3.n==0:
            return "ECoverF2(["+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"
        else:
            return "ECoverF2(["+repr(self.a1.n)+","+repr(self.a2.n)+","+repr(self.a3.n)+","+repr(self.a4.n)+","+repr(self.a6.n)+"],"+repr(self.ch)+","+repr(self.index)+")"

    def line(self,P,Q=None):
        raise NotImplementedError("This is not implemented.")

    def structure(self):
        raise NotImplementedError("This is not implemented.")


def EC(coefficient,character=None,index=None):
    """
    generate new elliptic curve class.
    """
    if isinstance(coefficient,list):
        if not character:
            return ECoverQ(coefficient)
        elif character == 1:
            raise ValueError("characteristic must be 0 or prime.")
        elif character == 2:
            if not index or index == 1: #field=F_2
                return ECoverF2(coefficient)
            else: #field=F_q,q=2^r
                """
                index is irred polynomial in F_p,deg=r
                To add this, we must exchange field and element.
                """
                raise NotImplementedError("now we can use only over finite prime fields.")
        else:
            if not index or index == 1: #field=F_p
                return ECoverFp(coefficient, character)
            else: #field=F_q,q=(character)^r
                """
                index is irred polynomial in F_p,deg=r
                To add this, we must exchange field and element.
                """
                raise NotImplementedError("now we can use only over finite prime fields.")
