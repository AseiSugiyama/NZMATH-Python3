import unittest
import operator
import sandbox.chainop as chainop


class BasicChainTest (unittest.TestCase):
    def testBasicChain(self):
        double = lambda x: x * 2
        self.assertEqual(62, chainop.basic_chain((operator.add, double), 2, 31))
        square = lambda x: x ** 2
        self.assertEqual(2**31, chainop.basic_chain((operator.mul, square), 2, 31))


class MultiChainTest (unittest.TestCase):
    def testMultiChain(self):
        double = lambda x: x * 2
        self.assertEqual([62, 93], chainop.multi_chains((operator.add, double), (2, 3), 31))
        square = lambda x: x ** 2
        self.assertEqual([2**31, 3**31], chainop.multi_chains((operator.mul, square), [2, 3], 31))


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
