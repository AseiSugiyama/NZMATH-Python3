"""
rational functions and fields of rational functions
"""
import warnings
import nzmath.rational as rational
import nzmath.ring as ring
import nzmath.polynomial as polynomial
import nzmath.compatibility


warnings.warn(DeprecationWarning("use poly.ratfunc instead"))


class RationalFunctionField (ring.QuotientField):
    """
    The class for rational function fields.
    """

    def __init__(self, field, vars):
        if isinstance(field, ring.QuotientField):
            ring.QuotientField.__init__(self, polynomial.PolynomialRing(field.basedomain, vars))
        else:
            ring.QuotientField.__init__(self, polynomial.PolynomialRing(field, vars))
        self.coefficientField = field
        if isinstance(vars, str):
            self.vars = set((vars,))
        else:
            self.vars = set(vars)

    def __str__(self):
        retval = str(self.coefficientField)
        retval += "("
        retval += ", ".join([str(v) for v in self.vars])
        retval += ")"
        return retval

    def __eq__(self, other):
        if not isinstance(other, RationalFunctionField):
            return False
        if self.coefficientField == other.coefficientField and self.vars == other.vars:
            return True
        elif isinstance(self.coefficientField, RationalFunctionField):
            return self.unnest() == other
        elif isinstance(other.coefficientField, RationalFunctionField):
            return self == other.unnest()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, element):
        if ring.getRing(element).issubring(self):
            return True
        return False

    def __hash__(self):
        return hash(self.coefficientField) ^ hash(repr(self.vars))

    def getQuotientField(self):
        return self

    def issubring(self, other):
        if isinstance(other, RationalFunctionField) and self.vars.issubset(other.vars):
            return True
        return False

    def issuperring(self, other):
        if isinstance(other, RationalFunctionField) and self.vars.issuperset(other.vars):
            return True
        elif self.coefficientField.issuperring(other):
            return True
        else:
            try:
                if self.issuperring(other.getQuotientField()):
                    return True
            except:
                pass
        return False

    def createElement(self, *seedarg, **seedkwd):
        return RationalFunction(*seedarg, **seedkwd)

    def getCharacteristic(self):
        """
        The characteristic of a rational function field is same as of
        its coefficient field.
        """
        return self.coefficientField.getCharacteristic()

    def unnest(self):
        """

        if self is a nested RationalFunctionField i.e. its
        coefficientField is also a RationalFunctionField, then the
        function returns one level unnested RationalFunctionField.

        For example:
        RationalFunctionField(RationalFunctionField(Q, "x"), "y").unnest()
        returns
        RationalFunctionField(Q, set(["x","y"])).

        """
        return RationalFunctionField(self.coefficientField.coefficientField, self.coefficientField.vars | self.vars)

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = RationalFunction(1)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = RationalFunction(0)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")


class RationalFunction (ring.QuotientFieldElement):
    """
    The class of rational functions.
    """
    def __init__(self, *arg, **kwd):
        if len(arg) == 1:
            if isinstance(arg[0], RationalFunction):
                self.numerator = arg[0].numerator
                self.denominator = arg[0].denominator
            else:
                self.numerator = arg[0]
                if "denominator" in kwd:
                    self.denominator = kwd["denominator"]
                else:
                    self.denominator = rational.Integer(1)
        elif len(arg) == 2:
            self.numerator = arg[0]
            self.denominator = arg[1]
        elif len(kwd) > 0:
            try:
                self.numerator = kwd["numerator"]
            except:
                raise ValueError("numerator must be specified.")
            try:
                self.denominator = kwd["denominator"]
            except:
                self.denominator = rational.Integer(1)
        else:
            raise ValueError("numerator must be specified.")

    def __eq__(self, other):
        try:
            return self.numerator * other.denominator == other.numerator * self.denominator
        except:
            return NotImplemented

    def getRing(self):
        if hasattr(self.numerator, "getVariableList"):
            nvars = self.numerator.getVariableList()
            if len(nvars) > 1:
                nring = self.numerator.getCoefficientRing(nvars)
            else:
                nring = self.numerator.getCoefficientRing()
        else:
            nvars = []
            nring = ring.getRing(self.numerator)
        if hasattr(self.denominator, "getVariableList"):
            total_vars = set(nvars + self.denominator.getVariableList())
        else:
            total_vars = set(nvars)
        if nring.isfield():
            return RationalFunctionField(nring, total_vars)
        else:
            return RationalFunctionField(nring.getQuotientField(), total_vars)
