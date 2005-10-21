import unittest
import ring
import rational
from real import theRealField
from imaginary import theComplexField

class CommutativeRingPropertiesTest (unittest.TestCase):
    def setUp(self):
        self.rp = ring.CommutativeRingProperties()
        assert self.rp

    def testIsfield(self):
        assert None == self.rp.isfield()
        self.rp.setIsfield(False)
        assert False == self.rp.isfield()
        self.rp.setIsfield(True)
        assert True == self.rp.isfield()

    def testIseuclidean(self):
        assert None == self.rp.iseuclidean()
        self.rp.setIseuclidean(True)
        assert True == self.rp.iseuclidean()
        self.rp.setIseuclidean(False)
        assert False == self.rp.iseuclidean()

    def testIsfieldImpliesIseuclidean(self):
        self.rp.setIsfield(True)
        assert True == self.rp.iseuclidean()
        self.rp.setIseuclidean(False)
        assert False == self.rp.isfield()

    def testIspid(self):
        assert None == self.rp.ispid()
        self.rp.setIspid(True)
        assert True == self.rp.ispid()
        self.rp.setIspid(False)
        assert False == self.rp.ispid()

    def testIseuclideanImpliesIspid(self):
        self.rp.setIseuclidean(True)
        assert True == self.rp.ispid()
        self.rp.setIspid(False)
        assert False == self.rp.iseuclidean()

    def testIsufd(self):
        assert None == self.rp.isufd()
        self.rp.setIsufd(True)
        assert True == self.rp.isufd()
        self.rp.setIsufd(False)
        assert False == self.rp.isufd()

    def testIspidImpliesIsufd(self):
        self.rp.setIspid(True)
        assert True == self.rp.isufd()
        self.rp.setIsufd(False)
        assert False == self.rp.ispid()

    def testIsnoetherian(self):
        assert None == self.rp.isnoetherian()
        self.rp.setIsnoetherian(True)
        assert True == self.rp.isnoetherian()
        self.rp.setIsnoetherian(False)
        assert False == self.rp.isnoetherian()

    def testIspidImpliesIsnoetherian(self):
        self.rp.setIspid(True)
        assert True == self.rp.isnoetherian()
        self.rp.setIsnoetherian(False)
        assert False == self.rp.ispid()

    def testIsdomain(self):
        assert None == self.rp.isdomain()

    def testIsufdImpliesIsdomain(self):
        self.rp.setIsufd(True)
        assert True == self.rp.isdomain()


class GetRingTest (unittest.TestCase):
    def testInt(self):
        Z = rational.theIntegerRing
        self.assertEqual(Z, ring.getRing(1))
        self.assertEqual(Z, ring.getRing(1L))
        self.assertEqual(rational.Integer(1).getRing(), ring.getRing(rational.Integer(1)))

    def testFloat(self):
        self.assertEqual(theRealField, ring.getRing(1.0))

    def testComplex(self):
        self.assertEqual(theComplexField, ring.getRing(1+1j))

def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
