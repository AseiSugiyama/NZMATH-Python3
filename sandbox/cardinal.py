"""
Cardinal numbers
"""

class Aleph(object):
    """
    Transfinite cardinal number Aleph(k).

    The cardinality of the set of all integers is Aleph(0).  Aleph(0)
    is bigger than any natural numbers (cardinality of finite sets).
    Alephs are ordered as Aleph(0) < Aleph(1) < ...
    """
    def __init__(self, index):
        """
        Define Aleph(k).
        """
        # The index k is expected to be an integer; this is not a
        # requirement, but a recomendation.  You may try
        # Aleph(Aleph(1)) etc., though I couldn't imagine real
        # applications of such cardinal number.
        if index < 0:
            raise ValueError("no negative Alephs")
        self.index = index

    def __lt__(self, other):
        if isinstance(other, Aleph):
            return self.index < other.index
        elif isinstance(other, (int, long)):
            return False
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Aleph):
            return self.index <= other.index
        elif isinstance(other, (int, long)):
            return False
        else:
            return NotImplemented

    def __eq__(self, other):
        return isinstance(other, Aleph) and self.index == other.index

    def __ne__(self, other):
        return not isinstance(other, Aleph) or self.index != other.index

    def __ge__(self, other):
        if isinstance(other, Aleph):
            return self.index >= other.index
        elif isinstance(other, (int, long)):
            return True
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Aleph):
            return self.index > other.index
        elif isinstance(other, (int, long)):
            return True
        else:
            return NotImplemented

    def __hash__(self):
        """
        hash(self) == hash(other) if self == other
        """
        return hash(Aleph) ^ hash(self.index)

    def __str__(self):
        return "Aleph" + str(self.index)

    def __repr_(self):
        return "%s(%d)" % (self.__class__.__name__, self.index)


# constant (maybe no one use other than this)
Aleph0 = Aleph(0)
