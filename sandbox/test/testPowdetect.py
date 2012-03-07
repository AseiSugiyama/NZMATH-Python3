import unittest
import sandbox.powdetect as powdetect


class PerfectTest(unittest.TestCase):
    """
    test for perfect_power_detection
    """
    def test_primepower(self):
        self.assertEqual((2, 2), powdetect.perfect_power_detection(2**2))
        self.assertEqual((2, 3), powdetect.perfect_power_detection(2**3))
        self.assertEqual((3, 2), powdetect.perfect_power_detection(3**2))
        self.assertEqual((4, 2), powdetect.perfect_power_detection(2**4))
        self.assertEqual((5, 2), powdetect.perfect_power_detection(5**2))
        self.assertEqual((3, 3), powdetect.perfect_power_detection(3**3))
        self.assertEqual((2, 5), powdetect.perfect_power_detection(2**5))
        self.assertEqual((11**5, 2), powdetect.perfect_power_detection(11**10))
        self.assertEqual((13**10, 2), powdetect.perfect_power_detection(13**20))

    def test_perfectpower(self):
        self.assertEqual((6, 2), powdetect.perfect_power_detection(6**2))
        self.assertEqual((15, 3), powdetect.perfect_power_detection(15**3))
        self.assertEqual((15**5, 3), powdetect.perfect_power_detection(15**15))

    def test_notapower(self):
        self.assertEqual((2, 1), powdetect.perfect_power_detection(2))
        self.assertEqual((6, 1), powdetect.perfect_power_detection(6))
        self.assertEqual((12, 1), powdetect.perfect_power_detection(12))
        self.assertEqual((17, 1), powdetect.perfect_power_detection(17))
        self.assertEqual((19, 1), powdetect.perfect_power_detection(19))


if __name__ == '__main__':
    unittest.main()
