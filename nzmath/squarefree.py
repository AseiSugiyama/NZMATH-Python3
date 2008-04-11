"""
Squarefreeness tests.

Definition:
  n: squarefree <=> there is no p whose square divides n.

Examples:
  - 0 is non-squarefree because any square of prime can divide 0.
  - 1 is squarefree because there is no prime dividing 1.
  - 2, 3, 5, and any other primes are squarefree.
  - 4, 8, 9, 12, 16 are non-squarefree composites.
  - 6, 10, 14, 15, 21 are squarefree composites.
"""

import math
import nzmath.arith1 as arith1
import nzmath.bigrange as bigrange
import nzmath.prime as prime
import nzmath.rational as rational
import nzmath.factor.methods as factor_methods


class Undetermined (Exception):
    """
    Undetermined state of calculation.
    """


def lenstra(n):
    """
    If return value is True, n is squarefree.  Otherwise, the
    squarefreeness is still unknown and Undetermined is raised.

    The condition is so strong that it seems n is a prime or a
    Carmichael number.

    pre-condition: n & 1
    reference: H.W.Lenstra 1973 ---
    """
    n = int(n) # see sf bug #1826712
    predn = n - 1
    bound = int(math.log(n)**2 + 1)
    for i in range(2, bound):
        if pow(i, predn, n) != 1:
            raise Undetermined("Lenstra's method can't determine squarefreeness")
    return True


def trial_division(n):
    """
    Test whether n is squarefree or not.

    The method is a kind of trial division.
    """
    try:
        return trivial_test(n)
    except Undetermined:
        pass

    for p in prime.generator():
        if not (n % (p*p)):
            # found a square factor
            return False
        elif not (n % p):
            # found a non-square factor
            n //= p
            try:
                return trivial_test(n)
            except Undetermined:
                pass
        if p*p*p > n:
            break
    # At the end of the loop:
    #   n doesn't have any factor less than its cubic root.
    #   n is not a prime nor a perfect square number.
    # The factor must be two primes p and q such that p < sqrt(n) < q.
    return True


def trivial_test(n):
    """
    Test whether n is squarefree or not.

    This method do anything but factorization.
    """
    if n == 1 or n == 2:
        return True
    if arith1.issquare(n):
        return False
    if n & 1:
        return lenstra(n)
    elif not (n % 4):
        return False
    raise Undetermined("trivial test can't determine squarefreeness")


def viafactor(n):
    """
    Test whether n is squarefree or not.

    It is obvious that if one knows the prime factorization of the number,
    he/she can tell whether the number is squarefree or not.
    """
    for p, e in factor_methods.factor(n):
        if e >= 2:
            return False
    return True


# ternary logic versions
#
# The third logical value means "uncertain" or "proof unknown".
# We designate None to this value.  It lets "unknown" status
# be, at least, not true.
# There are nothing corresponding to boolean logic operators.
# They are out of scope of this module.

def lenstra_ternary(n):
    """
    Test the squarefreeness of n.
    The return value is one of the ternary logical constants.
    If return value is TRUE, n is squarefree.  Otherwise, the
    squarefreeness is still unknown and UNKNOWN is returned.

    The condition is so strong that it seems n is a prime or a
    Carmichael number.

    pre-condition: n & 1
    reference: H.W.Lenstra 1973 ---
    """
    n = int(n) # see sf bug #1826712
    predn = n - 1
    bound = int(math.log(n)**2 + 1)
    for i in range(2, bound):
        if pow(i, n - 1, n) != 1:
            return None
    return True


def trivial_test_ternary(n):
    """
    Test the squarefreeness of n.
    The return value is one of the ternary logical constants.

    The method uses a series of trivial tests.
    """
    if n == 1 or n == 2:
        return True
    if arith1.issquare(n):
        return False
    if n & 1:
        return lenstra_ternary(n)
    elif not (n % 4):
        return False
    return None


def trial_division_ternary(n):
    """
    Test the squarefreeness of n.
    The return value is one of the ternary logical constants.

    The method is a kind of trial division.
    """
    result = trivial_test_ternary(n)
    if result is not None:
        return result

    for p in prime.generator():
        if not (n % (p*p)):
            # found a square factor
            return False
        elif not (n % p):
            # found a non-square factor
            n //= p
            result = trivial_test_ternary(n)
            if result is not None:
                return result
        if p*p*p > n:
            break
    # At the end of the loop:
    #   n doesn't have any factor less than its cubic root.
    #   n is not a prime nor a perfect square number.
    # The factor must be two primes p and q such that p < sqrt(n) < q.
    return True


# Just for symmetry, viafactor_ternary is defined as alias of viafactor.
viafactor_ternary = viafactor


class SquarefreeDecompositionMethod (factor_methods.TrialDivision):
    """
    Decomposition of an integer into square part and squarefree part.
    """
    def __init__(self):
        factor_methods.TrialDivision.__init__(self)
        self.primeseq = None # initialized later

    def continue_factor(self, tracker, **options):
        """
        Continue factoring and return the result of factorization.

        The argument 'tracker' should be an instance of FactoringInteger.
        The default returned type is FactoringInteger.
        """
        return_list = (options.get('return_type', '') == 'list')

        non_square = lambda b, i: i == 1 and not trivial_test_ternary(b)

        try:
            while True:
                target = tracker.getNextTarget(non_square)
                # A non-square composite is squarefree if there is no
                # facor up to its cubic root.
                self.primeseq = bigrange.range(2 + target % 2, arith1.floorpowerroot(target, 3) + 1, 2)
                p = self.find(target, **options)
                if 1 < p < target:
                    # factor found
                    tracker.register(p)
                elif p == 1:
                    # factor is not found, i.e. target is squarefree
                    tracker.register(target, True)
                    break
        except LookupError:
            # decomposition completed
            pass
        if return_list:
            return tracker.getResult()
        else:
            return tracker

    def find(self, target, **options):
        """
        Return a factor of 'target'.

        If 'target' is square, its square root is returned.
        Otherwise, it returns the minimum factor in the sequence.
        """
        sqrt = arith1.issquare(target)
        if sqrt:
            return sqrt
        # rest is the same as the base class TrialDivisionMethod
        return factor_methods.TrialDivision.find(self, target, **options)

    def issquarefree(self, n):
        """
        Return True if n is squarefree, False otherwise.

        The method uses partial factorization into squarefree parts,
        if such partial factorization is possible.  In other cases,
        It completely factor n by trial division.
        """
        if trivial_test_ternary(n):
            return True
        factorization = dict(self.factor(n, return_type='list'))
        return all(e == 1 for e in factorization.itervalues())


viadecomposition = SquarefreeDecompositionMethod().issquarefree
