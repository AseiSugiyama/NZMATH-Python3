import unittest
import nzmath.factor.mpqs as mpqs


class FactorTest (unittest.TestCase):
    def testMPQS(self):
        p = 4 * 6133 + 1
        result = mpqs.mpqs(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)

    def testQS(self):
        p = 4 * 6133 + 1
        result = mpqs.qs(p*154858631, 1500, 50)
        self.assertEqual([p, 154858631], result)


class FindTest (unittest.TestCase):
    def test_mpqsfind_13(self):
        # 13-digits
        p = 24533
        q = 154858631
        result = mpqs.mpqsfind(p * q)
        self.assertIn(result, (p, q))

    # def test_mpqsfind_30(self):
    #     # 30-digits
    #     p = 94323529592431
    #     q = 9792226322761229
    #     result = mpqs.mpqsfind(p * q)
    #     self.assertIn(result, (p, q))

    # def test_mpqsfind_35(self):
    #     # 35-digit
    #     p = 21866897605835123
    #     q = 2262004280557843933
    #     result = mpqs.mpqsfind(p * q)
    #     self.assertIn(result, (p, q))

    # def test_mpqsfind_40(self):
    #     # 40-digits
    #     p = 2549870142908559959
    #     q = 1324809104275093930309
    #     result = mpqs.mpqsfind(p * q)
    #     self.assertIn(result, (p, q))

    # def test_mpqsfind_55(self):
    #     # 55-digit
    #     p = 97922263227612134317650461
    #     q = 21458295943235295924297533843
    #     result = mpqs.mpqsfind(p * q)
    #     self.assertIn(result, (p, q))


class QuadraticPolynomialTest (unittest.TestCase):
    def setUp(self):
        number = 137174210013717421
        init_param = 12367
        self.qp = mpqs.QuadraticPolynomial(number, init_param)

    def test_attributes(self):
        self.assertTrue(hasattr(self.qp, "param"))
        self.assertEqual(12367, self.qp.param)
        self.assertTrue(hasattr(self.qp, "f_1"))
        self.assertEqual(12367 ** 2, self.qp.f_2)

    def test_next_polynomial_sieve_range(self):
        number = 137174210013717421
        qp = mpqs.QuadraticPolynomial.next_polynomial(number, sieve_range=200)
        self.assertTrue(qp)
        self.assertEqual(1151, qp.param)

    def test_next_polynomial_init_param(self):
        number = 137174210013717421
        qp = mpqs.QuadraticPolynomial.next_polynomial(number, init_param=1147)
        self.assertTrue(qp)
        self.assertEqual(1151, qp.param)
        self.assertEqual(1151 ** 2, qp.f_2)

    def test_call(self):
        number = 137174210013717421
        qp = mpqs.QuadraticPolynomial.next_polynomial(number, init_param=1147)
        self.assertEqual(qp.f_0, qp(0))
        self.assertEqual(qp.f_0 + qp.f_1 + qp.f_2, qp(1))
        self.assertEqual(qp.f_0 - qp.f_1 + qp.f_2, qp(-1))
 
    def test_delta(self):
        number = 137174210013717421
        qp = mpqs.QuadraticPolynomial.next_polynomial(number, init_param=1147)
        self.assertEqual(qp(-9) - qp(-10), qp.delta(-9))
        self.assertEqual(qp(1) - qp(0), qp.delta(1))
        self.assertEqual(qp(2) - qp(1), qp.delta(2))


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
