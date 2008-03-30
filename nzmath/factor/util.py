"""
factor.util -- utility module for factorization.
"""

import nzmath.arith1 as arith1
import nzmath.gcd as gcd
import nzmath.prime as prime

Unknown = None

class FactoringMethod (object):
    """
    Base class of factoring methods.
    """
    def __init__(self):
        # verbosity
        self._verbose = False

    def factor(self, number, **options):
        """
        Factor the given positive integer.

        The default returned type is a list of tuples.  Each tuple has
        a factor and its valuation, and the product is equal to the
        given number.  It looks like:
          [(p1, e1), ..., (pn, en)].

        an option 'return_type' is for the returned type, whose value can be:
        1) 'list' for default type described above.
        2) 'tracker' for FactoringInteger.

        an option 'need_sort' is boolean: True to sort the result.
        This should be specified with return_type='list'.
        """
        if not self._validate_input_number(number):
            return []

        tracker = FactoringInteger(number)
        options['return_type'] = options.get('return_type', 'list')
        result = self.continue_factor(tracker, **options)
        if options['return_type'] == 'list' and options.get('need_sort', False):
            result.sort()
        return result

    def continue_factor(self, tracker, **options):
        """
        Continue factoring and return the result of factorization.

        The argument 'tracker' should be an instance of FactoringInteger.
        The default returned type is FactoringInteger.

        This method should be overridden.
        """
        return_list = (options.get('return_type', '') == 'list')

        while True:
            try:
                target = tracker.getNextTarget()
            except LookupError:
                # factored completely
                break
            if prime.primeq(target):
                tracker.register(target, True)
            else:
                p = self.find(target, **options)
                if 1 < p < target:
                    # factor found
                    tracker.register(p)
                elif p == 1:
                    # failed to factor
                    break
        if return_list:
            return tracker.getResult()
        else:
            return tracker

    @staticmethod
    def _validate_input_number(number):
        """
        Return True if the given number is an integer greater than one.
        Return False if the given number is equal to one.
        Otherwise, raise ValueError.
        """
        if isinstance(number, (int, long)):
            if number == 1:
                return False
            if number > 1:
                return True
        raise ValueError("number must be a positive integer.")

    def find(self, target, **options):
        """
        Find a factor from the target number.

        This method must be overridden, or 'factor' method should be
        overridden not to call this method.
        """
        pass

    def _getVerbose(self):
        "getter for property verbose"
        return self._verbose

    def _setVerbose(self, boolean):
        "setter for property verbose"
        self._verbose = boolean

    verbose = property(_getVerbose, _setVerbose, None, "Verbosity: boolean")


class FactoringInteger (object):
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

    def register(self, divisor, isprime=Unknown):
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
            if common_divisor == 1:
                continue
            # common_divisor > 1:
            if common_divisor == divisor:
                k, coprime = arith1.vp(base, common_divisor)
                while not gcd.coprime(common_divisor, coprime):
                    # try a smaller factor
                    common_divisor = gcd.gcd(common_divisor, coprime)
                    k, coprime = arith1.vp(base, common_divisor)
                if k:
                    if coprime > 1:
                        self.replace(base, [(common_divisor, k), (coprime, 1)])
                    else:
                        self.replace(base, [(common_divisor, k)])
                    self.primality[divisor] = isprime
            else: # common_divisor properly divides divisor.
                self.register(common_divisor)
                self.register(divisor // common_divisor)

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
        Return a composite (or unknown primality) factor from factors
        in a form (base, index), whose base's primality is non-True.

        If there is no such factor, LookupError will be raised.
        """
        # use linear search because self.factors is a short list.
        for base, index in self.factors:
            if not self.primality[base]:
                return (base, index)
        raise LookupError("no factor matches.")

    def getNextTarget(self, cond=None):
        """
        Return the next target which meets 'cond'.  if 'cond' is not
        specified, then the next target is a composite (or unknown
        primality) factor of self.number.  'cond' can be a binary
        (arguments are base and index) predicate.

        If there is no such factor, LookupError will be raised.
        """
        if cond is None:
            cond = lambda base, index: not self.primality[base]
        # use linear search because self.factors is a short list.
        for base, index in self.factors:
            if cond(base, index):
                return base
        raise LookupError("no factor matches.")

    def getResult(self):
        """
        Return the factors in the form of [(base, index), ...].
        """
        return list(self.factors)

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
