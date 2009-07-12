from __future__ import division
import unittest
import nzmath.arith1 as arith1
import nzmath.poly.hensel as hensel


class HenselTestBase(unittest.TestCase):
    def assertEqualModulo(self, expected, actual, modulus, message=None):
        """
        assert expected == actual (mod modulus)
        """
        if message is None:
            for d, c in actual - expected:
                self.assertEqual(0, c % modulus,
                                 "degree %d\nactual = %s" % (d, str(actual)))
        else:
            for d, c in actual - expected:
                self.assertEqual(0, c % modulus,
                                 "degree %d\nactual = %s\n%s" % (d, str(actual), message))


class ExtgcdpTest(HenselTestBase):
    def testNonMonicIntermediate(self):
        f1 = hensel.the_ring.createElement({0:1, 1:1})
        f2 = hensel.the_ring.createElement({0:1, 2:1})
        p = 7
        # EXECUTION
        u1, u2, w = hensel._extgcdp(f1, f2, p)
        # POSTCONDITIONS
        self.assertEqualModulo(hensel.the_one, w, p)
        self.assertEqualModulo(w, f1*u1 + f2*u2, p)

    def testRegular(self):
        f1 = hensel.the_ring.createElement({0:0, 1:1})
        f2 = hensel.the_ring.createElement({0:1, 1:1})
        p = 2
        # EXECUTION
        u1, u2, w = hensel._extgcdp(f1, f2, p)
        # POSTCONDITIONS
        self.assertEqual(hensel.the_one, w)
        self.assertEqualModulo(w, f1*u1 + f2*u2, p)
        

class HenselTest(HenselTestBase):
    def testGlobal(self):
        self.assertEqual("Z[]", str(hensel.the_ring))
        self.assertEqual(hensel.the_one, hensel.the_one + hensel.the_zero)
        self.assertEqual(hensel.the_one, hensel.the_one * hensel.the_one)
        self.assertEqual(hensel.the_zero, hensel.the_zero + hensel.the_zero)
        self.assertEqual(hensel.the_zero, hensel.the_one * hensel.the_zero)
        self.assertEqual(hensel.the_zero, hensel.the_zero * hensel.the_zero)

    def test_lift_pair(self):
        f = hensel.the_ring.createElement(enumerate([15, 38, 14, 1]))
        a1 = hensel.the_ring.createElement(enumerate([1, 1, 1]))
        a2 = hensel.the_ring.createElement(enumerate([1, 1]))

        # PRECONDITIONS
        self.assertEqualModulo(f, a1 * a2, 2)

        # EXECUTION
        lifted, q = hensel.lift_upto(target=f,
                                     factors=[a1, a2],
                                     p=2,
                                     bound=100)
	# POSTCONDITIONS
        self.assertEqual(2, len(lifted))
        self.assertEqual(256, q) # q == p**8 == ((p**2)**2)**2
        self.assertEqualModulo(f, lifted[0] * lifted[1], 256)

    def test_lift_multi(self):
        f1 = hensel.the_ring.createElement({0:5, 1:1})
        f2 = hensel.the_ring.createElement({0:1, 1:1})
        f3 = hensel.the_ring.createElement({0:1, 2:1})
        factors = [f1, f2, f3]
        f = hensel.the_ring.createElement(enumerate([-9900, -1, -9899, -1, 1]))
        p = 7 # q is also 7

        # PRECONDITIONS
        # target = g1*g2*...*gm (mod q)
        self.assertEqualModulo(f, f1 * f2 * f3, p)

        # EXECUTION
        lifted, q = hensel.lift_upto(target=f,
                                     factors=factors,
                                     p=p,
                                     bound=100)

        # POSTCONDITIONS:
        self.assertEqual(3, len(lifted))
        self.assertEqual(7**4, q)
        # target = G1*G2*...*Gm (mod q*p),
        self.assertEqualModulo(f, arith1.product(lifted), q, str(lifted))
        # Gi = gi (mod q)
        for gi, Gi in zip(factors, lifted):
            self.assertEqualModulo(gi, Gi, 7)

    def test_pair_from_factors(self):
        f = hensel.the_ring.createElement(enumerate([15, 38, 14, 1]))
        a1 = hensel.the_ring.createElement(enumerate([1, 1, 1]))
        a2 = hensel.the_ring.createElement(enumerate([1, 1]))

        # PRECONDITIONS
        self.assertEqualModulo(f, a1 * a2, 2)

        # EXECUTION
        lifter = hensel.HenselLiftPair.from_factors(f, a1, a2, 2)

        # POSTCONDITIONS
        factors = lifter.factors
        ladder = lifter.u1, lifter.u2
	# asserting equality
        self.assertEqual(2, len(factors))
        self.assertEqual(a1, factors[0])
        self.assertEqual(a2, factors[1])
        # assert about ladder
        self.assertEqualModulo(hensel.the_one,
                               sum(u*g for (u, g) in zip(ladder, factors)),
                               2)

    def test_quadratic_lift_pair(self):
        f = hensel.the_ring.createElement(enumerate([15, 38, 14, 1]))
        a1 = hensel.the_ring.createElement(enumerate([1, 3, 1]))
        a2 = hensel.the_ring.createElement(enumerate([3, 1]))
        u1 = hensel.the_ring.createElement({0: 1})
        u2 = hensel.the_ring.createElement({1: 1})
        # PRECONDITIONS:
        ## if one of these assertions fails, then the setting is wrong.
        # p = 2, q = 4
        # gi are monic (i = 1, 2)
        self.assertEqual(1, a1.leading_coefficient(), "monic")
        self.assertEqual(1, a2.leading_coefficient(), "monic")
        # target == g1 * g2 mod q
        self.assertEqualModulo(f, a1*a2, 4)
        # u1*g1 + u2*g2 == 1 mod p
        self.assertEqualModulo(hensel.the_one, a1*u1 + a2*u2, 2)

        # EXECUTION
        lifter = hensel.HenselLiftPair(f, a1, a2, u1, u2, 2, 4)
        lifter.lift_ladder()
        new_ladder = lifter.u1, lifter.u2

        # POSTCONDITIONS:
        # Ui == ui mod p (i = 1, 2)
        self.assertEqualModulo(u1, lifter.u1, 2)
        self.assertEqualModulo(u2, lifter.u2, 2)
        # U1*g1 + U2*g2 == 1 mod p**2
        self.assertEqualModulo(hensel.the_one, a1*lifter.u1 + a2*lifter.u2, 4)

    def test_simultaneous(self):
        # f = (X**2 + 17)(X**4 + 2*(1-c)*X**2 + (1+c)**2)
        # c = 2**32*3
        f = hensel.the_ring.createElement({0:2822351843715648061457,
                                           2:166020696251069104163,
                                           4:-25769803757,
                                           6:1})
        f1 = hensel.the_ring.createElement({0:5, 1:1})
        f2 = hensel.the_ring.createElement({0:2, 1:1})
        f3 = hensel.the_ring.createElement({0:2, 2:1})
        f4 = hensel.the_ring.createElement({0:4, 2:1})
        factors = [f1, f2, f3, f4]
        p = 7 # q is also 7

        # PRECONDITIONS
        # target = g1*g2*...*gm (mod q)
        self.assertEqualModulo(f, f1 * f2 * f3 * f4, p)

        # EXECUTION
        lifted, q = hensel.lift_upto(target=f,
                                     factors=[f1, f2, f3, f4],
                                     p=p,
                                     bound=7**128)

        # POSTCONDITIONS:
        self.assertEqual(4, len(lifted))
        self.assertEqual(7**128, q)
        # target = G1*G2*...*Gm (mod q*p),
        self.assertEqualModulo(f, arith1.product(lifted), q, str(lifted))
        # Gi = gi (mod q)
        for gi, Gi in zip(factors, lifted):
            self.assertEqualModulo(gi, Gi, 7)


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
