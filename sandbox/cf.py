"""
cf --- continued fractions
"""

import nzmath.rational as rational
import nzmath.real as real


class RegularContinuedFraction(object):
    """
    A class of regular (or simple) continued fraction.

    [a0; a1, a2, ...]
    = a0 +     1
           ------------
            a1 +     1
                 ----------
                  a2 + ...

    A convergent pi/qi = [a0; a1, ..., ai].
    The integer part is the zeroth convergent.
    """
    def __init__(self, expansion):
        """
        ContinuedFraction(expansion) defines a number.

        expansion is an iterator generating integer series:
        [a0; a1, a2, ...]
        It can be either finite or infinite.
        """
        self._expansion = iter(expansion)
        self.numerator = 0
        self.denominator = 1
        self._numerator_old = 0
        self._denominator_old = 0
        self._counter = -1
        self._exhausted = False
        try:
            initial_term = self._expansion.next()
            self.numerator = initial_term
            self._counter = 0
        except StopIteration:
            self._exhausted = True
        if not self._exhausted:
            try:
                first_term = self._expansion.next()
                self.denominator, self._denominator_old = first_term, 1
                self.numerator, self._numerator_old = first_term * self.numerator + 1, self.numerator
                self._counter = 1
            except StopIteration:
                self._exhausted = True

    def convergent(self, atleast):
        """
        Return an n-th convergent, where n >= 'atleast' if available.
        """
        while not self._exhausted and self._counter < atleast:
            try:
                element = self._expansion.next()
            except StopIteration:
                self._exhausted = True
                break
            self.numerator, self._numerator_old = (
                element * self.numerator + self._numerator_old,
                self.numerator)
            self.denominator, self._denominator_old = (
                element * self.denominator + self._denominator_old,
                self.denominator)
            self._counter += 1
        return rational.Rational(self.numerator, self.denominator)


def expand(arational):
    """
    Return an iterator of a regular continued fraction expansion of
    given rational number.
    """
    floor = real.floor
    element = floor(arational)
    yield element
    p0, p1 = 1, element
    q0, q1 = 0, 1
    rest = arational - element
    assert 0 <= rest < 1
    while rest:
        element = floor(rest.inverse())
        yield element
        p0, p1 = p1, element * p1 + p0
        q0, q1 = q1, element * q1 + q0
        rest = rest.inverse() - element
