"""
algebraicessence --- essencial data structure for algebraic system.
"""

_OVERRID_WARNMSG = "%s have to be overridden"

class AlgebraicSystem(object):
    """
    This class is for (abstract) algebraic set.
    """

    # Global variable
    _instances = {}
   
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == AlgebraicSystem:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    def __contains__(self, element):
        """
        membership test.
        This method represents set form, so you must implement this method by subclass.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def card(self):
        """
        Return cardinality.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __eq__(self, other):
        """
        Equality test.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return str(self.__class__.__name__+"(STRING NOT DEFINED)") #FIXME:

    def __repr__(self):
        return repr(self.__class__.__name__)

    def __hash__(self):
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)

    def union(self, other):
        """
        Compute union. define proper extend set.
        """
        if self == other:
            return self
        else:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def intersection(self, other):
        """
        Compute union. define proper extend set.
        """
        if self == other:
            return self
        else:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def difference(self, other):
        """
        Return set whose element are in self but not in other.
        """
        return self.intersection(other.complement)

    def complement(self):
        """
        Compute complement. define proper set.
        """
        if self == other:
            return None # empty set
        else:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def issubset(self, other):
        if self == other:
            return True
        else:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def issuperset(self, other):
        if self == other:
            return True
        else:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def createElement(self, seed):
        try:
            return eval(self.__class__.__name__ + "Element(%s)" % str(seed))
        except:
            raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    @classmethod
    def getInstance(cls, value):
        """
        getInstance returns an instance of the class of specified
        value.
        """
        if value not in cls._instances:
            cls._instances[value] = self.__class__(value)
        return cls._instances[value]
    # have to be overridden


class AlgebraicSystemElement(object):
    """
    This class is for (abstract) element of algebraic set.
    """
    
    # Global variable
    _instances = {}
    
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == AlgebraicSystemElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
 
    def __eq__(self, other):
        """
        Equality test.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return str(self.__class__.__name__+"(STRING NOT DEFINED)") #FIXME:

    def __repr__(self):
        return repr(self.__class__.__name__)
 
    @classmethod
    def getInstance(cls, value):
        """
        getInstance returns an instance of the class of specified
        value.
        """
        if value not in cls._instances:
            cls._instances[value] = self.__class__(value)
        return cls._instances[value]
    # have to be overridden


class MultiplicativeSet(object):
    """
    Interface of multiplication set.
    Do not instanciate.
    """

    def mul(self, former, after):
        """ Compute multiplication of former and after on set.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def pow(self, element, index):
        """ Compute index-th power of element on set.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)
    

class MultiplicativeElement(object):
    """
    Interface of multiplication element.
    Do not instanciate.
    """

    def getMultiplicativeSet(self):
        """
        returns an object of multiplicative set for computation.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __mul__(self, other):
        return self.getMulitiplicativeSet().mul(self, other)

    def __rmul__(self, other):
        return self.MulitiplicativeSet().mul(other, self)

    def __pow__(self, index):
        """  pow() with three arguments is not supported.
        """
        return self.getMulitiplicativeSet().pow(self, index)


class AdditiveSet(object):
    """
    Interface of addition set.
    Do not instanciate.
    """

    def add(self, former, after):
        """ Compute addition of former and after on group.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def positive(self, element):
        """ Compute positive element. also return itself.
        """
        return element

    def scalarmul(self, element, scalar):
        """ Compute scalar multiplication.
        """
        # FIXME: please write window method!
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)


class AdditiveElement(object):
    """
    Interface of multiplication element.
    Do not instanciate.
    """

    def getAdditiveSet(self):
        """
        getModule returns an object of a subclass of
        module, to which the element belongs.
        """
        raise NotImplementedError(_OVERRID_WARNMSG % self.__name__)

    def __add__(self, other):
        return self.getAdditiveSet().add(self, other)

    def __radd__(self, other):
        return self.getAdditiveSet().add(other, self)

    def __pos__(self):
        return self

    def __mul__(self, other):
        """ return scalar multiplication of element.
        """
        return self.getAdditiveSet().scalarmul(self, other)

    __rmul__ = __mul__


