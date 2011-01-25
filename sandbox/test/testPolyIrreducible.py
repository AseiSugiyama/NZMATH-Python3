import unittest
import sandbox.poly.irreducible as irreducible
import nzmath.poly.uniutil as uniutil
import nzmath.rational as rational


Z = rational.theIntegerRing


class IrreducibleTest (unittest.TestCase):
    def setUp(self):
        """
	set up some polynomials
	"""
        self.f1 = uniutil.polynomial(enumerate([3, 6, 81, 1]), Z)
        self.f2 = uniutil.polynomial(enumerate([1, 81, 6, 3]), Z)
        self.f3 = uniutil.polynomial(enumerate([37, 6, 18, 1]), Z)
        self.f4 = uniutil.polynomial(enumerate([91, 7, 14, 1]), Z)
        # f5 = (x - 6)(x - 5)...x(x + 1)(x + 2) - 1
        self.f5 = uniutil.polynomial(enumerate([1439, -1368, -1324,
                                                1638, -231, -252,
                                                114, -18, 1]), Z)

    def testDumas(self):
        """
	test by Dumas's method
	"""
        self.assert_(irreducible.dumas(self.f1, 3))
        self.assert_(irreducible.dumas(self.f2, 3))
        self.assertEqual(None, irreducible.dumas(self.f2, 2))

    def testPerron(self):
        """
	test by Perron's method
	"""
        self.assert_(irreducible.perron(self.f1))
        self.assertEqual(None, irreducible.perron(self.f2), "non-monic")

    def testOsada(self):
        """
	test by Osada's method
	"""
        self.assertEqual(None, irreducible.osada(self.f1), "constant is small")
        self.assertEqual(None, irreducible.osada(self.f2), "non-monic")
        self.assert_(irreducible.osada(self.f3))
        self.assertEqual(None, irreducible.osada(self.f4), "composite constant")

    def testPolya(self):
        """
	test by Osada's method
	"""
        self.assert_(irreducible.polya(self.f5))
        self.assertEqual(False, irreducible.polya(self.f5 + 1))


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
