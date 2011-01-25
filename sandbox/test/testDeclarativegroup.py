import unittest
import sandbox.declarativegroup as declarativegroup

# aux
import operator
import nzmath.finitefield as finitefield
import sandbox.rewrite as rewrite


class S3Test (unittest.TestCase):
    """
    Test for FiniteGroup using S3 relations.
    """
    def setUp(self):
        """
	set up S3 (the whole group of 3 element permutations).
	"""
        rewriteS3 = rewrite.Rewrite(alphabet=("a", "b", "A", "B"),
                                    rules={"aa": "",
                                           "bbb": "",
                                           "bab": "a",
                                           "A": "a",
                                           "B": "bb"})
        def mul(a, b):
            return rewriteS3.simplify(a + b)
        def inv(a):
            return a.swapcase()[::-1]
        self.S3 = declarativegroup.declare_group(
            rewriteS3, "", mul, inv,
            properties={"finite": True, "grouporder": 6})

    def testClass(self):
        """
	class of self.S3 is FiniteGroup
	"""
        self.assertEqual(declarativegroup.FiniteGroup, self.S3.__class__)
        self.assertEqual(6, self.S3.grouporder)

    def testContains(self):
        """
        Whether or not each given string is a string on the alphabet,
        i.e., the string is in the Kleene closure.
        """
        # valid strings
        self.assert_("abaBbAbabababbbabaaaababbaabb" in self.S3)
        self.assert_("" in self.S3)
        # an invalid string
        self.assert_("abaBbAbabababbbabdaaababbaabb" not in self.S3)

    def testOp2(self):
        """
        Automatically defined op2 works.
        """
        self.assertEqual("", self.S3.op2('a', 0))
        self.assertEqual("a", self.S3.op2('a', 1))
        self.assertEqual("", self.S3.op2('a', 2))
        self.assertEqual("", self.S3.op2('a', 100))
        self.assertEqual("", self.S3.op2('b', 3))
        self.assertEqual("", self.S3.op2('b', -3))
        self.assertEqual("", self.S3.op2('B', 3))
        self.assertEqual("", self.S3.op2('ab', 2))
        self.assertEqual("", self.S3.op2('ba', 2))

    def testElementOrder(self):
        """
        elementorder method returns the order of given element.
        """
        self.assertEqual(1, self.S3.elementorder(""))
        self.assertEqual(2, self.S3.elementorder("a"))
        self.assertEqual(2, self.S3.elementorder("A")) # =a
        self.assertEqual(2, self.S3.elementorder("ab"))
        self.assertEqual(2, self.S3.elementorder("ba"))
        self.assertEqual(3, self.S3.elementorder("b"))
        self.assertEqual(3, self.S3.elementorder("bb"))
        self.assertEqual(3, self.S3.elementorder("B")) # = bb


class F7MultiplicativeTest (unittest.TestCase):
    """
    Test for FiniteAbelianGroup using multiplicative group of F7.
    """
    def setUp(self):
        """
	set up F7 (the field with exactly seven elements).
	"""
        F7 = finitefield.FinitePrimeField.getInstance(7)
        self.F7m = declarativegroup.declare_group(
            [F7.createElement(i) for i in range(1, 7)],
            F7.one, operator.mul, finitefield.FinitePrimeFieldElement.inverse,
            properties={"finite": True, "abelian": True, "grouporder": 6})

    def testClass(self):
        """
	class of self.F7m is FiniteAbelianGroup
	"""
        self.assertEqual(declarativegroup.FiniteAbelianGroup, self.F7m.__class__)
        self.assertEqual(6, self.F7m.grouporder)

    def testContains(self):
        """
        Whether or not given element of F7 is in multiplicative group.
        """
        F7 = finitefield.FinitePrimeField.getInstance(7)
        # valid elements
        self.assert_(F7.one in self.F7m)
        self.assert_(F7.createElement(3) in self.F7m)
        # an invalid element
        self.assert_(F7.zero not in self.F7m)

    def testOp2(self):
        """
        Automatically defined op2 works.
        """
        F7 = finitefield.FinitePrimeField.getInstance(7)
        self.assertEqual(F7.one, self.F7m.unity)
        self.assertEqual(F7.one, self.F7m.op2(F7.createElement(2), 0))
        self.assertEqual(self.F7m.baseset[1], self.F7m.op2(self.F7m.baseset[1], 1))
        self.assertEqual(self.F7m.baseset[3], self.F7m.op2(self.F7m.baseset[1], 2))
        self.assertEqual(self.F7m.unity, self.F7m.op2(self.F7m.baseset[1], 3))
        self.assertEqual(self.F7m.baseset[-1], self.F7m.op2(self.F7m.baseset[2], 3))

    def testElementOrder(self):
        """
        elementorder method returns the order of given element.
        """
        self.assertEqual(1, self.F7m.elementorder(self.F7m.baseset[0]))
        self.assertEqual(3, self.F7m.elementorder(self.F7m.baseset[1]))
        self.assertEqual(6, self.F7m.elementorder(self.F7m.baseset[2]))
        self.assertEqual(3, self.F7m.elementorder(self.F7m.baseset[3]))
        self.assertEqual(6, self.F7m.elementorder(self.F7m.baseset[4]))
        self.assertEqual(2, self.F7m.elementorder(self.F7m.baseset[5]))


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
