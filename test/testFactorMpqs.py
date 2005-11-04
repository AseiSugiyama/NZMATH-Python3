import unittest
import nzmath.factor.mpqs as mpqs


class FactorTest (unittest.TestCase):
    def testMPQS(self):
        p = 4 * 6133 + 1
        result = mpqs.mpqs(p*154858631)
        self.assertEqual([(p,1), (154858631,1)], result)


def suite():
    suite = unittest.makeSuite(FactorTest, 'test');
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
