import nzmath.rational as rational
import nzmath.factor.methods as facts

class Group:
    """
    This is a class for finite group.
    """

    def __init__(self, value, flag=0): # 0:group_instance 1:GroupElement
        self.main = 0
        if flag:
            import nzmath.ring
            self.classes = value
            if isinstance(self.classes, nzmath.ring.RingElement):
                self.classes = self.classes.getRing()
        else:
            self.classes = value

    def __repr__(self):
        if hasattr(self.classes, "__repr__"):
            return self.classes.__repr__()
        else:
            return repr(self.classes.__class__.__name__)

    def __str__(self):
        if hasattr(self.classes, "__str__"):
            return self.classes.__str__()
        else:
            return str(self.classes.__class__.__name__)

    def setmain(self, value):
        """
        Change group type for additive(0) or multiplicative(1).
        """
        if isinstance(value, int) :
            self.main = (value and 1)
        else:
            return TypeError("invalid input")

    def createElement(self, value):
        """
        Create group element with value.
        Return GroupElement instance.
        """
        return GroupElement(self.classes.createElement(value))

    def identity(self):
        """
        Return identity element(unit).
        Return addtive 0 or multiplicative 1.
        """
        if hasattr(self.classes, "identity"):
            return GroupElement(self.classes.identity())
        else:
            if self.main:
                return GroupElement(self.classes.one, 1)
            else:
                return GroupElement(self.classes.zero, 0)

    def grouporder(self):
        """
        Return group order(Cardinality).
        """
        order = 0
        if hasattr(self.classes, "grouporder"):
            order = self.classes.grouporder()
        else:
            if hasattr(self.classes, "__len__"):
                order = self.classes.__len__()
        if self.main and hasattr(self.classes, "zero"): # *-cyclic group
            order = order - 1
        return order

    def gr_order_fact(self):
        return facts.factor(self.grouporder())


class GroupElement:
    """
    This is a class for finite group element.
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
        if self.element == other.element:
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def type_check(self, value):
        """
        Check group type is value or not.
        """
        a=self.element
        if not (value and 1):
            if hasattr(a, "__add__") and hasattr(a, "__mul__"):
                return True
            else:
                return False
        else:
            if hasattr(a, "__mul__") and hasattr(a, "__pow__"):
                return True
            else:
                return False

    def setmain(self, value):
        """
        Change group type for additive(0) or multiplicative(1).
        """
        value = value and 1
        if isinstance(value, int) and self.type_check(value):
            self.main = value
        else:
            return TypeError("invalid input")
        self.classes.setmain(self.main)

    def ope(self, other):
        """
        Group basic operation.
        """
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
        """
        Group extended operation
        """
        if rational.isIntegerObject(other):
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
            return TypeError("input integer")

    def order(self):
        """
        Compute order using grouporder factorization.
        """
        if hasattr(self.classes.classes, "zero"):
            if self.element == self.classes.classes.zero:
                return 1
        ord = self.classes.grouporder()
        ordfact = self.classes.gr_order_fact()
        k = 1
        for p, e in ordfact:
            b = self.ope2(ord // (p ** e))
            while b != self.classes.identity():
                k = k * p
                b = b.ope2(p)
        return k

    def t_order(self, v=2):
        """
        Compute order using Terr's Baby-step Giant-step algorithm
        """
        if v < 1 or not(rational.isIntegerObject(v)):
            return TypeError("input integer v>=1")
        e = self.classes.identity()
        a = self.classes.identity()
        R = [(e, 0)]
        for i in range(1, v + 1):
            a = self.ope(a)
            if a == e:
                return i
            else:
                R.append((a, i))
        j = 0
        b = a.ope2(2)
        t = 2 * v
        while(1):
            for (c, k) in R:
                if b == c:
                    return (t - k)
            a = self.ope(a)
            j += 1
            R.append((a, j + v))
            b = a.ope(b)
            t += j + v
