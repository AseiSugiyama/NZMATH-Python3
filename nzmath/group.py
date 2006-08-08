"""
Group Theorical module
"""
import math
import nzmath.rational as rational
import nzmath.factor.methods as facts
import nzmath.vector as vector
import nzmath.matrix as matrix

class Group:
    """
    This is a class for finite group.
    """

    def __init__(self, value, main=-1):
        if isinstance(value, Group):
            self.classes = value.classes
            if main == -1:
                self.main = value.main
            else:
                self.setmain(main)
        else:
            self.classes = value
            if main == -1:
                self.setmain(0)
            else:
                self.setmain(main)

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

    def __eq__(self, other):
        if self.classes == other.classes and self.main == other.main:
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def setmain(self, value):
        """
        Change group type for additive(0) or multiplicative(1).
        """
        if isinstance(value, int) :
            self.main = (value & 1)
        else:
            raise TypeError("invalid input")

    def createElement(self, value):
        """
        Create group element with value.
        Return GroupElement instance.
        """
        return GroupElement(self.classes.createElement(value), self.main)

    def identity(self):
        """
        Return identity element(unit).
        Return addtive 0 or multiplicative 1.
        """
        if hasattr(self.classes, "identity"):
            return GroupElement(self.classes.identity(), self.main)
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
        elif hasattr(self.classes, "__len__"):
            order = len(self.classes)
        else:
            order = self.classes.m
        if self.main and hasattr(self.classes, "zero"): # *-cyclic group
            order -= 1
        return order


class GroupElement:
    """
    This is a class for finite group element.
    """

    def __init__(self, value, main=-1):
        self.main = main
        if isinstance(value, GroupElement):
            self.element = value.element
            self.classes = value.classes
            self.class_name = value.class_name
            if main == -1:
                self.main = value.main
            else:
                self.setmain(main)
        else:
            self.element = value
            if main == -1:
                if self.type_check(1):
                    self.main = 1
                if self.type_check(0):
                    self.main = 0
                if self.main == -1:
                    raise TypeError("This element isn't Group")
            self.classes = self.getGroup()
            self.setmain(self.main) # mainly operation
            self.class_name = self.classes.classes.__class__.__name__

    def __repr__(self):
        return self.class_name + ',' + repr(self.element)

    def __str__(self):
        return self.class_name + ',' + str(self.element)

    def __eq__(self, other):
        if self.element == other.element and self.main == other.main:
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
        if not (value & 1):
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
        if isinstance(value, int) and self.type_check(value):
            self.main = (value & 1)
        else:
            raise TypeError("invalid input")
        self.classes.setmain(self.main)

    def ope(self, other):
        """
        Group basic operation.
        """
        if  not self.main:
            return GroupElement(self.element + other.element, self.main)
        else:
            return GroupElement(self.element * other.element, self.main)

    def ope2(self, other):
        """
        Group extended operation
        """
        if rational.isIntegerObject(other):
            if not self.main:
                return GroupElement(self.element * other, self.main)
            else:
                return GroupElement(self.element ** other, self.main)
        else:
            raise TypeError("input integer")

    def inverse(self):
        """
        Return inverse element.
        """
        ele = self.element
        cla = self.classes
        main = self.main
        if hasattr(cla.classes, "zero") and (ele == cla.classes.zero):
            return self
        else:
            if not main:
                return GroupElement(-ele, main)
            elif hasattr(ele, "inverse"):
                return GroupElement(ele.inverse(), main)
            else:
                return GroupElement(self.ope2(cla.order() - 1), main)

    def order(self):
        """
        Compute order using grouporder factorization.
        """
        clas = self.classes.classes
        if hasattr(clas, "zero") and self.element == clas.zero:
            return 1
        ord = self.classes.grouporder()
        ordfact = facts.factor(ord)
        identity = self.classes.identity()
        k = 1
        for p, e in ordfact:
            b = self.ope2(ord // (p ** e))
            while b != identity:
                k = k * p
                b = b.ope2(p)
        return k

    def t_order(self, v=2):
        """
        Compute order using Terr's Baby-step Giant-step algorithm.
        """
        if (v < 1) or not(rational.isIntegerObject(v)):
            raise TypeError("input integer v >= 1")
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
        while True:
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
            if hasattr(self.element, "getRing"):
                return Group(self.element.getRing(), self.main)
            else:
                return Group(self.element, self.main)
        else:
            if hasattr(self.element, "getGroup"):
                return Group(self.element.getGroup(), self.main)
            else:
                return Group(self.element, self.main)


class GenerateGroup(Group):
    """
    This is a class for finite group with generator.
    """

    def __init__(self, value, main=-1):
        if isinstance(value, list):
            temp = value
            self.classes = GroupElement(value[0]).classes.classes
        elif isinstance(value, tuple): # (generator, class_name)
            temp = value[0]
            self.classes = value[1]
        else:
            TypeError("invalid input")
        self.generator = []
        for a in temp:
            self.generator.append(GroupElement(a))
        if main == -1:
            self.main = self.generator[0].main
        else:
            self.setmain(main)

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
            self.main = (value & 1)
        else:
            raise TypeError("invalid input")
        for a in self.generator:
            a.setmain(value)


class AbelianGenerate(GenerateGroup):
    """
    This is a class for finite abelian group with genarator.
    """

    def relationLattice(self):
        """
        Return relation lattice basis as column vector matrix for generator.
        If B[j]=transpose(b[1,j],b[2,j],..,b[l,j]),
        it satisfies that product(generator[i]**b[i,j])=1 for each j.
        """
        l = len(self.generator)
        b = matrix.IntegerSquareMatrix(l)
        H1 = [(self.identity(), vector.Vector([0] * l))]
        H2 = list(H1)
        m = 1
        a_baby_s, giant_s = list(H1), list(H2)
        pro_I1, pro_I2, pro_diag = 1, 1, 1
        e_vec = []
        g_gen = []
        for i in range(1, l + 1):
            e_i = vector.Vector([0] * l)
            e_i[i] = 1
            e_vec.append(e_i)
            g_gen.append(self.generator[i - 1])
        for j in range(1, l + 1):
            e = 1
            baby_s = list(a_baby_s)
            baby_e = GroupElement(g_gen[j - 1])
            giant_e = GroupElement(g_gen[j - 1])
            flag = False
            while not flag:
                for (g_g, v) in giant_s:
                    for (g_b, w) in baby_s:
                        if g_g.ope(giant_e) == g_b:
                            b[j] = v + w + (e * (e + 1) // 2) * e_vec[j - 1]
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    break
                for (g_a, v_a) in a_baby_s:
                    baby_s.append((g_a.ope(baby_e), v_a - e * e_vec[j - 1]))
                e += 1
                baby_e = baby_e.ope(g_gen[j - 1])
                giant_e = giant_e.ope(baby_e)
            if (j < l) and (b[j, j] > 1):
                pro_diag *= b[j, j]
                pro_diag_root = math.sqrt(pro_diag)
                if (b[j, j] * pro_I1) <= pro_diag_root or j == 1:
                    temp = list(H1)
                    for (g, v) in temp:
                        g_j_inv = g_gen[j - 1].inverse()
                        H1_1 = GroupElement(g)
                        for x in range(1, b[j, j]):
                            H1_1 = H1_1.ope(g_j_inv)
                            H1.append((H1_1, v + x * e_vec[j - 1]))
                    pro_I1 *= b[j, j]
                else:
                    if m > 1:
                        temp = list(H2)
                        for (g, v) in temp:
                            H2_1 = GroupElement(g)
                            for x in range(1, b[m, m]):
                                H2_1 = H2_1.ope(g_gen[m - 1])
                                H2.append((H2_1, v + x * e_vec[m - 1]))
                        pro_I2 *= b[m, m]
                    m = j
                s = int(math.ceil(pro_diag_root / pro_I1))
                if len(H2) > 1:
                    t = int(math.ceil(pro_diag_root / pro_I2))
                else:
                    t = 1
                a_baby_s, giant_s = list(H1), list(H2)
                g_m_inv = g_gen[m - 1].inverse()
                for (h1, v) in H1:
                    H1_1 = GroupElement(h1)
                    for r in range(1, s):
                        H1_1 = H1_1.ope(g_m_inv)
                        a_baby_s.append((H1_1, v + r * e_vec[m - 1]))
                g_m_s = g_gen[m - 1].ope2(s)
                for (h2, v) in H2:
                    H2_1 = GroupElement(h2)
                    for q in range(1, t):
                        H2_1 = H2_1.ope(g_m_s)
                        giant_s.append((H2_1, v + (q * s) * e_vec[m - 1]))
        return b

    def computeStructure(self):
        """
        Compute Finite Abelian Group Structure.
        """
        B = self.relationLattice()
        U_d, V, M = B.extsmithNormalForm()
        det = int(M.determinant())
        U = U_d.inverse()
        for i in range(U_d.row):
            U_d[i] = (U_d[i] % det)
        structure = []
        l = M.row
        for j in range(1, l):
            if M[j, j] != 1 or j == 1:
                g = self.identity()
                for i in range(1, l+1):
                    g = g.ope(self.generator[i-1].ope2(int(U[i, j])))
                structure.append((g, M[j, j]))
            else:
                break
        return structure, det
