import math
import random
import copy
import nzmath.gcd
import nzmath.arith1
import nzmath.group
import nzmath.rational
import nzmath.factor.misc
import nzmath.finitefield


def ct_rqf(id_x):
    a, b = computeClassNumber(id_x)
    c = b[:]
    d = []
    for i in c:
        d.append(ReducedQuadraticForm(i, b[0]))
    return d

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
        return self.__class__(computePDF(self.element, other.element), self.unit)

    def __pow__(self, exp):
        if not isinstance(exp, (int, long)):
            raise TypeError("powering index must be an integer.")
        if exp == 0:
            return self.unit
        elif exp == 1:
            return self.element
        eltemp = self.element
        while exp != 1:
            eltemp = computePDF(eltemp, self.element)
            exp = exp - 1
        return self.__class__(eltemp, self.unit)
    
    def __div__(self,other):
        invel = other.inverse()
        return computePDF(self.element, invel.element)

    def __eq__(self, other):
        if (self.element == other.element) and (self.unit == other.unit):
            return True
        else:
            return False

    def inverse(self):
        if self.element == self.unit:
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

def reducePDF(a):
    """
    Reduction of Positive Definite Forms
    f = (a[0], a[1], a[2])
    """
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
    elif (disc % 4) == 0 and nzmath.factor.misc.squarePart(disc / 4) == 1:
        discof = (disc / 4) % 4
        if discof == 2:
            return True
        elif discof == 3:
            return True
    return False


def ckfn(lwrbd, lwrbd_1, uprbd_1, h, n, ls, ll, q, nt):
    '''
    this is a submodule called by the module, bsgs.
    check bsgs is finished or not yet.
    '''
    h[0] = h[0] * n[0]
    if h[0] >= lwrbd:
        return h[0]
    uprbd_1[0] = uprbd_1[0] / n[0] # floor of uprbd_1[0] / n[0]
    lwrbd_1[0] = lwrbd_1[0] / n[0]  + 1 # floor + 1 of lwrbd_1[0] / n[0]
    q[0] = nzmath.arith1.floorsqrt(n[0])
    lsl = ls[:]
    ls = []
    lll = ll[:]
    ll = []
    for r in range(q[0]):
        for ss in lsl:
            ls.append((nt[0]**r) * ss) # multiple of two elements of G
    y = nt[0]**q[0]
    for a in range(q[0]):
        for eol in lll:
            ll.append((y**a) * eol) # multiple of two elements of G
    return -1

def cptodr(n, x, c_s1, ls, ll):
    # flg
    flg_bk = 1
    while flg_bk == 1:
        flg_bk = 0
#        print "&&&("
        lst_p = nzmath.factor.misc.primeDivisors(n[0])
        tp_ls = ls[:]
#        print n[0]
#        print lst_p
#        print tp_ls

        for tmpri in lst_p:
            # initialize c_s1
            c_s1 = []
            for ttp_ls in tp_ls:
                c_s1.append([(x[1] ** (n[0] / tmpri)) * ttp_ls, 0])
            # sort
            c_s1.sort()
            co_cs = c_s1[:]
            # check
            tp_ll = ll[:]
            for tmp_els in co_cs:
                for tmp_ell in tp_ll:
                    if tmp_els[0] == tmp_ell:
                        flg_bk = 1
                        n[0] = n[0] / tmpri
                        break
                if flg_bk == 1:
                    break

def cptgs(n, q, sz, sy, c_s1, uprbd_1, ll):
    gsll = ll[:]
    gscs = c_s1[:]

    #print "611"
    #print gsll
    #print gscs
    while 1:
        for tpw in gsll:
            sz1 = sz[0] * tpw
            for tpcs in gscs:
                if sz1 == tpcs[0]:
                    n[0] = n[0] - tpcs[1]
                    return True
        # continue (sp. 5)

        sz[0] = sy[0] * sz[0]
        n[0] = n[0] + q[0]
        if n[0] <= uprbd_1:
            continue
        else:
            raise ValueError("the order is larger than lower bound")
        
    
def cptssp(q, x , n, c_s1, lwrbd_1, uprbd_1, ls, ll, ut):
    # copy ls
    tpls = ls[:]
    flg_s = 0
    # initialize
    sy = [0]
    sz = [0]
    #print x[0] * x[1]
    for tr in range(q[0]):
        #print "#8821"
        #print x[0] * x[1]
        # compute 2 to q-1
        if (tr != 0) and (tr != 1):
            x[tr] = x[1] * x[tr - 1]
            #ttpx[tr] = ttpx[tr - 1] * ttpx[1]

        for ttr in tpls:
            print "###"
            print x[tr]
            print "###"
            tmpx = x[tr]*ttr
            if (flg_s == 0) and (tmpx == ut) and (tr != 0):
                print "aaaaaa"
                flg_s = 1
                n[0] = tr
                ##c_s1_r[tr].append(tmpx)
            c_s1.append([tmpx, tr])
                # sort ( if you want to sort it with your estimate,
                # you have to implement '__ge__' method of the class with your way.)
    c_s1.sort()
    print "##991"
    print c_s1
    print "##991"

    if flg_s == 1:
        # 6
        cptodr(n, x, c_s1, ls, ll)
    else:
        # step 4 to 5
        print x[1]
            
        print x[q[0] -1 ]
        
        sy[0] = x[1] * x[q[0] - 1]
        sz[0] = x[1] ** lwrbd_1[0]
        n[0] = lwrbd_1[0]
        #print "########"
        #print n[0]
        #print "########"
        # compute giant steps
        print "$$"
        cptgs(n, q, sz, sy, c_s1, uprbd_1, ll)
        print "$$$"
        # 6
        cptodr(n, x, c_s1, ls, ll)
    
        
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
    lwrbd_1 = []
    lwrbd_1.append(lwrbd)
    uprbd_1 = []
    uprbd_1.append(uprbd)

    # get the unit
    ut = iordmel.retunit()
    # append the unit to subgroups of G
    ls = [] # a subset of target group, G
    ll = [] # a subset of G
    ls.append(ut)
    ll.append(ut)
    # initialize variables
    n = [0]
    q = [0]
    h = [1] # order
    nt = [0] # next value
    ret = -1
    # take a new element of the group.
    while ret == -1:
        nt[0] = iordmel.retnext()
        q[0] = nzmath.arith1.floorsqrt(uprbd_1[0] - lwrbd_1[0] ) + 1

        print "RRR"
        print nt[0] * ut
        print ut * nt[0]
        print "RRR"
        print q[0]
        print "RRRR"
        # initialize variables
        #x = range(q[0] + 1) # x is the set of elements of G
        x = range(q[0]) # x is the set of elements of G
        c_s1 = [] # a subset of G
        # c_s1_r = range(q) # a set of subset of G
        for i in range(q[0]):
            x[i] = 0
            ##c_s1_r[i] = 0
        print "ttt"
        print x
        print "ttt"
        # compute small steps        
        x[0] =  ut # maybe, this code must not be here
        print "www"
        print q[0]
        print x
        print "www"
        print nt[0]
        print h[0]
        x[1] = (nt[0] ** h[0])
        print x[1]
        print "uuu"
        print x[0] * x[1]
        print x[1].ope(x[0])
        print "uuu"
        
        if x[1] == ut:
            n[0] = 1
        else:
            # 3kara6
            cptssp(q, x , n, c_s1, lwrbd_1, uprbd_1, ls, ll, ut)
        
        # finished?
        ret = ckfn(lwrbd, lwrbd_1, uprbd_1, h, n, ls, ll, q, nt)
    print "!!!!!!!!!!!!!!!!!!!!!!!!!"
    return ret


def exp_p(a):
    a.append(3)
    
def exp_s():
    a = []
    print a
    exp_p(a)
    print a
    
    
class Groupforbsgs(nzmath.group.GroupElement):
    def __init__(self, value):
        nzmath.group.GroupElement.__init__(self, value, 1)
        
    def __mul__(self, other):
        return Groupforbsgs(self.element * other.element)
        #return self.ope(other)

    def __pow__(self, other):
        return Groupforbsgs(self.element ** other)
        #return self.ope2(other)
    
class nxtel:
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
            #return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(tpa, self.odr))
            return Groupforbsgs(nzmath.finitefield.FinitePrimeFieldElement(3, self.odr))



# reload(quad)
# a = quad.nxtel(31)
# quad.bsgs(a, 26, 50)
# a = quad.nxtel(99991)
# quad.bsgs(a, 99999/2 + , 99999)
