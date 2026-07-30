from pint.compat import dask_array

from recipe_logic.recipe_scraper import fetch_recipe
from recipe_logic.recipe_class import Recipe
from urllib.parse import urlparse

class RecipeComparator:
    """
    main program class for recipe comparison. Receives two url, validates them,
    calls the scrapper, creates a Recipe object for each, then compares the recipes and returns
    the comparison
    """


    def __init__(self, data1:str, data1Type:str,
                 data2:str, data2Type:str):
        """
        Creates the attributes and calls methods to create recipes and
        run the comparison between recipes

        Parameters:
            data1: str
                can be a url or a string of ingredients
            data2: str
                can be a url or a string of ingredients
            dataType: str
                can be 'url' or 'ingredients' and depending on datatype affects
                what validation methods and scraping is called

        Raises:
            ValueError:
                if data1Type is not the correct value ('url' or 'ingredients')
                if data2Type is not the correct value ('url' or 'ingredients')
            TypeError:
                if data1Type not the correct type
                if data2Type not the correct type
                if data1 not the correct type
                if data2 not the correct type
        """
        if not isinstance(data1Type, str):
            raise TypeError(f"data1Type must be a str but is a "
                            f"{type(data1Type)}.")
        if not isinstance(data2Type, str):
            raise TypeError(f"data2Type must be a str but is a "
                            f"{type(data2Type)}.")
        if not isinstance(data1, str):
            raise TypeError(f"data1 must be a str but is a "
                            f"{type(data1)}.")
        if not isinstance(data2, str):
            raise TypeError(f"data2 must be a str but is a "
                            f"{type(data2)}.")
        if not (data1Type == "url" or data1Type == "ingredients"):
            raise ValueError(f"dataType must be 'url' or 'ingredients' but is "
                             f"{data1Type}")
        if not (data2Type == "url" or data2Type == "ingredients"):
            raise ValueError(f"dataType must be 'url' or 'ingredients' but is "
                             f"{data2Type}")

        if data1Type == "url":
            self.firstRecipe = self._create_recipe_with_url(data1)
        elif data1Type == "ingredients":
            self.firstRecipe = self._create_recipe_with_str(data1)

        if data2Type == "url":
            self.secondRecipe = self._create_recipe_with_url(data2)
        elif data2Type == "ingredients":
            self.secondRecipe = self._create_recipe_with_str(data2)

        self.comparison = self.firstRecipe.compare_recipe(self.secondRecipe)

    def get_first_recipe(self) -> Recipe:
        """
        getter for firstRecipe
        """
        return self.firstRecipe

    def get_second_recipe(self) -> Recipe:
        """
        getter for secondRecipe
        """
        return self.secondRecipe

    def get_comparison(self) -> list:
        """
        getting for the comparison of recipes
        """
        return self.comparison

    def _create_recipe_with_url(self, url:str) -> Recipe:
        """
        takes a url that points to a recipe and returns a Recipe object
        First validates the url, then scrapes the website, then creates a
        python object of a Recipe
        """
        self._validate_url(url)
        recipeScraped = fetch_recipe(url)

        if not recipeScraped:
            raise RecipeExtractionError(url)

        recipe = Recipe(recipeScraped["title"], url,
                        recipeScraped["ingredients"],
                        recipeScraped["steps"])

        return recipe

    def _create_recipe_with_str(self, data:str):
        """
        takes a string that contains ingredients separated by '\n' and
        returns a Recipe object.

        Parameters:
            data: str
                must contain ingredients separated by newline char
        """
        self._validate_data(data)

        # remove excess whitespace, create list on newline char
        ingredientList = [line.strip() for line in data.split('\n')
                          if line.strip()]

        # has empty title, url, and steps, only contains ingredients
        recipe = Recipe("", "", ingredientList, [""])

        return recipe


    def _validate_data(self, data) -> bool:
        """
        validates the raw data str can be parsed for ingredients
        """
        if not data or not data.strip():
            raise ValueError("No data extracted")

        # rejects too many characters
        if len(data) > 10000:
            raise ValueError("Input exceed maximum length of 10,000 "
                             "characters")

        return True


    def _validate_url(self, url:str) -> bool:
        """
        verifies url is a valid http/https url and returns True, otherwise
        raises a ValueError

        Raises:
            TypeError: is url is not the correct Type
            ValueError: is url is not a valid http/https URL
        """
        if not isinstance(url, str):
            raise TypeError(f"url must be a string but is a {type(url)}")
        try:
            urlparse(url)
            return True
        except ValueError:
            raise ValueError(f"url: {url} is not a valid url, please submit a valid url. Ensure "
                             "that the url includes http:// or https://")



class RecipeExtractionError(Exception):
    """Raised when a recipe cannot be extracted from a URL."""
    def __init__(self, url):
        self.url = url
        super().__init__(
            f"Sorry, we couldn’t automatically extract the recipe from {url}. "
            f"Please use the 'TEXT' option to enter the recipe manually."
        )

# r2 = "https://bakerbynature.com/the-best-cocoa-fudge-brownies/"
# r1 = "https://sallysbakingaddiction.com/seriously-fudgy-homemade-brownies/"

r1 = "https://donalskehan.com/recipes/raspberry-scones/"
x = RecipeComparator(r1, "url", r1, "url")