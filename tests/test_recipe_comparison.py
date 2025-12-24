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