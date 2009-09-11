from __future__ import division
import unittest
from nzmath.plugins import MATHMODULE as math, CMATHMODULE as cmath, \
     FLOATTYPE as Float, COMPLEXTYPE as Complex, \
     CHECK_REAL_OR_COMPLEX, PRECISION_CHANGEABLE, SETPRECISION


class ModulesTest(unittest.TestCase):
    """
    MATHMODULE and CMATHMODULE provide math and cmath compatible
    modules.  The requirement is Python 2.5 compatibility.
    """
    def testMath(self):
        math_members = ('acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
                        'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp',
                        'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow',
                        'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh')
        for member in math_members:
            self.assert_(member in dir(math), member)

    def testCmath(self):
        cmath_members = ('acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh',
                         'cos', 'cosh', 'e', 'exp', 'log', 'log10', 'pi', 'sin',
                         'sinh', 'sqrt', 'tan', 'tanh')
        for member in cmath_members:
            self.assert_(member in dir(cmath), member)


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
