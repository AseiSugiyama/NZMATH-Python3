"""
ternary

A module for ternary logic.
There are three logical values TRUE, FALSE and UNKNOWN.

NOT
-------
T  | F
F  | T
U  | U

OR | T   U   F
---------------
T  | T   T   T
U  | T   U   U
F  | T   U   F

AND| T   U   F
---------------
T  | T   U   F
U  | U   U   F
F  | F   F   F
"""

class TernaryValue (object):
    """
    Represent a value of Ternary Logic.

    Boolean operators are not available for the class.
    """

    _block = []

    def __init__(self, representative):
        """
        TernaryValue(representative)

        'representative' must one of True, False and None
        corresponding to TRUE, FALSE and UNKNOWN, respectively.

        There is no need to invoke the constructor for users.
        """
        if representative not in (True, False, None):
            raise ValueError("invalid initializer")
        if representative in self._block:
            raise ValueError("violate singleton constraint")
        self.value = representative
        self._block.append(self.value)

    def __nonzero__(self):
        """
        map TRUE to True, FALSE and UNKNOWN to False.
        """
        return self is TRUE

    def t_not(self):
        """
        Return negated logical value:
          not TRUE = FALSE
          not FALSE = TRUE
          not UNKNOWN = UNKNOWN
        """
        if self is TRUE:
            return FALSE
        if self is FALSE:
            return TRUE
        return UNKNOWN

    def t_or(self, other):
        """
        Return ternary or-ed logical value.
        """
        if self is TRUE or other is TRUE:
            return TRUE
        if self is FALSE and other is FALSE:
            return FALSE
        return UNKNOWN

    def t_and(self, other):
        """
        Return ternary and-ed logical value.
        """
        if self is TRUE and other is TRUE:
            return TRUE
        if self is FALSE or other is FALSE:
            return FALSE
        return UNKNOWN

    def __repr__(self):
        if self is TRUE:
            return "True"
        elif self is FALSE:
            return "False"
        else:
            return "Unknown"


TRUE = TernaryValue(True)
FALSE = TernaryValue(False)
UNKNOWN = TernaryValue(None)
