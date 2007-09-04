import unittest
import nzmath.compatibility


class CompatibilityTest (unittest.TestCase):
    def testSet(self):
        """
        set and frozen set is ready to use.
        """
        self.assert_(set([1]))
        self.assert_(frozenset([1]))


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
