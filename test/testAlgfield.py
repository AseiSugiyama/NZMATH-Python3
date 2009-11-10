import nzmath.polynomial as polynomial
import nzmath.rational as rational
import unittest
import nzmath.algfield as algfield

class NumberFieldTest (unittest.TestCase):
    def setUp(self):
        self.K = algfield.NumberField([-2,0,1])
        self.KI = algfield.NumberField([2,0,1])
        self.F = algfield.NumberField([-3,0,1])
        self.G = algfield.NumberField([-2,0,0,1])
        self.CF1 = algfield.NumberField([101,20,1])#cyclotomic field
        self.CF2 = algfield.NumberField([14521,-5302,725,-44,1])

    def testMul(self):
        L1 = [1,0,-10,0,1]
        L2 = [-23,36,27,4,-9,0,1]
        self.assertEqual(L1, (self.K * self.F).polynomial)
        self.assertEqual(L2, (self.F * self.G).polynomial)

    def testDisc(self):
        self.assertEqual(8, (self.K).disc())
        self.assertEqual(-108, (self.G).disc())
    
    def testSignature(self):
        self.assertEqual((2, 0), (self.K).signature())
        self.assertEqual((0, 1), (self.KI).signature())

#    def testPOLRED(self):
#        polred1 = (self.CF1).POLRED()[1]
#        self.assertEqual([1L, 0L, 1L], [polred1[i] for i in range(polred1.degree() + 1)])
#        polred2 = (self.CF2).POLRED()[1]
#        self.assertEqual([1L, 0L, -1L, 0L, 1L], [polred2[i] for i in range(polred2.degree() + 1)])

class BasicAlgNumberTest (unittest.TestCase):
    def setUp(self):
        self.a = algfield.BasicAlgNumber([[1, 1], 1], [-2, 0, 1])
        self.b = algfield.BasicAlgNumber([[-1, 2], 1], [-2, 0, 1])

    def testAdd(self):
        c = [[0, 3], 1]
        self.assertEqual(c, (self.a + self.b).value)

    def testMul(self):
        d = [[3, 1], 1]
        self.assertEqual(d, (self.a * self.b).value)

    def testPow(self):
        a_pow = [[3, 2], 1]
        b_pow = [[-25, 22], 1]
        self.assertEqual(a_pow, (self.a**2).value)
        self.assertEqual(b_pow, (self.b**3).value)

    def testInverse(self):
        a_inv = [[-1, 1], 1]
        b_inv = [[1, 2], 7]
        self.assertEqual(a_inv, (self.a).inverse().value)
        self.assertEqual(b_inv, (self.b).inverse().value)

    def testNorm(self):
        a_norm = -1
        b_norm = -7
        self.assertEqual(a_norm, (self.a).norm())
        self.assertEqual(b_norm, (self.b).norm())

    def testTrace(self):
        a_trace = 2
        b_trace = -2
        self.assertEqual(a_trace, (self.a).trace())
        self.assertEqual(b_trace, (self.b).trace())

class MatAlgNumberTest (unittest.TestCase):
    def setUp(self):
        self.a = algfield.MatAlgNumber([0, 1, 1], [-2, 0, 0, 1])
        self.b = algfield.MatAlgNumber([rational.Rational(-1, 2), rational.Rational(3, 2), rational.Rational(1, 1)], [-2, 0, 0, 1])

    def testAdd(self):
        c = [rational.Rational(-1, 2), rational.Rational(5, 2), rational.Rational(2, 1)]
        self.assertEqual(c, (self.a + self.b).coeff)

    def testMul(self):
        d = [rational.Rational(5, 1), rational.Rational(3, 2), rational.Rational(1, 1)]
        self.assertEqual(d, (self.a * self.b).coeff)

    def testInverse(self):
        a_inv = [rational.Rational(-1, 3), rational.Rational(1, 3), rational.Rational(1, 6)]
        b_inv = [rational.Rational(-2, 11), rational.Rational(2, 11), rational.Rational(2, 11)]
        self.assertEqual(a_inv, (self.a).inverse().coeff)
        self.assertEqual(b_inv, (self.b).inverse().coeff)

    def testPow(self):
        a_pow = [4, 2, 1]
        b_pow = [rational.Rational(13, 8), rational.Rational(93, 8), rational.Rational(51, 8)]
        self.assertEqual(a_pow, (self.a**2).coeff)
        self.assertEqual(b_pow, (self.b**3).coeff)

    def testNorm(self):
        a_norm = 6
        b_norm = rational.Rational(121, 8)
        self.assertEqual(a_norm, (self.a).norm())
        self.assertEqual(b_norm, (self.b).norm())

    def testTrace(self):
        a_trace = 0
        b_trace = rational.Rational(-3, 2)
        self.assertEqual(a_trace, (self.a).trace())
        self.assertEqual(b_trace, (self.b).trace())

# The following part is always unedited.
def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
