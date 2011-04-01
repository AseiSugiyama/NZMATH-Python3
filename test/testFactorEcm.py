import unittest
import logging
import nzmath.factor.ecm as ecm

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(message)s')

class EcmTest (unittest.TestCase):
    curve_types = (ecm.A1, ecm.A2, ecm.A3, ecm.A4, ecm.A5, ecm.B, ecm.S)

    def test_26927_63719(self):
        n = 26927*63719
        for curve_type in self.curve_types:
            f = ecm.ecm(n, curve_type)
            self.assertTrue(n % f == 0)

    def test_152077_172259(self):
        n = 152077*172259
        for curve_type in self.curve_types:
            f = ecm.ecm(n, curve_type)
            self.assertTrue(n % f == 0)

    # the following tests can take too long time.
    def xxxtestRun(self):
        for n in (71917*71993,
                  99991*99961,
                  123457*21121,
                  199967*199999,
                  1067063*3682177,
                  111999991*1234111111111111111111, #EF=9digits
                  1234567890123456789012345678901, #EF=13digits
                  148139754736864591*38681321803817920159601, # EF=18digits
                  ):
            for curve_type in self.curve_types:
                f = ecm.ecm(n, curve_type)
                self.assertTrue(n % f == 0)

    def xxxtestM67(self):
        n = 2**67 - 1 #n has 21 digits, #EF=9 digits
        for curve_type in self.curve_types:
            f = ecm.ecm(n, curve_type)
            self.assertTrue(n % f == 0)

    def xxxtestF7(self):
        n = 2**(2**7) + 1 #Ef=17digits
        for curve_type in self.curve_types:
            f = ecm.ecm(n, curve_type)
            self.assertTrue(n % f == 0)


class BoundsTest (unittest.TestCase):
    def testFirst(self):
        self.assertEqual(1000, ecm.Bounds(10**19).first)
        self.assertEqual(10000, ecm.Bounds(10**24).first)
        self.assertEqual(100000, ecm.Bounds(10**29).first)

    def testSecond(self):
        self.assertEqual(50000, ecm.Bounds(10**19).second)
        self.assertEqual(500000, ecm.Bounds(10**24).second)
        self.assertEqual(5000000, ecm.Bounds(10**29).second)

    def testIncrement(self):
        b = ecm.Bounds(10**19)
        self.assertEqual(1000, b.first)
        self.assertEqual(50000, b.second)
        b.increment()
        self.assertEqual(10000, b.first)
        self.assertEqual(500000, b.second)
        b.increment()
        self.assertEqual(100000, b.first)
        self.assertEqual(5000000, b.second)
        b.increment()
        self.assertEqual(1000000, b.first)
        self.assertEqual(50000000, b.second)


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
