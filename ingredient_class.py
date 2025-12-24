import json
class Ingredient:
    """
    represents an ingredient in a recipe
    """

    def __init__(self, name, amount, measure, type=None):
        """
        constructor class

        Parameters:
            name: str:
                name of the ingredient

            amount: int or float:
                the mass or volume or count of the ingredient

            measure: str:
                the measurement unit of the ingredient.
                example: g or ml or '' if dimenionless for ingredient such as
                1 egg

            type: str:
                possible type is solid or liquid or None
                used for determining possible conversion options

        """
        self._name = self._clean_name(name)
        self._amount = amount
        self._measure = measure
        self._type = None

        if type is None:
            density = None
        else:
            density = self._get_density_for_ingredient()

        self._density = density

    def name(self) -> str:
        return self._name

    def set_name(self, newName:str) -> None:
        if not isinstance(newName, str):
            raise TypeError(f"newName must be a str but is a {type(newName)}")
        self._name = newName

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

    def _get_density_for_ingredient(self) -> int | None:
        """
        internal method to get ingredient density
        returns the density as g/cup as an int if ingredient in json file
        otherwise returns None
        """
        DENSITIES = self._load_densities()
        try:
            density = DENSITIES[self._name]
            return density
        except KeyError:
            sortedKeys = sorted(DENSITIES.keys(), key=len, reverse=True)
            for key in sortedKeys:
                if key in self._name.lower():
                    return DENSITIES[key]
            return None

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
            if char.isalpha():
                cleanName += char.lower()

        return cleanName
