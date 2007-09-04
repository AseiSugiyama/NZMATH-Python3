"""
Term Order for polynomials.
"""

import re
import nzmath.ring as ring


_INTERFACE_MSG = "%s is interface"

class TermOrderInterface (object):
    """
    (abstract term order)

    A term order is primalily a function, which determines precedence
    between two terms (or monomials).  By the precedence, all terms
    are ordered.

    More precisely in terms of Python, a term order accepts two tuples
    of integers, each of which represents power indeces of the term,
    and returns 0, 1 or -1 just like cmp built-in function.

    A TermOrder object provides not only the precedence function, but
    also a method to format a string for a polynomial, to tell degree,
    leading coefficients, etc.
    """
    def __init__(self, comparator):
        """
        'comparator' accepts two tuples of integers, each of which
        represents power indeces of the term, and returns 0, 1 or -1
        just like cmp built-in function.
        """
        if type(self) is TermOrderInterface:
            raise NotImplementedError(_INTERFACE_MSG % self.__class__.__name__)
        self.comparator = comparator

    def cmp(self, left, right):
        """
        Compare two indeces left and right and determine precedence by
        self.comparator.
        """
        raise NotImplementedError(_INTERFACE_MSG % self.__class__.__name__)

    def format(self, polynom, **kwds):
        """
        Return the formatted string of the polynomial.
        """
        raise NotImplementedError(_INTERFACE_MSG % self.__class__.__name__)

    def leading_coefficient(self, polynom):
        """
        Return the leading coefficient of polynomial 'polynom' with
        respect to the term order.
        """
        raise NotImplementedError(_INTERFACE_MSG % self.__class__.__name__)

    def leading_term(self, polynom):
        """
        Return the leading term of polynomial 'polynom' as tuple of
        (degree index, coefficient) with respect to the term order.
        """
        raise NotImplementedError(_INTERFACE_MSG % self.__class__.__name__)


class UnivarTermOrder (TermOrderInterface):
    """
    term order for univariate polynomials.

    One thing special to univariate case is that powers are not tuples
    but integers.
    """

    _PLUS_MINUS = re.compile(r"\+ -")

    def __init__(self, comparator):
        """
        UnivarTermOrder(comparator)

        'comparator' can be any callable that accepts two integers and
        returns 0, 1 or -1 just like cmp, i.e. if they are equal it
        returns 0, first one is greater 1, and otherwise -1.
        Theoretically acceptable comparator is only the cmp function.
        """
        TermOrderInterface.__init__(self, comparator)

    def cmp(self, left, right):
        """
        Compare two indeces left and right and determine precedence by
        self.comparator.
        """
        return self.comparator(left, right)

    def format(self, polynom, varname="X", reverse=False):
        """
        Return the formatted string of the polynomial.

        - 'polynom' must be a univariate polynomial.
        - 'varname' can be set to the name of the variable (default to
          'X').
        - 'reverse' can be either True or False. If it's True, terms
          appear in reverse (descending) order.
        """
        degrees = [base for base in polynom.iterbases()]
        degrees.sort(cmp=self.comparator)
        if reverse:
            degrees.reverse()
        str_terms = [("%s * %s ** %d" % (polynom[d], varname, d)) for d in degrees]
        # constant
        if 0 in degrees:
            str_terms[str_terms.index("%s * %s ** 0" % (polynom[0], varname))] = str(polynom[0])
        # degree 1
        if 1 in degrees:
            str_terms[str_terms.index("%s * %s ** 1" % (polynom[1], varname))] = "%s * %s" % (polynom[1], varname)
        result = " + ".join(str_terms)
        # minus terms
        result = self._PLUS_MINUS.sub("- ", result)
        # coefficient is 1 (or -1)
        one_times_x = re.compile(r"(^| )1 \* %s" % varname)
        result = one_times_x.sub(" " + varname, result)
        result = result.lstrip()
        return result

    def degree(self, polynom):
        """
        Return the degree of the polynomial 'polynom'.
        """
        if hasattr(polynom, "degree"):
            return polynom.degree()
        degree = -1
        for d in polynom.iterbases():
            if self.comparator(degree, d) < 0:
                degree = d
        return degree

    def leading_coefficient(self, polynom):
        """
        Return the leading coefficient of polynomial 'polynom' with
        respect to the term order.
        """
        if hasattr(polynom, 'leading_coefficient'):
            return polynom.leading_coefficient()
        degree, lc = -1, 0
        for d, c in polynom:
            if self.comparator(degree, d) < 0:
                degree, lc = d, c
        return lc

    def leading_term(self, polynom):
        """
        Return the leading term of polynomial 'polynom' as tuple of
        (degree, coefficient) with respect to the term order.
        """
        if hasattr(polynom, 'leading_term'):
            return polynom.leading_term()
        degree, lc = -1, 0
        for d, c in polynom:
            if self.comparator(degree, d) < 0:
                degree, lc = d, c
        return degree, lc

    def tail_degree(self, polynom):
        """
        Return the least degree among all terms of the polynomial
        'polynom'.

        This method is EXPERIMENTAL.
        """
        if hasattr(polynom, "tail_degree"):
            return polynom.tail_degree()
        degree = -1
        for d in polynom.iterbases():
            if degree == -1 or self.comparator(degree, d) > 0:
                degree = d
                if degree == 0:
                    break
        return degree


ascending_order = UnivarTermOrder(cmp)


class MultivarTermOrder (TermOrderInterface):
    """
    A class of term orders for multivariate polynomials.
    """

    _PLUS_MINUS = re.compile(r"\+ -")

    def __init__(self, comparator):
        """
        'comparator' accepts two tuples of integers, each of which
        represents power indeces of the term, and returns 0, 1 or -1
        just like cmp built-in function.
        """
        self.comparator = comparator

    def cmp(self, left, right):
        """
        Compare two indeces left and right and determine precedence by
        self.comparator.
        """
        return self.comparator(left, right)

    def format(self, polynom, varnames=None, reverse=False, **kwds):
        """
        Return the formatted string of the polynomial.

        An additional keyword argument 'varnames' is required to name
        variables.
        """
        if varnames is None:
            raise TypeError("keyword argument 'varnames' is required")

        bases = polynom.bases()
        bases.sort(cmp=self.comparator)
        if reverse:
            bases.reverse()

        result = " + ".join([self._format_term((base, polynom[base]), varnames) for base in bases if polynom[base]])
        # minus terms
        result = self._PLUS_MINUS.sub("- ", result)
        # coefficient is 1 (or -1)
        for varname in varnames:
            one_times_x = re.compile(r"(^| )1 \* %s" % varname)
            result = one_times_x.sub(" " + varname, result)
        result = result.lstrip()
        if not result:
            result = "0"
        return result

    def _format_term(self, term, varnames):
        """
        Return formatted term string.

        'term' is a tuple of indeces and coefficient.
        """
        if not term[1]:
            return ""
        if term[1] == ring.getRing(term[1]).one:
            powlist = []
        else:
            powlist = [str(term[1])]
        for v, d in zip(varnames, term[0]):
            if d > 1:
                powlist.append("%s ** %d" % (v, d))
            elif d == 1:
                powlist.append(v)

        if not powlist:
            # coefficient is one and every variable has degree 0
            return str(term[1])
        return " * ".join(powlist)

    def leading_coefficient(self, polynom):
        """
        Return the leading coefficient of polynomial 'polynom' with
        respect to the term order.
        """
        if hasattr(polynom, 'leading_coefficient'):
            return polynom.leading_coefficient()
        return polynom[self._max(polynom.bases())]

    def leading_term(self, polynom):
        """
        Return the leading term of polynomial 'polynom' as tuple of
        (degree index, coefficient) with respect to the term order.
        """
        if hasattr(polynom, 'leading_term'):
            return polynom.leading_term()
        max_indeces = self._max(polynom.bases())
        return max_indeces, polynom[max_indeces]

    def _max(self, indeces_list):
        """
        Return the maximum indeces with respect to the comparator.
        """
        if not indeces_list:
            raise ValueError("max() arg is an empty sequence")
        it = iter(indeces_list)
        maxi = it.next()
        for indeces in it:
            if self.comparator(maxi, indeces) < 0:
                maxi = indeces
        return maxi


def _total_degree_lexicographic(left, right):
    """
    Total degree lexicographic (or graded lexicographic) term order :
      L < R iff
      (1) sum(li) < sum(ri) or
      (2) sum(li) = sum(ri) and
          there exists i s.t. l0 == r0, ..., li == ri, l(i+1) < r(i+1).
    """
    sum_left, sum_right = sum(left), sum(right)
    if sum_left != sum_right:
        return cmp(sum_left, sum_right)
    return cmp(left, right)

def _total_degree_reverse_lexicographic(left, right):
    """
    Total degree reverse lexicographic (or graded reverse
    lexicographic) term order :
      L < R iff
      (1) sum(li) < sum(ri) or
      (2) sum(li) = sum(ri) and
          there exists i s.t. l0 == r0, ..., li == ri, l(i+1) > r(i+1).
    """
    sum_left, sum_right = sum(left), sum(right)
    if sum_left != sum_right:
        return cmp(sum_left, sum_right)
    return cmp(right, left)


lexicographic_order = MultivarTermOrder(cmp)
total_degree_lexicographic_order = MultivarTermOrder(_total_degree_lexicographic)
total_degree_reverse_lexicographic_order = MultivarTermOrder(_total_degree_reverse_lexicographic)
