import unittest
import nzmath.poly.ratfunc as ratfunc
import nzmath.poly.uniutil as uniutil
import nzmath.poly.ring as ring
from nzmath.rational import theRationalField as Q
from nzmath.rational import theIntegerRing as Z


class RationalFunctionTest (unittest.TestCase):
    def setUp(self):
        self.f = ratfunc.RationalFunction(uniutil.polynomial({3:1, 0:1}, Z),
                                          uniutil.polynomial({2:1, 0:-2}, Z))
        self.f2 = self.f
        self.f3 = ratfunc.RationalFunction(uniutil.polynomial({4:1, 1:1}, Z),
                                           uniutil.polynomial({3:1, 1:-2}, Z))

    def testInit(self):
        self.assert_(self.f)

    def testEquals(self):
        self.assertEqual(self.f, self.f2)
        self.assertEqual(self.f, self.f3)

    def testGetRing(self):
        self.assert_(isinstance(self.f.getRing(), ring.RationalFunctionField))
        self.assertEqual(ring.RationalFunctionField(Q, 1), self.f.getRing())


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
