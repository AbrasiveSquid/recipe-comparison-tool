import unittest
from ..recipe_class import Recipe

class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # ingredients
        ingredients1 = ['1 cup (120g) fine cornmeal',
                        '1 cup (125g) all-purpose flour (spooned & leveled)',
                        '1 teaspoon baking powder', '1/2 teaspoon baking soda',
                        '1/8 teaspoon salt',
                        '1/2 cup (8 Tbsp; 113g) unsalted butter, melted and slightly cooled',
                        '1/3 cup (67g) packed light or dark brown sugar',
                        '2 Tablespoons (30ml) honey',
                        '1 large egg, at room temperature',
                        '1 cup (240ml) buttermilk, at room temperature*']
        ingredients2 = ['2 ½ cups flour', '1 cup cornmeal', '1 cup sugar',
                        '1 ½ tablespoons baking powder', '1 teaspoon salt',
                        '½ cup (8 tablespoons) butter (melted)', '½ cup oil',
                        '1 ¼ cups milk', '3 large eggs',
                        'honey and extra butter for serving (optional)']
        ingredients3 = ['1 cup all-purpose flour', '1 cup yellow cornmeal',
                        '0.66666668653488 cup white sugar',
                        '3.5 teaspoons baking powder', '1 teaspoon salt',
                        '1 cup milk', '0.33333334326744 cup vegetable oil',
                        '1 large egg']

        ingredients4 = ["1 egg", "3/4 cup white sugar", "25 ml olive oil"]
        ingredients5 = ["3 eggs", "100 g white sugar", "50 g brown sugar"]
        empty_ingredients = []

        self.steps1 = ["Preheat oven to 400°F (204°C). Grease and lightly flour a 9-inch square baking pan. Set aside.",
"Whisk the cornmeal, flour, baking powder, baking soda, and salt together in a large bowl. Set aside. In a medium bowl, whisk the melted butter, brown sugar, and honey together until completely smooth and thick. Then, whisk in the egg until combined. Finally, whisk in the buttermilk. Pour the wet ingredients into the dry ingredients and whisk until combined. Avoid over-mixing.",
"Pour batter into prepared baking pan. Bake for 20 minutes or until golden brown on top and the center is cooked through. Use a toothpick to test. Edges should be crispy at this point. Allow to slightly cool before slicing and serving. Serve cornbread with butter, honey, jam, or whatever you like.",
"Wrap leftovers up tightly and store at room temperature for up to 1 week."]

        self.steps2 = ["Preheat oven to 350 degrees and grease a 9x13 inch pan.",
"In a large bowl whisk together flour, cornmeal, sugar, baking powder, and salt.",
"In a medium bowl mix together butter, oil, milk, and eggs.",
"Add wet ingredients to dry ingredients and mix until combined.",
"Transfer batter to your prepared pan. Bake for 35-45 minutes until golden and a toothpick inserted in the middle comes out clean or with only a few crumbs (no wet batter).",
"Allow to cool for 15-20 minutes in the pan before cutting into squares and serving. Serve with butter and honey if desired. Store in airtight container at room temperature up to 3 days or in the fridge for 1 week."
        ]
        self.steps3 = [
        "Gather the ingredients.",
"Preheat the oven to 400 degrees F (200 degrees C). Grease a 9-inch round cake pan.",
"Whisk flour, cornmeal, sugar, baking powder, and salt together in a large bowl.",
"Add milk, vegetable oil, and egg; whisk until well combined.",
"Pour batter into the prepared pan.",
"Bake in the preheated oven until a toothpick inserted into the center of the pan comes out clean, 20 to 25 minutes.,"
"Slice and enjoy!"
        ]
        self.cornbread1 = Recipe("Sally's Cornbread", "https://sallysbakingaddiction.com/my-favorite-cornbread/", ingredients1, self.steps1)
        self.cornbread2 = Recipe("Supermoist Cornbread", "https://www.lecremedelacrumb.com/best-super-moist-cornbread/", ingredients2, self.steps2)
        self.cornbread3 = Recipe("Golden Sweet Cornbread", "https://www.allrecipes.com/recipe/17891/golden-sweet-cornbread/", ingredients3, self.steps3)

        self.recipe1 = Recipe("Test recipe 1", "x", ingredients4, ["fake step"])
        self.recipe2 = Recipe("Test recipe 2", "x", ingredients5, ["fake step"])
        self.empty_recipe = Recipe("Empty recipe", "x", empty_ingredients, ["empty"])


    def test_recipe_init(self):
        self.assertEqual(self.cornbread1.title(),"Sally's Cornbread")
        self.assertEqual(self.cornbread2.title(),"Supermoist Cornbread")
        self.assertEqual(self.cornbread3.title(),"Golden Sweet Cornbread")
        self.assertEqual(self.cornbread1.source(), "https://sallysbakingaddiction.com/my-favorite-cornbread/")
        self.assertEqual(self.cornbread2.source(), "https://www.lecremedelacrumb.com/best-super-moist-cornbread/")
        self.assertEqual(self.cornbread3.source(),"https://www.allrecipes.com/recipe/17891/golden-sweet-cornbread/")
        self.assertEqual(self.cornbread1.instructions(), self.steps1)
        self.assertEqual(self.cornbread2.instructions(), self.steps2)
        self.assertEqual(self.cornbread3.instructions(), self.steps3)

    def test_format_instructions(self):
        ans1 = """1. Preheat oven to 400°F (204°C). Grease and lightly flour a 9-inch square baking pan. Set aside.
2. Whisk the cornmeal, flour, baking powder, baking soda, and salt together in a large bowl. Set aside. In a medium bowl, whisk the melted butter, brown sugar, and honey together until completely smooth and thick. Then, whisk in the egg until combined. Finally, whisk in the buttermilk. Pour the wet ingredients into the dry ingredients and whisk until combined. Avoid over-mixing.
3. Pour batter into prepared baking pan. Bake for 20 minutes or until golden brown on top and the center is cooked through. Use a toothpick to test. Edges should be crispy at this point. Allow to slightly cool before slicing and serving. Serve cornbread with butter, honey, jam, or whatever you like.
4. Wrap leftovers up tightly and store at room temperature for up to 1 week.
"""

        ans2 = """1. Preheat oven to 350 degrees and grease a 9x13 inch pan.
2. In a large bowl whisk together flour, cornmeal, sugar, baking powder, and salt.
3. In a medium bowl mix together butter, oil, milk, and eggs.
4. Add wet ingredients to dry ingredients and mix until combined.
5. Transfer batter to your prepared pan. Bake for 35-45 minutes until golden and a toothpick inserted in the middle comes out clean or with only a few crumbs (no wet batter).
6. Allow to cool for 15-20 minutes in the pan before cutting into squares and serving. Serve with butter and honey if desired. Store in airtight container at room temperature up to 3 days or in the fridge for 1 week.
"""
        self.assertEqual(self.cornbread1._format_instructions(), ans1)
        self.assertEqual(self.cornbread2._format_instructions(), ans2)


    def test_compare_recipe(self):
        result = self.recipe1.compare_recipe(self.recipe2)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result),
                         4)  # Should contain pairs for eggs, white sugar, olive oil, brown sugar

        # Check ingredinet pairs and difference calculation
        self.assertEqual(str(result[0]["ingredient1"]), "1 egg")
        self.assertEqual(str(result[0]["ingredient2"]), "3 eggs")
        self.assertEqual(result[0]["diffKitchen"], ("-2", ""))

        self.assertEqual(str(result[1]["ingredient1"]), "0.75 cup white sugar")
        self.assertEqual(str(result[1]["ingredient2"]), "100 g white sugar")
        self.assertEqual(result[1]["diffKitchen"], ("0.25", "cup"))
        self.assertEqual(result[1]["diffMetric"], ("50", "g"))

        self.assertEqual(str(result[2]["ingredient1"]), "25 ml olive oil")
        self.assertEqual(str(result[2]["ingredient2"]), "0 ml olive oil")
        self.assertEqual(result[2]["diffKitchen"], ("1.86", "tablespoon"))
        self.assertEqual(result[2]["diffMetric"], ("25", "ml"))

        self.assertEqual(str(result[3]["ingredient1"]), "0 g brown sugar")
        self.assertEqual(str(result[3]["ingredient2"]), "50 g brown sugar")
        self.assertEqual(result[3]["diffKitchen"], ("-3.75", "tablespoon"))
        self.assertEqual(result[3]["diffMetric"], ("-50", "g"))

        # check it handles empty ingredient list
        with self.assertRaises(Exception) as context:
            self.recipe1.compare_recipe(self.empty_recipe)

        self.assertEqual(
            str(context.exception),
            "self and other must contain a list of ingredients"
        )

    def test_compare_helper(self):
        # Setup recipe with chocolate AND chocolate chips
        ing_a = [
            "4 ounces semi-sweet chocolate",
            "1 cup semi-sweet chocolate chips"
        ]
        # Setup recipe with ONLY chocolate chips
        ing_b = [
            "3/4 cup chocolate chips"
        ]

        recipe_a = Recipe("Recipe A", "x", ing_a, ["step"])
        recipe_b = Recipe("Recipe B", "x", ing_b, ["step"])

        result = recipe_a.compare_recipe(recipe_b)

        # Expected result structure:
        # 1. "4 ounces semi-sweet chocolate" should fail to match and pair with empty clone
        # 2. "1 cup semi-sweet chocolate chips" should correctly match "3/4 cup chocolate chips"

        self.assertEqual(len(result), 2)

        # Find the pair containing chocolate chips
        chip_pair = None
        for pair in result:
            if "chips" in str(pair["ingredient1"]).lower():
                chip_pair = pair
                break

        self.assertIsNotNone(chip_pair,
                             "Chocolate chips from Recipe A was not processed")
        self.assertIn("chips", str(chip_pair["ingredient2"]).lower(),
                      "Chocolate chips in Recipe A failed to pair with Chocolate chips in Recipe B")

        def test_compare_recipe_edge_cases(self):
            # Test 1: Completely empty recipe vs populated recipe
            empty_recipe = Recipe("Empty", "x", [], ["step"])
            populated_recipe = Recipe("Populated", "x",
                                      ["1 cup flour", "2 eggs"], ["step"])

            result = populated_recipe.compare_recipe(empty_recipe)
            self.assertEqual(len(result), 2)
            self.assertEqual(str(result[0]["ingredient1"]), "1 cup flour")
            self.assertEqual(str(result[0]["ingredient2"]), "0 cup flour")
            self.assertEqual(str(result[1]["ingredient1"]), "2 eggs")
            self.assertEqual(str(result[1]["ingredient2"]), "0 eggs")

            # Test 2: Reverse empty comparison (empty recipe as self)
            result_rev = empty_recipe.compare_recipe(populated_recipe)
            self.assertEqual(len(result_rev), 2)
            self.assertEqual(str(result_rev[0]["ingredient1"]), "0 cup flour")
            self.assertEqual(str(result_rev[0]["ingredient2"]), "1 cup flour")

            # Test 3: Out-of-order matching with identical items
            # Ensures similarity scoring doesn't rely on strict index alignment
            recipe1 = Recipe("R1", "x",
                             ["1 cup milk", "2 tbsp butter", "3 tsp salt"],
                             ["step"])
            recipe2 = Recipe("R2", "x",
                             ["3 tsp kosher salt", "1 cup whole milk",
                              "2 tablespoons butter"], ["step"])

            result_order = recipe1.compare_recipe(recipe2)
            self.assertEqual(len(result_order), 3)
            self.assertEqual(str(result_order[0]["ingredient1"]), "1 cup milk")
            self.assertIn("milk", str(result_order[0]["ingredient2"]))
            self.assertEqual(str(result_order[1]["ingredient1"]),
                             "2 tbsp butter")
            self.assertIn("butter", str(result_order[1]["ingredient2"]))
            self.assertEqual(str(result_order[2]["ingredient1"]), "3 tsp salt")
            self.assertIn("salt", str(result_order[2]["ingredient2"]))

            # Test 4: Ambiguous overlapping keywords (e.g., "vanilla extract" vs "almond extract" and "vanilla bean")
            recipe_ambig_1 = Recipe("RA1", "x", ["1 tsp vanilla extract",
                                                 "2 pods vanilla bean"],
                                    ["step"])
            recipe_ambig_2 = Recipe("RA2", "x", ["1 tsp almond extract",
                                                 "1 pod vanilla bean"],
                                    ["step"])

            result_ambig = recipe_ambig_1.compare_recipe(recipe_ambig_2)
            self.assertEqual(len(result_ambig), 2)
            # Vanilla extract should find extract/vanilla match, vanilla bean maps to vanilla bean
            self.assertEqual(str(result_ambig[0]["ingredient1"]),
                             "1 tsp vanilla extract")
            self.assertIn("extract", str(result_ambig[0]["ingredient2"]))
            self.assertEqual(str(result_ambig[1]["ingredient1"]),
                             "2 pods vanilla bean")
            self.assertIn("vanilla bean", str(result_ambig[1]["ingredient2"]))

            # Test 5: Completely disjoint recipes (no shared vocabulary words)
            recipe_food = Recipe("Food", "x", ["1 lb beef", "2 potatoes"],
                                 ["step"])
            recipe_hardware = Recipe("Hardware", "x",
                                     ["10 mm socket", "4 bolts"], ["step"])

            result_disjoint = recipe_food.compare_recipe(recipe_hardware)
            self.assertEqual(len(result_disjoint), 4)
            # Should pair all items from recipe_food with empty clones, followed by recipe_hardware unmatched items
            self.assertEqual(str(result_disjoint[0]["ingredient1"]),
                             "1 lb beef")
            self.assertEqual(str(result_disjoint[0]["ingredient2"]),
                             "0 lb beef")
            self.assertEqual(str(result_disjoint[3]["ingredient1"]),
                             "0 mm socket")
            self.assertEqual(str(result_disjoint[3]["ingredient2"]),
                             "10 mm socket")

             # Test 1: Substring overlaps and singular/plural variations
            ing_a = ["1 large egg", "2 cloves garlic", "1 tbsp olive oil"]
            ing_b = ["3 small eggs", "1 clove garlic", "2 cups extra virgin olive oil"]

            r1 = Recipe("R1", "x", ing_a, ["step"])
            r2 = Recipe("R2", "x", ing_b, ["step"])
            result = r1.compare_recipe(r2)

            self.assertEqual(len(result), 3)
            self.assertEqual(str(result[0]["ingredient1"]), "1 large egg")
            self.assertIn("egg", str(result[0]["ingredient2"]))
            self.assertEqual(str(result[1]["ingredient1"]), "2 cloves garlic")
            self.assertIn("garlic", str(result[1]["ingredient2"]))
            self.assertEqual(str(result[2]["ingredient1"]), "1 tbsp olive oil")
            self.assertIn("olive oil", str(result[2]["ingredient2"]))

            # Test 2: Highly overlapping multi-word ingredients competing for the same match
            # Ensures similarity scoring cleanly splits common tokens without cross-wiring wrong items
            ing_c = ["1 cup brown sugar", "1 cup white sugar"]
            ing_d = ["1 cup granulated white sugar", "1 cup dark brown sugar"]

            r3 = Recipe("R3", "x", ing_c, ["step"])
            r4 = Recipe("R4", "x", ing_d, ["step"])
            result2 = r3.compare_recipe(r4)

            self.assertEqual(len(result2), 2)
            # Brown sugar should map to brown sugar, white to white
            self.assertIn("brown sugar",
                          str(result2[0]["ingredient1"]).lower())
            self.assertIn("brown sugar",
                          str(result2[0]["ingredient2"]).lower())
            self.assertIn("white sugar",
                          str(result2[1]["ingredient1"]).lower())
            self.assertIn("white sugar",
                          str(result2[1]["ingredient2"]).lower())

            # Test 3: Partial keyword matches with mismatched counts (more items in recipe 2)
            ing_e = ["1 tsp salt"]
            ing_f = ["1 tsp sea salt", "1 pinch kosher salt",
                     "1 dash celery salt"]

            r5 = Recipe("R5", "x", ing_e, ["step"])
            r6 = Recipe("R6", "x", ing_f, ["step"])
            result3 = r5.compare_recipe(r6)

            # 1 match from r5 + 2 leftover unmatched items from r6 appended at end = 3 total pairs
            self.assertEqual(len(result3), 3)
            self.assertIn("salt", str(result3[0]["ingredient1"]))
            self.assertIn("salt", str(result3[0]["ingredient2"]))
            # Remaining items from r6 should have empty clones as ingredient1
            self.assertEqual(str(result3[1]["ingredient1"]),
                             "0 pinch kosher salt")
            self.assertEqual(str(result3[2]["ingredient1"]),
                             "0 dash celery salt")

            # Test 4: Order preservation check with interleaved matches and unique items
            ing_g = ["apple", "banana", "cherry", "date"]
            ing_h = ["banana", "blueberry", "apple", "fig"]

            r7 = Recipe("R7", "x", ing_g, ["step"])
            r8 = Recipe("R8", "x", ing_h, ["step"])
            result4 = r7.compare_recipe(r8)

            # Should preserve r7's exact index layout: apple(0), banana(1), cherry(2), date(3), plus unmatched r8 items at the end
            self.assertEqual(str(result4[0]["ingredient1"]), "apple")
            self.assertIn("apple", str(result4[0]["ingredient2"]))
            self.assertEqual(str(result4[1]["ingredient1"]),
                             "bannana" if "bannana" in str(
                                 result4[1]["ingredient1"]) else "banana")
            self.assertIn("banana", str(result4[1]["ingredient2"]))
            self.assertEqual(str(result4[2]["ingredient1"]), "cherry")
            self.assertEqual(str(result4[2]["ingredient2"]),
                             "0 cherry")  # unmatched, gets clone
            self.assertEqual(str(result4[3]["ingredient1"]), "date")
            self.assertEqual(str(result4[3]["ingredient2"]),
                             "0 date")  # unmatched, gets clone