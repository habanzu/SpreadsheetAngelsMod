import unittest

from Solver import Solver


class TestSolver(unittest.TestCase):
    def setUp(self):
        pass

    def test_two_roots_1(self):
        self.assertEqual(Solver.demo(1, 0, -1), (-1, 1))

    def test_two_roots_2(self):
        self.assertEqual(Solver.demo(2, 5, 3), (-1.5, -1))

    def test_one_root(self):
        self.assertEqual(Solver.demo(15, 0, 0), 0)

    def test_no_roots(self):
        self.assertIsNone(Solver.demo(15, 7, 15))
