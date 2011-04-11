from __future__ import division
import unittest
from nzmath.module import *
import nzmath.vector as vector
import nzmath.matrix as matrix
import nzmath.rational as rational
import nzmath.algfield as algfield

vect = vector.Vector
ra = rational.Rational
num_field = algfield.NumberField
field_ele = algfield.BasicAlgNumber

class SubmoduleTest(unittest.TestCase):
    def setUp(self):
        self.a1 = Submodule(2, 1, [vect([-1, -2])])
        self.a1_hnf = Submodule(2, 1, [vect([1, 2])], True)
        self.a2 = Submodule(2, 2, [vect([1, 2]), vect([3, 4])]) # full 1
        self.a2_hnf = Submodule(2, 2, [vect([1, 0]), vect([0, 2])], True)
        self.a3 = Submodule(2, 2, [vect([-2, 1]), vect([4, 2])]) # full 2
        self.a3_hnf = Submodule(2, 2, [vect([8, 0]), vect([6, 1])], True)
        self.a4 = Submodule(2, 2, [vect([1, 2]), vect([2, 4])]) # less rank
        self.a4_hnf = Submodule(2, 1, [vect([1, 2])], True)
        self.a5 = Submodule(
            2, 3, [vect([1, 2]), vect([3, 4]), vect([5, 7])])
        self.a6 = Submodule(2, 2, [vect([2, 0]), vect([1, 2])], True) # hnf
        self.a7 = Submodule(2, 2, [vect([10, 0]), vect([4, -2])])
        self.a8 = Submodule(2, 1, [vect([1, 0])])
        self.a9 = Submodule(2, 1, [vect([0, 2])]) # a8 and a9 is indep.
        self.zero = Submodule(2, 1, [vect([0, 0])]) # zero module

    def testIsSubmodule(self):
        self.assert_(self.a1.isSubmodule(self.a2))
        self.assert_(self.a4.isSubmodule(self.a2))
        self.assert_(not(self.a2.isSubmodule(self.a3)))
        self.assert_(not(self.a3.isSubmodule(self.a2)))
        self.assert_(self.a1.isSubmodule(self.a4)) #equal
        self.assert_(self.a4.isSubmodule(self.a1))
    
    def testIsEqual(self):
        self.assert_(self.a1.isEqual(self.a4))
        a6_2 = Submodule(2, 2, [vect([3, 2]), vect([1, 2])])
        self.assert_(self.a6.isEqual(a6_2))
        self.assert_(a6_2.isEqual(self.a6))
        self.assert_(self.a6.isEqual(self.a6)) # trivial
        self.assert_(not(self.a2.isEqual(self.a3)))
    
    def testIsContains(self):
        self.assert_(self.a1.isContains(vect([2, 4])))
        self.assert_(self.a3.isContains(vect([-16, 0])))
        self.assert_(not(self.a3.isContains(vect([4, 0]))))
    
    def testToHNF(self):
        a1_copy = Submodule.fromMatrix(self.a1)
        a1_copy.toHNF()
        self.assertEqual(a1_copy, self.a1_hnf)
        a2_copy = Submodule.fromMatrix(self.a2)
        a2_copy.toHNF()
        self.assertEqual(a2_copy, self.a2_hnf)
        a3_copy = Submodule.fromMatrix(self.a3)
        a3_copy.toHNF()
        self.assertEqual(a3_copy, self.a3_hnf)
        a4_copy = Submodule.fromMatrix(self.a4)
        a4_copy.toHNF()
        self.assertEqual(a4_copy, self.a4_hnf)
        zero_copy = Submodule(2, 2, [0, 0, 0, 0])
        zero_copy.toHNF()
        self.assertEqual(zero_copy, self.zero)
    
    def testSumOfSubmodules(self):
        a1_sum_a2 = Submodule(2, 2, [vect([1, 2]), vect([3, 4])])
        self.assert_(self.a1.sumOfSubmodules(self.a2).isEqual(a1_sum_a2))
        a2_sum_a3 = Submodule(2, 2, [vect([1, 0]), vect([0, 1])])
        self.assert_(self.a2.sumOfSubmodules(self.a3).isEqual(a2_sum_a3))
        a3_sum_a7 = Submodule(2, 2, [vect([2, 0]), vect([0, 1])])
        self.assert_(self.a3.sumOfSubmodules(self.a7).isEqual(a3_sum_a7))
        # trivial test
        self.assert_(self.a4.sumOfSubmodules(self.a4_hnf).isEqual(self.a4))
        # direct product
        self.assert_(self.a8.sumOfSubmodules(self.a9).isEqual(self.a2))
    
    def testIntersectionOfSubmodules(self):
        a1_intersect_a2 = Submodule(2, 1, [vect([1, 2])])
        self.assert_(
            self.a1.intersectionOfSubmodules(self.a2).isEqual(
            a1_intersect_a2))
        a2_intersect_a3 = Submodule(2, 2, [vect([8, 0]), vect([4, 2])])
        self.assert_(
            self.a2.intersectionOfSubmodules(self.a3).isEqual(
            a2_intersect_a3))
        a3_intersect_a7 = Submodule(2, 2, [vect([40, 0]), vect([36, 2])])
        self.assert_(
            self.a3.intersectionOfSubmodules(self.a7).isEqual(
            a3_intersect_a7))
        # trivial test
        self.assert_(self.a4.intersectionOfSubmodules(
            self.a4_hnf).isEqual(self.a4))
        # direct product
        self.assert_(self.a8.intersectionOfSubmodules(self.a9).isEqual(
            self.zero))

    def testRepresent_element(self):
        a1_vect = vect([-2, -4])
        self.assertEqual(
            self.a1_hnf.represent_element(a1_vect), vect([-2]))
        a2_vect = vect([3, 6])
        self.assertEqual(
            self.a2_hnf.represent_element(a2_vect), vect([3, 3]))
        a3_vect = vect([2, -1])
        self.assertEqual(
            self.a3_hnf.represent_element(a3_vect), vect([1, -1]))
        a4_vect = vect([10, 20])
        self.assertEqual(
            self.a4_hnf.represent_element(a4_vect), vect([10]))
        a4_false_1_vect = vect([1, 3])
        self.assertEqual(
            self.a4_hnf.represent_element(a4_false_1_vect), False)
        a4_false_2_vect = vect([-1, 2])
        self.assertEqual(
            self.a4_hnf.represent_element(a4_false_2_vect), False)
        a8_false_vect = vect([1, 1])
        a8_copy = Submodule.fromMatrix(self.a8)
        self.assertEqual(a8_copy.represent_element(a8_false_vect), False)
        zero_vect = vect([0, 0])
        self.assertEqual(self.zero.represent_element(zero_vect), vect([0]))


class ModuleTest(unittest.TestCase):
    def setUp(self):
        self.Q_rt_2 = num_field([-2, 0, 1])
        self.Q_rt_minus_3 = num_field([3, 0, 1]) # Eisenstein
        self.Q_cube_3 = num_field([3, 0, 0, 1])
        # 3/2 Z + 5*rt(2)/2 Z 
        self.b1 = Module([ [vect([3, 0]), vect([0, 5])], 2 ], self.Q_rt_2)
        self.b1_add = Module([ [vect([3, 0]), vect([0, 10])], 2 ], self.Q_rt_2)
        # (1+2*rt(2))/3 Z + (-1+rt(2))/5 Z
        self.b2 = Module([ [vect([5, 10]), vect([-3, 3])], 15 ],
                         self.Q_rt_2)
        self.b2_add = Module([ [vect([-1, 1])], 10 ], self.Q_rt_2)
        # 5/6 Z + rt(-3)/15 Z
        self.b3 = Module([ [vect([25, 0]), vect([0, 2])], 30 ],
                         self.Q_rt_minus_3)
        # 2/3 Z + 4 * rt(-3)/5 Z
        self.b4 = Module([ [vect([10, 0]), vect([0, 12])], 15],
                         self.Q_rt_minus_3)
        # -3/4 Z + 3*omega/2 Z= -3/4 Z + (-3+3*rt(-3))/4 Z
        self.omega_base = [ vect([1, 0]), vect([ra(-1, 2), ra(1, 2)]) ]
        self.b5 = Module([ [vect([-3, 0]), vect([0, 6])], 4 ],
                         self.Q_rt_minus_3, self.omega_base)
        # 3 Z + 2*cb(3) Z
        self.b6 = Module([ [vect([3, 0, 0]), vect([0, 2, 0])], 1],
                         self.Q_cube_3)
        # 2 (3Z) + 1/2 (3*theta Z)
        self.two_base = [ vect([3, 0]), vect([0, 3]) ]
        self.b7 = Module([ [vect([4, 0]), vect([0, 1])], 2], self.Q_rt_2)

    def testInit(self):
        b2_1 = Module([ [(5, 10), (-3, 3)], 15 ], self.Q_rt_2)
        self.assertEqual(self.b2, b2_1)
        b2_2 = Module([ matrix.RingMatrix(2, 2, 
             [vect([5, 10]), vect([-3, 3])]), 15 ], self.Q_rt_2)
        self.assertEqual(self.b2, b2_2)
        b2_3 = Module(matrix.RingMatrix(2, 2, 
            [vect([ra(1, 3), ra(2, 3)]), vect([ra(-1, 5), ra(1, 5)])]
            ), self.Q_rt_2)
        self.assertEqual(self.b2, b2_3)
        omega_base_1 = [(1, 0), (ra(-1, 2), ra(1, 2))]
        self.assertEqual(self.b5, 
            Module([ [vect([-3, 0]), vect([0, 6])], 4 ], 
            self.Q_rt_minus_3, omega_base_1))
        omega_base_2 = matrix.RingMatrix(2, 2, 
            [vect([1, 0]), vect([ra(-1, 2), ra(1, 2)])])
        self.assertEqual(self.b5, 
            Module([ [vect([-3, 0]), vect([0, 6])], 4 ], 
            self.Q_rt_minus_3, omega_base_2))

    def testEqual(self):
        b1_1 = Module([ [vect([3, 10]), vect([3, 15])], 2 ], 
            self.Q_rt_2)
        self.assertEqual(self.b1, b1_1)
        b1_2 = Module([ [vect([3, 0]), vect([0, -5]), vect([9, -20])],
            2 ], self.Q_rt_2)
        self.assertEqual(self.b1, b1_2)
        b1_false_1 = Module([ [vect([3, 0]), vect([0, 5])], 30 ], 
            self.Q_rt_2)
        self.assert_(not(self.b1 == b1_false_1))
        b1_false_2 = Module([ [vect([3, 0]), vect([0, 4])], 2 ], 
            self.Q_rt_2)
        self.assert_(not(self.b1 == b1_false_2))
        b6_1 = Module([ [vect([3, 0, 0]), vect([0, 2, 0])], 1], 
            self.Q_cube_3)
        self.assertEqual(self.b6, b6_1) #trivial

    def testContains(self):
        b1_vect = field_ele([[3, 5], 1], self.Q_rt_2.polynomial)
        self.assert_(b1_vect in self.b1)
        b3_vect = field_ele([[25, 49], 5], self.Q_rt_minus_3.polynomial)
        self.assert_(b3_vect in self.b3)
        b5_vect = field_ele([[-3, 3], 4], self.Q_rt_minus_3.polynomial)
        self.assert_(b5_vect in self.b5)
        b6_false_vect_1 = field_ele([[3, 2, 1], 1], self.Q_cube_3.polynomial)
        self.assert_(b6_false_vect_1 not in self.b6)
        b6_false_vect_2 = field_ele([[1, 2, 0], 1], self.Q_cube_3.polynomial)
        self.assert_(b6_false_vect_2 not in self.b6)
        b6_false_vect_3 = field_ele([[3, 2, 0], 2], self.Q_cube_3.polynomial)
        self.assert_(b6_false_vect_3 not in self.b6)
        # other type test
        b7_base_vect_1 = vect([0, ra(1, 2)]) # vect repr w.r.t. base
        self.assert_(b7_base_vect_1 in self.b7)
        b7_base_vect_2 = [ vect([4, 1]), 2 ] # list repr w.r.t. base
        self.assert_(b7_base_vect_2 in self.b7)

    def testAdd(self):
        
        b1_sum_b1_add = Module([ [vect([3, 0]), vect([0, 5])], 2], self.Q_rt_2)
        self.assertEqual(b1_sum_b1_add, self.b1 + self.b1_add)
        b2_sum_b2_add = Module([ [vect([10, 20]), vect([-3, 3])], 30], self.Q_rt_2)
        self.assertEqual(b2_sum_b2_add, self.b2 + self.b2_add)
        
    def testMul(self):
        # rational mul
        b1_rat_mul = Module([ [vect([6, 0]), vect([0, 10])], 1 ], self.Q_rt_2)
        self.assertEqual(b1_rat_mul, 4 * self.b1)
        self.assertEqual(b1_rat_mul, self.b1 * 4)
        b2_rat_mul = Module([ [vect([5, 10]), vect([-3, 3])], 21 ], 
            self.Q_rt_2)
        self.assertEqual(b2_rat_mul, ra(5, 7) * self.b2)
        b4_rat_mul = Module([ [vect([5, 0]), vect([0, 6])], 15],
                         self.Q_rt_minus_3)
        self.assertEqual(b4_rat_mul, ra(1, 2) * self.b4)
        # scalar mul
        b1_sca_mul = Module([ [vect([10, 0]), vect([0, 3])], 2], self.Q_rt_2)
        rt_2 = field_ele([[0, 1], 1], self.Q_rt_2.polynomial)
        self.assertEqual(b1_sca_mul, rt_2 * self.b1)
        b2_sca_mul = Module([ [vect([25, 15]), vect([3, 0])], 15], self.Q_rt_2)
        rt_2_one = rt_2 + 1
        self.assertEqual(b2_sca_mul, rt_2_one * self.b2)
        # module mul
        b1_b2_mul = Module([ [vect([15, 30]), vect([-9, 9]), vect([100, 25]), vect([30, -15])], 30 ], self.Q_rt_2)
        self.assertEqual(b1_b2_mul, self.b1 * self.b2)
        b4_b5_mul = Module([
            [vect([-15, 0]), vect([0, 15]), vect([0, 18]), vect([-54, 0])],
            30 ], self.Q_rt_minus_3)
        self.assertEqual(b4_b5_mul, self.b4 * self.b5)

    def testIntersect(self):
        b1_intersect = Module([ [vect([3, 0]), vect([0, 10])], 2], self.Q_rt_2)
        self.assertEqual(b1_intersect, self.b1.intersect(self.b1_add))
        b2_intersect = Module([ [vect([-1, 1])], 5], self.Q_rt_2)
        self.assertEqual(b2_intersect, self.b2.intersect(self.b2_add))

    def testIssubmodule(self):
        self.assert_(self.b1_add.issubmodule(self.b1))
        self.assert_(not(self.b2_add.issubmodule(self.b2)))
        self.assert_(not(self.b2.issubmodule(self.b2_add)))

    def testRepresent_element(self):
        b2_vect = field_ele([[7, 23], 5], self.Q_rt_2.polynomial)
        b2_vect_list = [6, 3]
        self.assertEqual(b2_vect_list, self.b2.represent_element(b2_vect))

    def testIndex(self):
        b1_idx = ra(15, 4)
        self.assertEqual(b1_idx, self.b1.index())
        b2_idx = ra(1, 5)
        self.assertEqual(b2_idx, self.b2.index())
        b5_idx = ra(9, 8)
        self.assertEqual(b5_idx, self.b5.index())

    def testSmallest_rational(self):
        b2_smallest = 3
        self.assertEqual(b2_smallest, self.b2.smallest_rational())
        b5_smallest = ra(3, 4)
        self.assertEqual(b5_smallest, self.b5.smallest_rational())

class IdealTest(unittest.TestCase):
    def setUp(self):
        self.Q_rt_2 = num_field([-2, 0, 1])
        self.Q_rt_minus_3 = num_field([3, 0, 1]) # Eisenstein
        # 3/2 Z + 5*rt(2)/2 Z 
        self.b1 = Ideal([ [vect([3, 0]), vect([0, 5])], 2 ], self.Q_rt_2)
        # (1+2*rt(2))/3 Z + (-1+rt(2))/5 Z
        self.b2 = Ideal([ [vect([5, 10]), vect([-3, 3])], 15 ],
                         self.Q_rt_2)
        # -3/4 Z + 3*omega/2 Z
        self.b3 = Ideal([ [vect([-3, 0]), vect([0, 6])], 4],
                        self.Q_rt_minus_3, self.Q_rt_minus_3.integer_ring())
        
    def testInverse(self):
        one_Q_rt_2 = Ideal([ [vect([1, 0]), vect([0, 1])], 1 ],
                           self.Q_rt_2, self.Q_rt_2.integer_ring())
        self.assert_(self.b2 * self.b2.inverse() == one_Q_rt_2)
        one_Q_rt_minus_3 = Ideal([ [vect([1, 0]), vect([0, 1])], 1],
                                 self.Q_rt_minus_3,
                                 self.Q_rt_minus_3.integer_ring())
        self.assert_(self.b3 * self.b3.inverse() == one_Q_rt_minus_3)

class Ideal_with_generatorTest(unittest.TestCase):
    def setUp(self):
        self.Q_rt_2 = num_field([-2, 0, 1])
        # 2 Z[rt(2)] = 2Z + 2rt(2)Z
        self.c1 = Ideal_with_generator(
            [field_ele([[2, 0], 1], self.Q_rt_2.polynomial)])
        # 2rt(2) Z[rt(2)] = 4Z + 2rt(2)Z
        self.c2 = Ideal_with_generator(
            [field_ele([[0, 2], 1], self.Q_rt_2.polynomial)])
        # (rt(2)+1)  Z[rt(2)] + (rt(2)-1) Z[rt(2)]
        # = (rt(2)+1)Z + (2+rt(2))Z + (rt(2)-1)Z + (2-rt(2))Z
        self.c3 = Ideal_with_generator(
            [field_ele([[1, 1], 1], self.Q_rt_2.polynomial),
             field_ele([[1, -1], 1], self.Q_rt_2.polynomial)])
        # (1/rt(2)) Z[rt(2)] = rt(2)/2 Z + Z
        self.c4 = Ideal_with_generator(
            [field_ele([[0, 1], 1], self.Q_rt_2.polynomial).inverse()])
        
    def testTo_HNFRepresentation(self):
        c1_hnf = Ideal([ [vect([2, 0]), vect([0, 2])], 1 ], self.Q_rt_2)
        self.assertEqual(c1_hnf, self.c1.to_HNFRepresentation())
        c2_hnf = Ideal([ [vect([4, 0]), vect([0, 2])], 1 ], self.Q_rt_2)
        self.assertEqual(c2_hnf, self.c2.to_HNFRepresentation())
        c3_hnf = Ideal([
            [vect([1, 1]), vect([2, 1]), vect([-1, 1]), vect([2, -1])], 1 ],
                       self.Q_rt_2)
        self.assertEqual(c3_hnf, self.c3.to_HNFRepresentation())
        c4_hnf = Ideal([
            [vect([0, 1]), vect([2, 0])], 2 ], self.Q_rt_2)
        self.assertEqual(c4_hnf, self.c4.to_HNFRepresentation())

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
