"""
base classes for rings.
"""

from __future__ import division
from nzmath.ring import *


class ProtocolError (RuntimeError):
    """
    Violation of protocols.
    """
    pass


class RingHomomorphism (object):
    """
    RingHomomorphism is a callable object, which represents ring
    homomorphism.

    The ring homomorphism laws:
    (1) f(a + b) = f(a) + f(b)
    (2) f(a b) = f(a) f(b)
    (3) f(1) = 1
    """
    def __init__(self, dom, codom, delegation=None):
        """
        Define a RingHomomorphism from dom to codom.  If an optional
        argument delegation is specified, it will be used to define
        the homomorphism.  Otherwise, set_delegation should be called
        later.  The delegation object must be a callable object which
        sends an element of dom to an element of codom, and obey the
        ring homomorphism laws.
        """
        self.dom = dom
        self.codom = codom
        self.delegation = delegation

    def set_delegation(self, delegation):
        """
        Set delegation.  If the RingHomomorphism object already has a
        delegation, it reject to set again.
        """
        if self.delegation is None:
            self.delegation = delegation
        else:
            raise ProtocolError("delegation is already set")

    def __call__(self, domobj):
        """
        Send domobj of ring dom to ring codom by delegated method.
        """
        return self.delegation(domobj)

    def compose(self, other):
        """
        Return the composite function g*f.
        The dom of the composite function is same as the self's,
        and the codom the other's.
        """
        if self.codom != other.dom:
            raise TypeError("unable to compose")
        func = lambda x: other.delegation(self.delegation(x))
        self.__class__(self.dom, other.codom, func)
