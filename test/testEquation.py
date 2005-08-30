from __future__ import division
import unittest
import equation

class GlobalEquationTest (unittest.TestCase):
    def test_e1(self):
        assert -3/2 == equation.e1([3, 2])

def suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GlobalEquationTest, "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
