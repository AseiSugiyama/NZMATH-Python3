"""
For sample powering(or scalar multiplication in additive group) method.
You shouldn't use directly, but choose the proper method and take in your module as __pow__(multiplicative group) or __mul__(additive group).
(It should be taken in module such as algebraicessence.py or group.py.)
"""

import math
import nzmath.arith1 as arith1

_OVERRID_WARNMSG = "%s have to be overridden"

class MultiplicativeSet:
    """
    Interface of multiplication set.
    Do not instanciate.
    """

    def mul(self, former, after):
        """ Compute multiplication of former and after on set.
        """
        return former * after
        # raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def square(self, element):
        """Compute squaring of element on set.
        """
        return element * element
        # raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def pow(self, element, index):
        """ Compute index-th power of element on set.
        """
        if not index: # zero powering
            if hasattr(self, identity):
                return self.identity
            else:
                raise TypeError("%s don't have identity" % self.__class__.__name__)
        idx = long(index)
        if index == idx:
            if index < 0:
                if hasattr(self, isinvertible) and self.isinvertible():
                    return self.pow(self.inverse(element), -idx)
                else:
                    raise TypeError("%s isn't invertible" % element)
            if idx == 1:
                return element
            if idx == 2:
                return self.square(element)
            else:
                # Choose proper below method!
                return self._lr_binary_pow(self, element, idx)
        else:
            # for special powerings(rational, irrational, complex number, etc.)
            # if you need, define them in subclass
            raise NotImplementedError

    # powering methods. Assume index is (constant) instance of long and index > 1.

    def _rl_binary_pow(self, element, index):
        """
        powering by using right-left binary method.
        This method don't call 'identity'
        """
        mul_part = element
        while True:
            if index & 1:
                try:
                    sol = self.mul(sol, mul_part)
                except NameError:
                    sol = mul_part
            index >>= 1
            if not index:
                return sol
            else:
                mul_part = self.square(mul_part)

    def _lr_binary_pow(self, element, index):
        """
        powering by using left-right binary method.
        This method don't call 'identity'
        """
        spot = 1 << (long(math.log(index, 2)) - 1)
        sol = element
        while spot:
            sol = self.square(sol)
            if spot & index:
                sol = self.mul(sol, element)
            spot >>= 1
        return sol

    def _three_pow(self, element, index):
        """
        powering by using left-right base 3 method.
        """
        digits = arith1.expand(index, 3)
        e = len(digits) - 1
        f = e
        # Precomputation
        pre_table = [element, self.square(element)]
        # Main Loop
        while f >= 0:
            tit = digits[f]
            if f == e:
                sol = pre_table[tit - 1]
            else:
                sol = self.mul(self.square(sol), sol)
                if tit:
                    sol = self.mul(sol, pre_table[tit - 1])
            f -= 1
        return sol

    def _two_pow_ary_pow(self, element, index):
        """
        powering by using left-right 2^size ary method.('size' is the proper integer)
        (Algorithm 1.2.4 of Cohen's book)
        size is selected by average analystic optimization
        """
        # Find the proper size
        log_n = long(math.log(index, 2))
        size = 1
        pow_size = 1
        while log_n > (size + 1) * (size + 2) * pow_size:
            pow_size <<= 1
            size += 1
        # Compute win_lst, sqr_lst
        pow_size <<= 1
        s, m = arith1.vp(index, 2)
        win_lst, sqr_lst = [], [s]
        while m > pow_size:
            m, b = divmod(m, pow_size)
            win_lst.append(b)
            s, m = arith1.vp(m, 2)
            sqr_lst.append(s + size)
        win_lst.append(m)
        e = len(win_lst) - 1
        f = e
        # Precomputation
        sqr = self.square(element)
        pre_table = [element]
        pow_size = (pow_size // 2) - 1
        for i in range(pow_size):
            pre_table.append(self.mul(pre_table[-1], sqr))
        # Main Loop
        while f >= 0:
            if f == e:
                sol = pre_table[(win_lst[f] - 1) >> 1]
            else:
                sol = self.mul(sol, pre_table[(win_lst[f] - 1) >> 1])
            for i in range(sqr_lst[f]):
                sol = self.square(sol)
            f -= 1
        return sol

    def _ones_and_zero_pows(self, element, index):
        """
        powering by 'ones' window method.
        """
        # Compute win_lst, sqr_lst
        b, n = arith1.vp(index, 2)
        win_lst, sqr_lst = [], [b]
        maxa = 1
        while True:
            ones = 0
            while n & 1:
                n >>= 1
                ones += 1
            win_lst.append(ones)
            if maxa < ones:
                maxa = ones
            if n == 0:
                break
            zeros = 0
            while not (n & 1):
                n >>= 1
                zeros += 1
            sqr_lst.append(zeros + win_lst[-1])
        e = len(win_lst) - 1
        f = e
        # Precomputation
        sqrs = element
        pre_table = [element]
        for i in range(maxa - 1):
            sqrs = self.square(sqrs)
            pre_table.append(self.mul(pre_table[-1], sqrs))
        # Main Loop
        while f >= 0:
            if f == e:
                sol = pre_table[win_lst[f] - 1]
            else:
                sol = self.mul(sol, pre_table[win_lst[f] - 1])
            for i in range(sqr_lst[f]):
                sol = self.square(sol)
            f -= 1
        return sol

    def _flexible_pow(self, element, index):
        """
        powering by using flexible base method.
        (Algorithm 1.2.4.1 & 1.2.4.2 of Cohen's book)
        size is selected by average analystic optimization
        """
        log_n = long(math.log(index, 2))
        # Find the proper window size
        size = 1
        pow_size = 1
        while log_n > (size + 1) * (size + 2) * pow_size:
            pow_size <<= 1
            size += 1
        pow_size <<= 1
        # Compute win_lst, sqr_lst
        b, n = arith1.vp(index, 2)
        win_lst, sqr_lst = [], [b]
        while True:
            m, r = divmod(n, pow_size)
            win_lst.append(r)
            if not(m):
                break
            b, n = arith1.vp(m, 2)
            sqr_lst.append(b + size)
        e = len(win_lst) - 1
        f = e
        # Precomputation
        sqrs = element
        pre_table = [element]
        pow_size >>= 1
        for i in range(pow_size - 1):
            sqrs = self.square(sqrs)
            pre_table.append(self.mul(pre_table[-1], sqrs))
        # Main Loop
        while f >= 0:
            if f == e:
                sol = pre_table[(win_lst[f] - 1) >> 1]
            else:
                sol = self.mul(sol, pre_table[(win_lst[f] - 1) >> 1])
            for i in range(sqr_lst[f]):
                sol = self.square(sol)
            f -= 1
        return sol

    def _window_pow(self, element, index):
        """
        powering by using small-window method
        window size is selected by average analystic optimization
        """
        log_n = long(math.log(index, 2))
        # Find the proper window size
        size = 2
        pow_size = 2
        while log_n > (size + 1) * (size + 2) * (pow_size - 1):
            pow_size <<= 1
            size += 1
        # Precomputation
        sqr = self.square(element)
        pre_table = [element]
        pow_size -= 1
        for i in range(pow_size):
            pre_table.append(self.mul(pre_table[-1], sqr))
        
        near_n = 1 << log_n
        spot = near_n
        while spot:
            if not(spot & index):
                sol = self.square(sol)
                spot >>= 1
            else:
                # Find the window
                f_spot, e_spot = spot, spot >> (size - 1)
                t_size = size
                if not(e_spot):
                    e_spot = 1
                    t_size = int(math.log(f_spot, 2)) + 1
                while True:
                    if e_spot & index:
                        spot = (e_spot >> 1)
                        window = 0
                        sqr = 1
                        while f_spot != e_spot: # Compute value of window
                            if index & e_spot:
                                window += sqr
                            sqr <<= 1
                            e_spot <<= 1
                        window += sqr
                        break
                    t_size -= 1
                    e_spot <<= 1
                # Compute a part of powering
                if f_spot == near_n:
                    sol = pre_table[(window - 1) >> 1]
                else:
                    for i in range(t_size):
                        sol = self.square(sol)
                    sol = self.mul(sol, pre_table[(window - 1) >> 1])
        return sol
