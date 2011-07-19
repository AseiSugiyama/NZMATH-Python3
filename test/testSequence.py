import unittest
import nzmath.sequence as sequence

class SequenceTest(unittest.TestCase):
    def testGeneratorFibonacci(self):
        gf = sequence.generator_fibonacci(40)
        fibo_40 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
            987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025,
            121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578,
            5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155]
        self.assertEqual(fibo_40, [i for i in gf])

    def testFibonacci(self):
        self.assertEqual(1, sequence.fibonacci(1))
        self.assertEqual(1, sequence.fibonacci(2))
        self.assertEqual(2, sequence.fibonacci(3))
        self.assertEqual(3, sequence.fibonacci(4))
        self.assertEqual(5, sequence.fibonacci(5))
        self.assertEqual(12586269025, sequence.fibonacci(50))
        self.assertEqual(354224848179261915075, sequence.fibonacci(100))

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
