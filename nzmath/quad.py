import sys
import math
import random
import copy
import nzmath.gcd as gcd
import nzmath.arith1 as arith1
import nzmath.group as group
import nzmath.prime as prime
import nzmath.factor.misc as misc
import nzmath.factor.mpqs as mpqs

class ReducedQuadraticForm:
    """
    The class is for reduced quadratic form.
    """
    def __init__(self, element, unit):
        self.element = element # form = [a_1, a_2, a_3]
        self.unit = unit 
        self.ind = -1
        self.alpha = []
        self.beta = []
        self.s_parent = 0
        self.g_parent = 0

    def __repr__(self):
        return_str = '%s' % self.element
        return return_str

    def __mul__(self, other):
        if not isinstance(other, ReducedQuadraticForm):
            return NotImplemented
        return self.__class__(compositePDF(self.element[:], other.element[:]), self.unit[:])

    def __pow__(self, exp):
        sy = self.unit[:]
        if not isinstance(exp, (int, long)):
            raise TypeError("powering index must be an integer.")
        # Right-Left Binary algorithm
        if exp == 1:
            return self.__class__(self.element[:], sy)
        if exp == 0:
            return self.__class__(sy, sy)
        if exp < 0:
            lexp = -exp
            sz = self.inverse().element[:]
        else:
            lexp = exp
            sz = self.element[:]
        while True:
            if (lexp % 2) == 1:
                sy = compositePDF(sz, sy)
            lexp = lexp // 2
            if lexp == 0:
                return self.__class__(sy, self.unit[:])
            else:
                sz = sqrPDF(sz)

    def __div__(self,other):
        invel = other.inverse()
        return compositePDF(self.element[:], invel.element[:])

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
        for valueofel in range(2):
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
        for valueofel in range(2):
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
        for valueofel in range(2):
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
        for valueofel in range(2):
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

        return_str = '%s + root(%s) / %s' % (rb, ld, a_m2)
        return return_str

class ClassGroup:
    """
    The class is for class group.
    """
    def __init__(self, disc, classnum, elements = []):
        # element is an element of some class (for example ReducedQuadraticForm
        self.disc = disc
        self.rootoftree = []
        self.copyofroot = 0
        self.rootornot = 0
        self.elements = copy.deepcopy(elements)
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
        
    def __repr__(self):
        return_str = "class of ClassGroup:\n"
        return_str = return_str + 'disc is %s\n' % self.disc
        return_str = return_str + 'rootoftree is %s' % self.rootoftree
        return return_str
    
    def inserels(self, newlist):
        for newel in newlist:
            self.inserel(newel)

    def inserel(self, newel):
        newestl = copy.deepcopy(newel)
        self.elements.append(newestl)

    def inststree(self, newlist):
        for newel in newlist:
            self.insttree(newel)

    def insttree(self, newel0):
        newel = copy.deepcopy(newel0)
        disc = newel.element[1]**2 - 4*newel.element[0]*newel.element[2]
        if disc != self.disc:
            raise ValueError("this value is not an element of the discriminant")
        if self.rootornot == 0:
            self.rootoftree = [newel, [], []]
            self.rootornot = 1
            return True
        else:
            curntpnt = self.rootoftree
        while curntpnt != []:
            if newel.element == curntpnt[0].element:
                return True
            elif newel.element < curntpnt[0].element:
                curntpnt = curntpnt[1]
            else:
                curntpnt = curntpnt[2]

        curntpnt.append(newel)
        self.elements.append(newel)
        curntpnt.append([])
        curntpnt.append([])

    def search(self, tarel):
        curntpnt = self.rootoftree
        while (curntpnt != []):
            if tarel.element == curntpnt[0].element:
                return curntpnt[0]
            elif tarel.element < curntpnt[0].element:
                curntpnt = curntpnt[1]
            else:
                curntpnt = curntpnt[2]
        return False

    def retel(self):
        self.copyofroot = copy.deepcopy(self.rootoftree)
        tpa = []
        while not self.copyofroot == []:
            curntpnt = self.copyofroot
            while True:
                if not curntpnt[1] == []:
                    curntpnt = curntpnt[1]
                    continue
                elif not curntpnt[2] == []:
                    curntpnt = curntpnt[2]
                    continue
                else:
                    tpa.append(curntpnt[0])
                    del curntpnt[0]
                    del curntpnt[0]
                    del curntpnt[0]
                    break
        return tpa

class retnext1:
    """
    """
    def __init__(self, disc):
        self.disc = disc
        self.utroot = unit_form(disc)
        self.cnt = 1
        self.previous = []
        self.elhash = range(int(math.sqrt(abs(disc) // 3)) + 2)
    def unit(self):
        utt = ReducedQuadraticForm(self.utroot[:], self.utroot[:])
        return utt
    def retnext(self):
        while True:
            next, self.cnt, self.previous = randomele1(self.disc, self.cnt, self.previous)
            self.cnt = self.cnt + 1
            next1 = ReducedQuadraticForm(next, self.utroot[:])
            rettp = ckhash1(self.elhash, next1)
            if type(rettp) == int:
                mkhash1(self.elhash, next1)
                return next1
        return next1

def class_formula(disc, uprbd):
    """
    Return the approximation of class number 'h' with the given discriminant.
    h = sqrt(|D|)/pi (1 - (D/p)(1/p))^{-1} where p is less than ubound.
    """
    ht = math.sqrt(abs(disc)) / math.pi
    ml = 1
    factors = mpqs.eratosthenes(uprbd)

    for factor in factors:
        ml = ml * (1 -(float(kronecker(disc, factor)) / factor))**(-1)
    return int(ht * ml)

def class_number(disc, limit_dis=100000):
    """
    Return class number with the given discriminant by counting reduced forms.
    Not only fundamental discriminant.
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
            f_b = 1
            f_c = -((disc - 1) / 4)

    while b <= c_b:
        chk_f = 0
        q = (b**2 - disc) / 4
        a = b
        if a <= 1:
            a = 1
            chk_f = 1
        while 1:
            if chk_f == 0:
                if (q % a == 0) and gcd.gcd_of_list([a, b, q/a])[0] == 1:
                    if (a == b) or (a**2 == q) or (b == 0):
                        h += 1
                        if disc < limit_dis:
                            f_a = a
                            f_b = b
                            f_c = -(disc - f_b*f_b)/(4*f_a)
                            ###ret_list.append([f_a, f_b, f_c])
                    else:
                        h += 2
                        if disc < limit_dis:
                            f_a = a
                            f_b = b
                            f_c = -(disc - f_b*f_b)/(4*f_a)
            chk_f = 0
            a += 1
            if a**2 > q:
                break
        b += 2
    return (h)

def class_group(disc, limit_dis=100000):
    """
    Return the class number and the class group with the given discriminant
    by counting reduced forms. Not only fundamental discriminant.
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
                if (q % a == 0) and gcd.gcd_of_list([a, b, q/a])[0] == 1:
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

def class_number_bsgs(disc, retelq = 0):
    """
    Return the class number with the given discriminant.
    """
    lx = max(arith1.floorpowerroot(abs(disc), 5), 500 * (math.log(abs(disc)))**2)
    uprbd = int(class_formula(disc, int(lx)) * float(3) / 2)
    lwrbd = uprbd / 2 - 1
    h = [1]
    lwrbd_1 = [lwrbd]
    uprbd_1 = [uprbd]

    # get the unit
    element = retnext1(disc)
    ut = element.unit()

    # append the unit to subset of G
    sossp = ClassGroup(disc, 0, [])
    sogsp = ClassGroup(disc, 0, [])
    sossp.insttree(ut)
    sogsp.insttree(ut)

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
        nt[0] = element.retnext()
        mstp1 = uprbd_1[0] - lwrbd_1[0]
        if (mstp1 == 0) or (mstp1 == 1):
            q[0] = 1
        else:
            tppm = misc.primePowerTest(mstp1)
            if tppm[1] == 2:
                q[0] = arith1.floorsqrt(mstp1)
            else:
                q[0] = arith1.floorsqrt(mstp1) + 1
        if q[0] <= 2:
            x = [0,0]
        else:
            x = [0] * q[0] # x is the set of elements of G
        c_s1 = ClassGroup(disc, 0, []) # a subset of G
        # compute small steps        
        x[0] =  ut # maybe, this code must not be here
        x[1] = (nt[0] ** h[0])
        if x[1] == ut:
            n[0] = 1
            # initialize order
            n[0] = h[0] * n[0]
            # compute the order of nt[1]
            sossp, sogsp = trorder(n, x, sossp, sogsp, c_s1, nt, disc)
        else:
            ret_val, sossp, sogsp = trbabysp(q, x , n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, h, nt, disc)

        # finished?
        ret, sossp, sogsp = isfinished_trbsgs(lwrbd, lwrbd_1, uprbd_1, h, n, sossp, sogsp, q, nt, y, disc)
    
    return ret

def class_group_bsgs(disc, classnum, qin):
    """
    Return the construction of the class group with the given discriminant.
    """
    matla = []
    lstofelg = []
    lpt = []

    # compute bounds
    qpt = qin[0] ** qin[1]
    uprbd = qpt + 1
    lwrbd = uprbd // 2 + 1
    if lwrbd > uprbd:
        raise TypeError("lower bound needs to be less than upper bound")
    if lwrbd <= (uprbd / 2):
        raise TypeError("upper bound / 2 needs to be more than lower bound")
    lwrbd_1 = [lwrbd]
    uprbd_1 = [uprbd]

    # get the unit
    uto = unit_form(disc)
    ut = ReducedQuadraticForm(uto, uto)

    # append the unit to subset of G
    sossp = ClassGroup(disc, classnum, []) # a subset of G
    sogsp = ClassGroup(disc, classnum, []) # a subset of G
    utwi = copy.deepcopy(ut)
    utwi.alpha.append([0, ut, 1])
    utwi.beta.append([0, ut, 1])
    sossp.insttree(utwi)
    sogsp.insttree(utwi)
    n = [0]
    q = [0]
    y = [0]
    ret = -1

    # take a new element of the group.
    indofg = 1
    while ret == -1:
        # get next element
        nt = generator(disc, classnum, qin)
        lstofelg.append(nt)
        mstp1 = uprbd_1[0] - lwrbd_1[0]
        if (mstp1 == 0) or (mstp1 == 1):
            q[0] = 1
        else:
            tppm = misc.primePowerTest(mstp1)
            if (tppm[1] != 0) and ((tppm[1] % 2) == 0):
                q[0] = arith1.floorsqrt(mstp1)
            else:
                q[0] = arith1.floorsqrt(mstp1) + 1
        if q[0] <= 2:
            x = [0,0]
        else:
            x = [0] * q[0] # x is the set of elements of G
        c_s1 = ClassGroup(disc, classnum, []) # a subset of G

        # compute small steps
        x[0] =  ut # maybe, this code must not be here
        x[1] = nt
        if x[1] == ut:
            raise ValueError
            n[0] = 1
            # initialize order
            tmp_ss, tmp_gs = ordercv(n, x, sossp, sogsp, c_s1, nt, disc, classnum)
        else:
            tmp_ss, tmp_gs = babyspcv(utwi, q, x , n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, nt, disc, classnum)
        setind(n, indofg, tmp_ss, tmp_gs, matla)
        ret, sossp, sogsp = isfinished_bsgscv(lwrbd, lwrbd_1, uprbd_1, n, sossp, sogsp, q, nt, y, lpt, qpt, disc, classnum, indofg)
        indofg = indofg + 1
    return lstofelg, matla

########################################################
# following function is sub function for above module. #
########################################################

def disc(f):
    """
    Return the discriminant of the given quadratic form 'f'.
    f = [a, b, c]
    """
    if len(f) != 3:
        raise ValueError
    for i in f:
        if (type(i) != int) and (type(i) != long):
            raise ValueError
    return (f[1]*f[1] - 4*f[0]*f[2])

def reducePDF(f):
    """
    Return the reduced form of the given positive definite form 'f'.
    f = (a[0], a[1], a[2])
    """
    a = f[:]
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

def sqrPDF(f):
    """
    Return the square of the given quadratic form 'f'.
    """
    f_1 = f[:]
    
    # compute disc and etc
    D = disc(f)
    sogsp = arith1.floorpowerroot(abs(float(D)/4), 4)
    (u, v, d_1) = euclid_exd(f_1[1], f_1[0])

    la = f_1[0] / d_1
    lb = f_1[1] / d_1
    lc = (-f_1[2] * u) % la
    c_1 = la - lc
    if c_1 < lc:
        lc = -c_1
        
    # partial reduction
    v_2, v_3, z, d , v = parteucl(la, lc, sogsp)

    if z == 0:
        g = (lb * v_3 + f_1[2]) / d
        a_2 = d**2
        c_2 = v_3 ** 2
        b_2 = f_1[1] + (d + v_3)**2 - a_2 - c_2
        c_2 = c_2 + g * d_1
        f_2 = reducePDF([a_2, b_2, c_2])
        return f_2

    e = (f_1[2] * v + lb * d) / la
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

def powPDF(f, exp):
    """
    Return the powering 'exp' of the given quadratic form 'f'. 
    """
    D = disc(f)
    ut = unit_form(D)

    if exp == 0:
        return ut[:]
    elif exp == 1:
        return f[:]
    elif f == ut:
        return f[:]
    if exp < 0:
        lexp = -exp
        sz = [f[0] , - f[1], f[2]]
    else:
        lexp = exp
        sz = f[:]
    sy = ut[:]
    while True:
        if (lexp % 2) == 1:
            sy = compositePDF(sz, sy)
        lexp = lexp // 2
        if lexp == 0:
            return sy
        else:
            sz = sqrPDF(sz)

def compositePDF(f_1, f_2):
    """
    Return the reduced form of composition of the given forms 'f_1' and 'f_2'.
    'f_1' and 'f_2' are quadratic forms with same disc.
    """
    if gcd.gcd_of_list(f_1)[0] != 1:
        raise ValueError(
            "coefficients of a quadratic form must be relativery prime")
    if gcd.gcd_of_list(f_2)[0] != 1:
        raise ValueError(
            "coefficients of a quadratic form must be relativery prime")
    if disc(f_1) != disc(f_2):
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

def unit_form(disc):
    """
    Return generated quadratic form with the given discriminant.
    """
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
    return [a, b, c]

def kronecker(a, b):
    """
    Compute the Kronecker symbol (a/b) using algo 1.4.10 in Cohen's book.
    """
    tab2 = [0, 1, 0, -1, 0, -1, 0, 1]
    if b == 0:
        if abs(a) != 1:
            return 0
        if abs(a) == 1:
            return 1
    if (a % 2 == 0) and (b % 2 == 0):
        return 0

    v = 0
    while (b % 2 == 0):
        v = v + 1
        b = b // 2
    if (v % 2 == 0):
        k = 1
    else:
        tp1 = a & 7
        k = tab2[tp1]
    if b < 0:
        b = -b
        if a < 0:
            k = -k
    while True:
        if a == 0:
            if b > 1:
                return 0
            if b == 1:
                return k
        v = 0
        while (a % 2) == 0:
            v = v + 1
            a = a // 2
        if (v % 2) == 1:
            tt = b & 7
            k = tab2[tt] * k
        tpa = a & b
        tpa2 = tpa & 2
        if (a & b & 2) != 0:
            k = -k
        r = abs(a)
        a = b % r
        b = r

def number_unit(disc):
    """
    Return the number of units with the given discriminant.
    """
    if disc < -4:
        return 2
    elif disc == -4:
        return 4
    elif disc == -3:
        return 6
    else:
        raise ValueError

def crt(inlist):
    """
    Chinese Remainder Theorem, Algo. 1.3.11 of Cohen's Book.
    """
    j = 2
    k = len(inlist)
    ccj = range(k+1)
    ccj[1] = 1
    inlist.sort()
    ellist = [()] + inlist
    if k < 2:
        raise ValueError
    yj = range(k+1)
    while j <= k:
        p = 1
        for inj in range(1, j):
            p = p * ellist[inj][1]
        p = p % ellist[j][1]
        tpl = gcd.gcd_of_list([p, ellist[j][1]])
        d = tpl[0]
        u = tpl[1][0]
        v = tpl[1][1]
        if d > 1:
            raise ValueError
        ccj[j] = u
        j = j + 1
    
    yj[1] = (ellist[1][0] % ellist[1][1])
    for indj in range(2, k + 1):
        intp = indj
        intp = intp - 1
        ctp = yj[intp]
        while intp > 1:
            ctp = yj[intp - 1] + ellist[intp - 1][1] * ctp
            intp = intp - 1
        yj[indj] = ((ellist[indj][0] - ctp) * ccj[indj]) % ellist[indj][1]
    ktp = k
    outp = yj[ktp]
    while ktp > 1:
        outp = yj[ktp - 1] + (ellist[ktp - 1][1]) * outp
        ktp = ktp - 1
    return outp

def generator(disc, classnum, qin):
    """
    Return the reduced random quadratic form with given discriminant and order t, 
    where t = classnum / a ** b and qin = [a, b].
    """
    q = qin[0]**qin[1]
    unit = unit_form(disc)
    while True:
        elgt1 = randomele(disc, unit)
        elg1 = elgt1 ** (classnum // q)
        if elg1.element == elg1.unit:
            continue
        return elg1

def sqroot(disc, p):
    """
    Return a reduced quadratic form with the given discriminant.
    'disc' is a quadratic residue mod 'p'.
    """
    if p == 2: # if 8 | disc => (disc / 8) = 0, 8 not | disc but 4 | disc => 2
        if (disc % 8) == 0:
            bp = disc
        elif (disc % 4) == 0: # 4 - 4 * odd % 8 => 0
            bp = 2
        elif (disc % 8) == 1: # disc is odd and disc % 8 is 1
            bp = disc
        else: # disc is odd and disc % 4 is 1 => impossible (-5 / 2) = -1
            bp = disc
            raise ValueError
    else:
        bpf1 = arith1.modsqrt(disc, p)
        bpf2 = disc
        bp = crt([(bpf1, p), (bpf2, 4)])
    if bp > p:
        bp = 2 * p - bp
        
    fpt = reducePDF([p, bp, ((bp ** 2) - disc) // (4 * p)])    
    return fpt

def randomele1(disc, cnt, previous):
    """
    Return a reduced random form with the given discriminant.
    'cnt' is count.
    """
    while True:
        nextp = prime.nextPrime(cnt)
        cnt = cnt + 1
        if (kronecker(disc, nextp) == 1):
            nxtfm = sqroot(disc, nextp)
            if (previous == []) or (nxtfm != previous):
                previous = nxtfm
                return nxtfm, cnt, previous
        
def randomele(disc, unit):
    """
    Return a reduced random form with the given discriminant and the given unit.
    Also random element is not unit.
    """
    limit = long(math.sqrt(float(-disc) / 3))
    while True:
        a = int(limit * random.random()) + 1
        ind = 0
        while ind < 2*a:
            b = int(a*random.random())
            ch = random.random()
            if ch < 0.5:
                b = -b
            tp = disc - b**2
            if tp % (-4 * a) == 0:
                c = tp // (-4 * a)
                if gcd.gcd_of_list([a, b, c])[0] != 1:
                    continue
                red = reducePDF([a, b, c])
                if red == unit:
                    ind = ind + 1
                    continue
                return ReducedQuadraticForm(red, unit)
            else:
                ind = ind + 1
                continue


def isfundamental(disc):
    """
    Determine whether the given discriminant is fundamental or not.
    """
    if disc == 1:
        return False
    if disc <= 0:
        spt = misc.squarePart(-disc)
    else:
        spt = misc.squarePart(disc)
    if (disc % 4) == 1 and spt == 1:
        return True
    elif (disc % 4) == 0:
        if disc <= 0:
            sptq = misc.squarePart(-disc // 4)
        else:
            sptq = misc.squarePart(disc // 4)
        if sptq != 1:
            return False
        discof = (disc // 4) % 4
        if discof == 2:
            return True
        elif discof == 3:
            return True
    return False

def euclid_exd(a, b):
    """
    Return a tuple (u, v, d); they are the greatest common divisor d
    of two integers a and b and u, v such that d = a * u + b * v.
    """
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

def parteucl(a, b, sogsp):
    """
    Do extended partial Euclidean algorithm on 'a' and 'b'.
    """
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

def mkhash1(hsh, sosp):
    """
    """
    if type(hsh[sosp.element[0]]) == int :
        hsh[sosp.element[0]] = [sosp]
    else:
        hsh[sosp.element[0]].append(sosp)
    return True

def ckhash1(hsh, sosp):
    """
    """
    if type(hsh[sosp.element[0]]) == int :
        return -1
    for tel in hsh[sosp.element[0]]:
        if sosp == tel:
            return tel
    return -1

def isfinished_bsgscv(lwrbd, lwrbd_1, uprbd_1, n, sossp, sogsp, q, nt, y, lpt, qpt, disc, classnum, indofg):
    """
    Determine whether the bsgs algorithm is finished or not yet.
    This is a submodule called by the bsgs module.
    """
    lpt.append(n[0])
    sumn = 1
    for nid in lpt:
        sumn = sumn * nid 
    if sumn == qpt:
        return n[0], sossp, sogsp
    elif sumn > qpt:
        raise ValueError
    
    if n[0] == 1:
        tpsq = [0, 2]
    else:
        tpsq = misc.primePowerTest(n[0])
    if (tpsq[1] != 0) and ((tpsq[1] % 2) == 0):
        q[0] = arith1.floorsqrt(n[0])
    else:
        q[0] = arith1.floorsqrt(n[0]) + 1

    lsl = copy.deepcopy(sossp)
    sossp = ClassGroup(disc, classnum, [])
    lll = copy.deepcopy(sogsp)
    sogsp = ClassGroup(disc, classnum, [])
    tnt = copy.deepcopy(nt)
    ss = lsl.retel()
    for r in range(q[0]):
        for ssi in ss:
            newel = (tnt ** r) * ssi
            if sossp.search(newel) == False:
                newel.alpha = ssi.alpha[:]
                lenal = len(newel.alpha)
                sfind = indofg - lenal
                for sit in range(sfind):
                    newel.alpha.append([lenal + sit, 0, 0])
                newel.alpha.append([indofg, tnt, r])
                sossp.insttree(newel) # multiple of two elements of G

    y[0] = nt ** q[0]
    ltl = lll.retel()
    for a in range(q[0] + 1):
        for eol in ltl:
            newel2 = (y[0]**(- a)) * eol
            if sogsp.search(newel2) == False:
                newel2.beta = eol.beta[:]
                lenbt = len(newel2.beta)
                gfind = indofg - lenbt
                for git in range(gfind):
                    newel2.beta.append([lenbt + git, 0, 0])
                newel2.beta.append([indofg, tnt, q[0] * (- a)])
                sogsp.insttree(newel2) # multiple of two elements of G
    return -1, sossp, sogsp

def ordercv(n, x, sossp, sogsp, c_s1, nt, disc, classnum, tmp_ss, tmp_gs):
    """
    """
    flg_bk = 1
    while flg_bk == 1:
        flg_bk = 0
        lst_p = misc.primeDivisors(n[0])
        tp_ls = copy.deepcopy(sossp)
        c_s1 = ClassGroup(disc, classnum, []) # a subset of G
        lstp_ls = tp_ls.retel()
        sogsptp = sogsp.retel()
        for tmpri in lst_p:
            for ttp_ls in lstp_ls:
                tmp_c_s1 = (nt ** (n[0] / tmpri)) * ttp_ls
                tmp_c_s1.s_parent = ttp_ls
                c_s1.insttree(tmp_c_s1)
            for tmp_ell in sogsptp:
                rete = c_s1.search(tmp_ell)
                if rete != False:
                    flg_bk = 1
                    n[0] = n[0] / tmpri
                    tmp_ss = rete.s_parent
                    tmp_gs = tmp_ell
                    break
            if flg_bk == 1:
                break
    return tmp_ss, tmp_gs

def giantspcv(n, q, sz, y, c_s1, uprbd_1, sogsp, classnum):
    """
    """
    while 1:
        sotp = sogsp.retel()
        for tpw in sotp:
            sz1 = sz[0] * tpw
            sz1.g_parent = tpw
            rete = c_s1.search(sz1)
            if rete != False:
                n[0] = n[0] - rete.ind
                return rete.s_parent, sz1.g_parent
        # continue (sp. 5)
        sz[0] = y[0] * sz[0]
        n[0] = n[0] + q[0]
        if n[0] -q [0] + 1 <= uprbd_1[0]:
        #####if n[0] -q [0] + 1 <= classnum:
            continue
        else:
            raise ValueError("the order is larger than upper bound")
    
def babyspcv(utwi, q, x, n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, nt, disc, classnum):
    """
    Compute small steps
    """
    flg_s = 0
    # initialize
    y[0] = 0
    sz = [0]
    for tr in range(q[0]):
        # compute 2 to q-1
        if (tr != 0) and (tr != 1):
            x[tr] = x[1] * x[tr - 1]
        sotp = sossp.retel()
        for ttr in sotp:
            tmpx = x[tr]*ttr
            tmpx.s_parent = ttr # tmpx belongs ttr in the set of smallstep
            if (flg_s == 0) and (tmpx == ut) and (tr != 0):
                flg_s = 1
                n[0] = tr
                tmp_ss = tmpx.s_parent
                tmp_gs = utwi
            # index of the element
            tmpx.ind = tr
            c_s1.insttree(tmpx)
    if flg_s != 1:
        y[0] = x[1] * x[q[0] - 1]
        sz[0] = x[1] ** lwrbd_1[0]
        n[0] = lwrbd_1[0]
        tmp_ss, tmp_gs = giantspcv(n, q, sz, y, c_s1, uprbd_1, sogsp, classnum)
    tmp_ss, tmp_gs = ordercv(n, x, sossp, sogsp, c_s1, nt, disc, classnum, tmp_ss, tmp_gs)
    return tmp_ss, tmp_gs

def trbabysp(q, x , n, c_s1, lwrbd_1, uprbd_1, sossp, sogsp, ut, y, h, nt, disc):
    """
    Compute small steps.
    """
    flg_s = 0
    # initialize
    y[0] = 0
    sz = [0]
    for tr in range(q[0]):
        # compute 2 to q-1
        if (tr != 0) and (tr != 1):
            x[tr] = x[1] * x[tr - 1]
            #ttpx[tr] = ttpx[tr - 1] * ttpx[1]
        sotp = sossp.retel()
        for ttr in sotp:
            tmpx = x[tr]*ttr
            if (flg_s == 0) and (tmpx == ut) and (tr != 0):
                flg_s = 1
                n[0] = tr
            tmpx.ind = tr
            c_s1.insttree(tmpx)
                # sort ( if you want to sort it with your estimate,
                # you have to implement '__ge__' method of the class with your way.)

    if flg_s != 1:
        y[0] = x[1] * x[q[0] - 1]
        sz[0] = x[1] ** lwrbd_1[0]
        n[0] = lwrbd_1[0]
        sogsp = trgiantsp(n, q, sz, y, c_s1, uprbd_1, sogsp)
    n[0] = h[0] * n[0] 
    sossp, sogsp = trorder(n, x, sossp, sogsp, c_s1, nt, disc)
    return True, sossp, sogsp

def trgiantsp(n, q, sz, y, c_s1, uprbd_1, sogsp):
    """
    Compute giant steps.
    """
    while 1:
        sotp = sogsp.retel()
        for tpw in sotp:
            sz1 = sz[0] * tpw
            rete = c_s1.search(sz1)
            if rete != False:
                n[0] = n[0] - rete.ind
                return sogsp
        sz[0] = y[0] * sz[0]
        n[0] = n[0] + q[0]
        if n[0] -q [0] + 1 <= uprbd_1[0]:
            continue
        else:
            raise ValueError("the order is larger than upper bound")
        
def trorder(n, x, sossp, sogsp, c_s1, nt, disc):
    """
    Compute the order. 
    """
    # flg
    flg_bk = 1
    while flg_bk == 1:
        flg_bk = 0
        lst_p = misc.primeDivisors(n[0])
        tp_ls = copy.deepcopy(sossp)
        c_s1 = ClassGroup(disc, 0, [])
        lstp_ls = tp_ls.retel()
        sogsptp = sogsp.retel()
        for tmpri in lst_p:
            # initialize c_s1
            for ttp_ls in lstp_ls:
                tmp_c_s1 = (nt[0] ** (n[0] / tmpri)) * ttp_ls
                c_s1.insttree(tmp_c_s1)
            for tmp_ell in sogsptp:
                rete = c_s1.search(tmp_ell)
                if rete != False:
                    flg_bk = 1
                    n[0] = n[0] / tmpri
                    break
            if flg_bk == 1:
                break

    return sossp, sogsp

def isfinished_trbsgs(lwrbd, lwrbd_1, uprbd_1, h, n, sossp, sogsp, q, nt, y, disc):
    """
    Determine whether bsgs is finished or not yet.
    This is a submodule called by the bsgs module.
    """
    h[0] = h[0] * n[0]
    if h[0] >= lwrbd:
        return h[0], sossp, sogsp
    uprbd_1[0] = uprbd_1[0] // n[0] # floor of uprbd_1[0] // n[0]
    if (lwrbd_1[0] % n[0]) == 0:
        lwrbd_1[0] = lwrbd_1[0] // n[0] # floor + 1 of lwrbd_1[0] // n[0]
    else:
        lwrbd_1[0] = lwrbd_1[0] // n[0]  + 1 # floor + 1 of lwrbd_1[0] // n[0]
    if n[0] == 1:
        tpsq = [0, 2]
    else:
        tpsq = misc.primePowerTest(n[0])
    if tpsq[1] == 2:
        q[0] = arith1.floorsqrt(n[0])
    else:
        q[0] = arith1.floorsqrt(n[0]) + 1
        
    lsl = copy.deepcopy(sossp)
    sossp = ClassGroup(disc, 0, [])
    lll = copy.deepcopy(sogsp)
    sogsp = ClassGroup(disc, 0, [])
    tnt = copy.deepcopy(nt[0])
    ss = lsl.retel()

    for r in range(q[0]):
        for ssi in ss:
            newel = (tnt ** r ) * ssi
            if sossp.search(newel) == False:
                sossp.insttree(newel)

    y[0] = nt[0]**q[0]
    ltl = lll.retel()
    for a in range(q[0] + 1):
        for eol in ltl:
            newel2 = (y[0]**a) * eol
            if sogsp.search(newel2) == False:
                sogsp.insttree(newel2) # multiple of two elements of G
    return -1, sossp, sogsp

def setind(n, indofg, tmp_ss, tmp_gs, matla):
    """
    """
    lgtinlst = indofg
    if lgtinlst == 1:
        matla.append([n[0]])
        return True
    tmp_mt = [n[0]]
    for idofel in range(lgtinlst):
        if idofel == 0:
            continue
        try:
            if type(tmp_ss.alpha[idofel][1]) != int: 
                ioind = tmp_ss.alpha[idofel][2]
            else:
                ioind = 0
        except IndexError :
            ioind = 0
        except:
            raise ValueError
        try:
            if type(tmp_gs.beta[idofel][1]) != int:
                joind = tmp_gs.beta[idofel][2]
            else:
                joind = 0
        except IndexError :
            joind = 0
        except:
            raise ValueError
        tmp_mt.append(ioind - joind)
    matla.append(tmp_mt)
    return True
        
