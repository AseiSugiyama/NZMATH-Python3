import unittest
import random
import bigrandom

trial_times = 100000
error_range = 0.03 

class BigrandomTest(unittest.TestCase):
    def testUniform(self):
        generated = {}
        for i in range(5,100,10):
            generated[i] = 0
        for i in range(trial_times):
            rnd = bigrandom.randrange(5,100,10)
            generated[rnd] += 1
        for i in range(5,100,10):
            assert abs(0.1 - generated[i]/float(trial_times)) < error_range

    def testRange(self):
        start = stop = step = 1
        for i in range(10000):
            start = random.randrange(-5000, 1)**3
            stop = random.randrange(1, 5000)**3
            step = random.randrange(1, 200)
            d = bigrandom.randrange(start, stop, step)
            assert (d - start)%step == 0
            assert start <= d < stop
            d = bigrandom.randrange(start**2, -stop**2, -step)
            assert (d - start**2)%step == 0
            assert start**2 >= d > -stop**2

    def testValueError(self):
        self.assertRaises(ValueError, bigrandom.randrange, 1, 50, 0)
        self.assertRaises(ValueError, bigrandom.randrange, 0.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 4.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 20, 1.5)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 2)
        self.assertRaises(ValueError, bigrandom.randrange, 3, 3)

def suite():
    suite = unittest.TestSuite() 
    suite.addTest(BigrandomTest("testRange"))
    suite.addTest(BigrandomTest("testValueError"))
    suite.addTest(BigrandomTest("testUniform"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

