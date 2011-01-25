from __future__ import division
import unittest
import sandbox.cartesian as cartesian


class TrivialTest (unittest.TestCase):
    def testEq(self):
        c = cartesian.Cartesian((1, 2, 3))
        self.assertEqual(c, c)

    def testNe(self):
        c = cartesian.Cartesian((1, 2, 3))
        self.assertNotEqual(c, cartesian.Cartesian((1, 2))) # shorter
        self.assertNotEqual(c, cartesian.Cartesian((1, 2, 3, 4))) # longer
        self.assertNotEqual(c, (1, 2, 3)) # different type

    def testPos(self):
        c = cartesian.Cartesian((1, 2, 3))
        self.assertEqual(c, +c)

    def testLen(self):
        c = cartesian.Cartesian((1, 2, 3))
        self.assertEqual(3, len(c))

    def testGetitem(self):
        c = cartesian.Cartesian((1, 2, 3))
        self.assertEqual(3, c[2])
        self.assertRaises(IndexError, c.__getitem__, 3)
        self.assertEqual(cartesian.Cartesian((1, 2)), c[:2])


class BinaryMethodsTest (unittest.TestCase):
    def setUp(self):
        self.c1 = cartesian.Cartesian((1, 2, 3))
        self.c2 = cartesian.Cartesian((4, 2, 7))

    def tearDown(self):
        pass

    def testAdd(self):
        s = cartesian.Cartesian((5, 4, 10))
        self.assertEqual(s, self.c1 + self.c2)
        self.assertEqual(s, self.c2 + self.c1)
        self.assertEqual(s, self.c1 + (4, 2, 7))

    def testSub(self):
        d1 = cartesian.Cartesian((-3, 0, -4))
        d2 = cartesian.Cartesian((3, 0, 4))
        self.assertEqual(d1, self.c1 - self.c2)
        self.assertEqual(d2, self.c2 - self.c1)
        self.assertEqual(d1, self.c1 - (4, 2, 7))

    def testMul(self):
        p = cartesian.Cartesian((4, 4, 21))
        self.assertEqual(p, self.c1 * self.c2)
        self.assertEqual(p, self.c2 * self.c1)
        self.assertEqual(p, self.c1 * (4, 2, 7))

    def testTruediv(self):
        q1 = cartesian.Cartesian((0.25, 1, 0.42857142857142855))
        q2 = cartesian.Cartesian((4, 1, 2.33333333333333333))
        self.assertEqual(q1, self.c1 / self.c2)
        self.assertEqual(q2, self.c2 / self.c1)
        self.assertEqual(q1, self.c1 / (4, 2, 7))

    def testFloordiv(self):
        q1 = cartesian.Cartesian((0, 1, 0))
        q2 = cartesian.Cartesian((4, 1, 2))
        self.assertEqual(q1, self.c1 // self.c2)
        self.assertEqual(q2, self.c2 // self.c1)
        self.assertEqual(q1, self.c1 // (4, 2, 7))

    def testMod(self):
        m1 = cartesian.Cartesian((1, 0, 3))
        m2 = cartesian.Cartesian((0, 0, 1))
        self.assertEqual(m1, self.c1 % self.c2)
        self.assertEqual(m2, self.c2 % self.c1)
        self.assertEqual(m1, self.c1 % (4, 2, 7))

    def testDivmod(self):
        qm1 = cartesian.Cartesian(((0, 1), (1, 0), (0, 3)))
        qm2 = cartesian.Cartesian(((4, 0), (1, 0), (2, 1)))
        self.assertEqual(qm1, divmod(self.c1, self.c2))
        self.assertEqual(qm2, divmod(self.c2, self.c1))
        self.assertEqual(qm1, divmod(self.c1, (4, 2, 7)))


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
