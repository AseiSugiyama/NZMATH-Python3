import arith1
import math
import polynomial 
import prime
import random
import rational 
        
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
            else:
                for i in range(0,len(self)):
                    if isinstance(coefficient[i],int):
                        if self.ch==2 or self.ch==3 or prime.millerRabin(self.ch)==1:
                            if len(self)==5:
                                self.a1=coefficient[0]%self.ch
                                self.a2=coefficient[1]%self.ch
                                self.a3=coefficient[2]%self.ch
                                self.a4=coefficient[3]%self.ch
                                self.a6=coefficient[4]%self.ch
                                self.b2=(self.a1**2+4*self.a2)%self.ch
                                self.b4=(self.a1*self.a3+2*self.a4)%self.ch
                                self.b6=(self.a3**2+4*self.a6)%self.ch
                                self.b8=(self.a1**2*self.a6+4*self.a2*self.a6-self.a1*self.a3*self.a4+self.a2*self.a3**2-self.a4**2)%self.ch
                                self.c4=(self.b2**2-24*self.b4)%self.ch
                                self.c6=(-self.b2**3+36*self.b2*self.b4-216*self.b6)%self.ch
                                self.disc=(-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6)%self.ch
                                if self.disc==0:
                                    raise ValueError, "singuler curve (@_@)"
                                j=rational.Rational(self.c4**3,self.disc)*1
                                if isinstance(j,rational.Rational):
                                    jd=j.denominator
                                    jn=j.numerator
                                else:
                                    jd=1
                                    jn=j
                                self.j=(jn*arith1.inverse(jd,self.ch))%self.ch
                            elif len(self)==2:
                                self.a=coefficient[0]%self.ch
                                self.b=coefficient[1]%self.ch
                                self.a1=0
                                self.a2=0
                                self.a3=0
                                self.a4=coefficient[0]%self.ch
                                self.a6=coefficient[1]%self.ch
                                self.b2=0
                                self.b4=(2*self.a)%self.ch
                                self.b6=(4*self.b)%self.ch
                                self.b8=(-self.a**2)%self.ch
                                self.c4=(-48*self.a)%self.ch
                                self.c6=(-864*self.b)%self.ch
                                self.disc=(-self.b2**2*self.b8-8*self.b4**3-27*self.b6**2+9*self.b2*self.b4*self.b6)%self.ch
                                if self.disc==0:
                                    raise ValueError, "singuler curve (@_@)"
                                j=rational.Rational(self.c4**3,self.disc)*1
                                if isinstance(j,rational.Rational):
                                    jd=j.denominator
                                    jn=j.numerator
                                else:
                                    jd=1
                                    jn=j
                                self.j=(jn*arith1.inverse(jd,self.ch))%self.ch
                            else:
                                raise ValueError, "coefficient is less or more, can't defined EC (-_-;)"
                        else:
                            raise ValueError "characteristic must be 0 or prime (-_-;)"
                    else:
                        raise ValueError, "you must input (coefficient,int) m(__)m"
        else:
            raise ValueError, "you must input (coefficient,list) m(__)m"
           
    def __len__(self):
        return len(self.coefficient)

    #def __call__
    #def __getitem__
   
    def __repr__(self):
        if len(self)==2 or self.a1==self.a2==self.a3==0:
            return "EC(["+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")"
        else:
            return "EC(["+repr(self.a1)+","+repr(self.a2)+","+repr(self.a3)+","+repr(self.a4)+","+repr(self.a6)+"],"+repr(self.ch)+")"

    def __str__(self):
        return str(polynomial.MultiVariableSparsePolynomial({(0,2):1,(1,1):self.a1,(0,1):self.a3,(3,0):-1,(2,0):-self.a2,(1,0):-self.a4,(0,0):-self.a6},["x","y"]))

#class Pt:

def simple(E): # over Fp

    """
    this transforms E:y^2+a1*x*y+a3*y=x^3+a2*x^2+a4*x+a6 to E':Y^2=X^3+(-27*c4)*X+(-54*c6),
    if ch is not 2 or 3
    
    """
    if len(E)==2 or (E.a1==E.a2==E.a3==0):
        raise "no need to simplyfy (^o^)"
    else:
        if E.ch==0:
            F=EC([-27*E.c4,-54*E.c6],E.ch)
            return F   
        elif E.ch==3:
            raise NotImplementedError, "Now making (>_<)"
        elif E.ch==2:
            raise NotImplementedError, "Now making (>_<)"
        else:
            F=EC([(-27*E.c4)%E.ch,(-54*E.c6)%E.ch],E.ch)
            return F

def changeCurve(E,V):
    
    """
    this transforms E to E' by V=[u,r,s,t] ; x->u^2*x'+r,y->u^3*y'+s*u^2*x'+t 
    
    """
    if isinstance(V,list): 
        if len(V)==4:
            if V[0]!=0:
                if E.ch==0:
                    F=EC([rational.Rational(E.a1+2*V[2],V[0])*1,
                          rational.Rational(E.a2-V[2]*E.a1+3*V[1]-V[2]**2,V[0]**2)*1,
                          rational.Rational(E.a3+V[1]*E.a1+2*V[3],V[0]**3)*1,
                          rational.Rational(E.a4-V[2]*E.a3+2*V[1]*E.a2-(V[3]+V[1]*V[2])*E.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4)*1,
                          rational.Rational(E.a6+V[1]*E.a4+V[1]**2*E.a2+V[1]**3-V[3]*E.a3-V[3]**2-V[1]*V[3]*E.a1,V[0]**6)*1],0) 
                    return F
                else: #E.ch!=0
                    for i in range(0,4):
                        if isinstance(V[i],int):
                            A=[rational.Rational(E.a1+2*V[2],V[0])*1,
                               rational.Rational(E.a2-V[2]*E.a1+3*V[1]-V[2]**2,V[0]**2)*1,
                               rational.Rational(E.a3+V[1]*E.a1+2*V[3],V[0]**3)*1,
                               rational.Rational(E.a4-V[2]*E.a3+2*V[1]*E.a2-(V[3]+V[1]*V[2])*E.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4)*1,
                               rational.Rational(E.a6+V[1]*E.a4+V[1]**2*E.a2+V[1]**3-V[3]*E.a3-V[3]**2-V[1]*V[3]*E.a1,V[0]**6)*1]
                            B=[]
                            for i in range(0,5):
                                if isinstanse(A[i],rational.Rational):
                                    ad=A[i].denominator
                                    an=A[i].numerator
                                    B.append((arith1.inverse(ad,E.ch),an))
                                else:
                                    ad=1
                                    an=A[i]
                                    B.append((arith1.inverse(ad,E.ch),an))
                            F=EC([(B[0][0]*B[0][1])%E.ch,
                                  (B[1][0]*B[1][1])%E.ch,
                                  (B[2][0]*B[2][1])%E.ch,
                                  (B[3][0]*B[3][1])%E.ch,
                                  (B[4][0]*B[4][1])%E.ch],E.ch)
                            return F
                        else:
                            raise ValueError, "you must input (,int) m(__)m"
            else: # u==0
                raise ValueError, "you must input nonzero u (-_-;)"
        else:        
            raise ValueError, "you must input (-_-;)"
    else:
        raise ValueError, "you must input (,list) m(__)m"

def changePoint(E,P,V):
    
    """
    this transforms P to P' by V=[u,r,s,t] ; x->u^2*x'+r,y->u^3*y'+s*u^2*x'+t
    
    """
    if isinstance(P,list) and isinstance(V,list):
        if len(P)==2 and len(V)==4 and V[0]!=0:
            if E.ch==0:
                Q0=rational.IntegerIfIntOrLong(P[0]-V[1])/rational.IntegerIfIntOrLong(V[0]**2)
                Q1=rational.IntegerIfIntOrLong(P[1]-V[2]*(P[0]-V[1])-V[3])/rational.IntegerIfIntOrLong(V[0]**3)
            else:
                qx=rational.Rational(P[0]-V[1],V[0]**2)*1
                if isinstance(qx,rational.Rational):
                    qxd=qx.denominator
                    qxn=qx.numetator
                else:
                    qxd=1
                    qxn=qx
                Q0=(qxn*arith1.inverse(qxd,E.ch))%E.ch
                qy=rational.Rational(P[1]-V[2]*(P[0]-V[1])-V[3],V[0]**3)*1
                if isinstance(qy,rational.Rational):
                    qyd=qy.denominator
                    qyn=qy.numerator
                else:
                    qyd=1
                    qyn=qy
                Q1=(qyn*arith1.inverse(qyd,E.ch))%E.ch
            Q=[Q0,Q1]
            return Q
        else:
            raise ValueError, "(-_-;)"
    else:
        raise ValueError, "m(__)m"

def point(E): # E(ch>3):y^2=x^3+a*x+b use change!!     

    """
    this returns a random point on eliiptic curve over ch(field)>3
    
    """
    if E.ch!=0:
        if len(E)==2 or (E.a1==E.a2==E.a3==0):    
            t=0
            while arith1.legendre(t,E.ch)!=1:
                s=random.randrange(0,E.ch) #random??
                t=s**3+E.a4*s+E.a6
            return [s,arith1.sqroot(t,E.ch)]
        elif E.ch!=2 or E.ch!=3:#len==5
            F=simple(E)
            t=0
            while arith1.legendre(t,E.ch)!=1:
                s=random.randrange(0,E.ch) #random??
                t=s**3+F.a*s+F.b
            x=rational.Rational(s-3*E.b2,36)*1
            if isinstance(x,rational.Rational):
                xd=x.denominator
                xn=x.numerator
            else:
                xd=1
                xn=x
            y=rational.Rational(1,2)*(rational.Rational(arith1.sqroot(t,E.ch),108)-E.a1*x-E.a3)
            if isinstance(y,rational.Rational):
                yd=y.denominator
                yn=y.numerator
            else:
                yd=1
                yn=y
            return [(xn*arith1.inverse(xd,E.ch))%E.ch,(yn*arith1.inverse(yd,E.ch))%E.ch]
        else: #E.ch==2 or 3
            raise NotImplementedError, "Now making (>_<)"
    else: #E.ch==0
        raise NotImplementedError, "I don't know (?_?)"

def whetherOn(E,P): # E(ch>3):y^2=x^3+a*x+b

    """
    Determine whether P is on curve or not.
    Return 1 if P is on, return 0 otherwise.

    """
    if isinstance(P,list):
        if len(P)==2:
            if E.ch==0:
                if P[1]**2+E.a1*P[0]*P[1]+E.a3*P[1]==P[0]**3+E.a2*P[0]**2+E.a4*P[0]+E.a6:
                    return 1
                else:
                    return 0
            else:
                if (P[1]**2+E.a1*P[0]*P[1]+E.a3*P[1])%E.ch==(P[0]**3+E.a2*P[0]**2+E.a4*P[0]+E.a6)%E.ch:
                    return 1
                else:
                    return 0
        elif P==[0]:
            return 1
        else:
            raise ValueError, "you must input (len(point)==2) (-_-;)"
    else:
        raise ValueError, "you must input (point,list) m(__)m"

def add(E,P,Q):

    """
    this returns P+Q
    
    """
    if isinstance(P,list) and isinstance(Q,list):
        if whetherOn(E,P) and whetherOn(E,Q):
            if len(P)==len(Q)==2:
                if E.ch==0:
                    if P[0]==Q[0]:
                        if P[1]+Q[1]+E.a1*Q[0]+E.a3==0:
                            return [0]
                        else: # P=Q
                            s=rational.IntegerIfIntOrLong(3*P[0]**2+2*E.a2*P[0]+E.a4-E.a1*P[1])/rational.IntegerIfIntOrLong(2*P[1]+E.a1*P[0]+E.a3)
                            t=rational.IntegerIfIntOrLong(-P[0]**3+E.a4*P[0]+2*E.a6-E.a3*P[1])/rational.IntegerIfIntOrLong(2*P[1]+E.a1*P[0]+E.a3)
                    else: # P!=Q
                        s=rational.IntegerIfIntOrLong(Q[1]-P[1])/rational.IntegerIfIntOrLong(Q[0]-P[0])
                        t=rational.IntegreIfIntOrLong(P[1]*Q[0]-Q[1]*P[0])/rational.IntegerIfIntOrLong(Q[0]-P[0])
                    x3=s**2+E.a1*s-E.a2-P[0]-Q[0]
                    y3=-(s+E.a1)*x3-t-E.a3
                    R=[x3,y3]
                    return R
                else:
                    if P[0]==Q[0]:
                        if (P[1]+Q[1]+E.a1*Q[0]+E.a3)%E.ch==0:
                            return [0]
                        else: # P=Q
                            s=rational.Rational(3*P[0]**2+2*E.a2*P[0]+E.a4-E.a1*P[1],2*P[1]+E.a1*P[0]+E.a3)
                            t=rational.Rational(-P[0]**3+E.a4*P[0]+2*E.a6-E.a3*P[1],2*P[1]+E.a1*P[0]+E.a3)
                    else: # P!=Q
                        s=rational.Rational(Q[1]-P[1],Q[0]-P[0])
                        t=rational.Rational(P[1]*Q[0]-Q[1]*P[0],Q[0]-P[0])
                    x=s**2+E.a1*s-E.a2-P[0]-Q[0]
                    if isinstance(x,rational.Rational):
                        xd=(s**2+E.a1*s-E.a2-P[0]-Q[0]).denominator
                        xn=(s**2+E.a1*s-E.a2-P[0]-Q[0]).numerator
                    else:
                        xd=1
                        xn=x
                    x3=xn*arith1.inverse(xd,E.ch)%E.ch
                    y=-(s+E.a1)*x3-t-E.a3
                    if isinstance(y,rational.Rational):
                        yd=(-(s+E.a1)*x3-t-E.a3).denominator
                        yn=(-(s+E.a1)*x3-t-E.a3).numerator
                    else:
                        yd=1
                        yn=y
                    y3=yn*arith1.inverse(yd,E.ch)%E.ch
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

def sub(E,P,Q): # P-Q

    """
    this retuens P-Q
    
    """
    if isinstance(P,list) and isinstance(Q,list):
        if whetheron(E,P) and whetheron(E,Q):
            if len(P)==len(Q)==2:
                x=Q[0]
                y=-Q[1]-E.a1*Q[0]-E.a3
                R=[x,y] # R=-Q
                return add(E,P,R) 
            elif (P==[0]) and (Q!=[0]):
                x=Q[0]
                y=-Q[1]-E.a1*Q[0]-E.a3
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
            
def mul(E,k,P):
    
    """
    this returns [k]*P
    
    """
    if k>=0:
        l=arith1.expand(k,2)
        Q=[0]
        for j in range(len(l)-1,-1,-1):
            Q=add(E,Q,Q)
            if l[j]==1:
                Q=add(E,Q,P)
        return Q
    else:
        l=arith1.expand(-k,2)
        Q=[0]
        for j in range(len(l)-1,-1,-1):
            Q=add(E,Q,Q)
            if l[j]==1:
                Q=E.add(Q,P)
        return sub(E,[0],Q)
