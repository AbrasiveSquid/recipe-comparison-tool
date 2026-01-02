import os
import nltk
from ingredient_class import *

project_root = os.path.dirname(os.path.abspath(__file__))
local_nltk_data = os.path.join(project_root, 'nltk_data')
os.environ['NLTK_DATA'] = local_nltk_data
nltk.data.path = [local_nltk_data]

def disabled_download(*args, **kwargs):
    print("NLTK download blocked - using local project data.")
    return True
nltk.download = disabled_download

from pint import UnitRegistry
from ingredient_parser import parse_ingredient

class Recipe:
    """
    this is the recipe class
    """
    def __init__(self, name:str, website:str, ingredientList:list, steps:str):
        self._name = name
        self._source = website
        self._instructions = steps
        self._ingredients = []

        self._parse_ingredients(ingredientList)

    def _parse_ingredients(self, ingredientList:list):
        if not isinstance(ingredientList, list):
            raise TypeError("ingredientList must be a list but is a "
                            f"{type(ingredientList)}")
        ureg = UnitRegistry()
        for ingredient in ingredientList:
            parsed = parse_ingredient(ingredient)

            if not parsed.amount:
                raise ValueError(f"No quantity found: {ingredient}")

            item = parsed.amount[0]

            qty = ureg(item.quantity)
            unit = ureg(str(item.unit))
            ingredientName = parsed.name[0].text
            self._ingredients.append(Ingredient(ingredientName, qty, unit))



ingredients1 = ['1 cup (120g) fine cornmeal', '1 cup (125g) all-purpose flour (spooned & leveled)', '1 teaspoon baking powder', '1/2 teaspoon baking soda', '1/8 teaspoon salt', '1/2 cup (8 Tbsp; 113g) unsalted butter, melted and slightly cooled', '1/3 cup (67g) packed light or dark brown sugar', '2 Tablespoons (30ml) honey', '1 large egg, at room temperature', '1 cup (240ml) buttermilk, at room temperature*']
ingredients2 = ['2 ½ cups flour', '1 cup cornmeal', '1 cup sugar', '1 ½ tablespoons baking powder', '1 teaspoon salt', '½ cup (8 tablespoons) butter (melted)', '½ cup oil', '1 ¼ cups milk', '3 large eggs', 'honey and extra butter for serving (optional)']
ingredients3 = ['1 cup all-purpose flour', '1 cup yellow cornmeal', '0.66666668653488 cup white sugar', '3.5 teaspoons baking powder', '1 teaspoon salt', '1 cup milk', '0.33333334326744 cup vegetable oil', '1 large egg']

