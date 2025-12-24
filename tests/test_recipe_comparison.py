import unittest

from ingredient_class import Ingredient


class TestRecipeComparison(unittest.TestCase):
    def setUp(self):
        self.flour = Ingredient('flour', 1, 'cup', 'solid')

    def test_ingredient_init(self):
        self.assertEqual(self.flour.name(), 'flour')
        self.assertEqual(self.flour.amount(), 1)
        self.assertEqual(self.flour.measure(), 'cup' )
        self.assertEqual(self.flour._density, 125)

    def test_clean_name(self):
        self.flour2 = Ingredient('flour2', 1, 'cup', 'solid')
        self.assertEqual(self.flour2.name(), 'flour')

        self.flour2.set_name('all-purpose-flour')
        self.assertEqual(self.flour2.name(), 'all purpose flour')

        self.flour2.set_name('ALL-PURPOSE_FLOuR')
        self.assertEqual(self.flour2.name(), 'all purpose flour')

    def test_update_density(self):
        self.assertEqual(self.flour._density, 125)
        self.flour.set_name('bread flour')
        self.assertEqual(self.flour.name(), 'bread flour')
        self.assertEqual(self.flour._density, 136)
