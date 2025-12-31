import unittest

from ingredient_class import Ingredient


class TestIngredientComparison(unittest.TestCase):
    def setUp(self):
        self.flour = Ingredient('flour', 1, 'cup')
        self.extraDarkBrownSugar = Ingredient('extra Dark-Brown sugar', 1, 'cup')
        self.vegOil = Ingredient('vegetable oil', '½', 'cup')
        self.butter = Ingredient('butter', 2, 'tablespoon')

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

        # test kilogram to gram conversion
        kiloFlour = Ingredient('flour', 1, 'kg')
        self.assertEqual(kiloFlour.amount(), 1000)
        self.assertEqual(kiloFlour.measure(), 'g')

        # test litre to ml conversion
        litreWater = Ingredient('water', 2.5, 'l')
        self.assertEqual(litreWater.amount(), 2500)
        self.assertEqual(litreWater.measure(), 'ml')

    def test_verify_amount(self):
        self.assertEqual(self.flour._verify_amount(10), 10)
        self.assertEqual(self.flour._verify_amount(10.5), 10.5)
        self.assertEqual(self.flour._verify_amount(0.32223), 0.32)
        self.assertEqual(self.flour._verify_amount(0.545), 0.55)
        self.assertEqual(self.flour._verify_amount('¼'), 0.25)
        self.assertEqual(self.flour._verify_amount('¾'), 0.75)
        self.assertEqual(self.flour._verify_amount('½'), 0.5)
        self.assertEqual(self.flour._verify_amount('⅓'), 0.33)
        self.assertEqual(self.flour._verify_amount('⅔'), 0.67)

        # incorrect types or values raise error
        with self.assertRaises(TypeError):
            self.flour._verify_amount([10])

        with self.assertRaises(ValueError):
            self.flour._verify_amount('1')

    def test_verify_measure(self):
        self.assertEqual(self.flour._verify_measure('cup'), 'cup')
        self.assertEqual(self.flour._verify_measure('cups'), 'cup')
        self.assertEqual(self.flour._verify_measure('tablespoon'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('tablespoons'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('teaspoon'), 'teaspoon')
        self.assertEqual(self.flour._verify_measure('teaspoons'), 'teaspoon')
        self.assertEqual(self.flour._verify_measure('ml'), 'ml')
        self.assertEqual(self.flour._verify_measure('l'), 'ml')
        self.assertEqual(self.flour._verify_measure('mls'), 'ml')
        self.assertEqual(self.flour._verify_measure('ls'), 'ml')
        self.assertEqual(self.flour._verify_measure('g'), 'g')
        self.assertEqual(self.flour._verify_measure('gs'), 'g')
        self.assertEqual(self.flour._verify_measure('kg'), 'g')
        self.assertEqual(self.flour._verify_measure('kgs'), 'g')

        with self.assertRaises(TypeError):
            self.flour._verify_measure(1)
            self.flour._verify_measure(['cup'])
            self.flour._verify_measure(('cup'))

        with self.assertRaises(ValueError):
            self.flour._verify_measure('1')
            self.flour._verify_measure('lbs')

    def test_verify_state(self):
        self.assertEqual(self.flour._verify_state('solid'), 'solid')
        self.assertEqual(self.flour._verify_state('SOLID'), 'solid')
        self.assertEqual(self.flour._verify_state('liquid'), 'liquid')
        self.assertEqual(self.flour._verify_state('LIQUID'), 'liquid')
        self.assertEqual(self.flour._verify_state(None), None)

        with self.assertRaises(TypeError):
            self.flour._verify_state(['liquid'])
            self.flour._verify_state(('liquid'))
            self.flour._verify_state(10)

        with self.assertRaises(ValueError):
            self.flour._verify_state('liquids')
            self.flour._verify_state('solids')
            self.flour._verify_state('gas')

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

    def test_convert_to_metric(self):
        # solid conversion
        self.assertEqual(self.flour._convert_to_metric(), (125, 'g'))
        # TODO Test for teaspoons/tablespoon amounts
        # liquid conversion
        self.assertEqual(self.vegOil._convert_to_metric(),(109, 'ml'))

    def test_to_metric(self):
        self.assertEqual(self.flour.to_metric(), '125 g')
        self.assertEqual(self.vegOil.to_metric(), '109 ml')
    def test_to_kitchen_measurement(self):
        self.assertEqual(self.flour.to_kitchen_measurement(), '1 cup')
