import unittest
import nzmath.poly.univar as univar


class BasicPolynomialTest (unittest.TestCase):
    def setUp(self):
        self.f = univar.BasicPolynomial({0:1, 1:2, 4:3})
        self.g = univar.BasicPolynomial({1:-1, 3:2})

    def testAdd(self):
        h = univar.BasicPolynomial({0:1, 1:1, 3:2, 4:3})
        self.assertEqual(h, self.f + self.g)
        self.assertEqual(h, self.g + self.f)

    def testNeg(self):
        h = univar.BasicPolynomial({0:-1, 1:-2, 4:-3})
        self.assertEqual(h, -self.f)

    def testMul(self):
        h = univar.BasicPolynomial({1:-1, 2:-2, 3:2, 4:4, 5:-3, 7:6})
        self.assertEqual(h, self.f * self.g)
        self.assertEqual(h, self.g * self.f)

    def testPow(self):
        h1 = univar.BasicPolynomial({0:1, 1:4, 2:4, 4:6, 5:12, 8:9})
        h2 = univar.BasicPolynomial({3:-1, 5:6, 7:-12, 9:8})
        self.assertEqual(h1, self.f ** 2)
        self.assertEqual(h2, self.g ** 3)

    def testDifferentiate(self):
        h = univar.BasicPolynomial({0:-1, 2:6})
        self.assertEqual(h, self.g.differentiate())

    def testSubstitution(self):
        self.assertEqual(45, self.f(-2))


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
