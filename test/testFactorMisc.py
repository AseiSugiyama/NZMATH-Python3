import unittest
import nzmath.factor.misc as misc


class MiscTest(unittest.TestCase):
    def testPrimeDivisors(self):
        # backward compatibility
        self.assertEqual([3, 5], misc.primeDivisors(15))

    def testSquarePart(self):
        # backward compatibility
        self.assertEqual(1, misc.squarePart(15))
        self.assertEqual(17, misc.squarePart(17**2 * 19))

    def testAllDivisors(self):
        # backward compatibility
        self.assertEqual([1], misc.allDivisors(1))
        self.assertEqual([1, 2], misc.allDivisors(2))
        self.assertEqual([1, 2, 4], misc.allDivisors(4))
        self.assertEqual([1, 2, 3, 6], misc.allDivisors(6))
        self.assertEqual([1, 2, 3, 4, 6, 12], misc.allDivisors(12))
        self.assertEqual([1, 2, 3, 5, 6, 10, 15, 30], misc.allDivisors(30))

    def testPrimePowerTest(self):
        # not a power
        self.assertEqual((12, 0), misc.primePowerTest(12))
        self.assertEqual((53, 1), misc.primePowerTest(53))
        # not a prime power
        self.assertEqual((36, 0), misc.primePowerTest(36))
        # powers
        self.assertEqual((7, 2), misc.primePowerTest(49))
        self.assertEqual((3, 4), misc.primePowerTest(81))
        self.assertEqual((5, 3), misc.primePowerTest(125))
        self.assertEqual((2, 7), misc.primePowerTest(128))


class FactoredIntegerTest(unittest.TestCase):
    def testEquality(self):
        fifteen = misc.FactoredInteger(15)
        self.assertEqual(15, fifteen)
        self.assertEqual(misc.FactoredInteger(15), fifteen)
        self.assertNotEqual(misc.FactoredInteger(16), fifteen)

    def testPrimeDivisors(self):
        fifteen = misc.FactoredInteger(15)
        self.assertEqual([3, 5], fifteen.prime_divisors())

    def testDivisors(self):
        fifteen = misc.FactoredInteger(15)
        self.assertEqual([1, 3, 5, 15], fifteen.divisors())

    def testProperDivisors(self):
        fortyfive = misc.FactoredInteger(45)
        self.assertEqual([3, 5, 9, 15], fortyfive.proper_divisors())

    def testSquarePart(self):
        fifteen = misc.FactoredInteger(15)
        self.assertEqual(1, fifteen.square_part())
        self.assertTrue(isinstance(fifteen.square_part(True), misc.FactoredInteger))
        self.assertEqual(1, fifteen.square_part(True).integer)
        self.assertEqual({}, fifteen.square_part(True).factors)
        factored45 = misc.FactoredInteger(45, {3:2, 5:1})
        self.assertEqual({3:1}, factored45.square_part(True).factors)

    def testSquarefreePart(self):
        fifteen = misc.FactoredInteger(15)
        self.assertEqual(15, fifteen.squarefree_part())
        self.assertTrue(isinstance(fifteen.squarefree_part(True), misc.FactoredInteger))
        self.assertEqual(15, fifteen.squarefree_part(True).integer)
        self.assertEqual({3:1, 5:1}, fifteen.squarefree_part(True).factors)
        factored45 = misc.FactoredInteger(45, {3:2, 5:1})
        self.assertEqual({5:1}, factored45.squarefree_part(True).factors)

    def testInitFactored(self):
        factored45 = misc.FactoredInteger(45, {3:2, 5:1})
        self.assertEqual(45, factored45.integer)
        self.assertEqual({3:2, 5:1}, factored45.factors)

    def testPartial(self):
        partial45 = misc.FactoredInteger.from_partial_factorization(45, {3:1})
        self.assertEqual(45, partial45.integer)
        self.assertEqual({3:2, 5:1}, partial45.factors)

    def testIsDivisibleBy(self):
        factored45 = misc.FactoredInteger(45, {3:2, 5:1})
        self.assertFalse(factored45.is_divisible_by(2))
        self.assertTrue(factored45.is_divisible_by(3))
        self.assertTrue(factored45.is_divisible_by(5))
        self.assertFalse(factored45.is_divisible_by(7))
        self.assertTrue(factored45.is_divisible_by(9))
        self.assertTrue(factored45.is_divisible_by(15))

    def testExactDivision(self):
        fortyfive = misc.FactoredInteger(45)
        self.assertEqual(45, int(fortyfive))
        fifteen = fortyfive.exact_division(3)
        self.assertEqual(15, int(fifteen))
        five = fortyfive // 9
        self.assertEqual(5, int(five))
        five = fortyfive.exact_division(misc.FactoredInteger(9, {3:2}))
        self.assertEqual(5, int(five))


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
