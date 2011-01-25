"""
Abstract Cyclic Group structure provided module.
"""
from __future__ import division
import logging

import nzmath.integerResidueClass as integerResidueClass
import nzmath.rational as rational
import sandbox.group as group
_log = logging.getLogger('sandbox.cyclicgroup')
import nzmath.factor.methods as factor_methods


class CyclicGroup(group.AbelianGroup):
    """
    This class is for (abstract) cyclic group.
    cyclic group is abelian group.
    """
    def __init__(self, generator, order=None):
        """
        This class is abstract and cannot be instanciated.
        """
        if type(self) is CyclicGroup:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        group.AbelianGroup.__init__(self)
        self.generator = generator
        self.basegroup = generator.getGroup() # generator correctly inherited GroupElement
        self._order = order

    def DiscreteLogarithm(self, base, dist):
        """ Compute discrete logarithm on group.
        return x such that for base**x = dist .
        """
        # Note: if the order is AlephZero, do not overridden this method.
        # FIXME: Instance of 'CyclicGroup' has no '__name__' member
        raise NotImplementedError("%s is not defined" % self.__name__)

    def GroupIsomorphic(self):
        """ return isomorphic structure, Z/pZ or Z.
        """
        try:
            # FIXME: Module 'nzmath.integerResidueClass' has no 'integerResidueClassRing' member
            return integerResidueClass.integerResidueClassRing(self.order)
        except not NotImplementedError: # FIXME:
            return rational.IntegerRing()


class CyclicGroupElement(group.AbelianGroupElement):
    """
    This class is for (abstract) element of an additive group.
    """
    def __init__(self, value, generator):
        """
        This class is abstract.
        """
        # FIXME: Undefined variable 'AdditiveGroupElement'
        if type(self) is AdditiveGroupElement:
            raise NotImplementedError("class %s is abstract" % self.__class__.__name__)
        self.group = generator # assumption that generator is CyclicGroup
        self.rep = value


class MultiplicativeCyclicGroup(CyclicGroup, group.MultiplicativeGroup):
    """
    This class is for multiplicative cyclic group.
    """
    def __init__(self, generator, order=None, cyclictest=True):
        """
        This class is abstract and cannot be instanciated.
        """
        CyclicGroup.__init__(self, generator, order)
        if self._order and cyclictest:
            if self.basegroup.pow(generator, order) != self.one:
                raise ValueError("order invalid")
            self._order = order
        self._one = self.basegroup.one

    # FIXME: Undefined variable 'self'
    mul = self.basegroup.mul
    pow = self.basegroup.pow
    inverse = self.basegroup.inverse
    div = self.basegroup.div

    def __contains__(self, element):
        """
        membership test.
        This method represents set form, so you must implement this method by subclass.
        """
        try:
            dl = self.DiscreteLogarithm(self.generator, element)
            return bool(dl)
        except:
            return None

    def createElement(self, seed):
        """ create element of this group.
        seed must be integer.
        """
        try:
            return self.pow(self.generator, seed)
        except:
            if seed in self: # seem to be nonsense
                return seed
            raise ValueError("invalid seed")

    def issubgroup(self, other):
        if self == other:
            return True
        if self.basegroup == other:
            return True
        if isinstance(other, MultiplicativeCyclicGroup):
            if self.basegroup == other.basegroup and other.generator in self:
                return True
        return False

    def issupergroup(self, other):
        if self == other:
            return True
        if isinstance(other, MultiplicativeCyclicGroup):
            if self.basegroup == other.basegroup and self.generator in other:
                return True
        return False

    def DiscreteLogarithm(self, base, dist):
        """ Compute discrete logarithm on group.
        return x such that for base**x = dist .
        """

        if self.order:
            if dist == self.one:
                return self.elementOrder(base)
            # FIXME: please implement rho-method!
            index = 1
            element = base
            while element != dist:
                index += 1
                element = self.mul(element, base)
            return index
        # FIXME: Instance of 'MultiplicativeCyclicGroup' has no '__name__' member
        raise NotImplementedError("%s is not defined" % self.__name__)

    def elementOrder(self, element):
        """ Compute order of element of group.
        """
        # FIXME: Undefined variable 'grouporder'
        if self._orderfactor is None:
            self._orderfactor = factor_methods.factor(grouporder)
        order = 1
        for p, e in self._orderfactor:
            b = self.pow(element, (self.order // (p**e)))
            while b != self.one:
                order = order * p
                b = self.pow(b, p)
        return order

    @classmethod
    def getInstance(cls, generator, order):
        """
        getInstance returns an instance of the class of specified
        value.
        """
        # FIXME: Class 'MultiplicativeCyclicGroup' has no '_instances' member
        if tuple(generator, order) not in cls._instances:
            # FIXME: Undefined variable 'self'
            cls._instances[tuple(generator, order)] = self.__class__(generator, order)
        return cls._instances[tuple(generator, order)]

    # properties
    def _getOrder(self):
        "getter for order"
        if self._order:
            return self._order
        self._order = 1
        element = self.generator
        try:
            while element != self.one:
                self._order += 1
                element = self.mul(element, self.generator)
        except MemoryError:
            self._order = None # Monster or AlephZero
        return self._order

    def _getOne(self):
        "getter for multiplicative identity, called one"
        return self._one

    order = property(_getOrder, None, None, "order of group.")
    one = property(_getOne, None, None, "multiplicative unit.")
    identity = one
