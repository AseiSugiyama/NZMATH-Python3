import sets
import rational

"""

rational functions and fields of rational functions

"""

class RationalFunctionField:
    """

    The class for rational function fields.

    """
    def __init__(self, field, vars):
        self.coefficientField = field
        if isinstance(vars, str):
            self.vars = sets.Set((vars,))
        else:
            self.vars = sets.Set(vars)

    def __str__(self):
        retval = str(self.coefficientField)
        retval += "("
        for v in self.vars:
            retval += str(v) + ", "
        retval = retval[:-2] + ")"
        return retval


    def __eq__(self, other):
        if not isinstance(other, RationalFunctionField):
            return False
        if self.coefficientField == other.coefficientField and self.vars == other.vars:
            return True
        elif isinstance(self.coefficientField, RationalFunctionField):
            return self.strip() == other
        elif isinstance(other.coefficientField, RationalFunctionField):
            return self == other.strip()
        return False

    def __contains__(self, element):
        try:
            if element.getRing().issubring(self):
                return True
        except:
            if rational.isIntegerObject(element) and rational.theIntegerRing.issubring(self):
                return True
        return False

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

    def strip(self):
        """

        if self is a nested RationalFunctionField i.e. its
        coefficientField is also a RationalFunctionField, then the
        function returns one level unnested RationalFunctionField.

        For example:
        RationalFunctionField(RationalFunctionField(Q, "x"), "y").strip()
        returns
        RationalFunctionField(Q, sets.Set(["x","y"])).

        """
        return RationalFunctionField(self.coefficientField.coefficientField, self.coefficientField.vars | self.vars)

class RationalFunction:
    """

    The class of rational functions.

    """
    def __init__(self, *arg, **kwd):
        pass
