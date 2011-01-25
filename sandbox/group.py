"""
Abstract Group structure provided module.
Support Group-like Properties.
"""
from __future__ import division

import logging

import sandbox.algebraicessence as algebraicessence
from sandbox.grouplikeset import Monoid, MonoidElement

_log = logging.getLogger('sandbox.group')


class Group(Monoid):
    """
    This class is for (abstract) group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is Group:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Monoid.__init__(self)
        self.grouplikestructure_properties.setIsinvertible(True)
        self._order = None
        self._orderfactor = None

    def card(self):
        """ Return order of a group.
        Order is the number of elements in the set.
        If the order is not finite, then the group is an infinite group.
        Order is equivalent to cardinality of a group.
        """
        return self.order

    def issubgroup(self, other):
        if self == other:
            return True
        else:
            return None

    def issupergroup(self, other):
        if self == other:
            return True
        else:
            return None

    def inverse(self, element):
        """ Compute inverse of element on group.
        """
        # FIXME: Instance of 'Group' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    def elementOrder(self, element):
        """ Compute order of element of group.
        """
        # FIXME: Instance of 'Group' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    # properties
    def _getOrder(self):
        "getter for order"
        # FIXME: Instance of 'Group' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    order = property(_getOrder, None, None, "order of group.") # have to be overridden


class GroupElement(MonoidElement):
    """
    This class is for (abstract) element of group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is GroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        self.group = None
        self._order = None

    def getGroup(self):
        """
        getGroup returns an object of a subclass of group,
        to which the element belongs.
        """
        # FIXME: Instance of 'GroupElement' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    def order(self):
        """return order of element.

        order is least positive integer n such that a**n = e,
        where an is multiplication of a by itself n times
        (or other suitable composition depending on the group
        operator). If no such n exists, then the order of a
        is said to be infinity.
        """
        return self.getGroup().elementOrder(self)

    def inverse(self):
        return self.getGroup().inverse(self)


class AbelianGroup(Group):
    """
    This class is for (abstract) commutative group.
    In general, it is usually called as abelian group.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if type(self) is AbelianGroup:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Group.__init__(self)
        self.grouplikestructure_properties.setIscommutative(True)


class AbelianGroupElement(GroupElement):
    """
    This class is for (abstract) element of an abelian group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is AbelianGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)


class MultiplicativeGroup(Group, algebraicessence.MultiplicativeSet):
    """
    This class is for (abstract) multiplicative group.
    The binary operation of element is denoted '*'.
    note: The group is not supposed commutative.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if type(self) is MultiplicativeGroup:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Group.__init__(self)

    def div(self, former, after):
        """ Compute division of former and after on group.
        """
        return self.mul(former, self.inverse(after))


class MultiplicativeGroupElement(GroupElement, algebraicessence.MultiplicativeElement):
    """
    This class is for (abstract) element of an multiplicative group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is MultiplicativeGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    getGroup = algebraicessence.MultiplicativeElement.getMultiplicativeSet # have to be overridden


class AdditiveGroup(AbelianGroup, algebraicessence.AdditiveSet):
    """
    This class is for (abstract) additive group.
    The binary operation of element is denoted '+'.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if type(self) is AdditiveGroup:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        Group.__init__(self)

    def add(self, former, after):
        """ Compute addition of former and after on group.
        """
        # FIXME: Instance of 'AdditiveGroup' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    def sub(self, former, after):
        """ Compute subtraction of former and after on group.
        """
        return self.add(former, self.negative(after))

    def negative(self, element):
        """ Compute positive element. also return itself.
        """
        # FIXME: Instance of 'AdditiveGroup' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    def inverse(self, element):
        """ Compute inverse of element on group.
        """
        return self.negative(element)

    # properties
    def _getZero(self):
        "getter for additive identity, called one"
        # FIXME: Instance of 'AdditiveGroup' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    zero = property(_getZero, None, None, "additive unit.") # have to be overridden
    identity = zero # have to be overridden


class AdditiveGroupElement(GroupElement, algebraicessence.AdditiveElement):
    """
    This class is for (abstract) element of an additive group.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is AdditiveGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    def getAdditiveGroup(self):
        """
        getModule returns an object of a subclass of
        module, to which the element belongs.
        """
        # FIXME: Instance of 'AdditiveGroupElement' has no '__name__' member
        raise NotImplementedError("%s have to be overridden" % self.__name__)

    def __add__(self, other):
        return self.getAdditiveGroup().add(self, other)

    def __radd__(self, other):
        return self.getAdditiveGroup().add(other, self)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __neg__(self):
        return self.getAdditiveSet().negative(self)

    def __mul__(self, other):
        """ return scalar multiplication of element.
        """
        return self.getAdditiveSet().scalarmul(self, other)

    __rmul__ = __mul__

    def __nonzero__(self):
        if self == self.getAdditiveSet().zero:
            return True
        return False

    getGroup = algebraicessence.AdditiveElement.getAdditiveSet # have to be overridden


class Module(AdditiveGroup):
    """
    This class is for (abstract) additive group.
    The binary operation of element is denoted '+'.
    """
    def __init__(self):
        """
        This class is abstract and cannot be instanciated.
        """
        if type(self) is Module:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        AbelianGroup.__init__(self)


class ModuleElement(AdditiveGroupElement):
    """
    This class is for (abstract) element of a module.
    """
    def __init__(self):
        """
        This class is abstract.
        """
        if type(self) is ModuleElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)

    def __radd__(self, other):
        return self + other # abelian 

    getGroup = algebraicessence.AdditiveElement.getAdditiveSet # have to be overridden


#===============================================================================
# Some Useful functions for group.
#===============================================================================
def Order(self, value):
    """ Compute order of element or group.
    """
    # trick or treat
    if isinstance(value, Group):
        return value.order
    if isinstance(value, GroupElement):
        return value.order()
    raise TypeError("value is neither Group nor GroupElement.")

