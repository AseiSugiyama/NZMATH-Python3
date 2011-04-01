import unittest
import nzmath.poly.groebner as groebner
import nzmath.rational as rational
import nzmath.poly.termorder as termorder
import nzmath.poly.multiutil as multiutil


class GroebnerTest (unittest.TestCase):
    def assertEqualUptoUnit(self, f, g):
        """
        Equality ignoring difference of unit.
        I.e. f divides g and g divides f.
        """
        r1, r2 = f.pseudo_mod(g), g.pseudo_mod(f)
        self.assertFalse(r1)
        self.assertFalse(r2)
    
    def setUp(self):
        self.lex = termorder.lexicographic_order

    def testBuchberger(self):
        """
        test Buchberger's algorithm.

        http://www.geocities.com/famancin/buchberger.html
        """
        F = (multiutil.polynomial({(2, 0): rational.Integer(1),
                                   (1, 2): rational.Integer(2)},
                                  rational.theRationalField, 2),
             multiutil.polynomial({(1, 1): rational.Integer(1),
                                   (0, 3): rational.Integer(2),
                                   (0, 0): rational.Integer(-1)},
                                  rational.theRationalField, 2))
        G_from_F = groebner.buchberger(F, self.lex)
        G_expected = list(
            F + (multiutil.polynomial({(1, 0): rational.Integer(1)},
                                      rational.theRationalField, 2),
                 multiutil.polynomial({(0, 3): rational.Integer(2),
                                       (0, 0): rational.Integer(-1)},
                                      rational.theRationalField, 2)))
        self.assertEqual(len(G_expected), len(G_from_F))
        for p, q in zip(G_expected, G_from_F):
            self.assertEqualUptoUnit(p, q)

    def testNormalStrategy(self):
        """
        test Buchberger's algorithm (normal strategy).

        same example with testBuchberger.
        """
        F = (multiutil.polynomial({(2, 0): rational.Integer(1),
                                   (1, 2): rational.Integer(2)},
                                  rational.theRationalField, 2),
             multiutil.polynomial({(1, 1): rational.Integer(1),
                                   (0, 3): rational.Integer(2),
                                   (0, 0): rational.Integer(-1)},
                                  rational.theRationalField, 2))
        G_from_F = groebner.normal_strategy(F, self.lex)
        G_expected = list(
            F + (multiutil.polynomial({(1, 0): rational.Integer(1)},
                                      rational.theRationalField, 2),
                 multiutil.polynomial({(0, 3): rational.Integer(2),
                                       (0, 0): rational.Integer(-1)},
                                      rational.theRationalField, 2)))
        self.assertEqual(len(G_expected), len(G_from_F))
        for p, q in zip(G_expected, G_from_F):
            self.assertEqualUptoUnit(p, q)


class ReducedGroebnerBasisTest (unittest.TestCase):
    def setUp(self):
        self.lex = termorder.lexicographic_order

    def testReduce(self):
        F = (multiutil.polynomial({(2, 0): rational.Integer(1),
                                   (1, 2): rational.Integer(2)},
                                  rational.theRationalField, 2),
             multiutil.polynomial({(1, 1): rational.Integer(1),
                                   (0, 3): rational.Integer(2),
                                   (0, 0): rational.Integer(-1)},
                                  rational.theRationalField, 2))
        rgb_expected = [multiutil.polynomial({(1, 0): rational.Integer(1)},
                                             rational.theRationalField, 2),
                        multiutil.polynomial({(0, 3): rational.Integer(1),
                                              (0, 0): rational.Rational(-1, 2)},
                                             rational.theRationalField, 2)]
        G_from_F = groebner.normal_strategy(F, self.lex)
        rgb = groebner.reduce_groebner(G_from_F, self.lex)
        self.assertEqual(2, len(rgb))
        self.assertEqual(rgb_expected, rgb)


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
