"""
(programming) object for set, group, etc.
"""

import nzmath.compatibility

class MathSet:
    """
    This class is for (abstract) mathmatical set.
    For example, N,Z,Q,R should inherit this class.
    """
    def __init__(self):
        """
        abstract initialization. Define proper __init__ in subclass. 
        """
        if type(self) is MathSet:
            raise NotImplementedError

    def __contains__(self, element):
        """
        membership test.
        This method represents set form,
        so you must implement this method by subclass.
        """
        raise NotImplementedError

    def card(self):
        """
        Return cardinality.
        """
        raise NotImplementedError

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)

    def __eq__(self, other):
        """
        Equality test.
        """
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not(self == other)

    def __ge__(self, other):
        return self.issubset(other)

    def __le__(self, other):
        return self.issuperset(other)

    def __str__(self):
        return str(self.__class__.__name__)

    def __repr__(self):
        return repr(self.__class__.__name__)

    def union(self, other):
        """
        Compute union. define proper extend set.
        """
        if self in (other, set()):
            return self
        else:
            raise NotImplementedError

    def intersection(self, other):
        """
        Compute union. define proper extend set.
        """
        if self == other:
            return self
        else:
            raise NotImplementedError

    def difference(self, other):
        """
        Return set whose element are in self but not in other.
        """
        if other == set():
            return self
        else:
            return self.intersection(other.complement)

    def complement(self):
        """
        Compute complement. define proper set.
        """
        raise NotImplementedError

    def issubset(self, other):
        """
        Check whether self is subset of other.
        """
        if self == other:
            return True
        if other == set():
            return False
        else:
            return None

    def issuperset(self, other):
        """
        Check whether self is superset of other.
        """
        if self in (other, set()):
            return True
        else:
            return None

    def createElement(self, seed):
        """
        Create element with seed
        """
        return eval(self.__class__.__name__ + "Element(%s)" % str(seed))

    def randElement(self):
        """
        Create random element
        """
        raise NotImplementedError


class MathSetElement:
    """
    For set element of MathSet 
    """

    def __init__(self, ele_value):
        """
        abstract initialization. Define proper __init__ in subclass. 
        """
        if type(self) is MathSetElement:
            raise NotImplementedError
        self._initialize(ele_value)

    def _initialize(self, ele_value):
        """
        default initialization. Use this method in subclass __init__
        """
        self.ele_value = ele_value

    def __eq__(self, other):
        """
        Equality test.
        """
        if isinstance(other, self.__class__):
            return self.ele_value == other.ele_value
        else:
            try:
                return self == self.__class__(other)
            except:
                try:
                    return other == other.__class__(self)
                except:
                    return False

    def __ne__(self, other):
        return not(self == other)

    def __lt__(self, other):
        """
        Ordered set has '<' method.
        """
        raise TypeError, "no order relation"

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        return str(self.__class__.__name__ + "(%s)") % str(self.ele_value)

    def __repr__(self):
        return repr(self.__class__.__name__ + "(%s)") % repr(self.ele_value)

    def getSet(self):
        return eval(self.__class__.__name__[:-7]())


class MetaMathSet:
    """
    This class is for (abstract) meta-mathematical set.
    For example, F_p, Z/nZ, Q_p should inherit this class.
    """

    # class variable
    _instances = {}

    def __init__(self, value):
        if type(self) is MetaMathSet:
            raise NotImplementedError
        self._initialize(value)

    def _initialize(self, value):
        """
        default initialization. Use this method in subclass __init__
        """
        self.value = value
        self.__class__.getInstance(value)

    def __contains__(self, element):
        """
        membership test.
        This method represents set form,
        so you must implement this method by subclass.
        """
        raise NotImplementedError

    def card(self):
        """
        Return cardinality.
        """
        raise NotImplementedError

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)

    def __eq__(self, other):
        """
        Equality test.
        """
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other):
        return not(self == other)

    def __ge__(self, other):
        return self.issubset(other)

    def __le__(self, other):
        return self.issuperset(other)

    def __str__(self):
        return "%s(%s)" % (str(self.__class__.__name__), str(self.value))

    def __repr__(self):
        return "%s(%s)" % (repr(self.__class__.__name__), repr(self.value))

    @classmethod
    def getInstance(cls, value):
        """
        getInstance returns an instance of the class of specified
        value.
        """
        if value not in cls._instances:
            cls._instances[value] = cls(value)
        return cls._instances[value]

    def union(self, other):
        """
        Compute union. define proper extend set.
        """
        if self == other:
            if self.value == other.value:
                return self
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def intersection(self, other):
        """
        Compute union. define proper extend set.
        """
        if self == other:
            if self.value == other.value:
                return self
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def difference(self, other):
        """
        Return set whose element are in self but not in other.
        """
        return self.intersection(other.complement)

    def complement(self):
        """
        Compute complement. define proper set.
        """
        raise NotImplementedError

    def issubset(self, other):
        """
        Check whether self is subset of other.
        """
        if isinstance(other, self.__class__):
            if self.value == other.value:
                return True
            else:
                return False
        else:
            return None

    def issuperset(self, other):
        """
        Check whether self is subset of other.
        """
        if isinstance(other, self.__class__):
            if self.value == other.value:
                return True
            else:
                return False
        else:
            return None

    def createElement(self, seed):
        """
        Create element with seed
        """
        ele_class = eval(self.__class__.__name__ + "Element")
        if isinstance(seed, ele_class):
            if self.value == seed.value:
                return ele_class
            else:
                raise TypeError, "conflict value"
        else:
            return eval("ele_class(%d)" % str(self.value, seed))

    def randElement(self):
        """
        Create random element
        """
        raise NotImplementedError


class MetaMathSetElement:
    """
    For set element of MetaMathSet
    """

    def __init__(self, ele_value, value):
        if type(self) is MetaMathSetElement:
            raise NotImplementedError
        self._initialize(ele_value, value)

    def _initialize(self, ele_value, value):
        """
        default initialization. Use this method in subclass __init__
        """
        self.ele_value = ele_value
        self.value = value

    def __eq__(self, other):
        """
        Equality test.
        """
        if isinstance(other, self.__class__) and self.value == other.value:
            return self.ele_value == other.ele_value
        else:
            try:
                return self == self.__class__(other)
            except:
                try:
                    return other == other.__class__(self)
                except:
                    return False

    def __ne__(self, other):
        return not(self == other)

    def __lt__(self, other):
        """
        Ordered set has '<' method.
        """
        raise TypeError, "no order relation"

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        return str(self.__class__.__name__ + "(%s) in (%s)") % (str(self.ele_value), str(self.value))

    def __repr__(self):
        return repr(self.__class__.__name__ + "(%s) in (%s)") % (repr(self.ele_value), repr(self.value))

    def getSet(self):
        return eval(self.__class__.__name__[:-7](self.value))

class Infinity:
    """
    for (only formal) definition of infinity (as limit of big real numbers)
    (we assume we only use for cardinarity)
    """
    def __init__(self, sign=True):
        self.sign = sign
    
    def __repr__(self):
        return "Infinity"

    def __str__(self):
        return "Infinity"

    def __neg__(self):
        return self.__class__(not(self.sign))

    def __pos__(self):
        return self.__class__(self.sign)

    def __add__(self, other):
        if isinstance(other, Infinity):
            if self.sign == other.sign:
                return self.__class__(self.sign)
            else:
                raise ValueError("indetermination")
        else: #assume other is some finite number
            return self.__class__(self.sign)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Infinity):
            return self.__class__(not(self.sign ^ other.sign))
        else:
            try:
                if not(other):
                    raise ValueError("indetermination")
                other_sign = (other > -other) # other>0 ?
                self.__class__(not(self.sign ^ other_sign))

    def __div__(self, other):
        if not(other):#other == 0
            return self.__class__(self.sign) # see other is +0
        return self * other.inverse()

