"""
Group by declaration.

Some kind of structures is treated as a group by declaring it is a group.
"""

import nzmath.factor.methods as factor_methods


class Group (object):
    """
    Declarative group class.
    """
    def __init__(self, baseset, unity, op, inv, op2, properties):
        """
        Group(baseset, unity, op, op2, properties)

        A 'baseset' is declared as a group with the operation 'op',
        the inverse function 'inv' and identity element 'unity'.  The
        argument 'op2' is a shorthand of natural action of integers.
        Another argument 'properties' is a property dictionary;
        though it is merely a reserved keyword for future extension
        """
        self.baseset = baseset
        self.unity = unity
        self.op = op
        self.inv = inv
        self.op2 = op2
        self.properties = properties

    def __contains__(self, element):
        """
        s in G
        """
        return element in self.baseset


class FiniteGroup (Group):
    """
    Declarative finite group class.
    """
    def __init__(self, baseset, unity, op, inv, op2, properties):
        """
        FiniteGroup(baseset, unity, op, op2, properties)

        A 'baseset' is declared as a finite group with the operation
        'op', the inverse function 'inv' and identity element 'unity'.
        The argument 'op2' is a shorthand of natural action of
        integers.  Another argument 'properties' is a property
        dictionary.  It should contain some hints for group order.
        """
        super(FiniteGroup, self).__init__(baseset, unity, op, inv, op2, properties)
        if 'grouporder' in self.properties:
            self.grouporder = self.properties['grouporder']
        self._orderfactor = None

    def elementorder(self, elem):
        """
        Find and return the order of the element in the group.
        """
        assert hasattr(self, grouporder), "tell me the group order!"
        if elem not in self:
            raise ValueError("%s is not in the group." % elem)
        if self._orderfactor is None:
            self._orderfactor = factor_methods.factor(self.grouporder)
        o = 1
        for p, e in self._orderfactor:
            b = self.op2(elem, self.grouporder // (p**e))
            while b != self.unity:
                o = o * p
                b = self.op2(b, p)
        return o


class AbelianGroup (Group):
    """
    Declarative abelian group class.
    """
    # You can declare something like group of units in an algebraic
    # integer ring but I don't know how much useful it is.
    
    def __init__(self, baseset, unity, op, inv, op2, properties):
        """
        AbelianGroup(baseset, unity, op, op2, properties)

        A 'baseset' is declared as an abelian group with the abelian
        operation 'op', the inverse function 'inv' and identity
        element 'unity'.  The argument 'op2' is a shorthand of natural
        action of integers.  Another argument 'properties' is a
        property dictionary; though it is merely a reserved keyword
        for future extension
        """
        super(AbelianGroup, self).__init__(baseset, unity, op, inv, op2, properties)


class FiniteAbelianGroup (FiniteGroup, AbelianGroup):
    """
    Declarative finite abelian group class.
    """
    def __init__(self, baseset, unity, op, inv, op2, properties):
        """
        FiniteAbelianGroup(baseset, unity, op, op2, properties)

        A 'baseset' is declared as an abelian group with the abelian
        operation 'op', the inverse function 'inv' and identity
        element 'unity'.  The argument 'op2' is a shorthand of natural
        action of integers.  Another argument 'properties' is a
        property dictionary.  It should contain some hints for group
        order.
        """
        super(FiniteAbelianGroup, self).__init__(baseset, unity, op, inv, op2, properties)


def declare_group(baseset, unity, op, inv, op2=None, properties=None):
    """
    Return a group wrapping the given 'baseset'.  The group
    structure is given by the operation 'op', the inverse function
    'inv' and identity element 'unity'.  The argument 'op2' can be a
    shorthand of natural action of integers.  Another argument
    'properties' can be a property dictionary;: {'abelian': True}, for
    example.
    """
    assert inv(unity) == unity
    if op2 is None:
        op2 = zaction(op, inv)
    if properties is None:
        properties = {}

    finite = properties.get('finite', False)
    abelian = properties.get('abelian', False)
    GroupDispatch = {(False, False): Group,
                     (False, True): AbelianGroup,
                     (True, False): FiniteGroup,
                     (True, True): FiniteAbelianGroup}
    return GroupDispatch[(finite, abelian)](baseset, unity, op, inv, op2, properties)


def zaction(op, inv):
    """
    Return a function
      f: (G, Z) -> G
          g, n |-> g op g op ... (n-1 times) ... op g

    If n is zero, it returns identity element.  If n is negative, it
    returns |n|-1 times op on the inverse of g.
    """
    def f(g, n):
        result = op(g, inv(g)) # identity
        if n < 0:
            g, n = inv(g), -n
        for i in range(n):
            result = op(result, g)
        return result
    return f
