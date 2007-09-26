import unittest
import nzmath.quad as quad

class ClassNumberTest (unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testClassNumber(self):
        self.assert_(quad.class_number(-4))
        #self.assertEqual("[1, 0, 1]", repr(quad.class_number(-4)))
        self.assertEqual(1, quad.class_number(-3))
        self.assertEqual(2, quad.class_number(-15))
        self.assertEqual(3, quad.class_number(-23))
        self.assertEqual(4, quad.class_number(-39))
        self.assertEqual(5, quad.class_number(-47))
        self.assertEqual(6, quad.class_number(-87))
        self.assertEqual(7, quad.class_number(-71))
        # -1 % 4 == 3
        self.assertRaises(ValueError, quad.class_number, -1)
        # 5 > 0
        self.assertRaises(ValueError, quad.class_number, 5)

    def testClassGroup(self):
        self.assert_(quad.class_group(-4))
        self.assertEqual("[[1, 1, 1]]", repr(quad.class_group(-3)[1]))
        self.assertEqual("[[1, 1, 4], [2, 1, 2]]", repr(quad.class_group(-15)[1]))
        self.assertEqual("[[1, 1, 6], [2, 1, 3], [2, -1, 3]]", repr(quad.class_group(-23)[1]))

    def testClassNumberBsgs(self):
        self.assertEqual(1, quad.class_number_bsgs(-3))
        self.assertEqual(2, quad.class_number_bsgs(-15))
        self.assertEqual(3, quad.class_number_bsgs(-23))
        self.assertEqual(4, quad.class_number_bsgs(-39))
        self.assertEqual(5, quad.class_number_bsgs(-47))
        self.assertEqual(6, quad.class_number_bsgs(-87))
        self.assertEqual(7, quad.class_number_bsgs(-71))
        # -1 % 4 == 3
        self.assertRaises(ValueError, quad.class_number_bsgs, -1)
        # 5 > 0
        self.assertRaises(ValueError, quad.class_number_bsgs, 5)

    def testClassGroupBsgs(self):
        unit1 = quad.ReducedQuadraticForm(quad.unit_form(-15), quad.unit_form(-15))
        subgroup1 = quad.class_group_bsgs(-15, 2, [2,1])

        unit2 = quad.ReducedQuadraticForm(quad.unit_form(-23), quad.unit_form(-23))
        subgroup2 = quad.class_group_bsgs(-23, 3, [3,1])

        unit3 = quad.ReducedQuadraticForm(quad.unit_form(-87), quad.unit_form(-87))
        subgroup3_1 = quad.class_group_bsgs(-87, 6, [2,1])
        subgroup3_2 = quad.class_group_bsgs(-87, 6, [3,1])        

        unit4 = quad.ReducedQuadraticForm(quad.unit_form(-1200), quad.unit_form(-1200))
        subgroup4_1 = quad.class_group_bsgs(-1200, 12, [2,2])
        subgroup4_2 = quad.class_group_bsgs(-1200, 12, [3,1])
        
        self.assertEqual(unit1, subgroup1[0][0]**subgroup1[1][0][0])
        self.assertEqual(unit2, subgroup2[0][0]**subgroup2[1][0][0])
        self.assertEqual(unit3, subgroup3_1[0][0]**subgroup3_1[1][0][0])
        self.assertEqual(unit3, subgroup3_2[0][0]**subgroup3_2[1][0][0])        
        self.assertEqual(unit4, subgroup4_1[0][0]**subgroup4_1[1][0][0])
        self.assertEqual(unit4, subgroup4_1[0][1]**subgroup4_1[1][1][0] * subgroup4_1[0][0]**subgroup4_1[1][1][1])
        self.assertEqual(unit4, subgroup4_2[0][0]**subgroup4_2[1][0][0])
        
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
