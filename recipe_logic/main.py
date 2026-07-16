from recipe_scraper import fetch_recipe
from recipe_class import Recipe
from urllib.parse import urlparse

class RecipeComparator:
    """ 
    main program class for recipe comparison. Receives two url, validates them,
    calls the scrapper, creates a Recipe object for each, then compares the recipes and returns
    the comparison
    """

    def __init__(self, url1:str, url2:str):
        self.firstRecipe = self._create_recipe(url1)
        self.secondRecipe = self._create_recipe(url2)
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

    def _create_recipe(self, url:str) -> Recipe:
        """
        takes a url that points to a recipe and returns a Recipe object
        First validates the url, then scrapes the website, then creates a python object of a Recipe
        """
        self._validate_url(url)
        recipeScraped = fetch_recipe(url)
        if recipeScraped:
            recipe = Recipe(recipeScraped["title"], url,
                            recipeScraped["ingredients"],
                            recipeScraped["steps"])
        else:
            raise ValueError(f"Failed to extract recipe data from url: "
                             f"{url}")
        return recipe

    def _validate_url(self, url:str) -> bool:
        """
        verifies url is a valid http/https url and returns True, otherwise raises a ValueError


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


# r1 = "https://www.allrecipes.com/recipe/40403/best-of-the-best-blueberry-muffins/"
# r2 = "https://www.allrecipes.com/recipe/40403/best-of-the-best-blueberry-muffins/"
# r1 = "https://www.culinaryhill.com/blueberry-muffins/"
# r2 = "https://www.inspiredtaste.net/18982/our-favorite-easy-blueberry-muffin-recipe/"
# r1 = "https://joyfoodsunshine.com/the-most-amazing-chocolate-chip-cookies/"
# r2 = "https://sallysbakingaddiction.com/chewy-chocolate-chip-cookies/"
# r1 = "https://www.loveandlemons.com/brownies-recipe/"
# r2 = "https://www.allrecipes.com/recipe/10549/best-brownies/"
# x = RecipeComparator(r1,r2)

