from __future__ import division
import arith1
import imaginary
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
                    if not isinstance(coefficient[i],(int,long)):
                        raise ValueError, "you must input integer coefficients. m(__)m"
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
            elif self.ch==3:
                raise NotImplementedError, "Now making (>_<)"
            elif self.ch==2:
                raise NotImplementedError, "Now making (>_<)"
            else:
                other=EC([(-27*self.c4)%self.ch,(-54*self.c6)%self.ch],self.ch)
                return other

    def changeCurve(self,V):
        """
        this transforms E to E' by V=[u,r,s,t] ; x->u^2*x'+r,y->u^3*y'+s*u^2*x'+t 
        """
        if isinstance(V,list): 
            if len(V)==4:
                if V[0]!=0:
                    if self.ch==0:
                        other=EC([rational.Rational(self.a1+2*V[2],V[0])*1,
                              rational.Rational(self.a2-V[2]*self.a1+3*V[1]-V[2]**2,V[0]**2)*1,
                              rational.Rational(self.a3+V[1]*self.a1+2*V[3],V[0]**3)*1,
                              rational.Rational(self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4)*1,
                              rational.Rational(self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1,V[0]**6)*1],0) 
                        return other
                    else: #self.ch!=0
                        for v in V:
                            if not isinstance(v,(int,long)):
                                raise ValueError, "you must input integer m(__)m"
                        A=[rational.Rational(self.a1+2*V[2],V[0])*1,
                           rational.Rational(self.a2-V[2]*self.a1+3*V[1]-V[2]**2,V[0]**2)*1,
                           rational.Rational(self.a3+V[1]*self.a1+2*V[3],V[0]**3)*1,
                           rational.Rational(self.a4-V[2]*self.a3+2*V[1]*self.a2-(V[3]+V[1]*V[2])*self.a1+3*V[1]**2-2*V[2]*V[3],V[0]**4)*1,
                           rational.Rational(self.a6+V[1]*self.a4+V[1]**2*self.a2+V[1]**3-V[3]*self.a3-V[3]**2-V[1]*V[3]*self.a1,V[0]**6)*1]
                        B=[]
                        for i in range(0,5):
                            if isinstanse(A[i],rational.Rational):
                                ad=A[i].denominator
                                an=A[i].numerator
                                B.append((arith1.inverse(ad,self.ch),an))
                            else:
                                ad=1
                                an=A[i]
                                B.append((arith1.inverse(ad,self.ch),an))
                        other=EC([(B[0][0]*B[0][1])%self.ch,
                              (B[1][0]*B[1][1])%self.ch,
                              (B[2][0]*B[2][1])%self.ch,
                              (B[3][0]*B[3][1])%self.ch,
                              (B[4][0]*B[4][1])%self.ch],self.ch)
                        return other
                else: # u==0
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
                    qx=rational.Rational(P[0]-V[1],V[0]**2)*1
                    if isinstance(qx,rational.Rational):
                        qxd=qx.denominator
                        qxn=qx.numetator
                    else:
                        qxd=1
                        qxn=qx
                    Q0=(qxn*arith1.inverse(qxd,self.ch))%self.ch
                    qy=rational.Rational(P[1]-V[2]*(P[0]-V[1])-V[3],V[0]**3)*1
                    if isinstance(qy,rational.Rational):
                        qyd=qy.denominator
                        qyn=qy.numerator
                    else:
                        qyd=1
                        qyn=qy
                    Q1=(qyn*arith1.inverse(qyd,self.ch))%self.ch
                Q=[Q0,Q1]
                return Q
            else:
                raise ValueError, "(-_-;)"
        else:
            raise ValueError, "m(__)m"

    def point(self): # E(ch>3):y^2=x^3+a*x+b use change!!     
        """
        this returns a random point on eliiptic curve over ch(field)>3
        """
        if self.ch!=0:
            if len(self)==2 or (self.a1==self.a2==self.a3==0):    
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) #random??
                    t=s**3+self.a4*s+self.a6
                return [s,arith1.sqroot(t,self.ch)]
            elif self.ch!=2 or self.ch!=3:#len==5
                other=self.simple()
                t=0
                while arith1.legendre(t,self.ch)!=1:
                    s=random.randrange(0,self.ch) #random??
                    t=s**3+other.a*s+other.b
                x=rational.Rational(s-3*self.b2,36)*1
                if isinstance(x,rational.Rational):
                    xd=x.denominator
                    xn=x.numerator
                else:
                    xd=1
                    xn=x
                y=rational.Rational(1,2)*(rational.Rational(arith1.sqroot(t,self.ch),108)-self.a1*x-self.a3)
                if isinstance(y,rational.Rational):
                    yd=y.denominator
                    yn=y.numerator
                else:
                    yd=1
                    yn=y
                return [(xn*arith1.inverse(xd,self.ch))%self.ch,(yn*arith1.inverse(yd,self.ch))%self.ch]
            else: #self.ch==2 or 3
                raise NotImplementedError, "Now making (>_<)"
        else: #self.ch==0
            raise NotImplementedError, "I don't know (?_?)"

    def coordinateX(self,x):
        """ 
        this returns the y(P)>0,x(P)==x
        """
        y1=self.a1*x+self.a3
        y2=x**3+self.a2*x**2+self.a4*x+self.a6
        if self.ch!=0:
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
        else: #self.ch==0
            if y1**2+4*y2>=0:
                return rational.Rational((-1)*y1+math.sqrt(y1**2-4*y2),2)*1
            else:
                raise ValueError, "(-_-;)"
    def whetherOn(self,P): # E(ch>3):y^2=x^3+a*x+b

        """
        Determine whether P is on curve or not.
        Return 1 if P is on, return 0 otherwise.

        """
        if isinstance(P,list):
            if len(P)==2:
                if self.ch==0:
                    if P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1]==P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6:
                        return 1
                    else:
                        return 0
                else:
                    if (P[1]**2+self.a1*P[0]*P[1]+self.a3*P[1])%self.ch==(P[0]**3+self.a2*P[0]**2+self.a4*P[0]+self.a6)%self.ch:
                        return 1
                    else:
                        return 0
            elif P==[0]:
                return 1
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
                            else: # P=Q
                                s=rational.IntegerIfIntOrLong(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1])/rational.IntegerIfIntOrLong(2*P[1]+self.a1*P[0]+self.a3)
                                t=rational.IntegerIfIntOrLong(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1])/rational.IntegerIfIntOrLong(2*P[1]+self.a1*P[0]+self.a3)
                        else: # P!=Q
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
                            else: # P=Q
                                s=rational.Rational(3*P[0]**2+2*self.a2*P[0]+self.a4-self.a1*P[1],2*P[1]+self.a1*P[0]+self.a3)
                                t=rational.Rational(-P[0]**3+self.a4*P[0]+2*self.a6-self.a3*P[1],2*P[1]+self.a1*P[0]+self.a3)
                        else: # P!=Q
                            s=rational.Rational(Q[1]-P[1],Q[0]-P[0])
                            t=rational.Rational(P[1]*Q[0]-Q[1]*P[0],Q[0]-P[0])
                        x=s**2+self.a1*s-self.a2-P[0]-Q[0]
                        if isinstance(x,rational.Rational):
                            xd=(s**2+self.a1*s-self.a2-P[0]-Q[0]).denominator
                            xn=(s**2+self.a1*s-self.a2-P[0]-Q[0]).numerator
                        else:
                            xd=1
                            xn=x
                        x3=xn*arith1.inverse(xd,self.ch)%self.ch
                        y=-(s+self.a1)*x3-t-self.a3
                        if isinstance(y,rational.Rational):
                            yd=(-(s+self.a1)*x3-t-self.a3).denominator
                            yn=(-(s+self.a1)*x3-t-self.a3).numerator
                        else:
                            yd=1
                            yn=y
                        y3=yn*arith1.inverse(yd,self.ch)%self.ch
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

    def sub(self,P,Q): # P-Q

        """
        this retuens P-Q
        
        """
        if isinstance(P,list) and isinstance(Q,list):
            if self.whetherOn(P) and self.whetherOn(Q):
                if len(P)==len(Q)==2:
                    x=Q[0]
                    y=-Q[1]-self.a1*Q[0]-self.a3
                    R=[x,y] # R=-Q
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

    def divPoly(self,m):
        f=[]
        f.append(0)
        if self.ch!=2: # E(ch>3):y^2=x^3+a*x+b
            for i in range(1,m+1):
                if i==1:
                    f.append(1)
                elif i==2:
                    f.append(polynomial.OneVariableSparsePolynomial({(1,):1},["y"]))
                elif i==3:
                    f.append(polynomial.OneVariableSparsePolynomial({(0,):-self.a**2,(1,):12*self.b,(2,):6*self.a,(4,):3},["x"]))
                elif i==4:
                    f.append(4*f[2]*polynomial.OneVariableSparsePolynomial({(0,):-self.a**3-8*self.b**2,(1,):-4*self.a*self.b,(2,):-5*self.a**2,(3,):20*self.b,(4,):5*self.a,(6,):1},["x"]))
                else:
                    if i%2!=0:
                        j=(i-1)//2
                        g=f[j+2]*f[j]**3-f[j-1]*f[j+1]**3
                        f.append(g)
                    else:
                        j=i//2
                        g=(f[j+2]*f[j-1]**2-f[j-2]*f[j+1]**2)*f[j] #div 2y??
                        f.append(g)
                        #h=f[m]#->f'
            return f[m] #->f'
        else: #E(ch=2):y^2+x*y=x^3+a2*x^2+a6
            for i in range(1,m+1):
                if i==1:
                    f.append(1)
                elif i==2:
                    f.append(OneVariableSparsePolynomial({(1,):1},["x"]))
                elif i==3:
                    f.append(OneVariableSparsePolynomial({(0,):a6,(3,):1,(4,):1},["x"]))
                elif i==4:
                    f.append(OneVariableSparsePolynomial({(2,):a6,(6,):1},["x"]))
                else:
                    if i%2!=0:
                        j=(i-1)//2
                        g=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                        f.append(g)
                    else:
                        j=i//2
                        g=((f[j+2]*f[j-1]*f[j-1]+f[j-2]*f[j+1]*f[j+1])*f[j])/(OneVariableSparsePolynomial({(1,):1},["x"])) 
                        f.append(g)
                        #h=f[m]
            return f[m]

    def order(self): # =#E(Fp)
        """
        this returns #E(Fp)
        """
        def schoof(self):
            def divPoly(self,m):
                f=[]
                f.append(0)
                if self.ch!=2: # E(ch>3):y^2=x^3+a*x+b
                    for i in range(1,m+1):
                        if i==1:
                            f.append(1)
                        elif i==2:
                            f.append(polynomial.OneVariableSparsePolynomial({(1,):1},["y"]))
                        elif i==3:
                            f.append(polynomial.OneVariableSparsePolynomial({(0,):-self.a**2,(1,):12*self.b,(2,):6*self.a,(4,):3},["x"]))
                        elif i==4:
                            f.append(4*f[2]*polynomial.OneVariableSparsePolynomial({(0,):-self.a**3-8*self.b**2,(1,):-4*self.a*self.b,(2,):-5*self.a**2,(3,):20*self.b,(4,):5*self.a,(6,):1},["x"]))
                        else:
                            if i%2!=0:
                                j=(i-1)//2
                                g=f[j+2]*f[j]*f[j]*f[j]-f[j-1]*f[j+1]*f[j+1]*f[j+1]
                                f.append(g)
                            else:
                                j=i//2
                                g=(f[j+2]*f[j-1]*f[j-1]-f[j-2]*f[j+1]*f[j+1])*f[j] #div 2y??
                                f.append(g)
                                h=f[m]#->f'
                    return h
                else: #E(ch=2):y^2+x*y=x^3+a2*x^2+a6
                    for i in range(1,m+1):
                        if i==1:
                            f.append(1)
                        elif i==2:
                            f.append(OneVariableSparsePolynomial({(1,):1},["x"]))
                        elif i==3:
                            f.append(OneVariableSparsePolynomial({(0,):a6,(3,):1,(4,):1},["x"]))
                        elif i==4:
                            f.append(OneVariableSparsePolynomial({(2,):a6,(6,):1},["x"]))
                        else:
                            if i%2!=0:
                                j=rational.Rational(i-1,2)*1
                                g=f[j+2]*f[j]*f[j]*f[j]+f[j-1]*f[j+1]*f[j+1]*f[j+1]
                                f.append(g)
                            else:
                                j=rational.Rational(i,2)
                                g=((f[j+2]*f[j-1]*f[j-1]+f[j-2]*f[j+1]*f[j+1])*f[j])/(OneVariableSparsePolynomial({(1,):1},["x"])) 
                                f.append(g)
                    h=f[m]
                    return h

        def Shanks_Mestre(self):
            """
            This program is using
            Algorithm 7.5.3(Shanks-Mestre assessment of curve order)
            Crandall & Pomerance ,PRIME NUMBERS
            """
            if self.ch!=0:
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
                    #def BSGS(E,P,W):
                    pass
            else:
                raise "now making m(__)m"

        #def SEA(self):
            
        return Shanks_Mestre(self)

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
# t=imaginary.Complex(a,b)

def q(t):

    """
    this returns exp(2*pi*j*t)
    t is complex and h.imag>0
    """
    return imaginary.exp(2*imaginary.pi*imaginary.j*t)

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
    while abs(a(i+1))>x:
       b=a(i)+b
       print i
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
    qq=imaginary.exp(imaginary.pi*imaginary.j/12)
    def a(i):
        if i%2==0:
            return qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2)
        else:
            return (-1)*(qt**((3*i**2-i)/2)+qt**((3*i**2-i)/2))
    i=1
    b=0
    while abs(a(i+1))>x:
       b=a(k)+b
       i=i+1
    return qq*(1+b)


def intersectionOfTwoLists(list1,list2):
    list1.sort()
    list2.sort()
    L=[]
    i,j=0,0
    while i<len(list1) and j<len(list2):
        if list1[i]<=list2[j]:
            if list1[i]==list2[j]:
                L.append(list1[i])
            i=i+1
            while i<len(list1)-1 and list1[i]==list1[i-1]:
                i=i+1
        else:
            j=j+1
            while j<len(list2)-1 and list2[j]==list2[j-1]:
                j=j+1
    return L
                
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

