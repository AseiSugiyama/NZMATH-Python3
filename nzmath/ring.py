import rational

class _IntegerRing:
    def __contains__(self, element):
        reduced = +element
        if isinstance(reduced, int) or isinstance(reduced, long):
            return 1
        else:
            return 0

theIntegerRing = _IntegerRing()

class _RationalField:
    def __contains__(self, element):
        reduced = +element
        if isinstance(reduced, rational.Rational) or reduced in theIntegerRing:
            return 1
        else:
            return 0
    def classNumber(self):
        """The class number of the rational field is one."""
        return 1

theRationalField = _RationalField()
