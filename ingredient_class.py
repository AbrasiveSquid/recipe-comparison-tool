import json
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

        """
        self._name = self._clean_name(name)
        self._amount = self._verify_amount(amount)
        self._measure = self._verify_measure(measure)
        self._density = None
        self._state = self._verify_state(ingState)

        self._set_density_and_state_for_ingredient()

    def _verify_amount(self, amount: str | int | float) -> int | float:
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
        if type(amount) == int or type(amount) == float:
            return round(amount, 2)

        if not isinstance(amount, str):
            raise TypeError("amount must be a float, int, or unicode character"
                            f" of a fractin but is a {type(amount)}")

        match amount:
            case '¼':
                return 0.25
            case '½':
                return 0.5
            case '¾':
                return 0.75
            case '⅓':
                return round(1/3, 2)
            case '⅔':
                return round(2/3, 2)
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
        POSSIBLE_VALUES = ('cup', 'tablespoon', 'teaspoon', 'ml', 'l', 'g',
                           'kg')
        if measure.lower() not in POSSIBLE_VALUES:
            # trim final character in case it is plural
            measure = measure[0:-1].lower()
            if measure not in POSSIBLE_VALUES:
                raise ValueError("measure must be either 'cup', 'tablespoon', "
                                 "'teaspoon', 'ml', 'l', 'g', or 'kg'")

        if measure == 'l': # convert to ml
            self._amount *= 1000
            return 'ml'
        elif measure == 'kg': # convert to g
            self._amount *= 1000
            return 'g'

        return measure.lower()

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

    def amount(self) -> int | float:
        return self._amount

    def set_amount(self, newAmount:int|float) -> None:
        if not (type(newAmount) == int or type(newAmount) == float):
            raise TypeError("newAmount must be an int or float but is a "
                            f"{type(newAmount)}")
        self._amount = newAmount

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
        # TODO figure out cutoff amount
        """
        if self._measure == 'cup':
            return f"{self._amount} {self._measure}"
        elif self._measure == 'g' or self._measure == 'ml':
            amount, measure = self._convert_to_metric()

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

        amount = self._amount * self._density
        if self._state == 'solid':
            return (amount, 'g')
        elif self._state == 'liquid':
            return (amount, 'ml')
        else:
            raise ValueError("self._state must be either 'solid' or liquid' "
                             f"but is {self._state}")



    def to_metric(self) -> str:
        """
        returns a string of the measurement in g (grams) if self._state is
        'solid' or mL if self._state is 'liquid'
        """
        pass


