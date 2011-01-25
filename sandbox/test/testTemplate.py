import unittest
import sandbox.hoge as hoge

class HogeTest (unittest.TestCase):
    """
    Test classes must inherite unittest.TestCase.
    They have name suffixed with 'Test'.
    """
    def setUp(self):
        """
	setUp is run before each test method run.
	"""
        pass

    def tearDown(self):
        """
	tearDown is run after each test method run.
	"""
        pass

    def testHuga(self):
        """
	Every test method have name prefixed with 'test'.
	"""
	# asserting something
        self.assert_(hoge.ishoge(), "optional message string")
	# asserting equality
        self.assertEqual(1, hoge.huga)

# The following part is always unedited.
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
