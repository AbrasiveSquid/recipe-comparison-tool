import unittest

from recipe_class import Recipe

class TestRecipe(unittest.TestCase):
    def setUp(self):
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
        self.steps1 = """Preheat oven to 400°F (204°C). Grease and lightly flour a 9-inch square baking pan. Set aside.
Whisk the cornmeal, flour, baking powder, baking soda, and salt together in a large bowl. Set aside. In a medium bowl, whisk the melted butter, brown sugar, and honey together until completely smooth and thick. Then, whisk in the egg until combined. Finally, whisk in the buttermilk. Pour the wet ingredients into the dry ingredients and whisk until combined. Avoid over-mixing.
Pour batter into prepared baking pan. Bake for 20 minutes or until golden brown on top and the center is cooked through. Use a toothpick to test. Edges should be crispy at this point. Allow to slightly cool before slicing and serving. Serve cornbread with butter, honey, jam, or whatever you like.
Wrap leftovers up tightly and store at room temperature for up to 1 week.
"""
        self.steps2 = """Preheat oven to 350 degrees and grease a 9x13 inch pan.
In a large bowl whisk together flour, cornmeal, sugar, baking powder, and salt.
In a medium bowl mix together butter, oil, milk, and eggs.
Add wet ingredients to dry ingredients and mix until combined.
Transfer batter to your prepared pan. Bake for 35-45 minutes until golden and a toothpick inserted in the middle comes out clean or with only a few crumbs (no wet batter).
Allow to cool for 15-20 minutes in the pan before cutting into squares and serving. Serve with butter and honey if desired. Store in airtight container at room temperature up to 3 days or in the fridge for 1 week.
"""
        self.steps3 = """
        Gather the ingredients.
Preheat the oven to 400 degrees F (200 degrees C). Grease a 9-inch round cake pan.
Whisk flour, cornmeal, sugar, baking powder, and salt together in a large bowl.
Add milk, vegetable oil, and egg; whisk until well combined.
Pour batter into the prepared pan.
Bake in the preheated oven until a toothpick inserted into the center of the pan comes out clean, 20 to 25 minutes.
Slice and enjoy!
"""
        self.cornbread1 = Recipe("Sally's Cornbread", "https://sallysbakingaddiction.com/my-favorite-cornbread/", ingredients1, self.steps1)
        self.cornbread2 = Recipe("Supermoist Cornbread", "https://www.lecremedelacrumb.com/best-super-moist-cornbread/", ingredients2, self.steps2)
        self.cornbread3 = Recipe("Golden Sweet Cornbread", "https://www.allrecipes.com/recipe/17891/golden-sweet-cornbread/", ingredients3, self.steps3)


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



