import unittest
import nzmath.squarefree as squarefree


class SquarefreeTest (unittest.TestCase):
    def testLenstra(self):
        lenstra = squarefree.lenstra
        self.assertTrue(lenstra(1))
        self.assertTrue(lenstra(3))
        self.assertTrue(lenstra(5))
        self.assertTrue(lenstra(7))
        self.assertRaises(squarefree.Undetermined, lenstra, 9)
        self.assertTrue(lenstra(11))
        self.assertTrue(lenstra(13))
        self.assertRaises(squarefree.Undetermined, lenstra, 15)

    def testTrivial(self):
        trivial = squarefree.trivial_test
        self.assertTrue(trivial(1), "1 is squarefree")
        self.assertTrue(trivial(2), "prime is squarefree")
        self.assertTrue(trivial(3), "prime is squarefree")
        self.assertFalse(trivial(4), "2*2 is not squarefree")
        self.assertTrue(trivial(5), "prime is squarefree")
        self.assertRaises(squarefree.Undetermined, trivial, 6)
        self.assertTrue(trivial(7), "prime is squarefree")
        self.assertFalse(trivial(8), "2*2*2 is not squarefree")
        self.assertFalse(trivial(9), "3*3 is not squarefree")
        self.assertRaises(squarefree.Undetermined, trivial, 15)

    def testTrialDivision(self):
        trial = squarefree.trial_division
        self.assertTrue(trial(1), "1 is squarefree")
        self.assertTrue(trial(2), "prime is squarefree")
        self.assertTrue(trial(3), "prime is squarefree")
        self.assertFalse(trial(4), "2*2 is not squarefree")
        self.assertTrue(trial(5), "prime is squarefree")
        self.assertTrue(trial(6), "2*3 is squarefree")
        self.assertTrue(trial(7), "prime is squarefree")
        self.assertFalse(trial(8), "2*2*2 is not squarefree")
        self.assertFalse(trial(9), "3*3 is not squarefree")
        self.assertTrue(trial(15), "3*5 is squarefree")


class TernaryTest (unittest.TestCase):
    def testLenstra(self):
        lenstra = squarefree.lenstra_ternary
        self.assertTrue(lenstra(1))
        self.assertTrue(lenstra(3))
        self.assertTrue(lenstra(5))
        self.assertTrue(lenstra(7))
        self.assertTrue(None is lenstra(9), lenstra(9))
        self.assertTrue(lenstra(11))
        self.assertTrue(lenstra(13))
        self.assertTrue(None is lenstra(15))

    def testTrivial(self):
        trivial = squarefree.trivial_test_ternary
        self.assertTrue(trivial(1), "1 is squarefree")
        self.assertTrue(trivial(2), "prime is squarefree")
        self.assertTrue(trivial(3), "prime is squarefree")
        self.assertFalse(trivial(4), "2*2 is not squarefree")
        self.assertTrue(trivial(5), "prime is squarefree")
        self.assertTrue(None is trivial(6))
        self.assertTrue(trivial(7), "prime is squarefree")
        self.assertFalse(trivial(8), "2*2*2 is not squarefree")
        self.assertFalse(trivial(9), "3*3 is not squarefree")
        self.assertTrue(None is trivial(15))

    def testTrialDivision(self):
        trial = squarefree.trial_division_ternary
        self.assertTrue(trial(1), "1 is squarefree")
        self.assertTrue(trial(2), "prime is squarefree")
        self.assertTrue(trial(3), "prime is squarefree")
        self.assertFalse(trial(4), "2*2 is not squarefree")
        self.assertTrue(trial(5), "prime is squarefree")
        self.assertTrue(trial(6), "2*3 is squarefree")
        self.assertTrue(trial(7), "prime is squarefree")
        self.assertFalse(trial(8), "2*2*2 is not squarefree")
        self.assertFalse(trial(9), "3*3 is not squarefree")
        self.assertTrue(trial(15), "3*5 is squarefree")


class SquarefreeDecompositionMethodTest (unittest.TestCase):
    def testViaDecomposition(self):
        decomp = squarefree.viadecomposition
        self.assertTrue(decomp(1), "1 is squarefree")
        self.assertTrue(decomp(2), "prime is squarefree")
        self.assertTrue(decomp(3), "prime is squarefree")
        self.assertFalse(decomp(4), "2*2 is not squarefree")
        self.assertTrue(decomp(5), "prime is squarefree")
        self.assertTrue(decomp(6), "2*3 is squarefree")
        self.assertTrue(decomp(7), "prime is squarefree")
        self.assertFalse(decomp(8), "2*2*2 is not squarefree")
        self.assertFalse(decomp(9), "3*3 is not squarefree")
        self.assertTrue(decomp(15), "3*5 is squarefree")
        self.assertFalse(decomp(27), "3*3*3 is not squarefree")
        # a Carmichael number
        c = 1296000000048526524000605664488558519786723203009
        # no factorization of c is needed and thus reasonablly fast
        self.assertTrue(decomp(101 * c))
        # prime power (97 ** 3)
        self.assertFalse(decomp(2738019), "3 * 97**3")
        # square ((97 * 101) ** 2)
        self.assertFalse(decomp(287943627), "3 * 97**2 * 101**2")
        self.assertFalse(decomp(101 * c ** 2), "101 * c **2")


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
