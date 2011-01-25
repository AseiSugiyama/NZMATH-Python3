import unittest
import sandbox.dlp as dlp

class DLPTest(unittest.TestCase):
    def testSilverPohligHellman(self):
        self.assertEqual(6, dlp.SilverPohligHellman(-2, 3, 17))
        self.assertEqual(78, dlp.SilverPohligHellman(71, 6, 109))


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
