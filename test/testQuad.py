import unittest
import nzmath.quad as quad

class QuadTest (unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testComputeClassNumber(self):
        self.assert_(quad.computeClassNumber(-4))
        self.assertEqual((1, [[1, 0, 1]]), quad.computeClassNumber(-4))
        self.assertEqual(1, quad.computeClassNumber(-3)[0])
        self.assertEqual(1, len(quad.computeClassNumber(-3)[1]))
        self.assertEqual(2, quad.computeClassNumber(-15)[0])
        self.assertEqual(2, len(quad.computeClassNumber(-15)[1]))
        self.assertEqual(3, quad.computeClassNumber(-23)[0])
        self.assertEqual(4, quad.computeClassNumber(-39)[0])
        self.assertEqual(5, quad.computeClassNumber(-47)[0])
        self.assertEqual(6, quad.computeClassNumber(-87)[0])
        self.assertEqual(7, quad.computeClassNumber(-71)[0])
        # -1 % 4 == 3
        self.assertRaises(ValueError, quad.computeClassNumber, -1)
        # 5 > 0
        self.assertRaises(ValueError, quad.computeClassNumber, 5)


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
