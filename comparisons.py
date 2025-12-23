import os
import nltk

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
ingredients2 = ['2 cups flour', '1 cup cornmeal', '1 cup sugar', '1 ½ tablespoons baking powder', '1 teaspoon salt', '½ cup (8 tablespoons) butter (melted)', '½ cup oil', '1 ¼ cups milk', '3 large eggs', 'honey and extra butter for serving (optional)']
ingredients3 = ['1 cup all-purpose flour', '1 cup yellow cornmeal', '0.66666668653488 cup white sugar', '3.5 teaspoons baking powder', '1 teaspoon salt', '1 cup milk', '0.33333334326744 cup vegetable oil', '1 large egg']


def normalize_ingredients(raw_string):
    parsed = parse_ingredient(raw_string)

    if not parsed.amount:
        return f"No quantity found: {raw_string}"

    first_item = parsed.amount[0]

    # 1. Access quantity (text)
    qty_str = first_item.quantity

    # 2. Get the unit as a string (e.g., 'cup' or 'pound')
    # Using str() is the most reliable way to extract the name from the Unit object
    unit_str = str(first_item.unit)

    try:
        # 3. Clean fractions
        qty = (qty_str.replace('½', '.5')
               .replace('¼', '.25')
               .replace('¾', '.75')
               .replace('1 ½', '1.5')
               .replace('1 ¼', '1.25'))
        qty = "".join(qty.split())

        # 4. Pint Math
        measure = ureg(f"{qty} {unit_str}")

        # Check if it's volume or mass to decide the output unit
        if measure.check('[mass]'):
            return f"{measure.to('grams'):.2f} g"

        return f"{measure.to('ml'):.2f} ml"

    except Exception as e:
        # This catch helps if Pint doesn't recognize a unit like 'large' for eggs
        return f"Unconvertible: {qty_str} {unit_str}"

for item in ingredients2:
    print(f"Original: {item} -> Normalized {normalize_ingredients(item)}")
