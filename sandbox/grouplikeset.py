"""
Abstract Group-like structure provided module.
Support Group-like Properties.
"""

import logging
import sandbox.algebraicessence as algebraicessence

_log = logging.getLogger('sandbox.grouplikeset')



class GrouplikeStructureProperties (object):
    """
    boolean properties of a group-like structure.

    Each property can have one of three values; True, False, or None.
    Of cource True is true and False is false, and None means that the
    property is not set neither directly nor indirectly.
    """

    def __init__(self):
        self._isunitary = None
        self._isinvertible = None
        self._isassociative = None
        self._iscancellative = None
        self._iscommutative = None

    def isunitary(self):
        """
        Return True/False according to the unitary flag value being set,
        otherwise return None.
        """
        return self._isunitary

    def setIsunitary(self, value):
        """
        Set True/False value to the unitary flag.
        Propergation:
          False -> invertible
        """
        self._isunitary = bool(value)
        if not self._isinvertible:
            self.setIsinvartible(False)

    def isinvertible(self):
        """
        Return True/False according to the invertible flag value being
        set, otherwise return None.
        """
        return self._isinvertible

    def setIsinvertible(self, value):
        """
        Set True/False value to the invertible flag.
        Propergation:
          True -> unitary, cancellative
        """
        self._isinvertible = bool(value)
        if self._isinvertible:
            self.setIsunitary(True)
            self.setIscancellative(True)

    def isassociative(self):
        """
        Return True/False according to the assosiative flag value
        being set, otherwise return None.
        """
        return self._associative

    def setIsassociative(self, value):
        """
        Set True/False value to the assosiative flag.
        """
        self._associative = bool(value)

    def iscancellative(self):
        """
        Return True/False according to the cancellative flag value
        being set, otherwise return None.
        """
        return self._cancellative

    def setIscancellative(self, value):
        """
        Set True/False value to the cancellative flag.
        Propergation:
          False -> invertible
        """
        self._cancellative = bool(value)
        if not self._isinvertible:
            self.setIsinvartible(False)

    def iscommutative(self):
        """
        Return True/False according to the commutative flag value
        being set, otherwise return None.
        """
        return self._commutative

    def setIscommutative(self, value):
        """
        Set True/False value to the commutative flag.
        """
        self._commutative = bool(value)
        

class Magma(algebraicessence.AlgebraicSystem):
    """
    This class is for (abstract) magma.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if self.__class__ == Magma:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        self.grouplikestructure_properties = GrouplikeStructureProperties()

    def isunitary(self):
        """
        isunitary returns True if the structure has a unit,
        False if not, or None if uncertain.
        """
        return self.grouplikestructure_properties.isunitary()

    def isinvertible(self):
        """
        isinvertible returns True if the structure has inverse elememt,
        False if not, or None if uncertain.
        """
        return self.grouplikestructure_properties.isinvertible()

    def isassociative(self):
        """
        isassociative returns True if the structure has associative law,
        False if not, or None if uncertain.
        """
        return self.grouplikestructure_properties.isassociative()

    def iscancellative(self):
        """
        iscancellative returns True if the structure has cancellation law,
        False if not, or None if uncertain.
        """
        return self.grouplikestructure_properties.iscancellative()

    def iscommutative(self):
        """
        iscommutative returns True if the structure has commutativity,
        False if not, or None if uncertain.
        """
        return self.grouplikestructure_properties.iscommutative()


class MagmaElement(algebraicessence.AlgebraicSystemElement):
    """
    This class is for (abstract) element of magma.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == MagmaElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)


class SemiGroup(Magma):
    """
    This class is for (abstract) monoid.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if self.__class__ == Monoid:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Magma.__init__(self)
        self.grouplikestructure_properties.setIsassociative(True)


class SemiGroupElement(MagmaElement):
    """
    This class is for (abstract) element of monoid.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == SemiGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)


class Monoid(SemiGroup):
    """
    This class is for (abstract) monoid.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if self.__class__ == Monoid:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        SemiGroup.__init__(self)
        self.grouplikestructure_properties.setIsunitary(True)
        self._identity = None

    # properties
    def _getIdentity(self):
        "getter for identity"
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    identity = property(_getIdentity, None, None, "identity element.") # have to be overridden


class MonoidElement(SemiGroupElement):
    """
    This class is for (abstract) element of monoid.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == MonoidElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

#================================================================================
# Follows are multiplicative systems. 
# Probably required for Natural, and Ring.
#================================================================================
        
class MultiplicativeSemiGroup(SemiGroup, algebraicessence.MultiplicativeSet):
    """
    This class is for (abstract) multiplicative monoid.
    The binary operation of element is denoted '*'.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == MultiplicativeSemiGroup:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        SemiGroup.__init__(self)



class MultiplicativeSemiGroupElement(SemiGroupElement, algebraicessence.MultiplicativeElement):
    """
    This class is for (abstract) element of an multiplicative group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if self.__class__ == MultiplicativeSemiGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    getSemiGroup = algebraicessence.MultiplicativeElement.getMultiplicativeSet # have to be overridden



class MultiplicativeMonoid(Monoid, algebraicessence.MultiplicativeSet):
    """
    This class is for (abstract) multiplicative monoid.
    The binary operation of element is denoted '*'.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if self.__class__ == MultiplicativeMonoid:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Monoid.__init__(self)

    # properties
    def _getOne(self):
        "getter for multiplicative identity, called one"
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    one = property(_getOne, None, None, "multiplicative unit.") # have to be overridden
    identity = one # have to be overridden


class MultiplicativeMonoidElement(MonoidElement, algebraicessence.MultiplicativeElement):
    """
    This class is for (abstract) element of an multiplicative group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if self.__class__ == MultiplicativeMonoidElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    getMonoid = algebraicessence.MultiplicativeElement.getMultiplicativeSet # have to be overridden

