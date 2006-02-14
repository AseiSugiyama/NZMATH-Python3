import math
import nzmath.gcd
import nzmath.arith1
import nzmath.rational

class ElementOfQuadraticForm:
    def __init__(self,element,unit):
        self.element = element
        self.unit = unit
    def __repr__(self):
        return_str = '%s' % self.element
        return return_str
    def __mul__(self, other):
        if not isinstance(other, ElementOfQuadraticForm):
            return NotImplemented
        return computePDF(self.element, other.element)
    def __pow__(self, exp):
        if type(exp) != int:
            raise ValueError
        if exp == 0:
            return self.unit
        elif exp == 1:
            return self.element
        eltemp = self.element
        while exp != 1:
            eltemp = computePDF(eltemp, self.element)
            exp = exp - 1
        return eltemp
            

class QuadraticForm:
    """
    This is a class of quadratic form.
    """
    def __init__(self, disc):
        self.disc = disc
        self.classnumber, tempelements = computeClassNumber(disc)
        self.unit = tempelements[0]
        self.elements = []
        for tempelement in tempelements:
            self.elements.append(ElementOfQuadraticForm(tempelement, self.unit))

            
    def __repr__(self):
        return_str = 'disc -> %s\nclassnumber -> %s\nelements -> %s\nunit -> %s' % (
            self.disc, self.classnumber, self.elements, self.unit)
        return return_str

    def __eq__(self, other):
        if not self and not other:
            return True
        if self is other:
            return True
        if isinstance(other, QuadraticForm):
            if self.disc == other.disc:
                return True
            else:
                return False
        else:
            return NotImplemented
        
def deg_rounity(dis):
    '''
    caluclation of w(D)
    '''
    if dis >= 0:
        raise ValueError
    if dis % 4 not in (0,1):
        raise ValueError
    
    if dis < -4:
        return 2
    elif dis == -4:
        return 4
    elif dis == -3:
        return 6
    else:
        print "unknown error"
        raise ValueError

def reducePDF(a):
    '''
    Reduction of Positive Definite Forms
    f = (a[0], a[1], a[2])
    '''
    if a[0] < 0:
        raise ValueError , ("a must be positive in quadratic form f=(a,b,c).")
    if (a[1]**2 - 4*a[0]*a[2]) >= 0:
        raise ValueError , ("discriminant (D= b^2 - 4*a*c) must be negative.")
    if (-a[0] <  a[1]) and (a[1] <= a[0]):
        if a[0] > a[2]:
            a[1] = -a[1]
            a[0], a[2] = a[2], a[0]
        else:
            if (a[0] == a[2]) and (a[1] < 0):
                a[1] = -a[1]
            return [a[0], a[1], a[2]]
    while 1:
        q = a[1] / (2*a[0])
        r = a[1] - q*(2*a[0])
        if r > a[0]:
            r = r - 2*a[0]
            q = q + 1
        a[2] = a[2] - ((a[1] + r)/2)*q
        a[1] = r
        if a[0] > a[2]:
            a[1] = -a[1]
            a[0], a[2] = a[2], a[0]
            continue
        else:
            if (a[0] == a[2]) and (a[1] < 0):
                a[1] = -a[1]
            return [a[0], a[1], a[2]]

def dis_chk(f):
    if len(f) != 3:
        raise ValueError
    for i in f:
        if type(i) != int:
            raise ValueError
    return (f[1]*f[1] - 4*f[0]*f[2])
    
def computePDF(f_1, f_2):

    '''
    Composition of Positive Definite Forms.
    '''

    if nzmath.gcd.gcd_of_list(f_1)[0] != 1:
        raise ValueError , \
              ("coefficients of a quadratic form must be relativery prime")
    if nzmath.gcd.gcd_of_list(f_2)[0] != 1:
        raise ValueError , \
              ("coefficients of a quadratic form must be relativery prime")
    if dis_chk(f_1) != dis_chk(f_2):
        raise ValueError , \
              ("two quadratic forms must have same discriminant")

    if f_1[0] > f_2[0]:
        f_1, f_2 = f_2, f_1
        
    s = (f_1[1] + f_2[1])/2
    n = f_2[1] - s

    if f_2[0] % f_1[0] == 0:
        y_1 = 0
        d = f_1[0]
    else:
        #        u, v, d = nzmath.gcd.extgcd(f_2[0], f_1[0])
        u, v, d = euclid_exd(f_2[0], f_1[0])
        y_1 = u

    if s % d == 0:
        y_2 = -1
        x_2 = 0
        d_1 = d
    else:
#        print s
#        print d
        #u, v, d_1 = nzmath.gcd.extgcd(s,d)
        u, v, d_1 = euclid_exd(s, d)
        x_2 = u
        y_2 = -v

    v_1 = (f_1[0] / d_1)
    v_2 = (f_2[0] / d_1)
    r = (y_1*y_2*n - x_2*f_2[2]) % v_1
    
    b_3 = f_2[1] + 2*v_2*r
    a_3 = v_1*v_2
    c_3 = (f_2[2]*d_1 + r*(f_2[1] + v_2*r))/v_1
    f_3 = [a_3, b_3, c_3]

    return reducePDF(f_3)
    
def computeClassNumber(disc, limit_dis=100000):
    '''
    counting reduced forms. not only fundamenta discriminant.
    '''

    if disc % 4 not in (0, 1):
        raise ValueError , \
              ("a discriminant must be 0 or 1 mod 4")
    if disc >= 0:
        raise ValueError , \
              ("a discriminant must be negative")

    h = 1
    b = disc % 2
    c_b = long(math.sqrt(float(- disc) / 3))

    if disc < limit_dis:
        ret_list = []
        f_a = 1
        if disc % 4 == 0:
            f_b = 0
            f_c = -(disc / 4)
        else:
            '''
            caution!!!
            reduced form of b is not -1 but 1
            f_b = -1
            '''
            f_b = 1
            f_c = -((disc - 1) / 4)
        ret_list.append([f_a, f_b, f_c])
        
    while b <= c_b:
        chk_f = 0
        q = (b**2 - disc) / 4
        a = b
        if a <= 1:
            a = 1
            chk_f = 1
        while 1:
            if chk_f == 0:
                if (q % a == 0) and nzmath.gcd.gcd_of_list([a, b, q/a])[0] == 1:
                    if (a == b) or (a**2 == q) or (b == 0):
                        h += 1
                        if disc < limit_dis:
                            f_a = a
                            f_b = b
                            f_c = -(disc - f_b*f_b)/(4*f_a)
                            ret_list.append([f_a, f_b, f_c])
                    else:
                        h += 2
                        if disc < limit_dis:                        
                            f_a = a
                            f_b = b
                            f_c = -(disc - f_b*f_b)/(4*f_a)
                            ret_list.append([f_a, f_b, f_c])
                            ret_list.append([f_a, -f_b, f_c])
                        
            chk_f = 0
            a += 1
            if a**2 <= q:
                continue
            else:
                break
        b += 2
        #        if b <= c_b:
        #            continue
        #        else:

    return h,ret_list

def euclid_exd(a,b):
    if (type(a) != int) or (type(b) != int):
        raise ValueError
    u = 1
    d = a
    if b == 0:
        v = 0
        return (u, v, d)
    else:
        v_1 = 0
        v_3 = b
        
        while 1:
            if v_3 == 0:
                v = (d - a*u)/b
                return (u, v, d)
            q = d/v_3
            t_3 = d % v_3
            t_1 = u - q*v_1
            u = v_1
            d = v_3
            v_1 = t_1
            v_3 = t_3
            
