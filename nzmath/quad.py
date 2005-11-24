import math
import time
import nzmath.gcd
import nzmath.factor.factor
import nzmath.arith1
import rational
import random
# import quad

def ret_nre(list_ofab, len_l, disc):
    '''
    determin c
    '''
#    print list_ofab
    while len(list_ofab[len_l][2]) != 0:
        tp_b = list_ofab[len_l][2].pop()
#        print type(tp_b)

#        print "###"
#        print list_ofab[len_l][0]
#        print tp_b
#        print "###"
        if (-disc - tp_b**2)%(-4*list_ofab[len_l][0]) != 0:
            tp_c = (-disc - tp_b**2)/(-4*list_ofab[len_l][0])
#            print 'AAA %s %s %s' % ( list_ofab[len_l][0],
#                                      tp_b,
#                                      tp_c)
            continue
        else:
            tp_c = (-disc - tp_b**2)/(-4*list_ofab[len_l][0])
#            print tp_c
            if list_ofab[len_l][0] > tp_c:
#                print 'BBB [%s,%s,%s]' %( list_ofab[len_l][0],
#                                          tp_b,
#                                          tp_c)
                continue
            elif nzmath.gcd.gcd(list_ofab[len_l][0],
                                nzmath.gcd.gcd(tp_b, tp_c)) != 1:
#                print 'BbC [%s,%s,%s]' %( list_ofab[len_l][0],
#                                          tp_b,
#                                          tp_c)
                continue
#                  Usually b of some reduced form is negative but
#                  in this program positive.
#                  or list_ofab[len_l][0] == tp_c) and (tp_b > 0):
            elif (list_ofab[len_l][0] == abs(tp_b)
                  or list_ofab[len_l][0] == tp_c) and (tp_b < 0 ):
#                print 'CBB [%s,%s,%s]' %( list_ofab[len_l][0],
#                                          tp_b,
#                                          tp_c)
                continue
            else:
#                print 'CCC [%s,%s,%s]' %( list_ofab[len_l][0],
#                                          tp_b,
#                                          tp_c)
                return [list_ofab[len_l][0], tp_b, tp_c], 0
    return [] , 1

def cs_n_e(disc,list_ofab):
    '''
    return a random element of the disc
    '''
    if disc < 0:
        raise ValueError
    while len(list_ofab) != 0:
        ret_lt = []
        len_l = len(list_ofab) - 1
        if list_ofab[len_l][1] == 0:
            list_ofab[len_l][1] = 1
            for t_f in range(list_ofab[len_l][0]):
                tt_f = t_f
                list_ofab[len_l][2].append(t_f)
                if t_f != 0:
                    list_ofab[len_l][2].append(-t_f)
            list_ofab[len_l][2].append(tt_f+1)
            list_ofab[len_l][2].append(-(tt_f+1))
            ret_lt, ret_on = ret_nre(list_ofab, len_l, disc)
            if ret_on == 0:
                return ret_lt
            else:
                continue
        elif list_ofab[len_l][1] == 1 and len(list_ofab[len_l][2]) != 0:
            ret_lt, ret_on = ret_nre(list_ofab, len_l, disc)
            if ret_on == 0:
                return ret_lt
            else:
                continue            
        else:
            list_ofab.pop()
            continue
    '''
    if there is not such element we want, return empty list.
    '''
    return []    

class QuadraticForm:
    """
    This is a class of quadratic form.
    """
    '''
    need to check discriminant!!.
    '''

    def __init__(self, rpfm):
        if type(rpfm) != list:
            raise ValueError
        self.f = rpfm

    def __mul__(self,oth):

        if type(oth) == type(self):
            return QuadraticForm(cps_ofpdf(self.f, oth.f))
        
        else:
            raise ValueError
    def __pow__(self,exp):
        if type(exp) != int:
            raise ValueError
        else:
            '''
            computing 1
            '''
            disc_t = self.f[1]**2 - (4*self.f[0]*self.f[2])
            self.u_t = []
            f_a = 1
            if disc_t % 4 == 0:
                f_b = 0
                f_c = -(disc_t / 4)
            else:
                f_b = 1
                f_c = -((disc_t - 1) / 4)
            self.u_t.append([f_a, f_b, f_c])


            if exp == 0:
                return self.u_t
            else:
                tmp_is = self.f[:]
                ret_is = QuadraticForm(tmp_is)
                id_x = 1
            
                while id_x < exp:
                    ret_is = ret_is * self
                    id_x += 1
                return ret_is


    def __repr__(self):
        return_str = '%s' % (self.f)

        return return_str

def test_of_crfo(disc):
    list_1 , list_2 , cls_nb = test_of_crf(disc)
    list_2.sort()
    flg_ofg = 0
    for k in range(cls_nb):
        temp_list = list_2[:]
        del temp_list[k]
        if list_2[k] in temp_list:
            flg_ofg = 1
            print "NOOOOO good"

    for i in range(cls_nb):
        list_1[i].sort()
        if list_1[i] != list_2:
            print list_1[i]
            print list_2
            print "no good"
            flg_ofg =1
        else:
            print list_1[i]
            print list_2
            print "very good"
    if flg_ofg == 0:
        print "OK"
    else:
        print "NG"
    print cls_nb
        
def test_of_crf(disc):
    cls_nb, list_of_qd = clsnbr_crf_not_fd(disc)
    ret_list = []
    
    for i in range(cls_nb):
        temp_list = []
        for j in range(cls_nb):
            temp_list.append(cps_ofpdf(list_of_qd[i], list_of_qd[j]))
        ret_list.append(temp_list)

    return ret_list, list_of_qd, cls_nb
    
    '''
    for i in list_of_qd:
        print i
    '''

def bsgs(disc, c_b, c_c):
    '''
    Shanks''s Baby-Step Giant-Step Method
    c_g is a name of class
    '''

    h = 1
    c_c1 = c_c
    c_b1 = c_b
    c_s = [1]
    c_l = [1]
    q = nzmath.arith1.floorsqrt(c_b1 - c_c1)
    x = range(q+1)
    c_s1_r = range(q+1) # This is a set of sets.
    #    c_s1 = range(q+1)
    c_s1 = []
    for i in range(q+1):
        x[i] = 0
        c_s1_r[i] = 0
        #       c_s1[i] = 0
    limit_ofa = nzmath.arith1.floorsqrt(-disc/3)
    list_ofa = range(1, limit_ofa + 1)
    ran_i = random.Random()
    ran_i.shuffle(list_ofa)
    list_ofab = []
    for tp_a in list_ofa:
        list_ofab.append([tp_a ,0,[]])
#    print list_ofab
    while len(list_ofab) > 0:
        '''
        choose a new random element
        '''
        try:
            '''
            class wo kaesu under construction
            '''
            '''
            print
            '''
            print cs_n_e(-disc, list_ofab)
            '''
            under construction
            '''
            continue
        except:
            print 'error'
            return 1
        else:
            pass
        '''
        gauss
        '''
        q = nzmath.arith1.floorsqrt(c_b1 - c_c1)
        
        x[0] = 1
        x[1] = g**h # g is an element of c_g
        smt_r = 0 # has 1 or not
        if x[1] == 1: # x_1 is an element of c_g
            n = 1
        else:
            for r in range(2,q):
                '''
                x[r] are elements of c_g
                '''
                x[r] = x[1]*x[r-1]
            for r in range(q):
                c_s1_r[r] = [el*x[r] for el in c_s]
                if smt_r == 0 and r != 0:
                    if 1 in c_s1_r[r]:
                        smt_r = r
                c_s1 = c_s1 + c_s1_r[r]
            c_s1.sort()
            if fg_on == 1:
                n = smt_r
            else:
                y = x[1]*x[q-1]
                z = x[1]**c_c1
                n = c_c1
                '''
                step 4 and 5
                '''
                fg_f = 0
                while 1:
                    for w in c_l:
                        z_1 = z*w
                        if z_1 in c_s1:
                            for rt in range(q):
                                if z_1 in c_s1_r[rt]:
                                    n = n - rt
                                    fg_f = 1
                                    break
                        
                        if fg_f == 1:
                            break
                    if fg_f == 1:
                        break
                    else:
                        '''
                        step 5
                        '''
                        z = y*z
                        n = n+q
                        if n <= c_b1:
                            continue
                        else:
                            print "stating that the order of G is larger than B"
                            return 1
                '''
                step 6
                '''
                n = h*h
                while 1:
                    '''
                    step 7
                    '''
                    '''
                    must init c_s1?
                    '''
                    fg_sn = 0
                    for p in nzmath.factor.factor.rhomethod(n):
                        c_s1 = c_s1 + [g**(n/p) for tp_s in c_s]
                        c_s1.sort()
                        for z in c_l:
                            if z in c_s1:
                                n = n/p
                                fg_sn = 1
                                break
                        if fg_sn == 1:
                            break
                    if fg_sn == 1:
                        continue
                '''
                step 8
                '''
                h = hn
                if h >= c_c:
                    return h
                else:
                    c_b1 = c_b1 / n
                    c_c1 = c_c1 / n
                    q = nzmath.arith1.floorsqrt(n)
                    for rp_t in range(q):
                        c_s = c_s + [(g**rp_t)*ss_et for ss_et in c_s]
                    y = g**q
                    for ap_l in range(q):
                        c_l = c_l + [(y**ap_l)*cl_et for cl_et in c_l]



                                
def fd_or_not(disc):
    '''
    cheking fundamental disc or not. if disc is not, raise error.
    '''
    
    if disc % 4 not in (0, 1):
        '''
        return "%s is not fundamental discriminant, since not 0,1 mod 4" % disc
        '''
        raise ValueError
        
    if disc >= 0:
        '''
        return "%s is not minus" % disc
        '''
        raise ValueError
    """
    checking fundamental discriminant of < 0
    """
    if disc == 1:
        '''
        return "%s is not fundamental discriminant" % disc
        '''
        raise ValueError    
    if (disc % 4 == 1) and nzmath.factor.factor.squarePart(-disc) == 1:
        return 0
    elif ((disc % 4 == 0) and nzmath.factor.factor.squarePart(-disc / 4) == 1
          and ((disc / 4) % 4 in (2,3))):
        return 0
    else:
        '''
        return "%s is not fundamental discriminant" % disc
        '''
        raise ValueError

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

def cls_num_ofdis(fun_dis, h_d0, f):
    '''
    caluclation h(D) from h(D_0)
    '''

    try:
        fd_or_not(fun_dis)
    except ValueError:
        print '%s is not fundamental discriminant' % fun_dis
        return 1
    except:
        print 'unknown error'
        return 1
    else:
        pass
#    print h_d0
    dis = fun_dis * (f*f)
#    print dis
    w_dis = deg_rounity(dis)
#    print w_dis
    w_fdis = deg_rounity(fun_dis)
#    print w_fdis
    m_p = 1
    for i in nzmath.factor.factor.rhomethod(f):
        m_p = m_p*(1 - nzmath.rational.Rational(nzmath.arith1.legendre(fun_dis, i[0]),i[0]))
    '''
    print m_p
    '''
    h_d = w_dis * nzmath.rational.Rational(h_d0 , w_fdis) * f * m_p
 #   print m_p
    return h_d


def red_pdf(a):
    '''
    Reduction of Positive Definite Forms
    f = (a[0], a[1], a[2])
    '''
    if a[0] < 0:
        raise ValueError
    for i in a:
        if type(i) != int:
            raise ValueError
        
    if (a[1]**2 - 4*a[0]*a[2]) >= 0:
        raise ValueError
    if (-a[0] <  a[1]) and (a[1] <= a[0]):
        if a[0] > a[2]:
            a[1] = -a[1]
            a[0], a[2] = a[2], a[0]
        else:
            if (a[0] == a[2]) and (a[1] < 0):
                a[1] = -a[1]
            return [a[0], a[1], a[2]]
    while 1:
        '''
        under construction!
        '''
        '''
        if a[1] < 0 and (a[1] % a[0]) !=0:
            print "aaa"
            tp_ba = (-a[1] / (2*a[0]))
            q = tp_ba + 1
            r = a[1] + (q*2*a[0])
        else:
        '''
        q = a[1] / (2*a[0])
        r = a[1] - q*(2*a[0])
#        print 'q=>%s' % q
#        print 'r=>%s' % r

        if r > a[0]:
#            print 'aaa'
            r = r - 2*a[0]
            q = q + 1
        a[2] = a[2] - ((a[1] + r)/2)*q
        a[1] = r
#        print 'a[2]=>%s' % a[2]
#        print 'a[1]=>%s' % a[1]
        if a[0] > a[2]:
#            print 'bbb'
            a[1] = -a[1]
            a[0], a[2] = a[2], a[0]
            continue
        else:
#            print 'ccc'
            if (a[0] == a[2]) and (a[1] < 0):
#                print 'ddd'
                a[1] = -a[1]
            return [a[0], a[1], a[2]]

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
    

def dis_chk(f):
    if len(f) != 3:
        raise ValueError
    for i in f:
        if type(i) != int:
            raise ValueError
    return (f[1]*f[1] - 4*f[0]*f[2])
    
def cps_ofpdf(f_1, f_2):

    '''
    Composition of Positive Definite Forms.
    '''

    if nzmath.gcd.gcd(f_1[0], nzmath.gcd.gcd(f_1[1], f_1[2])) != 1:
        raise ValueError
    if nzmath.gcd.gcd(f_2[0], nzmath.gcd.gcd(f_2[1], f_2[2])) != 1:
        raise ValueError                                                        

    if dis_chk(f_1) != dis_chk(f_2):
        raise ValueError

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

#    print f_3

    return red_pdf(f_3)

    
def clsnbr_crf(disc):
    '''
    counting reduced forms
    '''
    if disc % 4 not in (0, 1):
        raise ValueError
    if disc >= 0:
        raise ValueError
    """
    checking fundamental discriminant
    """
    if disc == 1:
        raise ValueError
    if (disc % 4 == 1) and nzmath.factor.factor.squarePart(disc) == 1:
        pass
    elif ((disc % 4 == 0) and nzmath.factor.factor.squarePart(disc / 4) == 1
          and ((disc / 4) % 4 in (2,3))):
        pass
    else:
        raise ValueError
    
    h = 1
    b = disc % 2
    c_b = long(math.sqrt(float(- disc) / 3))
    while 1:
        ck_f = 0
        q = (b**2 - disc) / 4
        a = b
        if a <= 1:
            a = 1
            chk_f = 1
        while 1:
            if chk_f == 0:
                if (q % a == 0) and nzmath.gcd.gcd(a, nzmath.gcd.gcd(b, q/a)) == 1:
                    if (a == b) or (a**2 == q) or (b == 0):
                        h += 1
                    else:
                        h += 2
            chk_f = 0
            a += 1
            if a**2 <= q:
                continue
            else:
                break
        b += 2
        if b <= c_b:
            continue
        else:
            return h

def clsnbr_crf_not_fd(disc, limit_dis=100000):
    '''
    counting reduced forms. not only fundamenta discriminant.
    '''
    time_a = time.time()
    if disc % 4 not in (0, 1):
        raise ValueError
    if disc >= 0:
        raise ValueError

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
        
    while 1:
        ck_f = 0
        q = (b**2 - disc) / 4
        a = b
        if a <= 1:
            a = 1
            chk_f = 1
        while 1:
            if chk_f == 0:
                if (q % a == 0) and nzmath.gcd.gcd(a, nzmath.gcd.gcd(b, q/a)) == 1:
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
        if b <= c_b:
            continue
        else:
            time_b = time.time()
            print time_b - time_a
            return h,ret_list

class BaseofQF:
    """
    BaseofQF is a class.
    """
    def __init__(self, disc, scal=1):
        self.dis = disc
        self.sca = scal

    def __repr__(self):
        return_str = '%s(%s + r(%s))/2' % (self.sca,
                                         self.dis,
                                       self.dis)
        return return_str
    
    def __add__(self, oth):
        if type(oth) == type(self):
            if oth.dis != self.dis:
                raise ValueError
            new_ins = BaseofQF(self.dis, oth.sca + self.sca)
            return new_ins
        else:
            raise ValueError
    def __mul__(self,oth):
        """
        only scalar mul
        """
        if type(oth) == int:
            new_ins = BaseofQF(self.dis, self.sca * oth)
            return new_ins
        else:
            raise ValueError

class QuadraticField:
    """
    QuadraticField is a class.
    """
    
    def __init__(self,disc):
        def checkDis(disc):
            qdisc = disc % 4
            if qdisc == 2:
                raise ValueError
            elif qdisc == 3:
                raise ValueError
            return self
        checkDis(disc)
        self.dis = disc # set discriminant

    def __repr__(self):
        return_str = '%s' % (self.dis)
        return return_str
    
    def creElement(self, a_0, a_1):
        return QuadraticFieldElement(self.dis, a_0, a_1)
        
class QuadraticFieldElement(QuadraticField):
    """
    QuadraticFieldElement is a class.
    """

    def __init__(self, disc, a_0, a_1):
        QuadraticField.__init__(self,disc)
        if (type(a_0) != int or type(a_1) != int):
            raise ValueError
        self.coefofel = [a_0, a_1]
        self.basew = BaseofQF(self.dis)
        self.gcd_a = nzmath.gcd.gcd(self.coefofel[0], self.coefofel[1])

    def __add__(self, oth):
        if type(oth) == type(self):
            if oth.basew.dis != self.basew.dis:
                raise ValueError
            else:
                return QuadraticFieldElement(self.dis,
                                             self.coefofel[0] + oth.coefofel[0],
                                             self.coefofel[1] + oth.coefofel[1])
        elif type(oth) == int:
            return QuadraticFieldElement(self.dis,
                                             self.coefofel[0] + oth,
                                             self.coefofel[1])
        else:
            raise ValueError

    def __sub__(self, oth):
        if type(oth) == type(self):
            if oth.basew.dis != self.basew.dis:
                raise ValueError
            else:
                return QuadraticFieldElement(self.dis,
                                             self.coefofel[0] - oth.coefofel[0],
                                             self.coefofel[1] - oth.coefofel[1])
        elif type(oth) == int:
            return QuadraticFieldElement(self.dis,
                                             self.coefofel[0] - oth,
                                             self.coefofel[1])
        else:
            raise ValueError


    def __mul__(self, oth):
        if type(oth) == type(self):
            if oth.basew.dis != self.basew.dis:
                raise ValueError
            b_0 = ((self.coefofel[0] * oth.coefofel[0]) +
                   (self.coefofel[1] * oth.coefofel[1]) *
                   (self.basew.dis - (self.basew.dis) ** 2) / 4)
            b_1 = ((self.coefofel[0] * oth.coefofel[1])
                    + (oth.coefofel[0] * self.coefofel[1])
                    + (self.coefofel[1] * oth.coefofel[1] * self.basew.dis))
            return QuadraticFieldElement(self.dis,
                                         b_0,
                                         b_1)
        elif type(oth) == int:
            return QuadraticFieldElement(self.dis,
                                             self.coefofel[0] * oth,
                                             self.coefofel[1] * oth)
        else:
            raise ValueError
        
    def __repr__(self):
        return_str = '%s(1) + %s(%s)' % (self.coefofel[0],
                                         self.coefofel[1],
                                         self.basew)
        return return_str

class QuadraticFieldElementQF(QuadraticField):
    """
    QuadraticFieldElementQF is a class.
    """

    def __init__(self, disc, a_0, a_1, a_2, a_3):
        QuadraticField.__init__(self,disc)
        if (type(a_0) != int or type(a_1) != int
            or type(a_2) != int or type(a_3) != int):
            raise ValueError
        if (a_2 == 0 and a_3 == 0):
            raise ValueError
        gcd_nrt = nzmath.gcd.gcd(a_0, a_1)
        gcd_dnt = nzmath.gcd.gcd(a_2, a_3)
        gcd_bt  = nzmath.gcd.gcd(gcd_nrt, gcd_dnt)
        print gcd_bt
        if gcd_bt > 1:
            a_0 = a_0 / gcd_bt
            a_1 = a_1 / gcd_bt
            a_2 = a_2 / gcd_bt
            a_3 = a_3 / gcd_bt
#        self.coefofel = [a_0, a_1, a_2, a_3]
        self.basew = BaseofQF(self.dis)
        self.q_nrt = QuadraticFieldElement(self.basew.dis, a_0, a_1) # gcd of a_0, a_1 is self.q_nrt.gcd_a
        self.q_dnt = QuadraticFieldElement(self.basew.dis, a_2, a_3)
        
    def __add__(self,oth):
        if type(oth) == type(self):
            if oth.dis != self.dis:
                raise ValueError
#            if oth.q_dnt.coefofel[0] == self.q_dnt.coefofel[0] and 
            
### under construction
        
        elif type(oth) == int:
            

            nzmath.gcd.gcd()

    def __repr__(self):
        return_str = '%s(1) + %s(%s) , %s(1) + %s(%s)' % (self.q_nrt.coefofel[0],
                                                          self.q_nrt.coefofel[1],
                                                          self.q_nrt.basew,
                                                          self.q_dnt.coefofel[0],
                                                          self.q_dnt.coefofel[1],
                                                          self.q_dnt.basew)
        return return_str


class SquareRootforQuad: 
    """
    SquareRootforQuad is a class.
    """
