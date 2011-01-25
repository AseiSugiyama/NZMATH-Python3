import unittest
import sandbox.rewrite as rewrite


class S3Test (unittest.TestCase):
    """
    Test for FiniteGroup using S3 relations.
    """
    def setUp(self):
        """
	set up S3 (the whole group of 3 element permutations).
	"""
        self.S3 = rewrite.Rewrite(alphabet=("a", "b", "A", "B"),
                                  rules={"aa": "",
                                         "bbb": "",
                                         "bab": "a",
                                         "A": "a",
                                         "B": "bb"})

    def testSimplify(self):
        """
	Simplify given strings.
	"""
        self.assertEqual("", self.S3.simplify("aA"))
        self.assertEqual("", self.S3.simplify("baba"))
        self.assertEqual("", self.S3.simplify("BABA"))
        self.assertEqual("a", self.S3.simplify("abbb"))
        self.assertEqual("b", self.S3.simplify("bbbb"))
        self.assert_(len(self.S3.simplify("abaBbAbabababbbabaaaababbaabb")) < 6)

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
