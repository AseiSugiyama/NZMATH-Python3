import unittest
import ring

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CommutativeRingPropertiesTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
