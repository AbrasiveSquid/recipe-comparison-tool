import unittest
import fractions
from ingredient_class import Ingredient


class TestIngredient(unittest.TestCase):
    def setUp(self):
        self.flour = Ingredient('flour', 1, 'cup')
        self.extraDarkBrownSugar = Ingredient('extra Dark-Brown sugar', 1, 'cup')
        self.whiteSugar = Ingredient('white sugar', 1, 'cup')
        self.icingSugar = Ingredient('icing sugar', 1, 'cup')

        self.allPurposeFlour = Ingredient('all-purpose Flour', 1, 'cup')
        self.extraVirginOliveOil = Ingredient('extra-virgin Olive Oil', 100, 'ml')
        self.vegOil = Ingredient('vegetable oil', '½', 'cup')
        self.butter = Ingredient('butter', 2, 'tablespoon')
        self.tableSpoonFlour = Ingredient('flour', 4, 'tablespoons')
        self.teaspoonFlour = Ingredient('flour', 2, 'teaspoons')

        # metric flour
        self.metricCupFlour = Ingredient('flour', 125, 'g')
        self.twoAndHalfMetricCupFlour = Ingredient('flour', 312.5, 'g')
        self.thirtyCupsFlour = Ingredient('flour', 3750, 'g')
        self.quarterCupFlour = Ingredient('flour', 31.25, 'g')
        self.tablespoonMetricFlour = Ingredient('flour', 7.8125, 'g')
        self.halfTablespoonMetricFlour = Ingredient('flour', 3.90625, 'g')
        self.teaspoonMetricFlour = Ingredient('flour', 2.60417, 'g')
        self.halfTeaspoonMetricFlour = Ingredient('flour', 1.30208, 'g')

        # metric veg oil
        self.metricCupVegOil = Ingredient('vegetable oil', 218, 'g')
        self.twoAndHalfMetricCupVegOil = Ingredient('vegetable oil', 545, 'g')
        self.thirtyCupsVegOil = Ingredient('vegetable oil', 6540, 'g')
        self.quarterCupVegOil = Ingredient('vegetable oil', 54.5, 'g')
        self.tablespoonMetricVegOil = Ingredient('vegetable oil', 13.625, 'g')
        self.halfTablespoonMetricVegOil = Ingredient('vegetable oil', 6.8125, 'g')
        self.teaspoonMetricVegOil = Ingredient('vegetable oil', 4.5416666667, 'g')
        self.halfTeaspoonMetricVegOil = Ingredient('vegetable oil', 2.2708333333, 'g')

    def test_ingredient_init(self):
        # flour test
        self.assertEqual(self.flour.name(), 'flour')
        self.assertEqual(int(self.flour.kitchen_amount()), fractions.Fraction(1,1))

        self.assertEqual(int(self.flour.kitchen_amount()), 1)
        self.assertEqual(self.flour.kitchen_measure(), 'cup' )
        self.assertEqual(self.flour._density, 125)
        self.assertEqual(int(self.flour.metric_amount()), 125)
        self.assertEqual(self.flour.metric_measure(), 'g')

        # test not perfect match with extra dark brown sugar
        self.assertEqual(self.extraDarkBrownSugar.name(), 'extra dark brown sugar')
        self.assertEqual(self.extraDarkBrownSugar.kitchen_amount(), fractions.Fraction(1,1))
        self.assertEqual(self.extraDarkBrownSugar.kitchen_measure(), 'cup')
        self.assertEqual(self.extraDarkBrownSugar._density, 230)
        self.assertEqual(int(self.extraDarkBrownSugar.metric_amount()), 230)
        self.assertEqual(self.extraDarkBrownSugar.metric_measure(), 'g')

        # test kilogram to gram conversion
        kiloFlour = Ingredient('flour', 1, 'kg')
        self.assertEqual(kiloFlour.metric_amount(), fractions.Fraction(1000))
        self.assertEqual(kiloFlour.metric_measure(), 'g')

        # test litre to ml conversion
        litreWater = Ingredient('water', 2.4, 'l')
        self.assertEqual(litreWater.metric_amount(), fractions.Fraction(2400))
        self.assertEqual(litreWater.metric_measure(), 'ml')
        self.assertEqual(litreWater.kitchen_amount(), fractions.Fraction(10,1))
        self.assertEqual(litreWater.kitchen_measure(), 'cup')

        # test keywords
        self.assertEqual(self.extraDarkBrownSugar.keywords(), ['brown sugar'])
        self.assertEqual(self.flour.keywords(), ['flour'])
        self.assertEqual(self.extraVirginOliveOil.keywords(), ['olive', 'oil'])
        self.assertEqual(self.whiteSugar.keywords(), ['white sugar'])
        self.assertEqual(self.icingSugar.keywords(), ['icing', 'sugar'])
        self.assertEqual(self.allPurposeFlour.keywords(), ['flour'])


    def test_verify_amount(self):
        self.assertEqual(self.flour._verify_amount(10), fractions.Fraction(10,1))
        self.assertEqual(self.flour._verify_amount(10.5), fractions.Fraction(21,2))
        self.assertEqual(self.flour._verify_amount(0.32223), fractions.Fraction(32223, 100000))
        self.assertEqual(self.flour._verify_amount(0.545), fractions.Fraction(545, 1000))
        self.assertEqual(self.flour._verify_amount('¼'), fractions.Fraction(1,4))
        self.assertEqual(self.flour._verify_amount('¾'), fractions.Fraction(3,4))
        self.assertEqual(self.flour._verify_amount('½'), fractions.Fraction(1,2))
        self.assertEqual(self.flour._verify_amount('⅓'), fractions.Fraction(1,3))
        self.assertEqual(self.flour._verify_amount('⅔'), fractions.Fraction(2,3))

        # numeric strings
        self.assertEqual(self.flour._verify_amount('10'), fractions.Fraction(10,1))
        self.assertEqual(self.flour._verify_amount('10.5'), fractions.Fraction(21,2))

        # incorrect types or values raise error
        with self.assertRaises(TypeError):
            self.flour._verify_amount([10])

    def test_verify_measure(self):
        self.assertEqual(self.flour._verify_measure('cup'), 'cup')
        self.assertEqual(self.flour._verify_measure('cups'), 'cup')
        self.assertEqual(self.flour._verify_measure('tablespoon'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('tablespoons'), 'tablespoon')
        # tbsp., Tbsp., Tb., or T. are all shorthand for tablespoon
        self.assertEqual(self.flour._verify_measure('tbsp'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('Tb'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('T'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('T.'), 'tablespoon')
        self.assertEqual(self.flour._verify_measure('tablespoons'), 'tablespoon')

        self.assertEqual(self.flour._verify_measure('teaspoon'), 'teaspoon')
        self.assertEqual(self.flour._verify_measure('teaspoons'), 'teaspoon')
        self.assertEqual(self.flour._verify_measure('tsp'), 'teaspoon')
        self.assertEqual(self.flour._verify_measure('t'), 'teaspoon')


        self.assertEqual(self.flour._verify_measure('ml'), 'ml')
        self.assertEqual(self.flour._verify_measure('l'), 'l')
        self.assertEqual(self.flour._verify_measure('ls'), 'l')
        self.assertEqual(self.flour._verify_measure('mls'), 'ml')
        self.assertEqual(self.flour._verify_measure('g'), 'g')
        self.assertEqual(self.flour._verify_measure('gs'), 'g')
        self.assertEqual(self.flour._verify_measure('kg'), 'kg')
        self.assertEqual(self.flour._verify_measure('kgs'), 'kg')

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
        flour2 = Ingredient('flour2', 1, 'cup', 'solid')
        self.assertEqual(flour2.name(), 'flour')

        flour3 = Ingredient('all-purpose-flour', 1, 'cup', 'solid')
        self.assertEqual(flour3.name(), 'all purpose flour')

        flour4 = Ingredient('ALL-PURPOSE_FLOuR', 1, 'cup', 'solid')
        self.assertEqual(flour4.name(), 'all purpose flour')

    def test_update_density_and_state(self):
        self.assertEqual(self.flour._density, 125)
        flour4 = Ingredient('bread flour', 1, 'cup', 'solid')
        self.assertEqual(flour4._density, 136)

    def test_convert_to_metric(self):
        # solid conversion
        self.assertEqual(self.flour._convert_to_metric(), (125, 'g'))
        # solid conversion teaspoon
        self.assertEqual(round(float(self.teaspoonFlour._convert_to_metric()[0]),4), 5.2083)
        self.assertEqual(self.tableSpoonFlour._convert_to_metric(), (31.2500, 'g'))

        # liquid conversion
        self.assertEqual(self.vegOil._convert_to_metric(),(109, 'ml'))

    def test_to_metric(self):
        self.assertEqual(self.flour.to_metric(), '125 g')
        self.assertEqual(self.vegOil.to_metric(), '109 ml')
        self.assertEqual(self.teaspoonFlour.to_metric(), '5.2083 g')
        self.assertEqual(self.tableSpoonFlour.to_metric(), '31.25 g')

    def test_convert_to_kitchen(self):
        # solids
        # cups
        self.assertEqual(self.metricCupFlour._convert_to_kitchen(), (1, 'cup'))
        self.assertEqual(self.twoAndHalfMetricCupFlour._convert_to_kitchen(), (2.5, 'cup'))
        self.assertEqual(self.thirtyCupsFlour._convert_to_kitchen(), (30, 'cup'))
        self.assertEqual(self.quarterCupFlour._convert_to_kitchen(), (.25, 'cup'))
        # tablespoons
        self.assertEqual(self.tablespoonMetricFlour._convert_to_kitchen(), (1, 'tablespoon'))
        self.assertEqual(self.halfTablespoonMetricFlour._convert_to_kitchen(), (0.5, 'tablespoon'))
        # teaspoons
        self.assertEqual(self.teaspoonMetricFlour._convert_to_kitchen(),(1, 'teaspoon')) # todo what is going on here
        self.assertEqual(self.halfTeaspoonMetricFlour._convert_to_kitchen(), (0.5, 'teaspoon'))

    #     # liquids
    #     # cups
    #     self.assertEqual(self.metricCupVegOil._convert_to_kitchen(), (1, 'cup'))
    #     self.assertEqual(self.twoAndHalfMetricCupVegOil._convert_to_kitchen(),(2.5, 'cups'))
    #     self.assertEqual(self.thirtyCupsVegOil._convert_to_kitchen(),(30, 'cups'))
    #     self.assertEqual(self.quarterCupVegOil._convert_to_kitchen(),(.25, 'cups'))
    #     # tablespoons
    #     self.assertEqual(self.tablespoonMetricVegOil._convert_to_kitchen(),(1, 'Tbsp'))
    #     self.assertEqual(self.halfTablespoonMetricVegOil._convert_to_kitchen(),(0.5, 'Tbsp'))
    #     # teaspoons
    #     self.assertEqual(self.teaspoonMetricVegOil._convert_to_kitchen(),(1, 'tsp'))
    #     self.assertEqual(self.halfTeaspoonMetricVegOil._convert_to_kitchen(),(0.5, 'tsp'))
    #
    # def test_to_kitchen_measurement(self):
    #     # solids
    #     # cups
    #     self.assertEqual(self.metricCupFlour.to_kitchen_measurement(), '1 cup')
    #     self.assertEqual(self.twoAndHalfMetricCupFlour.to_kitchen_measurement(),'2.5 cups')
    #     self.assertEqual(self.thirtyCupsFlour.to_kitchen_measurement(),'30 cups')
    #     self.assertEqual(self.quarterCupFlour.to_kitchen_measurement(),'0.25 cups')
    #     # tablespoons
    #     self.assertEqual(self.tablespoonMetricFlour.to_kitchen_measurement(), '1 Tbsp')
    #     self.assertEqual(self.halfTablespoonMetricFlour.to_kitchen_measurement(), '0.5 Tbsp')
    #     # teaspoons
    #     self.assertEqual(self.teaspoonMetricFlour.to_kitchen_measurement(),'1 tsp')
    #     self.assertEqual(self.halfTeaspoonMetricFlour.to_kitchen_measurement(), '0.5 tsp')
    #
    #     # liquids
    #     # cups
    #     self.assertEqual(self.metricCupVegOil.to_kitchen_measurement(), '1 cup')
    #     self.assertEqual(
    #         self.twoAndHalfMetricCupVegOil.to_kitchen_measurement(), '2.5 cups')
    #     self.assertEqual(self.thirtyCupsVegOil.to_kitchen_measurement(),'30 cups')
    #     self.assertEqual(self.quarterCupVegOil.to_kitchen_measurement(),'0.25 cups')
    #     # tablespoons
    #     self.assertEqual(self.tablespoonMetricVegOil.to_kitchen_measurement(),'1 Tbsp')
    #     self.assertEqual(
    #         self.halfTablespoonMetricVegOil.to_kitchen_measurement(),'0.5 Tbsp')
    #     # teaspoons
    #     self.assertEqual(self.teaspoonMetricVegOil.to_kitchen_measurement(),'1 tsp')
    #     self.assertEqual(self.halfTeaspoonMetricVegOil.to_kitchen_measurement(),'0.5 tsp')
    #
    # def test_compare_ingredient(self):
    #     brownSugar = Ingredient('Brown Sugar', 100, 'g')
    #     self.assertTrue(brownSugar.compare_ingredient(self.extraDarkBrownSugar))
    #     self.assertTrue(self.extraDarkBrownSugar.compare_ingredient(brownSugar))
    #
    #     # same ingredient
    #     self.assertTrue(self.flour.compare_ingredient(self.flour))
    #     self.assertTrue(self.metricCupFlour.compare_ingredient(self.flour))
    #
    #     # similar ingredients
    #     self.assertTrue(self.extraVirginOliveOil.compare_ingredient(self.vegOil))
    #

