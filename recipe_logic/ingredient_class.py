from __future__ import annotations
import json
import fractions
import inflect
import os

class Ingredient:
    """
    represents an ingredient in a recipe
    """
    # constants
    KITCHEN_MEASURES = ('cup', 'tablespoon', 'teaspoon')
    METRIC_MEASURES = ('ml', 'g', 'l', 'kg')
    OUTLIER_MEASURES = ("gill", "pint", "pt", "quart", "qt",
                        "gallon", "gal", "shot", "oz", "ounce", "lb",
                        "pound", "dash", "pinch", "drop", "smidgen",
                        "fl oz", "fluid ounce")
    ODD_MEASURES = (
        # Original odd measures
        "head", "heads", "clove", "cloves",
        # Produce physical units
        "sprig", "sprigs",  # herbs (rosemary, thyme)
        "bunch", "bunches",  # bananas, green onions, cilantro, asparagus
        "stalk", "stalks",  # celery, lemongrass
        "ear", "ears",  # corn
        "bulb", "bulbs",  # garlic, fennel
        "crown", "crowns",  # broccoli
        "piece", "pieces", "pc", "pcs",  # ginger, turmeric
        "leaf", "leaves",  # bay leaves, basil, mint
        "root", "roots",  # ginger, horseradish
        "slice", "slices",  # bread, cheese, bacon
        "cube", "cubes",  # bouillon, ice
        "strip", "strips",  # bacon, zest
        # Meat & protein cuts
        "fillet", "fillets", "filet", "filets",  # fish, beef
        "breast", "breasts",  # chicken
        "thigh", "thighs",  # chicken
        "link", "links",  # sausage
        "pat", "pats",  # butter
        "rasher", "rashers",  # bacon (common in UK/Irish recipes)
        # Commercial packaging / Containers
        "can", "cans",
        "jar", "jars",
        "bottle", "bottles",
        "package", "packages", "pkg", "pkgs", "pack", "packs",
        "bag", "bags",
        "box", "boxes",
        "container", "containers",
        "carton", "cartons",
        "tub", "tubs",
        "tin", "tins",
        "envelope", "envelopes",  # yeast, gelatin
        "block", "blocks",  # cheese, tofu, chocolate
        "loaf", "loaves",  # bread
        "pouch", "pouches",
        "sachet", "sachets",
        "sheet", "sheets",
        # Informal / Hand measurements
        "handful", "handfuls",
        "scoop", "scoops",
        "shaved", "shaving", "shavings"
    )

    def __init__(self, name, amount, measure, ingState=None):
        """
        constructor class

        Parameters:
            name: str:
                name of the ingredient

            amount: int or float or unicode fraction str:
                the mass or volume or count of the ingredient
                if a unicode fraction, only accepts '¼', '½', '¾', '⅓', '⅔'

            measure: str:
                the measurement unit of the ingredient.
                example: g or ml or '' if dimensionless for ingredient such as
                1 egg

            ingState: str:
                possible ingState is solid or liquid or None
                used for determining possible conversion options

        Attributes:
                self._density:
                    None or int
                    value of density of the ingredient in ml/cup or g/cup

                self._state:
                    'solid' or 'liquid' or 'thing'
                    determines if to use g/cup or ml/cup for conversion and
                    effects output strings
                    'thing' used for ingredient without a measurement and just
                    an amount or if there are no measurements included in the
                    parser (common with optional ingredients, such as 'salt to
                    taste')

                self._keywords:
                    list that contains key words of the ingredient
                    removes filler words such as 'all', 'extra', 'virgin',
                    'fine', 'coarse', etc that are adjectives. Makes comparison
                    of ingredients more efficient



        """
        self._name = self._clean_name(name)
        self._kitchenAmount = None
        self._kitchenMeasure = None
        self._metricAmount = None
        self._metricMeasure = None
        self._density = None
        self._state = None
        self._defaultMeasure = None
        self._keywords = []

        if measure:
            self._state = self._verify_state(ingState)
            self._set_density_and_state_for_ingredient()
            self._set_amounts_and_measures(amount, measure)

        else:  # dimensionless ingredient, eg. 1 large egg
            self._state = "thing"
            self._metricAmount = amount
            self._kitchenAmount = amount

        self._add_keywords()

    def _set_amounts_and_measures(self,
                                  amount: str|int|float|fractions.Fraction,
                                  measure: str) -> None:
        """
        sets the attributes for ._kitchenAmount, ._kitchenMeasure,
        ._metricAmount
        """
        measure = measure.lower().strip()



        if measure in self.OUTLIER_MEASURES:
            measure, amount = self._convert_from_outlier(measure, amount)
            amount = self._convert_to_fraction(amount)
        elif measure in self.ODD_MEASURES:
            self._state = "thing"
            self._kitchenAmount = self._verify_amount(amount)
            self._metricAmount = self._kitchenAmount
            self._kitchenMeasure = measure
            self._metricMeasure = measure
            self._defaultMeasure = "kitchen"
            return

        measure = self._verify_measure(measure)

        if measure in self.KITCHEN_MEASURES:
            self._kitchenMeasure = measure
            self._kitchenAmount = self._verify_amount(amount)
            # _convert_to_metric returns tuple as (amount, measure)
            metricAmount, metricMeasure = self._convert_to_metric()
            self._metricAmount = self._convert_to_fraction(metricAmount)
            self._metricMeasure = metricMeasure
            self._defaultMeasure = "kitchen"

        elif measure in self.METRIC_MEASURES:
            self._defaultMeasure = "metric"

            if measure in ('ml', 'g'):
                self._metricAmount = self._verify_amount(amount)
                self._metricMeasure = measure
            elif measure in ('l', 'kg'):
                if measure == 'l':
                    measure = 'ml'
                else:
                    measure = 'g'
                self._metricAmount = self._verify_amount(amount) * 1000
                self._metricMeasure = measure

            kitchenAmount, kitchenMeasure = self._convert_to_kitchen()
            self._kitchenAmount = self._convert_to_fraction(kitchenAmount)
            self._kitchenMeasure = kitchenMeasure

    def _convert_from_outlier(self, measure:str,
                              amount:fractions.Fraction) -> tuple:
        """
        converts an outlier measurement ("gill", "pint", "pt", "quart", "qt",
        "gallon", "gal", "shot", "oz", "ounce", "lb", "pound", "dash", "pinch",
         "drop", "smidgen", "fl oz", "fluid ounce", "oz, "ounce) into an
         equivalent kitchen measurement.

        Returns:
            tuple that contains a str of the kitch measurement and an amount
            as a fractions.Fraction
        """
        if not amount:
            amount = 1
        match measure:
            case "gill":
                return "cup", 0.5 * amount
            case "pint" | "pt":
                return "cup", 2 * amount
            case "quart" | "qt":
                return "cup", 4 * amount
            case "gallon" | "gal":
                return "cup", 16 * amount
            case "shot":
                return "tablespoon", 3 * amount
            case "fl oz" | "fluid ounce":
                return "tablespoon", 2 * amount
            case "lb" | "pound":
                return "g", 453.59 * amount
            case "dash":
                return "teaspoon", amount/8
            case "pinch":
                return "teaspoon", amount/16
            case "smidgen" | "drop":
                return "teaspoon", amount/32
            case "oz" | "ounce":
                if self._state == "solid":
                    return "g", amount * 28.34952
                elif self._state == "liquid":
                    return "tablespoon", 2 * amount
                else:
                    raise ValueError(f"state: {self._state} not compatible "
                                     f"with ounce measure")


    def _verify_amount(self, amount: str | int | float) -> fractions.Fraction:
        """
        sets the attributes for ._kitchen_amount and ._metric_amount that the
        amount if an acceptable attribute for self._amount.
        If amount is a unicode fraction character it will be converted to a
        Fraction

        Precondition:
            amount must be an int, float, Fraction, or unicode fraction str
            character
        Raises:
            ValueError:
                if amount is not a correct value
            TypeError:
                if amount is not a correct type
        """
        if isinstance(amount, fractions.Fraction):
            return amount
        if type(amount) == int or type(amount) == float:
            return self._convert_to_fraction(amount)

        if not isinstance(amount, str):
            raise TypeError("amount must be a float, int, or unicode character"
                            f" of a fraction but is a {type(amount)}")
        try:
            return self._convert_to_fraction((amount))
        except ValueError:
            match amount:
                case '¼':
                    return fractions.Fraction(1, 4)
                case '½':
                    return fractions.Fraction(1,2)
                case '¾':
                    return fractions.Fraction(3,4)
                case '⅓':
                    return fractions.Fraction(1,3)
                case '⅔':
                    return fractions.Fraction(2,3)
                case '⅛':
                    return fractions.Fraction(1,8)
                case '⅜':
                    return fractions.Fraction(3,8)
                case _: # default value
                    raise ValueError(f"{amount} is not a recognized ingredient "
                                     "amount")

    def _verify_measure(self, measure:str) -> str:
        """
        verifies that the measure if an acceptable attribute for self._measure

        Parameters:
            measure:
                str that contains either 'cup' or 'tablespoon' or 'teaspoon' or
                'ml' or 'l', or 'g', or 'kg'

        Precondition:
            measure must be the correct type and the correct value
        Raises:
            ValueError:
                if measure is not a correct value
            TypeError:
                if measure is not a correct type
        """
        if not isinstance(measure, str):
            raise TypeError("measure must be a string but is a "
                            f"{type(measure)}")
        if measure == 'T' or measure == 'T.':
            return 'tablespoon'
        measure = measure.lower()
        if measure[-6:] == "liters" or measure[-5:] == "liter":
            if measure == "milliliter" or measure == "milliliters":
                return "ml"
            elif measure == "liter" or measure == "liters":
                return 'l'
        elif measure[-5:] == "grams" or measure[-4:] == "gram":
            if measure == "gram" or measure == "grams":
                return "g"
            elif measure == "kilogram" or measure == "kilogram":
                return 'kg'

        POSSIBLE_VALUES = ('cup', 'tablespoon', 'tbsp', 'tb', 't', 'teaspoon',
                           'tsp','ml', 'l', 'g', 'kg')
        if measure not in POSSIBLE_VALUES:
            # trim final character in case it is plural or '.'
            measure = measure[0:-1]
            if measure not in POSSIBLE_VALUES:
                raise ValueError("measure must be either 'cup', 'tablespoon', "
                                 "'teaspoon', 'tsp' 'ml', 'l', 'g', or 'kg' "
                                 f"but is {measure}")


        if measure in ('tablespoon', 'tbsp', 'tb'):
            return 'tablespoon'
        elif measure in ('teaspoon', 'tsp', 't'):
            return 'teaspoon'

        return measure

    def _verify_state(self, ingState: str) -> str | None:
        """
        verifies that the ingState is a possible attribute value for
        self._state

        Parameters:
            ingState:
                str or None:
                    can only be 'solid' or 'liquid' or None

        Precondition:
            ingState must be the correct type
            ingState must be the correct value

        Raises:
            TypeError:
                if ingState not the correct type
            ValueError:
                if ingState not the correct value
        """
        if not (isinstance(ingState, str) or ingState is None):
            raise TypeError("ingState must be a str or None but is a "
                            f"{type(ingState)}")
        if ingState is None:
            return ingState

        if ingState.lower() not in ('liquid', 'solid', "thing"):
            raise ValueError("possible values of ingState is 'liquid' or "
                             "'solid or 'thing'")

        return ingState.lower()

    def name(self) -> str:
        return self._name

    def metric_amount(self) -> fractions.Fraction:
        return self._metricAmount

    def kitchen_amount(self) -> fractions.Fraction:
        return self._kitchenAmount

    def metric_measure(self) -> str:
        return self._metricMeasure

    def kitchen_measure(self) -> str:
        return self._kitchenMeasure

    def _load_densities(self, filename="ingredient_densities.json") -> dict:
        """
        internal method to load a density file where ingredients are keys
        and density in g/cup are values
        # TODO need to figure out how to avoid loading this for each ingredient, maybe should be in recipe?
        """
        currentDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(currentDir, filename)
        try:
            with open(filePath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{filename} does not exist, cannot use a density table")
            return {}

    def _set_density_and_state_for_ingredient(self) -> None:
        """
        internal method to set ingredient density and state
        sets self._density as the density as g/cup as an int if ingredient in
        json file. Sets the self._state to 'solid' or 'liquid'
        """
        DENSITIES = self._load_densities()
        try:
            ingDetails = DENSITIES[self._name]
            self._density = ingDetails['density']
            self._state = ingDetails['state']

        except KeyError:
            sortedKeys = sorted(DENSITIES.keys(), key=len, reverse=True)
            for key in sortedKeys:
                if key in self._name:
                    ingDetails = DENSITIES[key]
                    self._density = ingDetails['density']
                    self._state = ingDetails['state']
                    return
            self._density = 240
            self._state = "liquid"
            return

    def _clean_name(self, name:str) -> str:
        """
        internal method to clean up the name of an ingredient
        removes non-alpha characters and returns a lowercase string
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str but is a {type(name)}")

        if name.isalpha():
            return name.lower().strip()

        cleanName = ''
        for char in name:
            if char.isalpha() or char == ' ':
                cleanName += char.lower()
            elif char == '-' or char == '_':
                cleanName += ' '
        return cleanName.strip()

    def _add_keywords(self) -> None:
        """
        adds all keywords from self._name to self._keywords.
        keywords are words that are not adjectives such as 'all', 'coarse',
        'virgin', etc
        removes plural from a keyword
        """
        # constant
        FILLER_WORDS = ('all', 'purpose', 'extra', 'large', 'small', 'medium',
                        'fine', 'coarse', 'thick', 'thin', 'softened',
                        'chilled', 'cold', 'room', 'temperature', 'sifted',
                        'packed', 'leveled', 'spooned', 'grated', 'minced',
                        'chopped', 'diced', 'sliced', 'crushed', 'beaten',
                        'whisked', 'melted', 'organic', 'natural', 'virgin',
                        'unsalted', 'salted', 'sweetened', 'unsweetened',
                        'light', 'dark', 'filler', 'peeled', 'cored', 'seeded',
                        'pitted', 'halved', 'quartered', 'mashed', 'pureed',
                        'blanched', 'toasted', 'roasted',
                        'baked', 'boiled', 'steamed', 'smoked', 'cured',
                        'aged', 'ground', 'milled', 'cracked', 'shredded',
                        'torn', 'rinsed', 'drained', 'thawed', 'cubed',
                        'fresh', 'dried', 'raw', 'frozen', 'ripe', 'unripe',
                        'canned', 'tinned', 'bottled', 'jarred', 'homemade',
                        'pure', 'concentrated', 'clarified', 'evaporated',
                        'condensed', 'powdered', 'granulated', 'warm', 'hot',
                        'boiling', 'ice', 'iced', 'jumbo', 'mini', 'whole',
                        'mild', 'spicy', 'optional', 'taste', 'garnish',
                        'divided', 'plus', 'more', 'about', '')

        # hardcode ingredients that need multipart descriptors
        if "sweetened condensed milk" in self._name:
            self._keywords = ["sweetened condensed milk"]
        elif "unsweetened condensed milk" in self._name:
            self._keywords = ["unsweetened condensed milk"]
        elif "coconut milk" in self._name:
            self._keywords = ["coconut milk"]
        elif "baking soda" in self._name:
            self._keywords = ["baking soda"]
        elif "baking powder" in self._name:
            self._keywords = ["baking powder"]
        elif "white sugar" in self._name:
            self._keywords = ["white sugar"]
        elif "brown sugar" in self._name:
            self._keywords = ["brown sugar"]
        elif "powdered sugar" in self._name:
            self._keywords = ["powdered sugar"]
        elif "confectioners sugar" in self._name:
            self._keywords = ["confectioners sugar"]
        elif  "icing sugar" in self._name:
            self._keywords = ["icing sugar"]
        elif "evaporated milk" in self._name:
            self._keywords = ["evaporated milk"]
        elif "lemon juice" in self._name:
            self._keywords = ["lemon juice"]
        elif "lemon zest" in self._name:
            self._keywords = ["lemon zest"]
        else:
            words = self._name.split(' ')
            for word in words:
                if word not in FILLER_WORDS:
                    self._keywords.append(word)

        # remove keyword plural
        self._unpluralize_keywords()

    def _unpluralize_keywords(self):
        """
        goes through the current self._keywords and removes any plurals, to
        ensure comparison with other ingredients
        """
        if len(self._keywords) == 0:
            return

        p = inflect.engine()
        for i in range(len(self._keywords)):
            word = self._keywords[i]
            self._keywords[i] = p.singular_noun(word) or word

    def defMeasure(self):
        """
        returns the default measurement for this ingredient
        """
        return self._defaultMeasure

    def keywords(self) -> list:
        """
        returns a list of the ingredient's keywords
        """
        return self._keywords

    def _convert_to_kitchen(self) -> tuple:
        """
        converts ingredient amount of metric units to kithcen measurements
        of cups or tablespoons or teaspoons.
        Example 125 g of flour will convert to 1 cup

        Returns:
            tuple of strings in order of (amount, measure)

        Precondition:
            self._measure but be either `g` or `ml`

        Raises:
            ValueError:
                if self._measure not the correct value
        """
        METRIC_UNITS = ('g', 'ml')
        if self._metricMeasure not in METRIC_UNITS:
            raise ValueError("self._metricMeasure must be 'g' or 'ml'  but is "
                             f"{self._metricMeasure}")
        # constants
        TABLESPOON_TO_CUP = fractions.Fraction(1,16)
        TEASPOON_TO_CUP = fractions.Fraction(1,48)
        QUARTER_CUP = fractions.Fraction(1,4)

        amount = fractions.Fraction(self._metricAmount / self._density)

        # format kitchen measurement
        if amount >= QUARTER_CUP:
            # formattedAmount = self._format_amount(amount) # will convert 1.0000 to 1 for example
            # if formattedAmount != 1: # TODO come back and figure out how to handle this
            #     return amount, 'cups'
            # else:
            return amount.limit_denominator(48), 'cup'

        elif QUARTER_CUP > amount >= TABLESPOON_TO_CUP / 2:
            # amount is between 1/2 tablespoon and 1/4 cup
            amount = amount * (1/TABLESPOON_TO_CUP)
            return amount.limit_denominator(12), 'tablespoon'
        else:
            amount = amount * (1/TEASPOON_TO_CUP)
            return amount.limit_denominator(8), 'teaspoon'

    def to_metric(self) -> str:
        """
        returns a string of the measurement in g (grams) if self._state is
        'solid' or mL if self._state is 'liquid'
        """
        if self._state == 'thing':
            return ''
        measure = self._kitchenMeasure
        if measure == 'ml' or measure == 'g':
            return f"{self._metricAmount} {measure}"
        elif measure in ('cup', 'teaspoon', 'tablespoon') :
            amount, measure = self._convert_to_metric()
            return f"{self._format_amount(amount)} {measure}"
        else:
            raise Exception(f".self._kitchenMeasure: {measure} "
                            "is not a possible value")

    def _convert_to_metric(self) -> tuple:
        """
        converts ingredient amount and measure to metric units.
        Example 1 cup of flour will convert to 125 g

        Returns:
            tuple of strings in order of (amount, measure)

        Precondition:
            self._measure but be either `cup` or `tablespoon` or `teaspoon`

        Raises:
            ValueError:
                if self._measure not the correct value
        """
        KITCHEN_MEASURES = ('cup', 'tablespoon', 'teaspoon')
        if self._kitchenMeasure not in KITCHEN_MEASURES:
            raise ValueError("self._measure must be 'cup' or 'tablespoon' or"
                             f"'teaspoon', but is {self._measure}")
        if self._density is None:
            raise ValueError(f"Ingredient: {self._name} does not have a "
                              f"density and conversion to metric is not "
                              f"possible")

        if self._kitchenMeasure == 'cup':
            conversionFactor = 1
        elif self._kitchenMeasure == 'teaspoon':
            conversionFactor = 1/48
        elif self._kitchenMeasure == 'tablespoon':
            conversionFactor = 1/16
        else:
            raise Exception(f"self._kitchenMeasure: {self._kitchenMeasure} is "
                            "not a possible value.")

        amount = self._convert_to_fraction(self._kitchenAmount * self._density * conversionFactor)

        if self._state == 'solid':
            return amount, 'g'
        elif self._state == 'liquid':
            return amount, 'ml'
        else:
            raise ValueError("self._state must be either 'solid' or liquid' "
                             f"but is {self._state}")


    def _convert_to_fraction(self, value: str |int | float | fractions.Fraction) ->fractions.Fraction:
        """
        converts value into a fraction object

        Precondition:
            value must be the correct type

        Raises:
            TypeError:
                if value not the correct type
        """
        if isinstance(value, fractions.Fraction):
            return value
        if not (isinstance(value, str)
                or isinstance(value, int)
                or isinstance(value, float)):
            raise TypeError(f"value must be a str that can be converted to an "
                            f"int or float or an int or float")
        try:
            float(value)
            return fractions.Fraction(str(value)).limit_denominator(48)
        except ValueError:
            raise ValueError(f"value: {(value)} be a str that represents a "
                             f"int or float")

    def _format_amount(self, value: int | float | fractions.Fraction)  -> int | float:
        """
        formats an int, float, or fraction object into a human readable int or
        float

        Precondition:
            value must be the correct type

        Raises:
            TypeError:
                if value not the correct type
        """
        if not (isinstance(value, int)
                or isinstance(value, float)
                or isinstance(value, fractions.Fraction)):
            raise TypeError("value must be an int, float or Fraction but is "
                            f"{type(value)}")
        value = round(float(value), 4)
        if value == int(value): # checks if value is can be an int
            return int(value)

        return value


    def __str__(self) -> str:
        """
        returns print friendly str representation of an ingredient
        """
        if self._state == 'thing': # dimensionless
            return f"{self._kitchenAmount} {self._name}"
        elif self._defaultMeasure == "kitchen":
            return (f"{self.kitchen_amount_str()} {self.kitchen_measure()} "
                    f"{self._name}")
        else:
            return (f"{self.metric_amount_str()} {self.metric_measure()} "
                    f"{self._name}")

    def metric_amount_str(self) -> str:
        """
        formats the output for a metric amount into a readable string
        converts odd fractions to decimal
        """
        return f"{round(float(self._metricAmount), 2):g}"

    def kitchen_amount_str(self) -> str:
        return f"{round(float(self._kitchenAmount), 2):g}"

    def compare_ingredient(self, other) -> bool:
        """
        checks if other is a same or similar ingredient as self and returns
        a boolean

        Precondition:
            other must be the correct type

        Raises:
            TypeError:
                if other not the correct type
        """
        if not isinstance(other, Ingredient):
            raise TypeError("other must be an Ingredient but is a "
                            f"{type(other)}")

        for keyword in self._keywords:
            if keyword in other._keywords:
                return True
        return False

    def difference(self, other, kitchenMeasure:bool=False,
                   metricMeasure:bool=False) -> tuple:
        """
        normalizes other to self and returns the difference + or - that other
        is compared to self

        Parameters:
            other:
                Ingredient

            kitchenMeasure:
                bool:
                    default: false
                        flag to determine if difference returned as kitchen
                        measurement

            metricMeasure:
                bool:
                    default: false
                        flag to determine if difference returned as kitchen
                        metric measurement

        Precondition:
            other must be an Ingredient
            other must be a similar Ingredient (compare_ingredient returns True)
            other must the same ._state

        Raises:
            TypeError:
                if other is not the correct type
            ValueError:
                if other is not a comparable ingredient
                if other is not the correct ._state
        """
        if not isinstance(other, Ingredient):
            raise TypeError("other must be an Ingredient but is a "
                            f"{type(other)}")

        if self._state == "thing":
            amountDiff = self._kitchenAmount - other._kitchenAmount
            return f"{round(float(amountDiff),2):g}", ""

        if kitchenMeasure:
            amountDiff = self._kitchen_difference(other)
        elif metricMeasure:
            amountDiff = self._metric_difference(other)
        # elif self._defaultMeasure == other._defaultMeasure:
        #     if self._defaultMeasure == "metric":
        #         amountDiff = self._metric_difference(other)
        #     else:
        #         amountDiff = self._kitchen_difference(other)
        else:
             # returns kitchen measurement if not equal
            amountDiff = self._kitchen_difference(other)
        return f"{round(float(amountDiff[0]), 2):g}", amountDiff[1]


    def _metric_difference(self, other) -> tuple:
        """
        returns the difference of the metric amount between two ingredients
        as a tuple with the amount difference between self and other as
        the first element and the shared unit as the second element
        """
        amountDiff = self._metricAmount - other._metricAmount
        return amountDiff, self._metricMeasure



    def _kitchen_difference(self, other) -> tuple:
        """
        returns the difference in the largest shared unit of two measurements
        in kitchen units

        Parameters:
                firstMeasure:
                    tuple: of two elements. First element is a
                    fraction.Fraction. Second element is a kitchen measurement
                    such as ('cup', 'teaspoon', 'tablespoon')

        Returns:
                tuple: of two elements. First element is the difference as
                a fractions.Fractions between the fristMeasure and
                secondMeasure. Second element is the largest possible shared
                unit.
                Example:
                    firstMeasure: (1/2, "cup")
                    secondMeasure: (1, "cup")
                    returns: (-1/2, "cup")

                    example2:
                     firstMeasure: (1, "tablespoon")
                    secondMeasure: (2, "teaspoon")
                    returns: (1, "teaspoon")
        """
        if self.kitchen_measure() == other.kitchen_measure():
            amountDiff = self.kitchen_amount() - other.kitchen_amount()
            return amountDiff, self._kitchenMeasure

        # find smallest shared unit, convert and return difference
        else:
            if (self.kitchen_measure() == "teaspoon"
                    or other.kitchen_measure() == "teaspoon"):
                # convert to teaspoon
                amountDiff = (self._convert_to_teaspoon()
                              - other._convert_to_teaspoon())
                return amountDiff, "teaspoon"
            else:
                # convert to tablespoon, as one has to be less than cup
                amountDiff = (self._convert_to_tablespoon()
                              - other._convert_to_tablespoon())
                return amountDiff, "tablespoon"

    def _convert_to_teaspoon(self) -> fractions.Fraction:
        """
        converts a kitchen measurement to the amount in teaspoons and returns it
        """
        if self._kitchenMeasure == "teaspoon":
            return self._kitchenAmount
        elif self._kitchenMeasure == "tablespoon":
            return self._kitchenAmount * 3
        elif self._kitchenMeasure == "cup":
            return self._kitchenAmount * 48
        else:
            raise ValueError(f"self._kitchenMeasure must be a cup, "
                             f"tablespoon, or teaspoon, but was "
                             f"{self._kitchenMeasure}")


    def _convert_to_tablespoon(self) -> fractions.Fraction:
        """
        converts a kitchen measurement to the amount in tablespoons and returns it
        """
        if self._kitchenMeasure == "tablespoon":
            return self._kitchenAmount
        elif self._kitchenMeasure == "teaspoon":
            return self._kitchenAmount / 3
        elif self._kitchenMeasure == "cup":
            return self._kitchenAmount * 16
        else:
            raise ValueError(f"self._kitchenMeasure must be a cup, tablespoon, "
                             f"or teaspoon, but was {self._kitchenMeasure}")

    def clone(self) -> Ingredient:
        """
        creates a copy of the ingredient with all the same attributes
        returns a copy of tnis ingredient
        """
        if self._defaultMeasure == "kitchen":
            cloneIng = Ingredient(self._name, self.kitchen_amount(),
                              self.kitchen_measure(), self._state)
        elif self._defaultMeasure == "metric":
            cloneIng = Ingredient(self._name, self.metric_amount(),
                                  self.metric_measure(), self._state)
        else:
            cloneIng = Ingredient(self._name, self.kitchen_amount(),
                                  self.kitchen_measure(), self._state)
        return cloneIng

    def empty_ingredient(self):
        """
        sets all measurements to 0
        Used for comparison
        """
        self._kitchenAmount = self._convert_to_fraction(0)
        self._metricAmount = self._convert_to_fraction(0)