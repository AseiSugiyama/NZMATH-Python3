import unittest
import sandbox.squarefree as squarefree


class SquarefreeTest (unittest.TestCase):
    def testLenstra(self):
        lenstra = squarefree.lenstra
        self.assert_(lenstra(1))
        self.assert_(lenstra(3))
        self.assert_(lenstra(5))
        self.assert_(lenstra(7))
        self.assertRaises(squarefree.Undetermined, lenstra, 9)
        self.assert_(lenstra(11))
        self.assert_(lenstra(13))
        self.assertRaises(squarefree.Undetermined, lenstra, 15)

    def testTrivial(self):
        trivial = squarefree.trivial_test
        self.assert_(trivial(1), "1 is squarefree")
        self.assert_(trivial(2), "prime is squarefree")
        self.assert_(trivial(3), "prime is squarefree")
        self.failIf(trivial(4), "2*2 is not squarefree")
        self.assert_(trivial(5), "prime is squarefree")
        self.assertRaises(squarefree.Undetermined, trivial, 6)
        self.assert_(trivial(7), "prime is squarefree")
        self.failIf(trivial(8), "2*2*2 is not squarefree")
        self.failIf(trivial(9), "3*3 is not squarefree")
        self.assertRaises(squarefree.Undetermined, trivial, 15)

    def testTrialDivision(self):
        trial = squarefree.trial_division
        self.assert_(trial(1), "1 is squarefree")
        self.assert_(trial(2), "prime is squarefree")
        self.assert_(trial(3), "prime is squarefree")
        self.failIf(trial(4), "2*2 is not squarefree")
        self.assert_(trial(5), "prime is squarefree")
        self.assert_(trial(6), "2*3 is squarefree")
        self.assert_(trial(7), "prime is squarefree")
        self.failIf(trial(8), "2*2*2 is not squarefree")
        self.failIf(trial(9), "3*3 is not squarefree")
        self.assert_(trial(15), "3*5 is squarefree")


class TernaryTest (unittest.TestCase):
    def testLenstra(self):
        lenstra = squarefree.lenstra_ternary
        self.assert_(lenstra(1))
        self.assert_(lenstra(3))
        self.assert_(lenstra(5))
        self.assert_(lenstra(7))
        self.assert_(None is lenstra(9), lenstra(9))
        self.assert_(lenstra(11))
        self.assert_(lenstra(13))
        self.assert_(None is lenstra(15))

    def testTrivial(self):
        trivial = squarefree.trivial_test_ternary
        self.assert_(trivial(1), "1 is squarefree")
        self.assert_(trivial(2), "prime is squarefree")
        self.assert_(trivial(3), "prime is squarefree")
        self.failIf(trivial(4), "2*2 is not squarefree")
        self.assert_(trivial(5), "prime is squarefree")
        self.assert_(None is trivial(6))
        self.assert_(trivial(7), "prime is squarefree")
        self.failIf(trivial(8), "2*2*2 is not squarefree")
        self.failIf(trivial(9), "3*3 is not squarefree")
        self.assert_(None is trivial(15))

    def testTrialDivision(self):
        trial = squarefree.trial_division_ternary
        self.assert_(trial(1), "1 is squarefree")
        self.assert_(trial(2), "prime is squarefree")
        self.assert_(trial(3), "prime is squarefree")
        self.failIf(trial(4), "2*2 is not squarefree")
        self.assert_(trial(5), "prime is squarefree")
        self.assert_(trial(6), "2*3 is squarefree")
        self.assert_(trial(7), "prime is squarefree")
        self.failIf(trial(8), "2*2*2 is not squarefree")
        self.failIf(trial(9), "3*3 is not squarefree")
        self.assert_(trial(15), "3*5 is squarefree")


class SquarefreeDecompositionMethodTest (unittest.TestCase):
    def testViaDecomposition(self):
        decomp = squarefree.viadecomposition
        self.assert_(decomp(1), "1 is squarefree")
        self.assert_(decomp(2), "prime is squarefree")
        self.assert_(decomp(3), "prime is squarefree")
        self.failIf(decomp(4), "2*2 is not squarefree")
        self.assert_(decomp(5), "prime is squarefree")
        self.assert_(decomp(6), "2*3 is squarefree")
        self.assert_(decomp(7), "prime is squarefree")
        self.failIf(decomp(8), "2*2*2 is not squarefree")
        self.failIf(decomp(9), "3*3 is not squarefree")
        self.assert_(decomp(15), "3*5 is squarefree")
        self.failIf(decomp(27), "3*3*3 is not squarefree")
        # a Carmichael number
        c = 1296000000048526524000605664488558519786723203009
        # no factorization of c is needed and thus reasonablly fast
        self.assert_(decomp(101 * c))


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
