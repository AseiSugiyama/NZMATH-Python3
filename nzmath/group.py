"""
Group Theorical module
"""

import nzmath.rational as rational
import nzmath.factor.methods as facts


class Group:
    """
    This is a class for finite group.
    """

    def __init__(self, value, main=0):
        self.main = (main and 1)
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
                order = len(self.classes)
        if self.main and hasattr(self.classes, "zero"): # *-cyclic group
            order = order - 1
        return order

    def gr_order_fact(self):
        return facts.factor(self.grouporder())


class GroupElement:
    """
    This is a class for finite group element.
    """

    def __init__(self, value, opes=-1):
        self.element = value
        if opes == -1:
            if self.type_check(1):
                self.main = 1
            if self.type_check(0):
                self.main = 0
        else:
            self.main = opes # mainly operation
        self.classes = self.getGroup()
        self.class_name = self.classes.classes.__class__.__name__
        self.classes.setmain(self.main)

    def __repr__(self):
        return self.class_name + ',' + repr(self.element)

    def __str__(self):
        return self.class_name + ',' + str(self.element)

    def __eq__(self, other):
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
        a = self.element
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
        value = (value and 1)
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

    def inverse(self):
        """
        Return inverse element.
        """
        a = self.element
        if hasattr(self.classes.classes, "zero") and (self.element ==
        self.classes.classes.zero):
                return self
        else:
            if not(self.main):
                return GroupElement(-self.element, self.main)
            elif hasattr(a, "inverse"):
                return GroupElement(self.element.inverse(), self.main)
            else:
                return
        GroupElement(self.ope2(self.classes.grouporder() - 1), self.main)

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
        Compute order using Terr's Baby-step Giant-step algorithm.
        """
        if (v < 1) or not(rational.isIntegerObject(v)):
            return TypeError("input integer v >= 1")
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

    def getGroup(self):
        """
        Return the group which element belongs.
        """
        if self.type_check(0) and self.type_check(1):
            import nzmath.ring as ring
            if isinstance(self.element, ring.RingElement):
                return Group(self.element.getRing())
            else:
                return Group(self.element)
        else:
            if hasattr(self.element, "getGroup"):
                return Group(self.element.getGroup())
            else:
                return Group(self.element)


class GenerateGroup(Group):
    """
    This is a class for finite group with generator.
    """

    def __init__(self, generator, classes=-1):
        if isinstance(generator, list):
            self.generator = []
            for a in generator:
                self.generator.append(GroupElement(a))
        else:
            return TypeError("input generator list")
        if classes == -1:
            gr = generator[0].getGroup()
        else:
            gr = Group(classes)
        self.classes, self.main = gr.classes, gr.main

    def isGroupElement(self, other):
        """
        Check whether other is self group element or not.
        """
        pass

    def setmain(self, value):
        """
        Change group type for additive(0) or multiplicative(1).
        """
        if isinstance(value, int) :
            self.main = (value and 1)
        else:
            return TypeError("invalid input")
        for a in self.generator:
            a.setmain(value)


class AbelianGenerate(GenerateGroup):
    """
    This is a class for finite abelian group with genarator.
    """

    def relation_lattice(self):
        """
        Return relation lattice basis as column vector matrix for generator.
        If B[j]=transpose(b[1,j],b[2,j],..,b[l,j]),
        it satisfies that product(generator[i]**b[i,j])=1 for each j.
        """
        import nzmath.vector as vector
        import nzmath.matrix as matrix
        import math
        l = len(self.generator)
        b = matrix.SquareMatrix(l)
        H1 = [(self.identity(), vector.Vector([0] * l))]
        H2 = list(H1)
        I1, I2 = [], []
        s, t, m = 0, 0, 0
        a_baby_s, giant_s = list(H1), list(H2)
        for j in range(1, l + 1):
            e = 1
            g_j = self.generator[j - 1]
            baby_s = list(a_baby_s)
            baby_e = GroupElement(g_j.element, g_j.main)
            giant_e = GroupElement(g_j.element, g_j.main)
            e_j = vector.Vector([0] * l)
            e_j[j] = 1
            flag = False
            while(True):
                for (g, v) in giant_s:
                    for (gg, w) in baby_s:
                        if g.ope(giant_e) == gg:
                            b[j] = v + w + (e * (e + 1) // 2) * e_j
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    break
                for (g_d, v_d) in a_baby_s:
                    baby_s.append((g_d.ope(baby_e), v_d - e * e_j))
                e += 1
                baby_e = baby_e.ope(g_j)
                giant_e = giant_e.ope(baby_e)
            if (j < l) and (b[j, j] > 1):
                pro_I1, pro_diag = 1, 1
                for i in I1:
                    pro_I1 *= b[i, i]
                for i in range(1, j + 1):
                    pro_diag *= b[i, i]
                pro_diag = math.sqrt(pro_diag)
                if I1 == []:
                    pro_I1_2 = 0
                else:
                    pro_I1_2 = pro_I1
                if (b[j, j] * pro_I1_2) <= pro_diag:
                    temp = list(H1)
                    for (g, v) in temp:
                        H1_1 = GroupElement(g.element, g.main)
                        g_j_inv = g_j.inverse()
                        for x in range(b[j, j]):
                            H1.append((H1_1, v + x * e_j))
                            H1_1 = H1_1.ope(g_j_inv)
                    I1.append(j)
                else:
                    if m > 0:
                        temp = list(H2)
                        g_m = self.generator[m - 1]
                        e_m = vector.Vector([0] * l)
                        e_m[m] = 1
                        for (g, v) in temp:
                            H2_1 = GroupElement(g.element, g.main)
                            for x in range(b[m, m]):
                                H2.append((H2_1, v + x * e_m))
                                H2_1 = H2_1.ope(g_m)
                        I2.append(m)
                    m = j
                pro_I2 = 1
                for i in I2:
                    pro_I2 *= b[i, i]
                s = int(math.ceil(float(pro_diag) / pro_I1))
                t = int(math.ceil(float(pro_diag) / pro_I2))
                a_baby_s, g_s = [], []
                g_m = self.generator[m - 1]
                e_m = vector.Vector([0] * l)
                e_m[m] = 1
                g_m_inv = g_m.inverse()
                for (h1, v) in H1:
                    H1_1 = GroupElement(h1.element, h1.main)
                    for r in range(s):
                        a_baby_s.append((H1_1, v + r * e_m))
                        H1_1 = H1_1.ope(g_m_inv)
                g_m_s = g_m.ope2(s)
                for (h2, v) in H2:
                    H2_1 = GroupElement(h2.element, h2.main)
                    for q in range(t):
                        a_baby_s.append((H2_1, v + (q * s) * e_m))
                        H2_1 = H2_1.ope(g_m_s)
        return b

    def computeStructure(self):
        """
        Compute Finite Abelian Group Structure.
        """
        pass
