import unittest

from test_building import TestBuilding
from Solver import demo

'''def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSolver())
    suite.addTest(TestBuilding())
'''

class TestSolver(unittest.TestCase):
    def setUp(self):
        pass

    def test_two_roots_1(self):
        self.assertEqual(demo(1, 0, -1), (-1, 1))

    def test_two_roots_2(self):
        self.assertEqual(demo(2, 5, 3), (-1.5, -1))

    def test_one_root1(self):
        self.assertEqual(demo(15, 0, 0), 0)

    def test_one_root2(self):
        self.assertEqual(demo(1, 0, 0), 0)

    def test_no_roots(self):
        self.assertIsNone(demo(15, 7, 15))
