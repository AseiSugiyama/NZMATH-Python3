import unittest
import trialdivision

class TrialdivisionTest (unittest.TestCase):
    def runTest(self):
        assert trialdivision.trial(60) == [(2,2),(3,1),(5,1)]
        assert trialdivision.trial(128) == [(2,7)]
        assert trialdivision.trial(200819) == [(409,1),(491,1)]
        assert trialdivision.trial(1042387) ==  [(701,1),(1487,1)]
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TrialdivisionTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
