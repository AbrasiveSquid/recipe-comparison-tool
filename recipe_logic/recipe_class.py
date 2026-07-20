import os
import nltk
from .ingredient_class import *

project_root = os.path.dirname(os.path.abspath(__file__))
local_nltk_data = os.path.join(project_root, 'nltk_data')
os.environ['NLTK_DATA'] = local_nltk_data
nltk.data.path = [local_nltk_data]

def disabled_download(*args, **kwargs):
    print("NLTK download blocked - using local project data.")
    return True
nltk.download = disabled_download

from ingredient_parser import parse_ingredient

class Recipe:
    """
    this is the recipe class
    """
    def __init__(self, title:str, source:str, ingredientList:list, steps:list):
        self._title = title
        self._source = source
        self._instructions = steps
        self._ingredients = []
        self._ingredientCount = 0
        self._optionalIngredients = []

        self._parse_ingredients(ingredientList)

    def ingredient_count(self):
        """
        getter method, returns the number of ingredents
        """
        return self._ingredientCount

    def _parse_ingredients(self, ingredientList:list):
        if not isinstance(ingredientList, list):
            raise TypeError("ingredientList must be a list but is a "
                            f"{type(ingredientList)}")
        for ingredient in ingredientList:
            parsed = parse_ingredient(ingredient)

            if parsed.amount:
                qty, unit = self._get_qty_and_unit(parsed.amount)
                bestName = max(parsed.name,
                                      key=lambda x: x.confidence)
                ingredientName = bestName.text
                self._ingredients.append(Ingredient(ingredientName, qty, unit))
                self._ingredientCount += 1
            elif parsed.name:
                for optionalIngredient in parsed.name: # no qty available
                    self._optionalIngredients.append(
                        Ingredient(optionalIngredient.text, 0, 0))
            else:
                raise ValueError(f"No quantity found: {ingredient}")

    def _get_qty_and_unit(self, ingAmount) -> tuple:
        """
        Uses the amount of parsed ingredient and extracts the qty and unit
        of the item with the highest confidence, unless it is a composite,
        then finds the metric amount for easier conversion

        Parameters:
                ingAmount:
                    ParsedIngredent.amount

        Returns:
                tuple of a fractions.Fraction and str
        """
        # get highest confidence item
        standaloneAmounts = [amt for amt in ingAmount if
                              not hasattr(amt, 'amounts')]

        # get the max confidence of standaloneAmounts
        if standaloneAmounts:
            bestItem = max(standaloneAmounts,
                            key=lambda x: x.confidence)

        else: # flatten and take the highest confidence
            flatAmounts = []
            for amt in ingAmount:
                flatAmounts.extend(amt.amounts)
            bestItem = max(flatAmounts,
                            key=lambda x: x.confidence)

        return bestItem.quantity, str(bestItem.unit)

    def title(self) -> str:
        """
        getter returns self._title
        """
        return self._title

    def source(self) -> str:
        """
        getter for source of the recipe, returns self._source
        """
        return self._source

    def instructions(self) -> str:
        """
        getter, returns self._instructions
        """
        return self._instructions

    def ingredient_str(self) -> str:
        """
        returns a print friendly string representation of the ingredients
        """
        resultStr = ''

        if self._ingredients:
            resultStr += "\n**Ingredients**\n"
            for ingredient in self._ingredients:
                resultStr += f"\t{ingredient}\n"
        if self._optionalIngredients:
            resultStr += "\n**Optional Ingredients**\n"
            for ingredient in self._optionalIngredients:
                resultStr += f"\t{ingredient}\n"

        return resultStr

    def __str__(self) -> str:
        """
        returns a print friendly representation of the recipe
        """
        resultStr = f"Recipe: {self._title} from {self._source}\n"
        resultStr += self.ingredient_str()
        resultStr += f"\n**Instructions**\n{self._format_instructions()}"

        return resultStr

    def _format_instructions(self) -> str:
        """
        returns a print friendly string of the instructions as steps
        """
        instructions = ""
        for i in (range(len(self._instructions))):
            instructions += f"{i+1}. {self._instructions[i]}\n"
        return instructions

    def is_empty(self) -> bool:
        return len(self._ingredients) == 0

    def compare_recipe(self, other) -> list:
        """
        compares this recipe with another recipe by finding all same or similar
        ingredients and returning a string with the ingredients for each recipe

        Precondition:
            other must be the correct type

        Returns:
            list of dictionary with each dictionary containing the structure:
                {
                    "ingredient1": Ingredient,
                    "ingredient2": Ingredient,
                    "diffKitchen": (float, str),
                    "diffMetric": (float, str),
                    "defaultMeasure": str
                }

        Raises:
            TypeError:
                if other is not the correct type
            Exception:
                if other has no ingredients
                if self has no ingredients
        """
        if not isinstance(other, Recipe):
            raise TypeError("other must be a Recipe object but is a "
                            f"{type(other)}")
        if self.is_empty() or other.is_empty():
            raise Exception("self and other must contain a list of "
                            "ingredients")

        # match ingredients as a list of tuples
        thisRecipe = self._ingredients
        thisRecipe.reverse() # reverse more efficient to pop from end in loop
        otherRecipe = other._ingredients
        ingredientPairs = self._compare_helper(thisRecipe, otherRecipe)

        # create list of tuples with ingredient in pos 0 and 1, difference in 2
        result = []
        for pair in ingredientPairs:
            if pair[0].defMeasure == pair[1].defMeasure:
                defaultMeasure = pair[0].defMeasure
            else:
                defaultMeasure = "kitchen" # defaults to kitchen if not same

            pairDict = {
                "ingredient1": pair[0],
                "ingredient2": pair[1],
                "diffKitchen": pair[0].difference(pair[1], kitchenMeasure=True),
                "diffMetric": pair[0].difference(pair[1], metricMeasure=True),
                "defaultMeasure": defaultMeasure
            }
            result.append(pairDict)
        return result

    def _compare_helper(self, firstRecipe: list, secondRecipe: list) -> list:
        """
        takes two list of ingredients and returns a list of tuples that
        contians a tuple of each ingredient with the same ingredient from
        the other list. If there is no matching ingredient, the tuple will
        contain that ingredient and none

         Precondition:
            firstRecipe and secondRecipe are a list of ingredients and
            measurements as a string
            example: 3/4 cup of sugar

        Returns:
            list of pair ingredient tuples
            example: [("3/4 cup white sugar", "100 g white sugar")]

            Example:
                first_ing: ["1 egg", "3/4 cup white sugar", "25 ml olive oil"]
                second_ing: ["3 eggs", "100 g white sugar", "50 g brown sugar"]
                return value:
                    [("1 egg", "3 eggs"),
                    ("3/4 cup white sugar", "100 g white sugar"),
                    ("25 ml olive oil", "0 ml olive oil"),
                    ("0 g brown sugar", "50 g brown sugar")]
        """
        ingredientPairs = []

        while len(firstRecipe) and len(secondRecipe):
            thisIngredient = firstRecipe.pop()

            for i in range(len(secondRecipe)):
                if thisIngredient.compare_ingredient(secondRecipe[i]):
                    ingredientPairs.append(
                        (thisIngredient, secondRecipe.pop(i)))
                    break
            else:
                # if no matching ingredient, append an emptied clone ingredient
                duplicateIng = thisIngredient.clone()
                duplicateIng.empty_ingredient()
                ingredientPairs.append((thisIngredient, duplicateIng))

        # add remaining ingredients with an emptied clone ingredient
        for ingredient in firstRecipe:
            duplicateIng = ingredient.clone()
            duplicateIng.empty_ingredient()
            ingredientPairs.append((ingredient, duplicateIng))


        for ingredient in secondRecipe:
            duplicateIng = ingredient.clone()
            duplicateIng.empty_ingredient()
            ingredientPairs.append((duplicateIng, ingredient))

        return ingredientPairs

# sally = Recipe("Sally's Cornbread", "x", ['1 cup (120g) fine cornmeal',
#                                           '1 cup (125g) all-purpose flour (spooned & leveled)',
#                                           '1 teaspoon baking powder', '1/2 teaspoon baking soda',
#                                           '1/8 teaspoon salt',
#                                           '1/2 cup (8 Tbsp; 113g) unsalted butter, melted and slightly cooled',
#                                           '1/3 cup (67g) packed light or dark brown sugar',
#                                           '2 Tablespoons (30ml) honey',
#                                           '1 large egg, at room temperature',
#                                           '1 cup (240ml) buttermilk, at room temperature*'
#                                           ],
#                ["Preheat oven to 400°F (204°C). Grease and lightly flour a 9-inch square baking pan. Set aside.",
#                "Whisk the cornmeal, flour, baking powder, baking soda, and salt together in a large bowl. Set aside. In a medium bowl, whisk the melted butter, brown sugar, and honey together until completely smooth and thick. Then, whisk in the egg until combined. Finally, whisk in the buttermilk. Pour the wet ingredients into the dry ingredients and whisk until combined. Avoid over-mixing.",
#                "Pour batter into prepared baking pan. Bake for 20 minutes or until golden brown on top and the center is cooked through. Use a toothpick to test. Edges should be crispy at this point. Allow to slightly cool before slicing and serving. Serve cornbread with butter, honey, jam, or whatever you like.",
#                "Wrap leftovers up tightly and store at room temperature for up to 1 week."]
#                )
# moist = Recipe("Moise Cornbread", "y",['2 ½ cups flour', '1 cup cornmeal', '1 cup sugar',
#                         '1 ½ tablespoons baking powder', '1 teaspoon salt',
#                         '½ cup (8 tablespoons) butter (melted)', '½ cup oil',
#                         '1 ¼ cups milk', '3 large eggs',
#                         'honey and extra butter for serving (optional)'],
#                ["Preheat oven to 350 degrees and grease a 9x13 inch pan.",
#                 "In a large bowl whisk together flour, cornmeal, sugar, baking powder, and salt.",
#                 "In a medium bowl mix together butter, oil, milk, and eggs.",
#                 "Add wet ingredients to dry ingredients and mix until combined.",
#                 "Transfer batter to your prepared pan. Bake for 35-45 minutes until golden and a toothpick inserted in the middle comes out clean or with only a few crumbs (no wet batter).",
#                 "Allow to cool for 15-20 minutes in the pan before cutting into squares and serving. Serve with butter and honey if desired. Store in airtight container at room temperature up to 3 days or in the fridge for 1 week."
#                 ]
#                )
#
# print(sally.compare_recipe(moist))


# ingredients4 = ["1 egg", "3/4 cup white sugar", "25 ml olive oil"]
# ingredients5 = ["3 eggs", "100 g white sugar", "50 g brown sugar"]
# recipe1 = Recipe("Test recipe 1", "x", ingredients4, ["fake step"])
# recipe2 = Recipe("Test recipe 2", "x", ingredients5, ["fake step"])
# print(recipe1.compare_recipe(recipe2))