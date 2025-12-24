import unittest

from ingredient_class import Ingredient


class TestRecipeComparison(unittest.TestCase):
    def setUp(self):
        self.flour = Ingredient('flour', 1, 'cup')
        self.extraDarkBrownSugar = Ingredient('extra Dark-Brown sugar', 1, 'cup')

    def test_ingredient_init(self):
        # flour test
        self.assertEqual(self.flour.name(), 'flour')
        self.assertEqual(self.flour.amount(), 1)
        self.assertEqual(self.flour.measure(), 'cup' )
        self.assertEqual(self.flour._density, 125)

        # test not perfect match with extra dark brown sugar
        self.assertEqual(self.extraDarkBrownSugar.name(), 'extra dark brown sugar')
        self.assertEqual(self.extraDarkBrownSugar.amount(), 1)
        self.assertEqual(self.extraDarkBrownSugar.measure(), 'cup')
        self.assertEqual(self.extraDarkBrownSugar._density, 230)

    def test_clean_name(self):
        self.flour2 = Ingredient('flour2', 1, 'cup', 'solid')
        self.assertEqual(self.flour2.name(), 'flour')

        self.flour2.set_name('all-purpose-flour')
        self.assertEqual(self.flour2.name(), 'all purpose flour')

        self.flour2.set_name('ALL-PURPOSE_FLOuR')
        self.assertEqual(self.flour2.name(), 'all purpose flour')

    def test_update_density_and_state(self):
        self.assertEqual(self.flour._density, 125)
        self.flour.set_name('bread flour')
        self.assertEqual(self.flour.name(), 'bread flour')
        self.assertEqual(self.flour._density, 136)


