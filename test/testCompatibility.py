import unittest
import nzmath.compatibility


class SetTest(unittest.TestCase):
    def testSet(self):
        """
        set and frozen set is ready to use.
        """
        self.assertTrue(set([1]))
        self.assertTrue(frozenset([1]))


class CardTest(unittest.TestCase):
    def testCardInsteadofLen(self):
        """
        card() instead of len()
        """
        self.assertEqual(1, card(set([1])))
        self.assertRaises(TypeError, card, 1)

    def testMethodCard(self):
        """
        card() for virtual sets
        """
        class VirtualSet(object):
            def card(self):
                return 2**1000

        self.assertEqual(2**1000, card(VirtualSet()))
        self.assertRaises(TypeError, len, VirtualSet())

    def testLenCompatibility(self):
        """
        Old style is problematic.

        If this test will fail, replace the assertion line to ensure
        the correctness of len with:
        self.assertEqual(2**1000, len(VirtualSet()))
        """
        class VirtualSet(object):
            def __len__(self):
                return 2**1000

        self.assertRaises(OverflowError, len, VirtualSet())

        
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
