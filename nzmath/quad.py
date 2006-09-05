import math
import random
import copy
import nzmath.gcd
import nzmath.arith1
import nzmath.group
import nzmath.rational
import nzmath.factor.misc
import nzmath.factor.methods
import nzmath.finitefield
import nzmath.permute
import nzmath.integerResidueClass
import sys

class ReducedQuadraticForm:
    def __init__(self, element, unit):
        self.element = element
        self.unit = unit

    def __repr__(self):
        return_str = '%s' % self.element
        return return_str

    def __mul__(self, other):
        if not isinstance(other, ReducedQuadraticForm):
            return NotImplemented
        return self.__class__(computePDF(self.element[:], other.element[:]), self.unit[:])

    def __pow__(self, exp):
        if not isinstance(exp, (int, long)):
            raise TypeError("powering index must be an integer.")
        if exp == 0:
            return self.__class__(self.unit[:], self.unit[:])
        elif exp == 1:
            return self.__class__(self.element[:], self.unit[:])
        eltemp = self.element
        # Right-Left Binary algorithm
        sy = self.unit[:]
        if exp == 0:
            return self.__class__(sy,self.unit[:])
        if exp < 0:
            lexp = -exp
            sz = self.inverse().element[:]
        else:
            lexp = exp
            sz = self.element[:]
        while True:
            if (lexp % 2) == 1:
                sy = computePDF(sz, sy)
            lexp = lexp // 2
            if lexp == 0:
                return self.__class__(sy, self.unit[:])
            else:
                sz = sqrPDF(sz)
        
    def __div__(self,other):
        invel = other.inverse()
        return computePDF(self.element[:], invel.element[:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if (self.element == other.element) and (self.unit == other.unit):
            return True
        else:
            return False
    def __ge__(self, other):
        if self.__class__ != other.__class__:
            return False
        for valueofel in range(3):
            if (self.element[valueofel] > other.element[valueofel]):
                return True
            elif (self.element[valueofel] == other.element[valueofel]):
                continue
            else:
                return False
        return True
    def __le__(self, other):
        if self.__class__ != other.__class__:
            return False
        for valueofel in range(3):
            if (self.element[valueofel] < other.element[valueofel]):
                return True
            elif (self.element[valueofel] == other.element[valueofel]):
                continue
            else:
                return False
        return True
    
    def __gt__(self, other):
        if self.__class__ != other.__class__:
            return False
        for valueofel in range(3):
            if (self.element[valueofel] > other.element[valueofel]):
                return True
            elif (self.element[valueofel] == other.element[valueofel]):
                continue
            else:
                return False
        return False
    def __lt__(self, other):
        if self.__class__ != other.__class__:
            return False
        for valueofel in range(3):
            if (self.element[valueofel] < other.element[valueofel]):
                return True
            elif (self.element[valueofel] == other.element[valueofel]):
                continue
            else:
                return False
        return False
    def __ne__(self, other):
        if type(other) == list:
            return True
        if self.__class__ != other.__class__:
            return True
        if (self.element != other.element):
            return True
        else:
            return False
    def inverse(self):
        if self.element == self.unit[:]:
            return copy.deepcopy(self)
        else:
            cpyel = self.element[:]
            cpyel[1] = -cpyel[1]
            return ReducedQuadraticForm(reducePDF(cpyel), self.unit[:])
        
    def repOfModule(self):
        ld = self.element[1]**2 - 4*self.element[0]*self.element[2]
        a_m2 = 2*self.element[0]
        rb = -self.element[1]

        return_str = '%s * i r(%s) / %s' % (rb, ld, a_m2)
        return return_str

def deg_rounity(dis):
    """
    caluclation of w(D)
    """
    if dis >= 0:
        raise ValueError
    if dis % 4 not in (0, 1):
        raise ValueError

    if dis < -4:
        return 2
    elif dis == -4:
        return 4
    elif dis == -3:
        return 6
    else:
        raise ValueError("unknown error")

def reducePDF(at):
    """
    Reduction of Positive Definite Forms
    f = (a[0], a[1], a[2])
    """
    a = at[:]
    if a[0] < 0:
        raise ValueError("a must be positive in quadratic form f=(a,b,c).")
    if (a[1]**2 - 4*a[0]*a[2]) >= 0:
        raise ValueError("discriminant (D= b^2 - 4*a*c) must be negative.")
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
    """
    Composition of Positive Definite Forms.
    """

    if nzmath.gcd.gcd_of_list(f_1)[0] != 1:
        raise ValueError(
            "coefficients of a quadratic form must be relativery prime")
    if nzmath.gcd.gcd_of_list(f_2)[0] != 1:
        raise ValueError(
            "coefficients of a quadratic form must be relativery prime")
    if dis_chk(f_1) != dis_chk(f_2):
        raise ValueError(
            "two quadratic forms must have same discriminant")

    if f_1[0] > f_2[0]:
        f_1, f_2 = f_2, f_1

    s = (f_1[1] + f_2[1])/2
    n = f_2[1] - s

    if f_2[0] % f_1[0] == 0:
        y_1 = 0
        d = f_1[0]
    else:
        u, v, d = euclid_exd(f_2[0], f_1[0])
        y_1 = u

    if s % d == 0:
        y_2 = -1
        x_2 = 0
        d_1 = d
    else:
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
    """
    counting reduced forms. not only fundamental discriminant.
    """

    if disc % 4 not in (0, 1):
        raise ValueError("a discriminant must be 0 or 1 mod 4")
    if disc >= 0:
        raise ValueError("a discriminant must be negative")

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
            # caution!!!
            # reduced form of b is not -1 but 1
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
            if a**2 > q:
                break
        b += 2

    eounit = ret_list[0]
    for i, t_lt in enumerate(ret_list):
        ret_list[i] = ReducedQuadraticForm(t_lt, eounit)

    return (h, ret_list)

def euclid_exd(a, b):
    if not isinstance(a, (int, long)) or not isinstance(b, (int, long)):
        raise TypeError
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

def fundOrNot(disc):
    if disc == 1:
        return False
    if (disc % 4) == 1 and nzmath.factor.misc.squarePart(disc) == 1:
        return True
    elif (disc % 4) == 0 and nzmath.factor.misc.squarePart(disc // 4) == 1:
        discof = (disc // 4) % 4
        if discof == 2:
            return True
        elif discof == 3:
            return True
    return False


def ckfn(lwrbd, lwrbd_1, uprbd_1, h, n, sossp, sogsp, q, nt, y):
    '''
    this is a submodule called by the module, bsgs.
    check bsgs is finished or not yet.
    '''
    
    h[0] = h[0] * n[0]
    if h[0] >= lwrbd:
        return h[0]
    uprbd_1[0] = uprbd_1[0] // n[0] # floor of uprbd_1[0] // n[0]
    if (lwrbd_1[0] % n[0]) == 0:
        lwrbd_1[0] = lwrbd_1[0] // n[0] # floor + 1 of lwrbd_1[0] // n[0]
    else:
        lwrbd_1[0] = lwrbd_1[0] // n[0]  + 1 # floor + 1 of lwrbd_1[0] // n[0]
    if n[0] == 1:
        tpsq = [0, 2]
    else:
        tpsq = nzmath.factor.misc.primePowerTest(n[0])
    if tpsq[1] == 2:
        q[0] = nzmath.arith1.floorsqrt(n[0])
    else:
        q[0] = nzmath.arith1.floorsqrt(n[0]) + 1

    lsl = sossp[:]
    del sossp[:]
    lll = sogsp[:]
    del sogsp[:]

    for r in range(q[0]):
        for ss in lsl:
            newel = (nt[0]**r) * ss
            if newel not in sossp:
                sossp.append(newel) # multiple of two elements of G

    y[0] = nt[0]**q[0]

    for a in range(q[0] + 1):
        for eol in lll:
            newel2 = (y[0]**a) * eol
            if newel2 not in sogsp:
                sogsp.append(newel2) # multiple of two elements of G
    return -1

def cptodr(n, x, sossp, sogsp, c_s1, nt):
    # flg
    flg_bk = 1
    while flg_bk == 1:
        flg_bk = 0
        lst_p = nzmath.factor.misc.primeDivisors(n[0])
        tp_ls = sossp[:]

        del c_s1[:]
        for tmpri in lst_p:
            # initialize c_s1
            for ttp_ls in tp_ls:
                c_s1.append([(nt[0] ** (n[0] / tmpri)) * ttp_ls, 0])
                #c_s1.append([(x[1] ** (n[0] / tmpri)) * ttp_ls, 0])
            # sort
            c_s1.sort()

            for tmp_els in c_s1:
                for tmp_ell in sogsp:
                    if tmp_els[0] == tmp_ell:

                        flg_bk = 1
                        n[0] = n[0] / tmpri
                        break
                if flg_bk == 1:
                    break
            if flg_bk == 1:
                break

def cptgs(n, q, sz, y, c_s1, uprbd_1, sogsp):

    while 1:
        ########################### loop
        for tpw in sogsp:
            sz1 = sz[0] * tpw
            for tpcs in c_s1:
                if sz1 == tpcs[0]:
                    n[0] = n[0] - tpcs[1]
                    return True
        # continue (sp. 5)
        sz[0] = y[0] * sz[0]
        n[0] = n[0] + q[0]
        if n[0] -q [0] + 1 <= uprbd_1[0]:
            continue
        else:
            raise ValueError("the order is larger than upper bound")
    
def cptssp(q, x , n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, h, nt):
    '''
    compute small steps
    '''
    flg_s = 0
    # initialize
    y[0] = 0
    sz = [0]
    for tr in range(q[0]):
        # compute 2 to q-1
        if (tr != 0) and (tr != 1):
            x[tr] = x[1] * x[tr - 1]
            #ttpx[tr] = ttpx[tr - 1] * ttpx[1]
        for ttr in sossp:
            tmpx = x[tr]*ttr
            if (flg_s == 0) and (tmpx == ut) and (tr != 0):
                flg_s = 1
                n[0] = tr
            c_s1.append([tmpx, tr])
                # sort ( if you want to sort it with your estimate,
                # you have to implement '__ge__' method of the class with your way.)

    c_s1.sort()
    
    if flg_s != 1:
        y[0] = x[1] * x[q[0] - 1]
        sz[0] = x[1] ** lwrbd_1[0]
        n[0] = lwrbd_1[0]
        cptgs(n, q, sz, y, c_s1, uprbd_1, sogsp)
    n[0] = h[0] * n[0] 
        # 6
    cptodr(n, x, sossp, sogsp, c_s1, nt)
        
def bsgs(iordmel, lwrbd, uprbd):
    '''
    iordmel is a class. it return a random element of target infinite group.
    it return a unit of the group too.
    '''
    # check of bounds
    if lwrbd > uprbd:
        raise TypeError("lower bound needs to be less than upper bound")
    if lwrbd <= (uprbd / 2):
        raise TypeError("upper bound / 2 needs to be more than lower bound")
    h = [1] # h is integer
    lwrbd_1 = [lwrbd]
    uprbd_1 = [uprbd]
    # get the unit
    ut = iordmel.retunit()
    # append the unit to subset of G
    sossp = [] # a subset of target group, G
    sogsp = [] # a subset of G
    sossp.append(ut)
    sogsp.append(ut)
    # initialize variables
    n = [0]
    q = [0]
    h = [1] # order
    nt = [0] # next value
    y = [0]
    ret = -1
    # take a new element of the group.
    while ret == -1:
        # get next element
        nt[0] = iordmel.retnext()
        mstp1 = uprbd_1[0] - lwrbd_1[0]
        if (mstp1 == 0) or (mstp1 == 1):
            q[0] = 1
        else:
            tppm = nzmath.factor.misc.primePowerTest(mstp1)
            if tppm[1] == 2:
                q[0] = nzmath.arith1.floorsqrt(mstp1)
            else:
                q[0] = nzmath.arith1.floorsqrt(mstp1) + 1
        if q[0] <= 2:
            x = [0,0]
        else:
            x = [0] * q[0] # x is the set of elements of G
        c_s1 = [] # a subset of G
        # compute small steps        
        x[0] =  ut # maybe, this code must not be here
        x[1] = (nt[0] ** h[0])
        if x[1] == ut:
            n[0] = 1
            # initialize order
            n[0] = h[0] * n[0]
            # compute the order of nt[1]
            cptodr(n, x, sossp, sogsp, c_s1, nt)
        else:
            cptssp(q, x , n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, h, nt)
        # finished?
        ret = ckfn(lwrbd, lwrbd_1, uprbd_1, h, n, sossp, sogsp, q, nt, y)
    return ret
    
class Groupforbsgs(nzmath.group.GroupElement):
    def __init__(self, value):
        nzmath.group.GroupElement.__init__(self, value, 1)
        
    def __mul__(self, other):
        return Groupforbsgs(self.element * other.element)
    
    def __pow__(self, other):
        return Groupforbsgs(self.element ** other)


class NextElement:
    '''
    
    '''
    def retunit(self):
        return self
    def retnext(self):
        return self
    
class Nxtel(NextElement):
    def __init__(self, odr):
        if type(odr) != int:
            raise TypeError("the value must be integer")
        self.numlst = range(odr)
        self.odr = odr
        random.shuffle(self.numlst)
        
    def retunit(self):
        return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(1, self.odr))

    def retnext(self):
        while 1:
            tpa =  self.numlst.pop()
            if tpa == 1 or tpa == 0:
                continue
            return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(tpa, self.odr))


def sqrPDF(frm):
    '''
    return the square of frm = (a, b, c)
    '''
    frm_1 = frm[:]
    
    # compute disc and etc
    disc = frm_1[1]**2 - 4*frm_1[0]*frm_1[2]
    sogsp = nzmath.arith1.floorpowerroot(abs(float(disc)/4), 4)
    (u, v, d_1) = euclid_exd(frm_1[1], frm_1[0])

    la = frm_1[0] / d_1
    lb = frm_1[1] / d_1
    lc = (-frm_1[2] * u) % la
    c_1 = la - lc
    if c_1 < lc:
        lc = -c_1
    # partial reduction
    v_2, v_3, z, d , v = parteucl(la, lc, sogsp)

    if z == 0:
        g = (lb * v_3 + frm_1[2]) / d
        a_2 = d**2
        c_2 = v_3 ** 2
        b_2 = frm_1[1] + (d + v_3)**2 - a_2 - c_2
        c_2 = c_2 + g * d_1
        f_2 = reducePDF([a_2, b_2, c_2])
        return f_2
    e = (frm_1[2] * v + lb * d) / la
    g = (e * v_2 - lb) / v
    b_2 = e * v_2 + v * g
    if d_1 > 1:
        b_2 = d_1 * b_2
        v = d_1 * v
        v_2 = d_1 * v_2
        
    a_2 = d ** 2
    c_2 = v_3 ** 2
    b_2 = b_2 + (d + v_3) ** 2 - a_2 - c_2
    a_2 = a_2 + e * v
    c_2 = c_2 + g * v_2
    f_2 = reducePDF([a_2, b_2, c_2])
    return f_2

def parteucl(a, b, sogsp):
    v = 0
    d = a
    v_2 = 1
    v_3 = b
    z = 0

    while 1:
        if abs(v_3) > sogsp:
            # euclidean step
            q = d / v_3
            t_3 = d % v_3
            t_2 = v - (q * v_2)
            v = v_2
            d = v_3
            v_2 = t_2
            v_3 = t_3
            z = z + 1
            continue
        else:
            if z % 2 != 0:
                v_2 = -v_2
                v_3 = -v_3
            return (v_2, v_3, z, d, v)

def nucomp(f_1, f_2):

    if dis_chk(f_1) != dis_chk(f_2):
        raise ValueError(
            "two quadratic forms must have same discriminant")
    disc = f_1[1]**2 - 4*f_1[0]*f_1[2]
    sogsp = nzmath.arith1.floorpowerroot(abs(float(disc)/4), 4)
    # initialize
    if f_1[0] < f_2[0]:
        f_1, f_2 = f_2, f_1
    s = (f_1[1] + f_2[1]) / 2
    n = f_2[1] - s

    # euclidean step
    u, v, d = euclid_exd(f_2[0], f_1[0])
    if d == 1:
        la = -u*n
        d_1 = d
    else:
        if (s % d) == 0:
            la = -u*n
            d_1 = d
            f_1[0] = f_1[0] / d_1
            f_2[0] = f_2[0] / d_1
            s = s / d_1
        else:
            print "c"
            # second euclidean step
            u_1, v_1, d_1 = euclid_exd(s,d)
            if d_1 > 1:
                f_1[0] = f_1[0] / d_1
                f_2[0] = f_2[0] / d_1
                s = s / d_1
                d = d / d_1
            # initialization of reduction
            f_1[2] = f_1[2] % d
            f_2[2] = f_2[2] % d
            l = ((-u_1*(u * f_1[2] + v * f_2[2])) % d)
            la = -u*(u / d) + l*(f_1[0] / d)
    # partial reduction

    la = la % f_1[0]
    la_1 = f_1[0] - la
    if la_1 < la:
        la = -la_1
    v_2, v_3, z, d, v = parteucl(f_1[0], la, sogsp)
    # special case
    if z == 0:
        lq_1 = f_2[0] * v_3
        lq_2 = lq_1 + n
        f = lq_2 / d
        g = (v_3 * s + f_2[2]) / d
        a_3 = d * f_2[0]
        c_3 = v_3 * d + g * d_1
        b_3 = 2 * lq_1 + f_2[1]

        f_3 = reducePDF([a_3, b_3, c_3])
        return f_3
    # final computations
    b = (f_2[0] * d + n * v) / f_1[0]
    lq_1 = b * v_3
    lq_2 = lq_1 + n
    f = lq_2 / d
    e = (s * d + f_2[2]) / f_1[0]
    lq_3 = e * v_2
    lq_4 = lq_3 - s
    g = lq_4 / v
    if d_1 > 1:
        v_2 = d_1 * v_2
        v = d_1 * v
    a_3 = d * b + e * v
    c_3 = v_3 * f + g * v_2
    b_3 = lq_1 + lq_2 + d_1 * (lq_3 + lq_4)
    f_3 = reducePDF([a_3, b_3, c_3])
    return f_3


class nxtel_5:
    def __init__(self, disc):
        if type(disc) != int:
            raise TypeError("the value must be integer")
        self.numlst = computeClassNumber(disc)[1]
        self.disc = disc
        self.unit = self.numlst[0]
        random.shuffle(self.numlst)
        
    def retunit(self):
        return Groupforbsgs_5(self.unit)

    #def retiis(self):
        #return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(2, self.odr)) ** 0
    
    def retnext(self):
        while 1:
            tpa =  self.numlst.pop()

            #return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(tpa, self.odr))
            return Groupforbsgs_5(tpa)

class Groupforbsgs_5(nzmath.group.GroupElement):
    def __init__(self, value):
        nzmath.group.GroupElement.__init__(self, value, 1)
        
    def __mul__(self, other):
        return Groupforbsgs(self.element * other.element)
    
        #return self.ope(other)

    def __pow__(self, other):
        return Groupforbsgs(self.element ** other)
    
        #return self.ope2(other)
    
class QuadraticGroup:
    '''
    '''
    def __init__(self, disc, classnum, elements = []):
        # element is an element of some class (for example ReducedQuadraticForm
        self.disc = disc
        self.rootoftree = []
        self.copyofroot = 0
        self.rootornot = 0
        self.elements = elements
        self.classnum = classnum
        if disc % 4 == 0:
            a = 1
            b = 0
            c = disc // -4
        elif disc % 4 == 1:
            a = 1
            b = 1
            c = (disc - 1) // -4
        else:
            raise ValueError
        self.expunit = [a, b, c]
    def insertelements(self, newlist):
        for newel in newlist:
            self.insertelement(newel)
    def insertelement(self, newel):
        self.elements.append(newel)

    def instelementstree(self, newlist):
        for newel in newlist:
            self.insertelementtree(newel)

    def insertelementtree(self, newel):
        #if type(newel) != list:
        #    raise ValueError("this value must be list")
        #if len(newel.element) != 3:
        #    raise ValueError("this value must be list of three element")
        dis = newel.element[1]**2 - 4*newel.element[0]*newel.element[2]
        if dis != self.disc:
            raise ValueError("this value is not an element of the discriminant")
        if self.rootornot == 0:
            self.rootoftree = [newel, [], []]
            self.rootornot = 1
            return True
        else:
            curntpnt = self.rootoftree
        while curntpnt != []:
            if newel.element == curntpnt[0].element:
                # already inserted
                return True
            elif newel.element < curntpnt[0].element:
                curntpnt = curntpnt[1]
            else:
                curntpnt = curntpnt[2]

        curntpnt.append(newel)
        curntpnt.append([])
        curntpnt.append([])

    def search(self, tarel):
        curntpnt = self.rootoftree
        while (curntpnt != []):
            if tarel.element == curntpnt[0].element:
                return True
            elif tarel.element < curntpnt[0].element:
                curntpnt = curntpnt[1]
            else:
                curntpnt = curntpnt[2]
        return False
    def retel(self):
        if self.copyofroot == 0:
            self.copyofroot = copy.deepcopy(self.rootoftree)
            #self.copyofroot = 1
        #print self.copyofroot
        while not self.copyofroot == []:
            #print self.copyofroot
            curntpnt = self.copyofroot
            while True:
                if not curntpnt[1] == []:
                    curntpnt = curntpnt[1]
                    continue
                elif not curntpnt[2] == []:
                    curntpnt = curntpnt[2]
                    continue
                else:
                    print curntpnt[0]
                    del curntpnt[0]
                    del curntpnt[0]
                    del curntpnt[0]

                    #return self.copyofroot
                    break
    def qpartofg(self,q):
        gq = []
        for elem in self.elements:
            gq.append(elem ** q)
            
    def findind(self,qin):
        q = qin[0]**qin[1]
        #print q
        while True:
            elgt1 = self.randomele()
            elg1 = elgt1 ** q
            if elg1.element == elg1.unit:
                continue
            return elg1
        
    def retstructure(self):
        q = nzmath.factor.methods.factor(self.classnum)
        for qin in q:
            a = self.findind(qin)
            print a
        
    def randomele(self):
        limita = long(math.sqrt(float(-self.disc) / 3))
        while True:
            a = int(limita * random.random()) + 1
            ind = 0
            while ind < a:
                b = int(a*random.random()) + 1
                ch = random.random()
                if ch < 0.5:
                    b = -b
                tp = self.disc - b**2
                if tp % (-4 * a) == 0:
                    c = tp // (-4 * a)
                    unit = self.expunit[:]
                    red = reducePDF([a, b, c])
                    if red == unit:
                        ind = ind + 1
                        continue
                    return ReducedQuadraticForm(red, unit)
                else:
                    ind = ind + 1
                    continue
