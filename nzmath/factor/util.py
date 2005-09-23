"""
factor.util -- utility module for factorization.
"""

#import nzmath.arith1 as arith1
import nzmath.prime as arith1
import nzmath.gcd as gcd

Unknown = None

class FactoringMethod (object):
    """
    Base class of factoring methods.
    """
    def __init__(self):
        # verbosity
        self._verbose = False

    def factor(self, number):
        """
        Factor the given positive integer.
        The returned value must be in the form of [(p1, e1), ..., (pn, en)].

        Each derived class must override this method.

        Sample code:
        
        validate_input_number(number)
        tracker = FactoringInteger(number)
        target = tracker.getNextTarget()
        while True:
            if prime.primeq(target):
                tracker.register(target, True)
            else:
                p = find_a_factor_from(target)
                tracker.register(p, prime.primeq(p))
            try:
                target = tracker.getNextTarget()
            except LookupError:
                break
        return tracker.getFinalFactors()
        """
        pass

    def _getVerbose(self):
        "getter for property verbose"
        return self._verbose

    def _setVerbose(self, boolean):
        "setter for property verbose"
        self._verbose = boolean

    verbose = property(_getVerbose, _setVerbose, None, "Verbosity: boolean")


class FactoringInteger:
    """
    A class for keeping track of factorization.
    """
    def __init__(self, number):
        """
        The given number must be a composite.
        """
        self.number = number
        self.factors = [(number, 1)]
        self.primality = {number:False}

    def register(self, divisor, isprime = Unknown):
        """
        Register a divisor of the number, if the divisor is a true
        divisor of the number.  The number is divided by the divisor
        as many times as possible.
        """
        for base, index in self.factors:
            if base == divisor:
                if isprime and not self.primality[base]:
                    self.setPrimality(base, isprime)
                break
            common_divisor = gcd.gcd(base, divisor)
            if common_divisor > 1:
                if common_divisor == divisor:
                    k, coprime = arith1.vp(base, divisor)
                    if k:
                        if coprime > 1:
                            self.replace(base, [(divisor, k), (coprime, 1)])
                        else:
                            self.replace(base, [(divisor, k)])
                        self.primality[divisor] = isprime
                elif common_divisor < divisor:
                    self.register(common_divisor)

    def replace(self, number, factors):
        """
        Replace a number with factors.
        It is assumed that number = product of factors.
        """
        try:
            replacee = self.getMatchingFactor(number)
            self.factors.remove(replacee)
            replacee_index = replacee[1]
            for base, index in factors:
                if replacee_index == 1:
                    self.factors.append((base, index))
                else:
                    self.factors.append((base, index * replacee_index))
                if base not in self.primality:
                    self.setPrimality(base, Unknown)
        except LookupError:
            raise ValueError("no factor matches to %d." % number)

    def getMatchingFactor(self, number):
        """
        Find a factor matching to number.
        """
        # use linear search because self.factors is a short list.
        for base, index in self.factors:
            if base == number:
                return (base, index)
        raise LookupError("no factor matches.")

    def getCompositeFactor(self):
        """
        Return a composite (or unknown primality) factor from factors.
        """
        # use linear search because self.factors is a short list.
        for base, index in self.factors:
            if not self.primality[base]:
                return (base, index)
        raise LookupError("no factor matches.")

    def getNextTarget(self):
        """
        Return a composite (or unknown primality) factor of self.number.

        If there is no such factor, LookupError will be raised.
        """
        # use linear search because self.factors is a short list.
        for base, index in self.factors:
            if not self.primality[base]:
                return base
        raise LookupError("no factor matches.")

    def getResult(self):
        """
        Return the factors in the form of [(base, index), ...].
        """
        return self.factors[:]

    def setPrimality(self, number, isprime):
        """
        Set primality for number to isprime.
        """
        self.primality[number] = isprime

    def sortFactors(self):
        """
        Sort factors list. Return nothing.
        """
        if len(self.factors) > 1:
            self.factors.sort()
