import json
import fractions

class Ingredient:
    """
    represents an ingredient in a recipe
    """

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
        self._amount = self._verify_amount(amount)
        self._measure = None
        self._density = None
        self._state = None
        self._keywords = []

        if measure:
            self._measure = self._verify_measure(measure)
            self._state = self._verify_state(ingState)
            self._set_density_and_state_for_ingredient()

        else: # dimensionless ingredient, eg. 1 large egg
            self._state = 'thing'

        self._add_keywords()


    def _verify_amount(self, amount: str | int | float) -> fractions.Fraction:
        """
        verifies that the amount if an acceptable attribute for self._amount
        If amount is a unicode fraction character it will be converted to float

        Precondition:
            amount must be an int, float, or unicode fraction str character
        Raises:
            ValueError:
                if amount is not a correct value
            TypeError:
                if amount is not a correct type
        """
        if (type(amount) == int or type(amount) == float or
                type(amount) == fractions.Fraction):
            return self._convert_to_fraction(float(amount))

        if not isinstance(amount, str):
            raise TypeError("amount must be a float, int, or unicode character"
                            f" of a fraction but is a {type(amount)}")
        try:
            return self._convert_to_fraction((float(amount)))
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

        POSSIBLE_VALUES = ('cup', 'tablespoon', 'tbsp', 'tb', 't', 'teaspoon',
                           'tsp','ml', 'l', 'g', 'kg')
        if measure not in POSSIBLE_VALUES:
            # trim final character in case it is plural or '.'
            measure = measure[0:-1]
            if measure not in POSSIBLE_VALUES:
                raise ValueError("measure must be either 'cup', 'tablespoon', "
                                 "'teaspoon', 'tsp' 'ml', 'l', 'g', or 'kg' but"
                                 f"is {measure}")

        if measure == 'l': # convert to ml
            self._amount *= 1000
            return 'ml'
        elif measure == 'kg': # convert to g
            self._amount *= 1000
            return 'g'
        elif measure in ('tablespoon', 'tbsp', 'tb'):
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

        if ingState.lower() not in ('liquid', 'solid'):
            raise ValueError("possible values of ingState is 'liquid' or "
                             "'solid")

        return ingState.lower()

    def name(self) -> str:
        return self._name

    def set_name(self, newName:str) -> None:
        if not isinstance(newName, str):
            raise TypeError(f"newName must be a str but is a {type(newName)}")
        self._name = self._clean_name(newName)
        self._set_density_and_state_for_ingredient()

    def amount(self) -> fractions.Fraction:
        return self._amount

    def set_amount(self, newAmount:int|float) -> None:
        if not (type(newAmount) == int or type(newAmount) == float):
            raise TypeError("newAmount must be an int or float but is a "
                            f"{type(newAmount)}")
        self._amount = self._convert_to_fraction(newAmount)

    def measure(self) -> str:
        return self._measure

    def set_measure(self, newMeasure:str) -> None:
        if not isinstance(newMeasure, str):
            raise TypeError("newMeasure must be a str but is a "
                            f"{type(newMeasure)}")
        self._measure = newMeasure

    def _load_densities(self, filename="ingredient_densities.json") -> dict:
        """
        internal method to load a density file where ingredients are keys
        and density in g/cup are values
        # TODO need to figure out how to avoid loading this for each ingredient, maybe should be in recipe?
        """
        try:
            with open(filename, 'r') as f:
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
            return

    def _clean_name(self, name:str) -> str:
        """
        internal method to clean up the name of an ingredient
        removes non-alpha characters and returns a lowercase string
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str but is a {type(name)}")

        if name.isalpha():
            return name.lower()

        cleanName = ''
        for char in name:
            if char.isalpha() or char == ' ':
                cleanName += char.lower()
            elif char == '-' or char == '_':
                cleanName += ' '
        return cleanName

    def to_kitchen_measurement(self) -> str:
        """
        returns a string of the measurement with number of cups or tablespoons
        or teaspoons depending on the amount
        """
        if self._state == 'thing':
            return ''

        measure = self._measure
        if measure == 'cup':
            return f"{self._amount} {measure}"
        elif measure == 'g' or measure == 'ml':
            amount, measure = self._convert_to_kitchen()
            return f"{amount} {measure}"
        else:
            raise Exception(f"._measure: {self._measure} is not a possible "
                            "value")

    def _add_keywords(self) -> None:
        """
        adds all keywords from self._name to self._keywords.
        keywords are words that are not adjectives such as 'all', 'coarse',
        'virgin', etc
        """
        # constant
        FILLER_WORDS = ('all', 'purpose', 'extra', 'large', 'small', 'medium',
                        'fine', 'coarse', 'thick', 'thin', 'melted',
                        'softened', 'chilled', 'cold', 'room', 'temperature',
                        'sifted', 'packed', 'leveled', 'spooned', 'grated',
                        'minced', 'chopped', 'diced', 'sliced', 'crushed',
                        'beaten', 'whisked', 'melted', 'organic', 'natural',
                        'virgin', 'unsalted', 'salted', 'sweetened',
                        'unsweetened', 'light', 'dark')

        words = self._name.split(' ')
        for word in words:
            if word not in FILLER_WORDS:
                self._keywords.append(word)

        # hardcode white and brown sugar so aren't returned as the same
        if self._keywords == ['white', 'sugar']:
            self._keywords = ['white sugar']
        elif self._keywords == ['brown', 'sugar']:
            self._keywords = ['brown sugar']


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
        if self._measure not in METRIC_UNITS:
            raise ValueError("self._measure must be 'g' or 'ml'  but is "
                             f"{self._measure}")
        # constants
        TABLESPOON_TO_CUP = fractions.Fraction(1,16)
        TEASPOON_TO_CUP = fractions.Fraction(1,48)
        QUARTER_CUP = fractions.Fraction(1,4)

        amount = fractions.Fraction(self._amount / self._density)

        # format kitchen measurement
        if amount >= QUARTER_CUP:
            amount = self._format_amount(amount)
            if amount != 1:
                return amount, 'cups'
            else:
                return amount, 'cup'
        elif amount < QUARTER_CUP and amount >= TABLESPOON_TO_CUP / 2:
            # amount is between 1/2 tablespoon and 1/4 cup
            amount = self._format_amount(amount * 1/TABLESPOON_TO_CUP)
            return amount, 'Tbsp'
        else:
            amount = self._format_amount(amount * 1/TEASPOON_TO_CUP)
            return amount, 'tsp'

    def to_metric(self) -> str:
        """
        returns a string of the measurement in g (grams) if self._state is
        'solid' or mL if self._state is 'liquid'
        """
        if self._state == 'thing':
            return ''
        measure = self._measure
        if measure == 'ml' or measure == 'g':
            return f"{self._amount} {measure}"
        elif measure in ('cup', 'teaspoon', 'tablespoon') :
            amount, measure = self._convert_to_metric()
            return f"{amount} {measure}"
        else:
            raise Exception(f"._measure: {self._measure} is not a possible "
                            "value")

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
        if self._measure not in KITCHEN_MEASURES:
            raise ValueError("self._measure must be 'cup' or 'tablespoon' or"
                             f"'teaspoon', but is {self._measure}")

        if self._measure == 'cup':
            conversionFactor = 1
        elif self._measure == 'teaspoon':
            conversionFactor = 1/48
        elif self._measure == 'tablespoon':
            conversionFactor = 1/16
        else:
            raise Exception(f"_measure: {self._measure} is not a possible"
                            " value.")

        amount = self._amount * self._density * conversionFactor

        amount = self._format_amount(amount)

        if self._state == 'solid':
            return amount, 'g'
        elif self._state == 'liquid':
            return amount, 'ml'
        else:
            raise ValueError("self._state must be either 'solid' or liquid' "
                             f"but is {self._state}")


    def _convert_to_fraction(self, value:int | float) -> fractions.Fraction:
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
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("value must be an int, float or Fraction but is "
                            f"{type(value)}")

        return fractions.Fraction(value)

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
            if self._amount == 0:
                return f"{self._name}"
            else:
                return f"{self._amount} {self._name}"
        else:
            return f"{self._amount} {self._measure} {self._name}"

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
