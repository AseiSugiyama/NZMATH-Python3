import polynomial

class Quadratic:
    def __init__(self,valuelist,root):
        if len(valuelist) == 2:
            self.dis = root
            self.quad = valuelist
            if self.dis % 4 == 2:
                self.type = 0
            elif self.dis % 4 == 3:
                self.type = 0
            elif self.dis % 4 == 1:
                self.type = 1
            else:
                raise ValueError
        else:
            raise ValueError
    def __repr__(self):
        return_str = '%s(%s,%s)' % (self.__class__.__name__,
                                       repr(self.quad),
                                       repr(self.dis))
        return return_str
    def __str__(self):
        if self.type == 0:
            return "%s+%s*sqrt(%s)" % (self.quad[0],self.quad[1],self.dis)
        else:
            return "%s+%s*(1+sqrt(%s))/2" % (self.quad[0],self.quad[1],self.dis)
    def __add__(self,other):
        return Quadratic([self.quad[0]+other[0],self.quad[1]+other[1]],self.dis)
    def __sub__(self,other):
        return Quadratic([self.quad[0]-other[0],self.quad[1]-other[1]],self.dis)
    def __mul__(self,other):
        if self.type == 0:
            return Quadratic([self.quad[0]*other[0]+self.quad[1]*other[1]*self.dis,self.quad[0]*other[1]+self.quad[1]*other[0]],self.dis)
        else:
            return Quadratic([self.quad[0]*other[0]+self.quad[1]*other[1]*(self.dis-1)/4,self.quad[0]*other[1]+self.quad[1]*other[0]+self.quad[1]*other[1]],self.dis)
    def __getitem__(self,index):
        return self.quad[index]
    def __setitem__(self,index,value):
        self.quad[index] = value
    def Discriminant(self):
        if self.type == 0:
            return 4*self.dis
        else:
            return self.dis
    def poly(self,variable):
        x = '%s' % (variable)
        return polynomial.OneVariableDensePolynomial([-self.dis,0,1],x)
    def translation(self):
        if self.type == 0:
            return FundamentalQuadratic([self.quad[0]-2*self.quad[1]*self.dis,self.quad[1]],self.dis*4)
        else:
            return FundamentalQuadratic([self.quad[0]+self.quad[1]*(1-self.dis)/2,self.quad[1]],self.dis)

class FundamentalQuadratic(Quadratic):
    def __init__(self,Valuelist,Root):
        if len(Valuelist) == 2:
            self.dis = Root
            self.quad = Valuelist
            if self.dis % 4 == 0:
                if self.dis/4 == 1:
                    raise ValueError
                elif self.dis/4 == 0:
                    raise ValueError
            elif self.dis % 4 == 1:
                raise ValueError
        else:
            raise ValueError
    def __str__(self):
        return "%s+%s*(%s+sqrt(%s))/2" % (self.quad[0],self.quad[1],self.dis,self.dis) 
    def __add__(self,other):
        return FundamentalQuadratic([self.quad[0]+other[0],self.quad[1]+other[1]],self.dis)
    def __sub__(self,other):
        return FundamentalQuadratic([self.quad[0]-other[0],self.quad[1]-other[1]],self.dis)
    def __mul__(self,other):
        return FundamentalQuadratic([self.quad[0]*other[0]+self.quad[1]*other[1]*(self.dis-self.dis**2)/4,self.quad*other[1]+self.quad[1]*other[1]+self.quad[1]*other[1]*self.dis],self.dis)
    def translation(self):
        if self.dis % 4 == 1:
            return Quadratic([self.quad[0]+self.quad[1]*(self.dis-1)/2,self.quad[1]],self.dis)
        else:
            return Quadratic([self.quad[0]+2*self.quad[1]*self.dis/4,self.quad[1]],self.dis/4)
    def Discriminant(self):
        return self.dis
