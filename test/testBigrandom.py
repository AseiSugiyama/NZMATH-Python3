import unittest
import random
import nzmath.bigrandom as bigrandom


class BigrandomTest(unittest.TestCase):
    def testUniform(self):
        trial_times = 100000
        error_range = 0.03 

        dist = {}
        for i in range(5, 100, 10):
            dist[i] = 0
        for i in range(trial_times):
            rnd = bigrandom.randrange(5, 100, 10)
            dist[rnd] += 1
        for i in range(5, 100, 10):
            self.assertTrue(abs(0.1 - dist[i]/float(trial_times)) < error_range)

        dist = {}
        for i in range(trial_times):
            rnd = bigrandom.randrange(-1, 255)
            dist[rnd] = dist.get(rnd, 0) + 1
        distkeys = dist.keys()
        distkeys.sort()
        self.assertEqual(distkeys, range(-1, 255))

    def testRange(self):
        for i in range(10000):
            start = random.randrange(-5000, 1)**3
            stop = random.randrange(1, 5000)**3
            step = random.randrange(1, 200)
            d = bigrandom.randrange(start, stop, step)
            self.assertEqual(0, (d - start) % step)
            self.assertTrue(start <= d < stop)
            d = bigrandom.randrange(start**2, -stop**2, -step)
            self.assertEqual(0, (d - start**2) % step)
            self.assertTrue(start**2 >= d > -stop**2)

    def testHugeRange(self):
        self.assertTrue(2 <= bigrandom.randrange(2, 10**500) < 10**500)

    def testValueError(self):
        self.assertRaises(ValueError, bigrandom.randrange, 1, 50, 0)
        self.assertRaises(ValueError, bigrandom.randrange, 0.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 4.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 20, 1.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 2)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 3)


class ChoiceTest (unittest.TestCase):
    """
    tests for bigrandom.map_choice
    """
    def testidentity(self):
        i = lambda x: x
        self.assertTrue(0 <= bigrandom.map_choice(i, 2**100) < 2**100)

    def testeven(self):
        double = lambda x: x + x
        self.assertTrue(0 <= bigrandom.map_choice(double, 2**100) < 2**101)
        self.assertEqual(0, bigrandom.map_choice(double, 2**100) % 2)

    def testpartial(self):
        def odd(n):
            """
            Return None for even numbers.
            """
            if n % 2:
                return n
        self.assertEqual(1, bigrandom.map_choice(odd, 2**100) % 2)


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
