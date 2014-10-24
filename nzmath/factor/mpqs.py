import math
import time
import logging
import nzmath.arith1 as arith1
import nzmath.gcd as gcd
import nzmath.prime as prime


SCALE = 30

_log = logging.getLogger('nzmath.factor.mpqs')


class QS(object):
    def __init__(self, n, sieverange, factorbase):
        self.number = n
        self.sqrt_n = int(math.sqrt(n))
        for p in (2, 3, 5, 7, 11, 13, 17, 19):
            if n % p == 0:
                raise ValueError("This number is divided by %d" % p)

        self.digit = arith1.log(self.number, 10) + 1
        self.Srange = sieverange
        self.FBN = factorbase

        self.move_range = range(self.sqrt_n-self.Srange, self.sqrt_n+self.Srange+1)
        self.FB = [-1]
        self.FB_log = [0]
        self.set_factor_base(factorbase)
        self.maxFB = self.FB[-1]
        N_sqrt_list = []
        for i in self.FB:
            if i != 2 and i != -1:
                e = int(math.log(2*self.Srange, i))
                N_sqrt_modp = sqroot_power(self.number, i, e)
                N_sqrt_list.append(N_sqrt_modp)
        self.solution = N_sqrt_list  #This is square roots of N on Z/pZ, p in factor base.

        poly_table = []
        log_poly = []
        minus_val = []
        for j in self.move_range:
            jj = (j**2)-self.number
            if jj < 0:
                jj = -jj
                minus_val.append(j-self.sqrt_n+self.Srange)
            elif jj == 0:
                jj = 1
            lj = int((math.log(jj)*30)*0.97)  # 0.97 is an erroe
            poly_table.append(jj)
            log_poly.append(lj)
        self.poly_table = poly_table  # This is Q(x) value , x in [-M+sqrt_n,M+sqrt_n].
        self.log_poly = log_poly      # This is log(Q(x)) value.
        self.minus_check = minus_val # This is "x" that Q(x) is minus value.

    def set_factor_base(self, factorbase_size):
        for p, log_p in zip(PRIMES_TABLE, PRIMES_LOG_TABLE):
            if arith1.legendre(self.number, p) == 1:
                self.FB.append(p)
                self.FB_log.append(log_p)
                if len(self.FB) == factorbase_size:
                    return

    def run_sieve(self):
        T = time.time()
        M = self.Srange
        start_location = []
        logp = [0]*(2*M+1)
        j = 2
        for i in self.solution:
            k = 0
            start_p = []
            while k < len(i):
                ppow = self.FB[j]**(k+1)
                q = self.sqrt_n // ppow
                s_1 = q*ppow + i[k]
                s_2 = q*ppow + (ppow - i[k])
                while True:
                    if s_1 < self.sqrt_n-M:
                        s_1 = s_1 + ppow
                        break
                    else:
                        s_1 = s_1 - ppow
                while True:
                    if s_2 < self.sqrt_n-M:
                        s_2 = s_2 + ppow
                        break
                    else:
                        s_2 = s_2 - ppow
                start_p.append([s_1-self.sqrt_n+M,s_2-self.sqrt_n+M])

                k += 1
            start_location.append(start_p)
            j += 1
        self.start_location = start_location

        if self.poly_table[0] & 1 == 0:
            i = 0
            while i <= 2*M:
                j = 1
                while True:
                    if self.poly_table[i] % (2**(j+1)) == 0:
                        j += 1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i += 2
        else:
            i = 1
            while i <= 2*M:
                j = 1
                while True:
                    if self.poly_table[i] % (2**(j+1)) == 0:
                        j += 1
                    else:
                        break
                logp[i] += self.FB_log[1]*j
                i += 2
        L = 2
        for j in self.start_location:
            k = 0
            while k < len(j):
                s_1 = j[k][0]
                s_2 = j[k][1]
                h_1 = 0
                h_2 = 0
                while s_1+h_1 <= 2*M:
                    logp[s_1+h_1] += self.FB_log[L]
                    h_1 += self.FB[L]**(k+1)
                while s_2+h_2 <= 2*M:
                    logp[s_2+h_2] += self.FB_log[L]
                    h_2 += self.FB[L]**(k+1)
                k += 1
            L += 1

        self.logp = logp
        smooth = []
        for t in range(2*M+1):
            if logp[t] >= self.log_poly[t]:
                poly_val = self.poly_table[t]
                index_set = set()
                for i, p in enumerate(self.FB):
                    if p == -1:
                        if t in self.minus_check:
                            index_set.add(0)
                    else:
                        r = 0
                        if arith1.vp(poly_val, p)[0] & 1:
                            index_set.add(i)
                smooth.append([index_set, (poly_val, t+self.sqrt_n-M)])
        _log.info(" Sieve time is %f sec" % (time.time()-T))
        _log.info(" Found smooth numbers are %d / %d" % (len(smooth), len(self.FB)))
        self.smooth = smooth
        return smooth


class MPQS(object):
    def __init__(self, n, sieverange=0, factorbase=0, multiplier=0):
        _log.info("%d; MPQS starting", n)

        if prime.primeq(n):
            raise ValueError("This number is Prime Number")
        for p in (2, 3, 5, 7, 11, 13):
            if n % p == 0:
                raise ValueError("This number is divided by %d" % p)

        self.number = n
        self.multiplier = 1
        self.last_poly = None
        self.sieve_range = 0
        self.FBN = 0
        self.FB = [-1]
        self.FB_log = [0]
        self.n_sqrt_p = []
        self.smooth = []
        self.sievingtime = 0
        self.coefficienttime = 0

        #Decide prameters for each digits
        digit = arith1.log(self.number, 10) + 1

        self._init_srange(sieverange, digit)
        self._init_fbn(factorbase, digit)

        self._init_multiplier(multiplier)
        self.number = self.multiplier * self.number

        _log.info("%d - digits Number", digit)
        _log.info("Multiplier is %d", self.multiplier)

        # Table of (log p) , p in FB
        self._init_fb()

        # Solve x^2 = n (mod p^e)
        self._init_nsqrt()

    def _init_srange(self, sieverange, digit):
        if sieverange != 0:
            self.sieve_range = sieverange
        elif digit < min(PARAMETERS_FOR_MPQS):
            self.sieve_range = PARAMETERS_FOR_MPQS[min(PARAMETERS_FOR_MPQS)][0]
        elif digit > max(PARAMETERS_FOR_MPQS):
            self.sieve_range = PARAMETERS_FOR_MPQS[max(PARAMETERS_FOR_MPQS)][0]
        else:
            self.sieve_range = PARAMETERS_FOR_MPQS[digit][0]

    def _init_fbn(self, factorbase, digit):
        if factorbase != 0:
            self.FBN = factorbase
        elif digit < min(PARAMETERS_FOR_MPQS):
            self.FBN = PARAMETERS_FOR_MPQS[min(PARAMETERS_FOR_MPQS)][1]
        elif digit > max(PARAMETERS_FOR_MPQS):
            self.FBN = PARAMETERS_FOR_MPQS[max(PARAMETERS_FOR_MPQS)][1]
        else:
            self.FBN = PARAMETERS_FOR_MPQS[digit][1]

    def _init_multiplier(self, multiplier):
        """
        Decide k such that k*n = 1 (mod4) and k*n has many factor base
        """
        if multiplier == 0:
            sqrt_state = []
            for p in (3, 5, 7, 11, 13):
                sqrt_state.append(arith1.legendre(self.number, p))

            if self.number % 8 == 1 and sqrt_state == [1, 1, 1, 1, 1]:
                self.multiplier = 1
            else:
                index8 = (self.number & 7) >> 1
                j = 0
                while sqrt_state != PRIME_8[index8][j][1]:
                    j += 1
                self.multiplier = PRIME_8[index8][j][0]
        else:
            if self.number & 3 == 1:
                self.multiplier = 1
            else:
                if multiplier == 1:
                    raise ValueError("This number is 3 mod 4 ")
                else:
                    self.multiplier = multiplier

    def _init_fb(self):
        """
        Table of (log p) , p in FB
        """
        i = 0
        while len(self.FB) < self.FBN:
            p = PRIMES_TABLE[i]
            if arith1.legendre(self.number, p) == 1:
                self.FB.append(p)
                self.FB_log.append(PRIMES_LOG_TABLE[i])
            i += 1

    def _init_nsqrt(self):
        """
        Solve x^2 = n (mod p^e)
        """
        assert self.FB[1] == 2
        for p in self.FB[2:]:
            e = int(math.log(2*self.sieve_range, p))
            self.n_sqrt_p.append(sqroot_power(self.number, p, e))

    def make_poly(self):
        """
        Make coefficients of f(x)= ax^2+b*x+c
        """
        T = time.time()
        self._make_next_coefficients()

        # Get solution of  F(x) = 0 (mod p^i)
        solutions = self._get_solutions(self.last_poly.f_2, self.last_poly.f_1)
        self.coefficienttime += time.time() - T
        return solutions

    def _make_next_coefficients(self):
        """
        Make new quadratic polynomial ax^2 + b*x + c with next bigger a.
        """
        if self.last_poly is None:
            self.last_poly = QuadraticPolynomial.next_polynomial(self.number, sieve_range=self.sieve_range)
        else:
            self.last_poly = QuadraticPolynomial.next_polynomial(self.number, init_param=self.last_poly.param)

        while self.last_poly.param in self.FB:
            self.last_poly = QuadraticPolynomial.next_polynomial(self.number, init_param=self.last_poly.param)

    def _get_solutions(self, a, b):
        """
        Get solution of  F(x) = 0 (mod p^i)
        """
        solution = []
        for p, s in zip(self.FB[2:], self.n_sqrt_p):
            k = 0
            p_solution = []
            ppow = 1
            while k < len(s):
                ppow *= p
                a_inverse = arith1.inverse(2*a, ppow)
                x_1 = ((-b + s[k])*a_inverse) % ppow
                x_2 = ((-b + (ppow - s[k]))*a_inverse) % ppow
                p_solution.append((x_1, x_2))
                k += 1
            solution.append(p_solution)
        return solution

    def run_sieve(self):
        solutions = self.make_poly()
        T = time.time()

        poly_table = []  # This is F(x) value , x in [-M,M].
        log_poly = []    # This is log(F(x)) value.
        minus_check = self._make_value_tables(poly_table, log_poly)

        start_location = self._prepare_start_location(solutions)

        logp = [0] * (2 * self.sieve_range + 1)

        # sieve by 2 & its powers
        self._sieve_2(logp, poly_table)

        for p, log_p, start_p in zip(self.FB[2:], self.FB_log[2:], start_location):
            # sieve by p
            self._sieve_p(logp, p, log_p, start_p)

        smooth = self._collect_smooth_vectors(logp, log_poly, poly_table, minus_check)
        self.sievingtime += time.time() - T
        _log.debug("Sieving Time = %f sec", self.sievingtime)
        return smooth

    def _make_value_tables(self, poly_table, log_poly):
        """
        Make tables poly_table and log_poly, which will be sieved.
        """
        diminished_scale = SCALE * 0.95  # 0.95 is an error
        rho = math.exp(1 / diminished_scale)
        rough_lower = 0
        rough_upper = 0
        minus_check = set()  # set of x where F(x) is negative.
        q_j = self.last_poly(-self.sieve_range - 1)
        for j in xrange(-self.sieve_range, self.sieve_range + 1):
            q_j += self.last_poly.delta(j)
            f_j = q_j
            if f_j < 0:
                f_j = -f_j
                minus_check.add(j + self.sieve_range)
            elif f_j == 0:
                f_j = 1
            if not (rough_lower <= f_j <= rough_upper):
                l_j = int(math.log(f_j) * diminished_scale)
                rough_lower = int(f_j / rho) + 1
                rough_upper = int(f_j * rho)
            poly_table.append(f_j)
            log_poly.append(l_j)
        return minus_check

    def _prepare_start_location(self, solutions):
        """
        For each odd prime in the factor base, find start location of
        sieve process.
        """
        start_location = []
        for p, solution in zip(self.FB[2:], solutions):
            start_p = []
            ppow = 1
            for s_k in solution:
                ppow *= p
                q = -self.sieve_range // ppow
                s_1 = (q + 1) * ppow + s_k[0] + self.sieve_range
                s_2 = (q + 1) * ppow + s_k[1] + self.sieve_range
                while s_1 >= ppow:
                    s_1 -= ppow
                while s_2 >= ppow:
                    s_2 -= ppow
                start_p.append((s_1, s_2))
            start_location.append(start_p)
        return start_location

    def _sieve_2(self, logp, poly_table):
        """
        Sieve by 2; update logp.
        """
        log_2 = self.FB_log[1]
        fullrange = 2 * self.sieve_range + 1
        ppow = 1
        solutions = []
        for pos in (0, 1):
            if poly_table[pos] & 1 == 0:
                solutions.append(pos)
        for i in range(12):
            ppow *= 2
            new_solutions = []
            for pos in solutions:
                for j in xrange(pos, fullrange, ppow):
                    logp[j] += log_2
                if poly_table[pos] % (ppow * 2) == 0:
                    new_solutions.append(pos)
                elif pos + ppow < fullrange and poly_table[pos + ppow] % (ppow * 2) == 0:
                    new_solutions.append(pos + ppow)
            if not new_solutions:
                break
            solutions = tuple(new_solutions)

    def _sieve_p(self, logp, p, log_p, start_p):
        """
        Sieve by p; update logp.
        """
        fullrange = 2 * self.sieve_range + 1
        ppow = 1
        for starts in start_p:
            ppow *= p
            for divisible in starts:
                for index in xrange(divisible, fullrange, ppow):
                    logp[index] += log_p

    def _collect_smooth_vectors(self, logp, log_poly, poly_table, minus_check):
        """
        Return smooth vectors collected from sieved tables.
        """
        a = self.last_poly.f_2
        b = self.last_poly.f_1
        d = self.last_poly.param
        smooth = []
        y = arith1.inverse(2 * d, self.number)
        for t in range(2 * self.sieve_range + 1):
            if logp[t] >= log_poly[t]:
                poly_val = poly_table[t]
                index_set = set()
                # -1
                if t in minus_check:
                    index_set.add(0)
                # p
                for i, p in enumerate(self.FB[1:], 1):
                    if arith1.vp(poly_val, p)[0] & 1:
                        index_set.add(i)
                H = y*(2*a*(t - self.sieve_range) + b) % self.number
                smooth.append([index_set, (poly_val, H)])
        return smooth

    def get_vector(self):
        _start = time.time()
        necessary = len(self.FB)
        if necessary < 100:
            necessary += 5
        else:
            necessary += 1
        self.smooth = []
        while len(self.smooth) < necessary:
            self.smooth.extend(self.run_sieve())
        _log.info("Found smooth numbers are %d / %d", len(self.smooth), len(self.FB))
        _log.info("Sieving Time = %f sec", self.sievingtime)
        _log.info("Total time of getting enough smooth numbers = %f sec", time.time() - _start)
        return self.smooth


class QuadraticPolynomial(object):
    """
    A quadratic polynomial to use in MPQS.
    """
    def __init__(self, number, init_param):
        self.number = number
        self.param = init_param
        # coefficents: f_0 + f_1 * x + f_2 * x^2, later initialized
        self.f_0 = self.f_1 = self.f_2 = None
        # coefficents: d_0 + d_1 * x = F(x) - F(x - 1)
        self.d_0 = self.d_1 = None
        self.init_coefficients()

    @classmethod
    def next_polynomial(cls, number, sieve_range=None, init_param=None):
        """
        Return the next polynomial.

        If init_param optional argument is given, start searching the
        parameter from init_param + 4.  The argument should be 3 mod 4,
        otherwise factorization does not work.

        If sieve_range optional argument is given and init_param is not
        given, the parameter will be the smallest one.
        """
        if init_param is None:
            param = int(math.sqrt((math.sqrt(number)/(math.sqrt(2)*sieve_range)))) | 3
        else:
            param = init_param + 4

        while not prime.primeq(param) or arith1.legendre(number, param) != 1:
            param += 4

        return cls(number, param)

    def init_coefficients(self):
        """
        Initialize the coefficients f_0, f_1 & f_2 of the quadratic
        polynomial, determined from the parameter.
        """
        self.f_2 = self.param**2
        h_0 = pow(self.number, (self.param - 3) >> 2, self.param)
        h_1 = h_0 * self.number % self.param
        h_2 = (arith1.inverse(2, self.param) * h_0 * (self.number - h_1 ** 2) // self.param) % self.param
        self.f_1 = (h_1 + h_2 * self.param) % self.f_2
        if self.f_1 & 1 == 0:
            self.f_1 -= self.f_2
        self.f_0 = (self.f_1 * self.f_1 - self.number) // (4 * self.f_2)

        self.d_0 = self.f_1 - self.f_2
        self.d_1 = 2 * self.f_2

    def __call__(self, num):
        """
        Return the value as quadratic polynomial function.
        """
        return (self.f_2 * num + self.f_1) * num + self.f_0
 
    def delta(self, num):
        """
        Return f(num) - f(num - 1)
        """
        return self.d_0 + self.d_1 * num


class Elimination(object):
    def __init__(self, smooth, fb_size):
        self.vector = []
        self.history = []
        for i, vec in enumerate(smooth):
            self.vector.append(vec[0])
            self.history.append(set((i,)))
        self.FB_number = fb_size
        self.row_size = len(self.vector)

    def vector_add(self, i, j):
        self.vector[j] = self.vector[i] ^ self.vector[j]

    def history_add(self, i, j):
        self.history[j] = self.history[i] ^ self.history[j]

    def gaussian(self):
        T = time.time()
        pivot = set()
        Smooth = len(self.vector)
        for j in range(self.FB_number):
            for k, V_k in enumerate(self.vector):
                if k in pivot or j not in V_k:
                    continue
                pivot.add(k)
                for h in range(k + 1, Smooth):
                    if h in pivot or j not in self.vector[h]:
                        continue
                    self.history_add(k, h)
                    self.vector_add(k, h)
                break

        zero_vector = []
        for check in range(Smooth):
            if check not in pivot and not self.vector[check]:
                zero_vector.append(check)
        _log.info("Time of Gaussian Elimination = %f sec", time.time() - T)
        return zero_vector


# qs, mpqs factors n completely
def qs(n, s, f):
    """
    This is main function of QS
    Arguments are (composite_number, sieve_range, factorbase_size)
    You must input these 3 arguments.
    """
    a = time.time()
    Q = QS(n, s, f)
    _log.info("Sieve range is [ %d , %d ] , Factorbase size = %d , Max Factorbase %d" % (Q.move_range[0], Q.move_range[-1], len(Q.FB), Q.maxFB))
    Q.run_sieve()
    V = Elimination(Q.smooth, len(Q.FB))
    A = V.gaussian()
    _log.info("Found %d linearly dependent relations" % len(A))
    answerX_Y = []
    N_factors = []
    for i in A:
        X = 1
        Y = 1
        for j in V.history[i]:
            X *= Q.smooth[j][1][0]
            Y *= Q.smooth[j][1][1]
            Y = Y % Q.number
        X = sqrt_modn(X, Q.number)
        answerX_Y.append(X-Y)
    for k in answerX_Y:
        if k != 0:
            factor = gcd.gcd(k, Q.number)
            if factor not in N_factors and factor != 1 and \
               factor != Q.number and prime.primeq(factor) == 1:
                N_factors.append(factor)
    N_factors.sort()
    _log.info("Total time = %f sec" % (time.time()-a))
    _log.info(str(N_factors))
    return N_factors


def mpqs(n, s=0, f=0, m=0):
    """
    This is main function of MPQS.
    Arguments are (composite_number, sieve_range, factorbase_size, multiplier)
    You must input composite_number at least.
    """
    T = time.time()
    M = MPQS(n, s, f, m)
    _log.info("Sieve range is [ %d , %d ] , Factorbase size = %d , Max Factorbase %d" % (-M.sieve_range, M.sieve_range, len(M.FB), max(M.FB)))
    M.get_vector()
    N = M.number // M.multiplier
    V = Elimination(M.smooth, len(M.FB))
    A = V.gaussian()
    _log.info("Found %d linerly dependent relations" % len(A))
    answerX_Y = []
    N_prime_factors = []
    N_factors = []
    output = []
    for i in A:
        X = 1
        Y = 1
        for j in V.history[i]:
            X *= M.smooth[j][1][0]
            Y *= M.smooth[j][1][1]
            Y = Y % M.number
        X = sqrt_modn(X, M.number)
        if X != Y:
            answerX_Y.append(X-Y)
    NN = 1
    for k in answerX_Y:
        factor = gcd.gcd(k, N)
        if factor not in N_factors and factor != 1 and factor != N \
               and factor not in N_prime_factors:
            if prime.primeq(factor):
                NN = NN*factor
                N_prime_factors.append(factor)
            else:
                N_factors.append(factor)

    _log.info("Total time = %f sec" % (time.time() - T))

    if NN == N:
        _log.debug("Factored completely!")
        N_prime_factors.sort()
        for p in N_prime_factors:
            N = N // p
            i = arith1.vp(N, p, 1)[0]
            output.append((p, i))
        return output
    elif NN != 1:
        f = N // NN
        if prime.primeq(f):
            N_prime_factors.append(f)
            _log.debug("Factored completely !")
            N_prime_factors.sort()
            for p in N_prime_factors:
                N = N // p
                i = arith1.vp(N, p, 1)[0]
                output.append((p, i))
            return output

    for F in N_factors:
        for FF in N_factors:
            if F != FF:
                Q = gcd.gcd(F, FF)
                if prime.primeq(Q) and Q not in N_prime_factors:
                    N_prime_factors.append(Q)
                    NN = NN*Q

    N_prime_factors.sort()
    for P in N_prime_factors:
        i, N = arith1.vp(N, P)
        output.append((P, i))

    if  N == 1:
        _log.debug("Factored completely!! ")
        return output

    for F in N_factors:
        g = gcd.gcd(N, F)
        if prime.primeq(g):
            N_prime_factors.append(g)
            N = N // g
            i = arith1.vp(N, g, 1)[0]
            output.append((g, i))
    if N == 1:
        _log.debug("Factored completely !! ")
        return output
    elif prime.primeq(N):
        output.append((N, 1))
        _log.debug("Factored completely!!! ")
        return output
    else:
        N_factors.sort()
        _log.error("Sorry, not factored completely")
        return output, N_factors


########################################################
#                                                      #
# Following functions are subfunction for main program #
#                                                      #
########################################################

def eratosthenes(n):
    return list(prime.generator_eratosthenes(n))

def prime_mod8():
    """
    Make a table for choosing multiplier which makes N to have
    factorbase(2,3,5,7,11,13)
    """
    primes = eratosthenes(8090)
    PrimeList = {1:[], 3:[], 5:[], 7:[]}
    sp = (3, 5, 7, 11, 13)
    for p in primes[6:]:
        leg = [arith1.legendre(p, q) for q in sp]
        if leg not in PrimeList[p & 7]:
            PrimeList[p & 7].append([p, leg])
    return [PrimeList[1], PrimeList[3], PrimeList[5], PrimeList[7]]

def eratosthenes_log():
    primes = PRIMES_TABLE
    primes_log = [int(math.log(p) * SCALE) for p in primes]
    return primes_log

def sqrt_modn(n, modulo):
    import nzmath.factor.methods as methods
    factorOfN = methods.trialDivision(n)
    prod = 1
    for p, e in factorOfN:
        prod = (prod * pow(p, e >> 1, modulo)) % modulo
    return prod

def sqroot_power(a, p, n):
    """
    return a square root of a mod p^k for k = 2,3,...,n for each k
    """
    x = arith1.modsqrt(a, p)
    answer = [x]
    ppower = p
    inverse = arith1.inverse(x << 1, p)
    for i in range(n - 1):
        x += (a - x ** 2) // ppower * inverse % p * ppower
        ppower *= p
        answer.append(x)
    return answer

#################
# Initial items #
#################
PRIMES_TABLE = eratosthenes(10**5)
PRIMES_LOG_TABLE = eratosthenes_log()
PRIME_8 = prime_mod8()
# {#digits: (sieve_range, factorbase_size)}
PARAMETERS_FOR_MPQS = {
    9: (100, 20),
    10: (100, 21),
    11: (100, 22),
    12: (100, 24),
    13: (100, 26),
    14: (100, 29),
    15: (100, 32),
    16: (200, 35),
    17: (300, 40),
    18: (300, 60),
    19: (300, 80),
    20: (300, 90),
    21: (300, 100),
    22: (300, 120),
    23: (300, 140),
    24: (600, 160),
    25: (900, 180),
    26: (1000, 200),
    27: (1200, 220),
    28: (1600, 240),
    29: (2000, 260),
    30: (2400, 350),
    31: (2700, 370),
    32: (3000, 390),
    33: (4000, 410),
    34: (5000, 500),
    35: (6000, 600),
    36: (6500, 700),
    37: (7000, 8500),
    38: (8000, 1000),
    39: (9000, 1200),
    40: (10000, 1500),
    41: (12000, 1600),
    42: (14000, 1700),
    43: (15000, 1800),
    44: (15000, 1900),
    45: (15000, 2200),
    46: (20000, 2400),
    47: (25000, 2500),
    48: (27500, 2700),
    49: (30000, 2800),
    50: (35000, 2900),
    51: (40000, 3000),
    52: (50000, 3200),
    53: (50000, 3500),
    54: (55000, 3800),
    55: (60000, 4000),
}

###
### only find a factor
###

def mpqsfind(n, s=0, f=0, m=0, verbose=False):
    """
    This is the main function of MPQS.
    The main argument is the composite_number to be factored.
    Parameters are s=sieve_range, f=factorbase_size, m=multiplier
    and verbose.
    """
    # verbosity
    if verbose:
        _log.setLevel(logging.DEBUG)
        _log.debug("verbose")
    else:
        _log.setLevel(logging.NOTSET)

    starttime = time.time()
    M = MPQS(n, s, f, m)
    _log.info("Sieve range is [%d, %d]", -M.sieve_range, M.sieve_range)
    _log.info("Factorbase size = %d, Max Factorbase %d", len(M.FB), M.FB[-1])
    M.get_vector()
    N = M.number // M.multiplier
    V = Elimination(M.smooth, len(M.FB))
    A = V.gaussian()
    _log.info("Found %d linearly dependent relations", len(A))
    for i in A:
        X = 1
        Y = 1
        for j in V.history[i]:
            X *= M.smooth[j][1][0]
            Y *= M.smooth[j][1][1]
            Y = Y % M.number
        X = arith1.floorsqrt(X) % M.number
        if X != Y:
            divisor = gcd.gcd(X - Y, N)
            if 1 < divisor < N:
                _log.info("Total time = %f sec", time.time() - starttime)
                return divisor
