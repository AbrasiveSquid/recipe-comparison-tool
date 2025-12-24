import os
import nltk
import json

# 1. Force NLTK to use ONLY your local project folder
# This 'NLTK_DATA' environment variable is the strongest way to redirect it
project_root = os.path.dirname(os.path.abspath(__file__))
local_nltk_data = os.path.join(project_root, 'nltk_data')
os.environ['NLTK_DATA'] = local_nltk_data

# 2. Tell the Python NLTK module to point there too
nltk.data.path = [local_nltk_data]

# 3. "Fake" the download function so if any library calls it, nothing happens
def disabled_download(*args, **kwargs):
    print("NLTK download blocked - using local project data.")
    return True

nltk.download = disabled_download

from pint import UnitRegistry
from ingredient_parser import parse_ingredient


ureg = UnitRegistry()

ingredients1 = ['1 cup (120g) fine cornmeal', '1 cup (125g) all-purpose flour (spooned & leveled)', '1 teaspoon baking powder', '1/2 teaspoon baking soda', '1/8 teaspoon salt', '1/2 cup (8 Tbsp; 113g) unsalted butter, melted and slightly cooled', '1/3 cup (67g) packed light or dark brown sugar', '2 Tablespoons (30ml) honey', '1 large egg, at room temperature', '1 cup (240ml) buttermilk, at room temperature*']
ingredients2 = ['2 ½ cups flour', '1 cup cornmeal', '1 cup sugar', '1 ½ tablespoons baking powder', '1 teaspoon salt', '½ cup (8 tablespoons) butter (melted)', '½ cup oil', '1 ¼ cups milk', '3 large eggs', 'honey and extra butter for serving (optional)']
ingredients3 = ['1 cup all-purpose flour', '1 cup yellow cornmeal', '0.66666668653488 cup white sugar', '3.5 teaspoons baking powder', '1 teaspoon salt', '1 cup milk', '0.33333334326744 cup vegetable oil', '1 large egg']

def load_densities(filename="ingredient_densities.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{filename} does not exist, cannot use a density table")
        return {}

DENSITIES = load_densities()

def get_density_for_ingredient(ingredient:str) -> int | None:
    try:
        density = DENSITIES[ingredient.lower()]
        return density
    except KeyError:
        sortedKeys = sorted(DENSITIES.keys(), key=len, reverse=True)
        for key in sortedKeys:
            if key in ingredient.lower():
                return DENSITIES[key]
        return None

def normalize_ingredients(raw_string):
    try:
        parsed = parse_ingredient(raw_string)

        if not parsed.amount:
            return f"No quantity found: {raw_string}"

        first_item = parsed.amount[0]

        # 1. Access quantity (text)
        qty_str = first_item.quantity

        unit_str = str(first_item.unit)
        ingredient = parsed.name[0].text
        measure = ureg(f"{qty_str} {unit_str}")

        # Check if it's volume or mass to decide the output unit
        # if measure.check('[mass]'):
        if not unit_str:
            return ingredient, f"{measure}"
        elif measure.check('[mass]'):
            return ingredient, f"{measure.to('g'):.1f}"

        elif str(measure.dimensionality) == 'dimensionless':
            return measure

        elif measure.check('[volume]'):
            densityValue = get_density_for_ingredient(ingredient)

            if densityValue:
                density = ureg.Quantity(densityValue, "gram / cup")
                mass = measure * density
                return ingredient, f"{mass.to('g'):.1f}"
            else:
                water_density = ureg.Quantity(240, "gram / cup")
                mass = measure * water_density
                return ingredient, f"{mass.to('g'):.1f}"
        else:
            raise Exception

    except Exception as e:
        # This catch helps if Pint doesn't recognize a unit like 'large' for eggs
        return f"Unconvertible: {qty_str} {unit_str}"


def compare_recipes(recipe1:list, recipe2:list) -> str:
    firstRecipeList = []
    secondRecipeList = []

    # TODO need to find ways to link ingredients together
    for item in recipe1:
        firstRecipeList.append(normalize_ingredients(item))

    for item in recipe2:
        secondRecipeList.append(normalize_ingredients(item))

    print(firstRecipeList)
    print(secondRecipeList)
    print("Recipe 1\t\t\t\t\t\t\t\tRecipe2")
    n = len(firstRecipeList)
    m = len(secondRecipeList)
    i = 0
    while i < n and i < m:
        print(f"{firstRecipeList[i][0]}: {firstRecipeList[i][1]}\t\t\t\t\t\t{secondRecipeList[i][0]}: {secondRecipeList[i][1]}")
        i += 1
    while i < n:
        print(f"{firstRecipeList[i][0]}: {firstRecipeList[i][1]}")
        i += 1
    while i < m:
        print(f"\t\t\t\t\t\t\t{secondRecipeList[i][0]}: {secondRecipeList[i][1]}")
        i += 1


compare_recipes(ingredients1, ingredients2)


