import unittest
import itertools
from sys import maxint
import nzmath.bigrange as bigrange


class CountTest (unittest.TestCase):
    def testCount(self):
        from_maxint = [maxint, maxint+1, maxint+2]
        self.assertEqual(from_maxint,
                         [i for i in itertools.islice(bigrange.count(maxint), 3)])
        # otoh, itertools.count raises ...
        self.assertRaises(OverflowError,
                          itertools.islice(itertools.count(maxint), 3).next)


class ProgressionTest (unittest.TestCase):
    def testArithmeticProgression(self):
        from_maxint = [maxint, maxint+1, maxint+2]
        self.assertEqual(from_maxint,
                         [i for i in itertools.islice(bigrange.arithmetic_progression(maxint, 1), 3)])

    def testGeometricProgression(self):
        self.assertEqual([3, 6, 12, 24],
                         [i for i in itertools.islice(bigrange.geometric_progression(3, 2), 4)])


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
