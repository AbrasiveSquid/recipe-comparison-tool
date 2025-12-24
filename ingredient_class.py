
class Ingredient:
    """
    represents an ingredient in a recipe
    """

    def __init__(self, name, amount, measure):
        self._name = name
        self._amount = amount
        self._measure = measure

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