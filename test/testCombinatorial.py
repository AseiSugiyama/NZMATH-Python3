import unittest
import doctest
from nzmath.combinatorial import *


class BinomialTest (unittest.TestCase):
    def testPositiveAndPositive(self):
        assert 1 == binomial(1,1)
        assert 2 == binomial(2,1)
        assert 6 == binomial(4,2)
        assert 2000 == binomial(2000, 1999)
        assert 0 == binomial(1999, 2000)

    def testZero(self):
        assert 1 == binomial(0,0)
        assert 1 == binomial(1111111111111111111111111111111111111111111, 0)
        self.assertRaises(ValueError, binomial, 0, 3)
        self.assertRaises(ValueError, binomial, -1, 0)

    def testNegativeAndPositive(self):
        self.assertRaises(ValueError, binomial, -1, 2)

    def testPositiveAndNegative(self):
        self.assertRaises(ValueError, binomial, 2, -1)

    def testNegativeAndNegative(self):
        self.assertRaises(ValueError, binomial, -2, -3)
        self.assertRaises(ValueError, binomial, -1, -1)

    def testNonInteger(self):
        self.assertRaises(TypeError, binomial, 1.8, 1)
        self.assertRaises(TypeError, binomial, 1, 1.8)


class FactorialTest (unittest.TestCase):
    def testPositive(self):
        assert 1 == factorial(1)
        assert 2 == factorial(2)
        assert 6 == factorial(3)
        assert 24 == factorial(4)

    def testZero(self):
        assert 1 == factorial(0)

    def testError(self):
        self.assertRaises(TypeError, factorial, 1.5)
        self.assertRaises(ValueError, factorial, -1)


class BernoulliTest (unittest.TestCase):
    def testZero(self):
        assert 1 == bernoulli(0)

    def testOdd(self):
        import nzmath.rational as rational
        assert rational.Rational(-1, 2) == bernoulli(1)
        assert 0 == bernoulli(3)
        assert 0 == bernoulli(101)
        assert 0 == bernoulli(1010111111111111777979797979794555)

    def testEven(self):
        import nzmath.rational as rational
        assert rational.Rational(1, 6) == bernoulli(2)
        assert rational.Rational(-1, 30) == bernoulli(4)
        assert rational.Rational(1, 42) == bernoulli(6)


class CatalanTest (unittest.TestCase):
    def testNormal(self):
        self.assertEqual([1, 1, 2, 5, 14], [catalan(i) for i in range(5)])


class EulerTest (unittest.TestCase):
    def testOdd(self):
        self.assertEqual(0, euler(1))
        self.assertEqual(0, euler(101))

    def testEven(self):
        self.assertEqual(1, euler(0))
        self.assertEqual(-1, euler(2))
        self.assertEqual(5, euler(4))
        self.assertEqual(-61, euler(6))


class MultinomialTest (unittest.TestCase):
    def testBinomial(self):
        """
        test for binomial cases.
        """
        self.assertEqual(binomial(3, 1), multinomial(3, (1, 2)))
        self.assertEqual(binomial(4, 2), multinomial(4, (2, 2)))

    def testTrinomial(self):
        """
        test for binomial cases.
        """
        self.assertEqual(factorial(3), multinomial(3, [1]* 3))
        self.assertEqual(12, multinomial(4, (1, 1, 2)))

    def testError(self):
        """
        test for error cases.
        """
        # n != sum(parts)
        self.assertRaises(ValueError, multinomial, 2, [1, 1, 1])
        self.assertRaises(ValueError, multinomial, 5, [1, 1, 1])
        # parts is not a sequence of natural numbers.
        self.assertRaises(ValueError, multinomial, 2, [-1, 2, 1])


class StirlingTest (unittest.TestCase):
    def testStirling1(self):
        self.assertEqual(1, stirling1(0, 0))
        self.assertEqual(-1, stirling1(2, 1))
        self.assertEqual(-3, stirling1(3, 2))
        self.assertEqual(stirling1(4, 2), stirling1(3, 1) - 3*stirling1(3, 2))
        self.assertEqual(stirling1(5, 2), stirling1(4, 1) - 4*stirling1(4, 2))
        self.assertEqual(-50, stirling1(5, 2))
        self.assertEqual(35, stirling1(5, 3))
        self.assertEqual(-16669653, stirling1(14, 9))
        self.assertEqual(1474473, stirling1(14, 10))
        # (x)_n = \sum_{i=0}^{n} s(n, i) * x**i
        self.assertEqual(fallingfactorial(10, 5), sum([stirling1(5, i) * 10**i for i in range(6)]))

    def testStirling2(self):
        self.assertEqual(1, stirling2(0, 0))
        self.assertEqual(1, stirling2(1, 1))
        self.assertEqual(3, stirling2(3, 2))
        self.assertEqual(65, stirling2(6, 4))
        # x**n = \sum_{i=0}^{n} S(n, i) * (x)_i
        self.assertEqual(10**5, sum([stirling2(5, i) * fallingfactorial(10, i) for i in range(6)]))
        # negative numbers
        self.assertEqual(factorial(3), stirling2(-1, -4))
        self.assertEqual(85, stirling2(-4, -6))
        # directly calling underlying function
        self.assertEqual(factorial(3), stirling2_negative(4, 1))
        self.assertEqual(85, stirling2_negative(6, 4))

    def testBell(self):
        self.assertEqual(1, bell(0))
        self.assertEqual(1, bell(1))
        self.assertEqual(2, bell(2))
        self.assertEqual(52, bell(5))


class CombinationIngexGeneratorTest(unittest.TestCase):
    def testOne(self):
        self.assertEqual([[0]], [i for i in combinationIndexGenerator(1, 1)])

    def testTwo(self):
        self.assertEqual([[0, 1]], list(combinationIndexGenerator(2, 2)))
        self.assertEqual([[0], [1]], list(combinationIndexGenerator(2, 1)))

    def test53(self):
        self.assertEqual([[0, 1, 2],
                          [0, 1, 3],
                          [0, 1, 4],
                          [0, 2, 3],
                          [0, 2, 4],
                          [0, 3, 4],
                          [1, 2, 3],
                          [1, 2, 4],
                          [1, 3, 4],
                          [2, 3, 4]], list(combinationIndexGenerator(5, 3)))


class PermutationGeneratorTest(unittest.TestCase):
    def testOne(self):
        self.assertEqual([[0]], list(permutationGenerator(1)))

    def testTwo(self):
        self.assertEqual([[0, 1], [1, 0]], list(permutationGenerator(2)))

    def testThree(self):
        self.assertEqual([[0, 1, 2],
                          [0, 2, 1],
                          [1, 0, 2],
                          [1, 2, 0],
                          [2, 0, 1],
                          [2, 1, 0]], list(permutationGenerator(3)))

    def testNumber(self):
        for i in (4, 5, 6):
            self.assertEqual(factorial(i), len(list(permutationGenerator(i))))


class DyckWordGeneratorTest(unittest.TestCase):
    def testZero(self):
        self.assertEqual([()], list(dyck_word_generator(0)))

    def testOne(self):
        self.assertEqual([(0, 1)], list(dyck_word_generator(1)))

    def testTwo(self):
        self.assertEqual([(0, 1, 0, 1), (0, 0, 1, 1)],
                         list(dyck_word_generator(2)))

    def testNumber(self):
        for i in range(3, 8):
            self.assertEqual(catalan(i), len(list(dyck_word_generator(i))))


class PartitionTest (unittest.TestCase):
    def testForZero(self):
        self.assertEqual([()], [p for p in partitionGenerator(0)])

    def testForOne(self):
        self.assertEqual([(1,)], [p for p in partitionGenerator(1)])

    def testForTwo(self):
        for partition in partitionGenerator(2):
            self.assertEqual(2, sum(partition))
        self.assertEqual(2, len([p for p in partitionGenerator(2)]))
        self.assertEqual([(1, 1)], [p for p in partitionGenerator(2, 1)])

    def testForSix(self):
        for partition in partitionGenerator(6):
            self.assertEqual(6, sum(partition))
        self.assertEqual(11, len([p for p in partitionGenerator(6)]))
        self.assertEqual(7, len([p for p in partitionGenerator(6, 3)]))
        self.assertEqual([(1,)*6], [p for p in partitionGenerator(6, 1)])

    def testForNine(self):
        for partition in partitionGenerator(9):
            self.assertEqual(9, sum(partition))
        self.assertEqual(30, len([p for p in partitionGenerator(9)]))
        self.assertEqual(23, len([p for p in partitionGenerator(9, 5)]))
        self.assertEqual([(1,)*9], [p for p in partitionGenerator(9, 1)])

    def testMaxiExceedNumber(self):
        self.assertEqual(11, len([p for p in partitionGenerator(6, 12)]))

    def testConjugate(self):
        self.assertEqual((3, 2, 2, 1, 1), partition_conjugate((5, 3, 1)))


class OddPartitionTest (unittest.TestCase):
    def setUp(self):
        self.generator = partition_into_odd_generator

    def testForOne(self):
        self.assertEqual([(1,)], list(self.generator(1)))

    def testForTwo(self):
        for partition in self.generator(2):
            self.assertEqual(2, sum(partition))
            self.assertTrue(all(x % 2 for x in partition))
        self.assertEqual(1, len(list(self.generator(2))))
        self.assertEqual([(1, 1)], list(self.generator(2, 1)))

    def testForSix(self):
        for partition in self.generator(6):
            self.assertEqual(6, sum(partition))
            self.assertTrue(all(x % 2 for x in partition))
        # 5+1,3*2,3+1*3,1*6
        self.assertEqual(4, len(list(self.generator(6))))
        self.assertEqual(3, len(list(self.generator(6, 3))))
        self.assertEqual([(1,)*6], list(self.generator(6, 1)))

    def testForNine(self):
        for partition in self.generator(9):
            self.assertEqual(9, sum(partition))
            self.assertTrue(all(x % 2 for x in partition))
        # 9,7+1*2,5+3+1,5+1*4,3*3,3*2+1*3,3+1*6,1*9
        self.assertEqual(8, len(list(self.generator(9))))
        self.assertEqual(6, len(list(self.generator(9, 5))))
        self.assertEqual([(1,)*9], list(self.generator(9, 1)))

    def testMaxiExceedNumber(self):
        self.assertEqual(4, len(list(self.generator(6, 12))))


class PartitionNumberTest (unittest.TestCase):
    def testPartitionNumbersUpto(self):
        self.assertEqual([1], partition_numbers_upto(0))
        self.assertEqual([1, 1, 2], partition_numbers_upto(2))
        # Ramanujan
        p_upto_1000 = partition_numbers_upto(1000)
        self.assertFalse([p for p in p_upto_1000[4::5] if p % 5]) 
        self.assertFalse([p for p in p_upto_1000[5::7] if p % 7]) 
        self.assertFalse([p for p in p_upto_1000[6::11] if p % 11]) 

    def testPartitionNumber(self):
        self.assertEqual(1, partition_number(0))
        self.assertEqual(1, partition_number(1))
        self.assertEqual(2, partition_number(2))
        self.assertEqual(3, partition_number(3))
        self.assertEqual(5, partition_number(4))
        self.assertEqual(30, partition_number(9))
        upto_101 = partition_numbers_upto(101)
        self.assertEqual(upto_101[100],
                         partition_number(100))
        self.assertEqual(upto_101[101],
                         partition_number(101))


class PermutationTest(unittest.TestCase):
    """
    test for permutationGenerator
    """
    def testNumber(self):
        self.assertEqual(factorial(2), len(list(permutationGenerator(2))))
        self.assertEqual(factorial(3), len(list(permutationGenerator(3))))
        self.assertEqual(factorial(4), len(list(permutationGenerator(4))))

    def testIsPermutation(self):
        setof100 = set(range(100))
        # test only first 10, since 100! is to big to test all.
        for i, perm in zip(range(10), permutationGenerator(100)):
            self.assertEqual(100, len(perm))
            self.assertEqual(setof100, set(perm))


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    # doctest
    import nzmath.combinatorial as combinatorial
    suite.addTest(doctest.DocTestSuite(combinatorial))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
