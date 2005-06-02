class quadratic:
    def __init__(self,valuelist,discriminant):
        if len(valuelist) == 2:
            self.dis = discriminant
            self.quad = valuelist
            self.int = self.quad[0]
            self.alg = self.quad[1]
            if discriminant%4 == 2 or 3:
                self.type = 0
            elif discriminant%4 == 1:
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
        return "%s+%s*sqrt(%s)" % (self.int,self.alg,self.dis)
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
    def display(self):
        print self.quad
    
