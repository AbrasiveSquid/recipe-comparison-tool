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

from ingredient_parser import parse_ingredient

class Recipe:
    """
    this is the recipe class
    """
    def __init__(self, title:str, source:str, ingredientList:list, steps:str):
        self._title = title
        self._source = source
        self._instructions = steps
        self._ingredients = []
        self._optionalIngredients = []

        self._parse_ingredients(ingredientList)

    def _parse_ingredients(self, ingredientList:list):
        if not isinstance(ingredientList, list):
            raise TypeError("ingredientList must be a list but is a "
                            f"{type(ingredientList)}")
        for ingredient in ingredientList:
            parsed = parse_ingredient(ingredient)

            if parsed.amount:
                item = parsed.amount[0]

                qty = item.quantity
                unit = str(item.unit)
                ingredientName = parsed.name[0].text
                self._ingredients.append(Ingredient(ingredientName, qty, unit))
            elif parsed.name:
                for optionalIngredient in parsed.name: # no qty available
                    self._optionalIngredients.append(Ingredient(optionalIngredient.text, 0, 0))

            else:
                raise ValueError(f"No quantity found: {ingredient}")

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
        resultStr += f"\n**Instructions**\n{self._instructions}\n"

        return resultStr

