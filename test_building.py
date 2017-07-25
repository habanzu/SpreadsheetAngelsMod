from unittest import TestCase

from Recipes import Building


class TestBuilding(TestCase):
    def setUp(self):
        self.a = Building("Building a")
        self.b = Building("Building b", base_speed=2, no_modules=5, module_speed=1)
        self.c = Building("Building c", base_speed=1.75, no_modules=3, module_speed=0.7)

    def test_buiding_contstructor(self):
        with self.assertRaises(ValueError):
            _ = Building("")

    def test_update_modules(self):
        self.a.update_modules(5)
        self.a.module_speed = 5

    def test_get_speed(self):
        self.assertEqual(self.a.get_speed(), 1)
        self.assertEqual(self.b.get_speed(), 12)
        self.assertEqual(self.c.get_speed(), 5.4)


class TestRecipe(TestCase):
    def setUp(self):
        self.a = Building("Building a")
        self.b = Building("Building b", base_speed=2, no_modules=5, module_speed=1)
        self.c = Building("Building c", base_speed=1.75, no_modules=3, module_speed=0.7)
