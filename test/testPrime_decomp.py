import unittest
import nzmath.algfield as algfield
import nzmath.module as module
import nzmath.matrix as matrix
from nzmath.prime_decomp import *


class PrimeDecompositionTest(unittest.TestCase):
    def setUp(self):
        # result transform function (for checking values are valid) 
        def e_f(result):
            e_f_lst = [(result[i][1], result[i][2]) for i in range(len(result))]
            e_f_lst.sort()
            return e_f_lst
        def pow_mul(result):
            pow_ele = result[0][0] ** result[0][1]
            for i in range(1, len(result)):
                pow_ele *= result[i][0] ** result[i][1]
            return pow_ele
        self.result_transform = lambda result: (e_f(result), pow_mul(result).to_HNFRepresentation())
        
        self.Q_rt_minus_1 = [1, 0, 1]
        self.Q_cb_2 = [-2, 0, 0, 1]
        self.cubic_first = [1, 9, 0, 1]
        self.cubic_second = [1, 8, 0, 1]
        self.sextic_first = [7, 6, 5, 4, 3, 2, 1]
        self.sextic_second = [6480, 1296, -252, 36, -7, 1] #corresponding to [5, 6, -7, 6, -7, 6]
        
        
    def testEasyCase(self):
        # Q_rt_minus_1 [1, 0, 1]
        field = algfield.NumberField(self.Q_rt_minus_1)
        # p=2
        Q_rt_minus_1_2_index = [(2, 1)] # ramify
        Q_rt_minus_1_2_prime = 2 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(2, self.Q_rt_minus_1))
        self.assertEqual(result_e_f, Q_rt_minus_1_2_index)
        self.assertEqual(result_mul, Q_rt_minus_1_2_prime)
        # p=3
        Q_rt_minus_1_3_index = [(1, 2)] # inert
        Q_rt_minus_1_3_prime = 3 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(3, self.Q_rt_minus_1))
        self.assertEqual(result_e_f, Q_rt_minus_1_3_index)
        self.assertEqual(result_mul, Q_rt_minus_1_3_prime)
        # p=5
        Q_rt_minus_1_5_index = [(1, 1), (1, 1)] # split
        Q_rt_minus_1_5_prime = 5 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(5, self.Q_rt_minus_1))
        self.assertEqual(result_e_f, Q_rt_minus_1_5_index)
        self.assertEqual(result_mul, Q_rt_minus_1_5_prime)

        # Q_cb_2 [-2, 0, 0, 1]
        field = algfield.NumberField(self.Q_cb_2)
        # p=3
        Q_cb_2_3_index = [(3, 1)] # ramify
        Q_cb_2_3_prime = 3 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(3, self.Q_cb_2))
        self.assertEqual(result_e_f, Q_cb_2_3_index)
        self.assertEqual(result_mul, Q_cb_2_3_prime)
        # p=5
        Q_cb_2_5_index = [(1, 1), (1, 2)] # split & inert
        Q_cb_2_5_prime = 5 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(5, self.Q_cb_2))
        self.assertEqual(result_e_f, Q_cb_2_5_index)
        self.assertEqual(result_mul, Q_cb_2_5_prime)
        # p=31
        Q_cb_2_31_index = [(1, 1), (1, 1), (1, 1)] # split
        Q_cb_2_31_prime = 31 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(31, self.Q_cb_2))
        self.assertEqual(result_e_f, Q_cb_2_31_index)
        self.assertEqual(result_mul, Q_cb_2_31_prime)
        

    def testMainCase(self):
        # cubic_first [1, 9, 0, 3]
        field = algfield.NumberField(self.cubic_first)
        # p=3
        cubic_first_3_index = [(1, 1), (2, 1)] # split & ramify
        cubic_first_3_prime = 3 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(3, self.cubic_first))
        self.assertEqual(result_e_f, cubic_first_3_index)
        self.assertEqual(result_mul, cubic_first_3_prime)

        # cubic_second [1, 8, 0, 3]
        field = algfield.NumberField(self.cubic_second)
        # p=5
        cubic_second_5_index = [(1, 1), (1, 2)] # split & inert
        cubic_second_5_prime = 5 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(5, self.cubic_second))
        self.assertEqual(result_e_f, cubic_second_5_index)
        self.assertEqual(result_mul, cubic_second_5_prime)

        # sextic_first [7, 6, 5, 4, 3, 2, 1]
        field = algfield.NumberField(self.sextic_first)
        # p=2
        sextic_first_2_index = [(2, 1), (4, 1)] # split & ramify
        sextic_first_2_prime = 2 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(2, self.sextic_first))
        self.assertEqual(result_e_f, sextic_first_2_index)
        self.assertEqual(result_mul, sextic_first_2_prime)

        # sextic_second [6480, 1296, -252, 36, -7, 1]
        field = algfield.NumberField(self.sextic_second)
        # p=2
        sextic_second_2_index = [(1, 1), (1, 4)] # split & ramify
        sextic_second_2_prime = 2 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(2, self.sextic_second))
        self.assertEqual(result_e_f, sextic_second_2_index)
        self.assertEqual(result_mul, sextic_second_2_prime)
        # p=3
        sextic_second_3_index = [(1, 1), (1, 1), (1, 1), (1, 2)] # split & inert
        sextic_second_3_prime = 3 * module.Ideal(
            matrix.unitMatrix(field.degree), field, field.integer_ring())
        result_e_f, result_mul = self.result_transform(prime_decomp(3, self.sextic_second))
        self.assertEqual(result_e_f, sextic_second_3_index)
        self.assertEqual(result_mul, sextic_second_3_prime)
        

def suite(suffix = "Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__== '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
