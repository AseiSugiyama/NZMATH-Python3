from __future__ import division

import math
import nzmath.arith1 as arith1
import nzmath.equation as equation
import nzmath.gcd as gcd
import nzmath.lattice as lattice 
import nzmath.matrix as matrix
import nzmath.factor.misc as misc
import nzmath.poly.uniutil as uniutil
import nzmath.poly.multiutil as multiutil
import nzmath.rational as rational
import nzmath.ring as ring
import nzmath.squarefree as squarefree
import nzmath.round2 as round2


class NumberField (ring.Field):
    """
<<<<<<< local
    A class of number field.
=======
    The class for number field.
>>>>>>> other
    """
    def __init__(self, polynomial):
        """
        Initialize a number field with given polynomial coefficients
        (in ascending order).
        """
        ring.Field.__init__(self)
        self.polynomial = polynomial
        self.degree = len(polynomial) - 1

    def __repr__(self):
        return_str = '%s(%s)' % (self.__class__.__name__, self.polynomial)
        return return_str

    def __mul__(self, other):
        """
        Output composite field of self and other.
        """
        common_options = {"coeffring": rational.theIntegerRing,
                          "number_of_variables": 2}
        flist = [((d, 0), c) for (d, c) in enumerate(self.polynomial)]
        f = multiutil.polynomial(flist, **common_options)
        g = zpoly(other.polynomial)
        diff = multiutil.polynomial({(1, 0): 1, (0, 1):-1}, **common_options)
        compos = f.resultant(g(diff), 0)
        return NumberField([compos[i] for i in range(compos.degree() + 1)])

    def disc(self):
        """
        Compute the discriminant of self.
        However the output is not disc of self but disc of self.polynomial.
        """
        degree = self.degree

        def theta(j, K):
            base = [0] * K.degree
            base[j] = 1
            return BasicAlgNumber([base, 1], K.polynomial)

        traces = []
        for i in range(degree):
            for j in range(degree):
                s = theta(i, self)*theta(j, self)
                traces.append(s.trace())

<<<<<<< local
        M = matrix.RingSquareMatrix(degree, degree, traces)
        return M.determinant()
=======
        M = matrix.SquareMatrix(degree, degree, list)
        D = M.determinant()
        return D
>>>>>>> other

    def signature(self):
        """
        Using Strum's algorithm, compute the signature of self.
        Algorithm 4.1.11 in Cohen's Book
        """
        degree = self.degree
        #Step 1.
        if degree == 0:
            return (0, 0)
        # no check for degree 1?

        minpoly = zpoly(self.polynomial)
        d_minpoly = minpoly.differentiate()
        A = minpoly.primitive_part()
        B = d_minpoly.primitive_part()
        g = 1
        h = 1
        pos_at_inf = A.leading_coefficient() > 0
        pos_at_neg = pos_at_inf == (degree % 2)
        r_1 = 1

        #Step 2.
        while True:
            deg = A.degree() - B.degree()
            residue = A.pseudo_mod(B)
            if not residue:
                raise ValueError("not squarefree")
            if B.leading_coefficient() > 0 or deg % 2:
                residue = - residue
            #Step 3.
            degree_res = residue.degree()
            pos_at_inf_of_res = residue.leading_coefficient() > 0

            if pos_at_inf_of_res != pos_at_inf:
                pos_at_inf = not pos_at_inf
                r_1 -= 1

            if pos_at_inf_of_res != (pos_at_neg == (degree_res % 2 == 0)):
                pos_at_neg = not pos_at_neg
                r_1 += 1

            #Step 4.
            if degree_res == 0:
                return (r_1, (degree - r_1)//2)

            A, B = B, residue.scalar_exact_division(g*(h**deg))
            g = abs(A.leading_coefficient())
            if deg == 1:
                h = g
            elif deg > 1:
                h = g**deg // h**(deg - 1)

    def POLRED(self):
        """
        Given a polynomial f i.e. a field self, output some polynomials
        defining subfield of self, where self is a field defined by f.
        Algorithm 4.4.11 in Cohen's book.
        """
        n = self.degree
        appr = equation.SimMethod(self.polynomial)

        #Step 1.
        # Using the round 2 method, compute an integral basis.
        Basis, disc = round2.round2(self.polynomial)
        BaseList = []
        for i in range(n):
            AlgInt = MatAlgNumber(Basis[i], self.polynomial)
            BaseList.append(AlgInt)
        
        #Step 2.
<<<<<<< local
        traces = []
        if self.signature()[1] == 0:
=======
        flag = 1
        while flag == 1:
            deg = A.degree() - B.degree()
            pseudo = polynomial.pseudoDivision(A, B)
            Q = pseudo[0]
            R = pseudo[1]
            if R == 0:
                raise ValueError
            else:
                if B.leadingCoefficient() > 0 or deg%2 == 1:
                    R = - R
            #Step 3.
            degree_R = R.degree()
            if R.leadingCoefficient() > 0:
                sign_R = 1
            else:
                sign_R = - 1

            if sign_R != s:
                s = - s
                r_1 = r_1 - 1

            if sign_R != ((-1)**degree_R)*t:
                t = - t
                r_1 = r_1 + 1

            #Step 4.
            if degree_R == 0:
                return (r_1, (n - r_1)/2)
            else:
                A = B
                B = R/(g*(h**deg))
                g = abs(A.leadingCoefficient())
                h = (h**(1-deg))*(g**deg)
                flag = 1

    def pow_sum(K, k):
        """
        Compute the sum of roots k-th powring of the field K.
        Prop4.3.3 in Cohen's book. 
        """
        poly = K.polynomial
        degree = K.degree
        
        S = 0
        if k <= degree:
            S = -k * poly[degree - k]

        for i in range(1, k):
            S = S - poly[degree - i]*K.pow_sum(k-i)
        return S

    def size(K):
        """
        Compute the size of defining polynomial of the given field K.
        """
        if K.signature()[1] == 0:
            return K.pow_sum(2)
        else:
            return "Not Implemented."

    def POLRED(K):
        """
        Given a polynomial f i.e. a field K, output some polynomials
        defining subfield of K, where K is a field defined by f.
        Algorithm 4.4.11 in Cohen's book.
        """
        f = polynomial.OneVariableDensePolynomial(K.polynomial, "x")
        n = K.degree
        appr = equation.SimMethod(K.polynomial)

        #Step 1.
        """
        Using the round 2 method, compute an integral basis.
        """
        Basis = round2.round2(f)
        BaseList = []
        for i in range(n):
            Int = Basis[0][i].coefficient.getAsList()
            if len(Int) != n:
                for j in range(n - len(Int)):
                    Int.append(0)
            AlgInt = MatAlgNumber(Int, K.polynomial)
            BaseList.append(AlgInt)
        print BaseList
        
        #Step 2.
        list = []
        if K.signature()[1] == 0: 
>>>>>>> other
            for i in range(n):
                for j in range(n):
                    s = BaseList[i]*BaseList[j]
                    traces.append(s.trace())
        else:
            sigma = equation.SimMethod(self.polynomial)
            f = []
            for i in range(n):
<<<<<<< local
                f.append(zpoly(Basis[i]))
=======
                char = (BaseList[i].ch_basic()).ch_approx(appr[0]).charpoly
                sigma = equation.SimMethod(char)
                Sigma.append(sigma)
>>>>>>> other
            for i in range(n):
                for j in range(n):
                    m = 0
                    for k in range(n):
                        m += f[i](sigma[k])*f[j](sigma[k].conjugate())
                    traces.append(m.real)

        #Step 3.
        M = matrix.createMatrix(n, n, traces)
        S = matrix.unitMatrix(n)
<<<<<<< local
=======
        #print S
>>>>>>> other
        L = lattice.LLL(S, M)[0]
        
        #Step 4.
        Ch_Basis = []
        for i in range(n):
<<<<<<< local
            base_cor = changetype(0, self.polynomial).ch_matrix()
=======
            base_cor = changetype(0, K.polynomial).ch_matrix()
>>>>>>> other
            for v in range(n):
                base_cor += BaseList[v]*L.compo[v][i]
            Ch_Basis.append(base_cor)

        C = []
        #print Ch_Basis[0]
        a = Ch_Basis[0]
        for i in range(n):
<<<<<<< local
            coeff = Ch_Basis[i].ch_approx(appr[0]).charpoly
            C.append(zpoly(coeff))
=======
            C.append(polynomial.OneVariableDensePolynomial((Ch_Basis[i].ch_basic()).ch_approx(appr[0]).charpoly, "x"))
>>>>>>> other
            
        #Step 5.
        P = []
        for i in range(n):
<<<<<<< local
            diff_C = C[i].differentiate()
            gcd_C = C[i].subresultant_gcd(diff_C)
            P.append(C[i].exact_division(gcd_C))

=======
            diff_C = C[i].differentiate("x")
            gcd_C = polynomial.subResultantGCD(C[i], diff_C)
            P.append(C[i]/gcd_C)
        
>>>>>>> other
        return P

<<<<<<< local
=======
    def unity(self):
        """
        Return the unity of K.
        """
        n = self.degree
        A = []
        for i in range(n):
            if i == 1:
                A.append(1)
            else:
                A.append(0)
        return BasicAlgNumber([A, 1], self.polynomial)

>>>>>>> other
    def isIntBasis(self):
        """
        Determine whether self.basis is integral basis of self field.
        """
        D = self.disc()
        if squarefree.trial_division(abs(D)):
            return True
        else:
            if D % 4 == 0:
                if squarefree.trial_division(abs(D)//4) and (D//4) % 4 != 1:
                    return True
        return "Can not determined"

    def isGaloisField(self, other = None):
        """
        Determine whether self/other is Galois field.
        """
        if self.signature[0] == 0 or self.signature[1] == 0:
            return "Can not determined"
        else:
            return False

    def isFieldElement(self, A):
        """
        Determine whether A is field element of self field or not.  
        """
        poly = A.polynomial
        if poly == self.polynomial:
            return True
        else:
            if poly == self.POLRED():
                return True
            else:
                return False

    def getCharacteristic(self):
        """
        Return characteristic of the field (it is always zero).
        """
        return 0

    def createElement(self, seed):
        """
        createElement returns an element of the field with seed.
        """
        raise NotImplementedError

    def issubring(self, other):
        """
        Report whether another ring contains the field as a subring.
        """
        if self is other or self.isSubField(other):
            return True
        raise NotImplementedError("don't know how to tell")

    def issuperring(self, other):
        """
        Report whether the field is a superring of another ring.
        """
        if self is other:
            return True
        elif other.issubring(rational.theRationalField):
            return True
        raise NotImplementedError("don't know how to tell")

    def __eq__(self, other):
        """
        Equality test.
        """
        if self.issubring(other) and self.issuperring(other):
            return True
        return False

class BasicAlgNumber(object):
    """
    The class for algebraic number.
    """
    def __init__(self, valuelist, polynomial):
        if len(polynomial) != len(valuelist[0])+1:
            raise ValueError
        self.value = valuelist
        self.coeff = valuelist[0]
        self.denom = valuelist[1]
        self.degree = len(polynomial) - 1
        self.polynomial = polynomial
        self.field = NumberField(self.polynomial)
        Gcd = gcd.gcd_of_list(self.coeff)
        GCD = gcd.gcd(Gcd[0], self.denom) 
        if GCD != 1:
            self.coeff = [i//GCD for i in self.coeff]
            self.denom = self.denom//GCD
    
    def __repr__(self):
        return_str = '%s(%s, %s)' % (self.__class__.__name__, [self.coeff, self.denom], self.polynomial)
        return return_str
    
    def __neg__(self):
        coeff = []
        for i in range(len(self.coeff)):
            coeff.append(-self.coeff[i])
        return BasicAlgNumber([coeff, self.denom], self.polynomial)

    def __add__(self, other):
        d = self.denom*other.denom
        coeff = []
        for i in range(len(self.coeff)):
            coeff.append(other.denom*self.coeff[i] + self.denom*other.coeff[i])
        return BasicAlgNumber([coeff, d], self.polynomial)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if not isinstance(other, BasicAlgNumber):
            Coeff = [i*other for i in self.coeff] 
            return BasicAlgNumber([Coeff, self.denom], self.polynomial)
        else:
            d = self.denom*other.denom
            f = zpoly(self.polynomial)
            g = zpoly(self.coeff)
            h = zpoly(other.coeff)
            j = (g * h).pseudo_mod(f)
            jcoeff = [j[i] for i in range(self.degree)]
            return BasicAlgNumber([jcoeff, d], self.polynomial)

    def __pow__(self, exponent, mod=None):
        d = self.denom**exponent
        f = zpoly(self.polynomial)
        g = zpoly(self.coeff)
        if mod is None:
            j = pow(g, exponent, f)
        else:
            j = pow(g, exponent, f) % mod
            # what does mod exactly means?
        jcoeff = [j[i] for i in range(self.degree)]
        return BasicAlgNumber([jcoeff, d], self.polynomial)

    def inverse(self):
        f = zpoly(self.polynomial)
        g = zpoly(self.coeff)
        quotient, remainder = f.pseudo_divmod(g)

        if not remainder:
            icoeff = [i*self.denom for i in self.coeff]
            new_denom = 1
        else:
            icoeff = [self.denom * quotient[i] for i in range(self.degree)]
            new_denom = -remainder[0]
        return BasicAlgNumber([icoeff, new_denom], self.polynomial)

    def __truediv__(self, other):
        f = zpoly(self.polynomial)
        g = zpoly(self.coeff)
        t = BasicAlgNumber([other.coeff, other.denom], self.polynomial)
        k = t.inverse()
        h = zpoly(k.coeff)
        d = self.denom * k.denom
        j = (g * h).monic_mod(f)
        jcoeff = [j[i] for i in range(self.degree)]
        return BasicAlgNumber([jcoeff, d], self.polynomial)

    def getRing(self):
        """
        Return the algebraic number field contained self.
        """
        return NumberField(self.polynomial)
    
    def trace(self):
        """
        Compute the trace of self in K.
        """
        denom = self.denom
        n = len(self.polynomial) - 1
        
        tlist = [n]
        s = 0
        for k in range(1, n):
            for i in range(1, k):
                s += tlist[k - i] * self.polynomial[n - i]
            tlist.append(-k * self.polynomial[n - k] - s)

        t = 0
        for j in range(len(tlist)):
            t += tlist[j] * self.coeff[j]

        if denom == 1:
            return t
        elif t % denom == 0:
            return t // denom
        else:
            return rational.Rational(t, denom)

    def norm(self):
        """
        Compute the norm of self in K.
        """
        f = zpoly(self.polynomial)
        g = zpoly(self.coeff)
        R = f.resultant(g)

        if self.denom == 1:
            return int(R)
        else:
            denom = self.denom**self.degree
            if isinstance(R, int):
                if R % denom == 0:
                    return R // denom
                else:
                    return rational.Rational(R, denom)
            else:
                return R / denom

    def isAlgInteger(self):
        """
        Determine whether self is an algebraic integer or not. 
        """
        Norm = self.norm()
        if isinstance(Norm, int):
            return True
        else:
            return False

<<<<<<< local
    def ch_matrix(self):
        """
        Change style to MatAlgNumber.
        """
        list = []
        if self.denom == 1:
            list = self.coeff
        else:
            for i in range(self.degree):
                list.append(rational.Rational(self.coeff[i], self.denom))
        return MatAlgNumber(list, self.polynomial)
=======
        #step.3
        Prime_A = misc.primeDivisors(Da)
        Prime_B = misc.primeDivisors(Db)
        
        for i in Prime_A:
            if arith1.vp(Da, i)[0]%2 == 0:
                Prime_A.remove(i)
>>>>>>> other

    def ch_approx(self, approx):
        """
        Change style to ApproxAlgNuber.
        """
        list = []
        if self.denom == 1:
            list = self.coeff
        else:
            list = self.coeff
        return ApproxAlgNumber(list, approx, self.polynomial)

<<<<<<< local
class MatAlgNumber(object):
=======

        #step.5

        return "Not"
    
    def isFieldIsom(self, other):
        if self.degree == other.degree:
            if self.disc() == other.disc():
                return True
            else:
                return False
        else:
            return "Not Implemented"

class MatAlgNumber:
>>>>>>> other
    """
    The class for algebraic number represented by matrix.
    """
    def __init__(self, coefficient, polynomial):
        self.coeff = coefficient
        self.degree = len(coefficient)
        List = []
        for i in range(self.degree):
            stbasis = [0] * self.degree
            stbasis[i] = 1
            List.append(stbasis)
        List.append([- polynomial[i] for i in range(self.degree)])
        for l in range(self.degree - 2):
            basis1 = []
            basis = []
            for j in range(self.degree):
                if j == 0:
                    basis1.append(0)
                if j < self.degree - 1:
                    basis1.append(List[l + self.degree][j])
                elif j == self.degree - 1:
                    basis2 = [List[l + self.degree][j] * - polynomial[k] for k in range(self.degree)]
            for i in range(self.degree):
                basis.append(basis1[i] + basis2[i])
            List.append(basis)
        Matrix = []
        flag = 0
        for i in range(self.degree):
            basis3 = []
            for j in range(self.degree):
                basis3.append([self.coeff[j] * k for k in List[j+flag]])
            for l in range(self.degree):
                t = 0
                for m in range(self.degree):
                    t += basis3[m][l]
                Matrix.append(t)
            flag += 1
        
        self.matrix = matrix.createMatrix(self.degree, self.degree, Matrix)
        self.polynomial = polynomial
        self.field = NumberField(self.polynomial)

    def __repr__(self):
        return_str = '%s(%s, %s)' % (self.__class__.__name__, self.matrix.__repr__(), self.polynomial)
        return return_str

    def __neg__(self):
        mat = - self.matrix
        coeff = []
        for i in range(mat.row):
            coeff.append(mat[0][i])
        return MatAlgNumber(coeff, self.polynomial)

    def __add__(self, other):
        mat = self.matrix + other.matrix
        coeff = []
        for i in range(mat.row):
            coeff.append(mat[i+1][1])
        return MatAlgNumber(coeff, self.polynomial)

    def __sub__(self, other):
        mat = self.matrix - other.matrix
        coeff = []
        for i in range(mat.row):
            coeff.append(mat[i+1][1])
        return MatAlgNumber(coeff, self.polynomial)

    def __mul__(self, other):
        if not isinstance(other, MatAlgNumber):
            mat = other * self.matrix
        else:
            mat = self.matrix * other.matrix
        coeff = []
        for i in range(mat.row):
            coeff.append(mat[i+1][1])
        return MatAlgNumber(coeff, self.polynomial)

    def __pow__(self, other):
        mat = self.matrix ** other
        coeff = []
        for i in range(mat.row):
            coeff.append(mat[i+1][1])
        return MatAlgNumber(coeff, self.polynomial)
        
    def inverse(self):
        mat = self.matrix
        inv = mat.inverse()
        coeff = []
        for i in range(inv.row):
            coeff.append(inv[i+1][1])
        return MatAlgNumber(coeff, self.polynomial)
    
    def norm(self):
        return (self.matrix).determinant()

    def trace(self):
        return (self.matrix).trace()

    def getRing(self):
        """
        Return the algebraic number field contained self.
        """
        return NumberField(self.polynomial)

    def ch_basic(self):
        """
        Return BasicAlgNumber type for the given MatAlgNumber.
        """
        denom = 1
        for i in range(self.degree):
            if not isinstance(self.coeff[i], int):
                denom *= gcd.lcm(denom, (self.coeff[i]).denominator)
        coeff = []
        for i in range(self.degree):
            if isinstance(self.coeff[i], int):
                coeff.append(self.coeff[i] * denom)
            else:
                coeff.append(int((self.coeff[i]).numerator * denom / (self.coeff[i]).denominator))
        return BasicAlgNumber([coeff, denom], self.polynomial)

<<<<<<< local
=======
class BasicAlgNumber:
    """
    The class for algebraic number.
    """
    def __init__(self, valuelist, polynomial):
        if len(polynomial) != len(valuelist[0])+1:
            raise ValueError
        self.coeff = valuelist[0]
        self.denom = valuelist[1]
        self.degree = len(polynomial) - 1
        self.polynomial = polynomial
        self.field = NumberField(self.polynomial)
        Gcd = gcd.gcd_of_list(self.coeff)
        GCD = gcd.gcd(Gcd[0], self.denom) 
        if GCD != 1:
            self.coeff = [i//GCD for i in self.coeff]
            self.denom = self.denom//GCD
    
    def __repr__(self):
        return_str = '%s(%s, %s)' % (self.__class__.__name__, [self.coeff, self.denom], self.polynomial)
        return return_str
    
    def __neg__(self):
        list = []
        for i in range(len(self.coeff)):
            list.append(-self.coeff[i])
        return BasicAlgNumber([list, self.denom], self.polynomial)

    def __add__(self, other):
        d=self.denom*other.denom
        list = []
        for i in range(len(self.coeff)):
            list.append(other.denom*self.coeff[i]+self.denom*other.coeff[i])
        return BasicAlgNumber([list, d], self.polynomial)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if not isinstance(other, BasicAlgNumber):
            Coeff = [i*other for i in self.coeff] 
            return BasicAlgNumber([Coeff, self.denom], self.polynomial)
        else:
            d = self.denom*other.denom
            f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
            g = polynomial.OneVariableDensePolynomial(self.coeff, "x")
            h = polynomial.OneVariableDensePolynomial(other.coeff, "x")
            j = (g*h)%f
            list = j.coefficient.getAsList()
            if len(list) != self.degree:
                for i in range(self.degree - len(list)):
                    list.append(0)
            return BasicAlgNumber([list, d], self.polynomial)
    
    def __pow__(self, exponent, mod = None):
        d = self.denom**exponent
        f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
        g = polynomial.OneVariableDensePolynomial(self.coeff, "x")
        if mod == None:
            j = g.__pow__(exponent, f)
        else:
            j = g.__pow__(exponent, f)%mod
        list = j.coefficient.getAsList()
        if len(list) != self.degree:
            for i in range(self.degree - len(list)):
                list.append(0)
        return BasicAlgNumber([list, d], self.polynomial)

    def inverse(self):
        f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
        g = polynomial.OneVariableDensePolynomial(self.coeff, "x")
        h = polynomial.pseudoDivision(f, g)

        LIST = h[0].coefficient.getAsList()
        list = []
        for i in range(len(LIST)):
            list.append(self.denom*LIST[i])
        if h[1] == 0:
            Coeff = [i*self.denom for i in self.coeff]
            return BasicAlgNumber([Coeff, 1], self.polynomial)
        else:
            D = h[1].coefficient.getAsList()
            if len(list) != self.degree:
                for i in range(self.degree - len(list)):
                    list.append(0)
        return BasicAlgNumber([list, (-1)*D[0]], self.polynomial)
    
    def __truediv__(self, other):
        f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
        g = polynomial.OneVariableDensePolynomial(self.coeff, "x")
        t = BasicAlgNumber([other.coeff, other.denom], self.polynomial)
        k = t.inverse()
        h = polynomial.OneVariableDensePolynomial(k.coeff, "x")
        d = self.denom*k.denom
        j = (g*h)%f
        list = j.coefficient.getAsList()
        if len(list) != self.degree:
            for i in range(self.degree - len(list)):
                list.append(0)
        return BasicAlgNumber([list, d], self.polynomial)

    def getRing(self):
        """
        Return the algebraic number field contained self.
        """
        return NumberField(self.polynomial)
    
    def trace(self):
        """
        Compute the trace of self in K.
        """
        denom = self.denom
        f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
        n = len(self.polynomial) - 1
        
        list = [n]
        s = 0
        for k in range(1,n):
            for i in range(1,k):
                s = s + list[k-i]*self.polynomial[n-i]
            list.append(-k*self.polynomial[n-k]-s)

        t = 0
        for j in range(len(list)):
            t = t + list[j]*self.coeff[j]

        if denom == 1:
            return t
        elif t%denom == 0:
            return t//denom
        else:
            return rational.Rational(t, denom)
    
    def norm(self):
        """
        Compute the norm of self in K.
        """
        degree = self.degree
        denom = self.denom
        Denom = denom**degree
        f = polynomial.OneVariableDensePolynomial(self.polynomial, "x")
        g = polynomial.OneVariableDensePolynomial(self.coeff, "x")        
        R = polynomial.resultant(f, g)

        if denom == 1:
            return int(R)
        else:
            if isinstance(R, int) == True:
                if R % Denom == 0:
                    return R//Denom
                else:
                    return rational.Rational(R, Denom)
            else:
                return R/Denom

    def isAlgInteger(self):
        """
        Determine whether self is an algebraic integer or not. 
        """
        Norm = self.norm()
        if isinstance(Norm, int) == True:
            return True
        else:
            return False

    def ch_matrix(self):
        """
        Change style to MatAlgNumber.
        """
        list = []
        if self.denom == 1:
            list = self.coeff
        else:
            for i in range(self.degree):
                list.append(rational.Rational(self.coeff[i], self.denom))
        return MatAlgNumber(list, self.polynomial)

>>>>>>> other
    def ch_approx(self, approx):
        return (self.ch_basic()).ch_approx(approx)
                    
class ApproxAlgNumber:
    """
    The class for algebraic number represented by minimum polynomial.    
    """
    def __init__(self, valuelist, approx, poly):
        self.coeff = valuelist[0]
        self.denom = valuelist[1]
        self.degree = len(self.coeff)
        self.polynomial = poly
        conj = equation.SimMethod(self.polynomial)
        self.conj = conj
        self.base_approx = approx

        Approx = 0
        for i in range(self.degree):
            Approx += self.coeff[i]*(approx**i)
        self.approx = Approx/self.denom

        Conj = []
        for i in range(self.degree):
            conj_approx = 0
            for j in range(self.degree):
                conj_approx += (self.coeff[j])*((self.conj[i])**j)
            Conj.append(conj_approx)
        P = uniutil.polynomial({0:-Conj[0], 1:1}, ring.getRing(Conj[0]))
        for i in range(1, self.degree):
<<<<<<< local
            P *= uniutil.polynomial({0:-Conj[i], 1:1}, ring.getRing(Conj[i]))
=======
            P *= polynomial.OneVariableDensePolynomial([-Conj[i], 1], "x")

>>>>>>> other
        charcoeff = []
        for i in range(self.degree + 1):
<<<<<<< local
            if hasattr(P[i], "real"):
                charcoeff.append(int(math.floor(P[i].real + 0.5)))
            else:
                charcoeff.append(int(math.floor(P[i] + 0.5)))
        self.charpoly = charcoeff
=======
            charcoeff.append(int(math.floor(P.coefficient[i].real + 0.5)))

        if self.denom == 1:
            self.charpoly = charcoeff
        else:
            coefflist = [charcoeff[i]*(self.denom**i) for i in range(self.degree + 1)]
            GCD = gcd.gcd_of_list(coefflist)[0]
            self.charpoly = [coefflist[i]//GCD for i in range(self.degree + 1)]
>>>>>>> other

    def __repr__(self):
        return_str = '%s(%s, %s)' % (self.__class__.__name__, self.approx, self.charpoly)
        return return_str
    
    def __neg__(self):
        list = []
        for i in range(self.degree):
            list.append(-self.coeff[i])
        return ApproxAlgNumber([list, self.denom], self.base_approx, self.polynomial)

    def __add__(self, other):
        basic = BasicAlgNumber([self.coeff, self.denom], self.polynomial) + BasicAlgNumber([other.coeff, other.denom], self.polynomial)
        return ApproxAlgNumber([basic.coeff, basic.denom], self.base_approx, self.polynomial)

    def __sub__(self, other):
        return self.__add__(-other)

<<<<<<< local
=======
    def __mul__(self, other):
        basic = BasicAlgNumber([self.coeff, self.denom], self.polynomial) * BasicAlgNumber([other.coeff, other.denom], self.polynomial)
        return ApproxAlgNumber([basic.coeff, basic.denom], self.base_approx, self.polynomial)

>>>>>>> other
def changetype(a, polynomial):
    """
    Change a integer 'a' to be an element of field K defined polynomial
    """
    n = len(polynomial)
    coeff = []
    for i in range(n - 1):
        if i == 0:
            coeff.append(a)
        else:
            coeff.append(0)
    return BasicAlgNumber([coeff, 1], polynomial)

def disc(A):
    """
    Compute the discriminant of a_i, where A=[a_1, ..., a_n]
    """
    n = A[0].degree
    list = []
    for i in range(n):
        for j in range(n):
            s = A[i]*A[j]
    list.append(s.trace())
    M = matrix.createMatrix(n, n, list)
    return M.determinant()
<<<<<<< local

class Module:
    def __init__(self, denominator, form, field):
        #form is a integer matrix.
        #field is a Number field.
        self.denominator = denominator
        self.field = field
        self.form = form
        self.transform = form.transpose()
        self.hnf = self.form.hermiteNormalForm()
        self.transhnf = self.hnf.transpose()
        self.rank = self.hnf.rank()
        
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, [self.denominator, repr(self.transhnf)], repr(self.field))

    def __add__(self, other):
        return "Not Implemented"

    def isSameModele(self, other):
        if self.hnf == other.hnf:
            return True
        else:
            return "Can not determined"

class Module_element:
    def __init__(self, coefficient, module):
        #coefficient is a vector.
        self.coefficient = coefficient
        self.module = module

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.coefficient, repr(self.module))
        
    def __add__(self, other):
        coeff = self.coefficient + other.coefficient
        return Module_element(coeff, self.module)

    def __sub__(self, other):
        coeff = self.coefficient + other.coefficient
        return Module_element(coeff, self.module)

    def __mul__(self, a):
        return Module_element(a*self.coefficient, self.module)

def qpoly(coeffs):
    """
    Return a rational coefficient polynomial constructed from given
    coeffs.  The coeffs is a list of coefficients in ascending order.
    """
    terms = [(i, rational.Rational(c)) for (i, c) in enumerate(coeffs)]
    return uniutil.polynomial(terms, rational.theRationalField)

def zpoly(coeffs):
    """
    Return an integer coefficient polynomial constructed from given
    coeffs.  The coeffs is a list of coefficients in ascending order.
    """
    return uniutil.polynomial(enumerate(coeffs), rational.theIntegerRing)
=======
>>>>>>> other
