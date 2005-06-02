import polynomial

class quadratic:
    def __init__(self,valuelist,val):
        if len(valuelist) == 2:
            self.dis = val
            self.quad = valuelist
            self.int = self.quad[0]
            self.alg = self.quad[1]
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
            return "%s+%s*sqrt(%s)" % (self.int,self.alg,self.dis)
        else:
            return "%s+%s*(1+sqrt(%s))/2" % (self.int,self.alg,self.dis)
    def __add__(self,other):
        return quadratic([self.int+other[0],self.alg+other[1]],self.dis)
    def __sub__(self,other):
        return quadratic([self.int-other[0],self.alg-other[1]],self.dis)
    def __mul__(self,other):
        if self.type == 0:
            return quadratic([self.int*other[0]+self.alg*other[1]*self.dis,self.int*other[1]+self.alg*other[0]],self.dis)
        else:
            return quadratic([self.int*other[0]+self.alg*other[1]*(self.dis-1)/4,self.int*other[1]+self.alg*other[0]+self.alg*other[1]],self.dis)
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
