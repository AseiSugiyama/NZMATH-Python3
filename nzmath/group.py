class Group:
    """
    This is a class for Group.
    """

    def __init__(self, value, flag=0): # 0:class_name 1:GroupElement
        self.main = 0
        if flag:
            import nzmath.ring
            self.classes = value
            if isinstance(self.classes, nzmath.ring.RingElement):
                self.classes = self.classes.getRing()
            """
            else:
                if isinstance(a, == nzmath.group.GroupElement)
                    self.classes = self.classes.getGroup()
            """
        else:
            self.classes = value

    def __repr__(self):
        if (hasattr(self.classes, "__repr__")):
            return self.classes.__repr__()
        else:
            return repr(self.classes.__class__.__name__)

    def __str__(self):
        if (hasattr(self.classes, "__str__")):
            return self.classes.__str__()
        else:
            return str(self.classes.__class__.__name__)

    def setmain(self, value):
        if isinstance(value, int) :
            self.main = (value & 1)
        else:
            return ValueError("invalid input")

    def createElement(self, value):
        return GroupElement(self.classes.createElement(value))

    def identify(self):
        if hasattr(self.classes, "identify"):
            return GroupElement(self.classes.identify())
        else:
            if self.main:
                if hasattr(self.classes, "_getOne"):
                    return GroupElement(self.classes._getOne(), 1)
            else:
                if hasattr(self.classes, "_getZero"):
                    return GroupElement(self.classes._getZero(), 0)
        return -1

    def grouporder(self):
        order = 0
        if hasattr(self.classes, "grouporder"):
            order = self.classes.grouporder()
        else:
            if hasattr(self.classes, "__len__"):
                order = self.classes.__len__()
        if self.main & hasattr(self.classes, "_getZero"): # *-cyclic group
            order = order - 1
        return order

    def gr_order_fact(self):
        import nzmath.factor.methods as facts
        return facts.factor(self.grouporder())

    """
    def homomorphism(self):
        return 0
    """


class GroupElement:
    """
    This is for Group (especially,Abelian) Element.
    """

    def __init__(self, value, opes = -1):
        self.element = value
        if opes == -1:
            if self.type_check(1):
                self.main = 1
            if self.type_check(0):
                self.main = 0
        else:
            self.main = opes # mainly operation
        self.classes = Group(self.element, 1)
        self.class_name = self.classes.classes.__class__.__name__
        self.classes.setmain(self.main)

    def __repr__(self):
        return self.class_name + ',' + repr(self.element)

    def __str__(self):
        return self.class_name + ',' + str(self.element)

    def __eq__(self,other):
        if(self.element == other.element):
            return True
        else:
            return False

    def __ne__(self, other):
        return not(self == other)

    def type_check(self, value):
        a=self.element
        if not(value & 1):
            if hasattr(a, "__add__") & hasattr(a, "__mul__"):
                return True
            else:
                return False
        else:
            if hasattr(a, "__mul__") & hasattr(a, "__pow__"):
                return True
            else:
                return False

    def setmain(self, value):
        value = value & 1
        if isinstance(value, int) & self.type_check(value):
            self.main = value
        else:
            return ValueError("invalid input")
        self.classes.setmain(self.main)

    def ope(self, other):
        if  not self.main:
            if  other.type_check(0):
                return GroupElement(self.element + other.element, self.main)
            else:
                return TypeError("don't have add operation")
        else:
            if  other.type_check(1):
                return GroupElement(self.element * other.element, self.main)
            else:
                return TypeError("don't have mul operation")

    def ope2(self, other):
        if isinstance(other, (int, long)):
            if not self.main:
                if self.type_check(0):
                    return GroupElement(self.element * other, self.main)
                else:
                    return TypeError("don't have mul operation")
            else:
                if self.type_check(1):
                    return GroupElement(self.element ** other, self.main)
                else:
                    return TypeError("don't have pow operation")
        else:
            return ValueError("input integer")

    def order(self):
        if hasattr(self.classes.classes, "_getZero"):
            if self.element == self.classes.classes._getZero():
                return 1
        ord = self.classes.grouporder()
        ordfact = self.classes.gr_order_fact()
        k = 1
        for p, e in ordfact:
            b = self.ope2(ord // (p ** e))
            while b != self.classes.identify():
                k = k * p
                b = b.ope2(p)
        return k


