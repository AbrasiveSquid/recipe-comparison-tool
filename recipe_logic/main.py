from recipe_scraper import fetch_recipe
from recipe_class import Recipe
from urllib.parse import urlparse

def main():
    """
    main method that gets two url from the url and creates
    two Recipe objects, then compares them
    """
    # for debugging
    # userInput1 = "https://www.allrecipes.com/recipe/40403/best-of-the-best-blueberry-muffins/"
    # userInput2 = "https://www.epicurious.com/recipes/food/views/blueberry-muffin-recipe"
    # userInput2 = "https://www.foodnetwork.com/recipes/alton-brown/blueberry-muffins-recipe-1941521"
    while True:
        userInput1 = input("Enter a url for the first recipe: ")
        if is_valid_url(userInput1):
            break
        print(f"{userInput1} is not a valid url. Ensure it includes the full "
              f"url including http:// or https://")

    while True:
        userInput2 = input("Enter a url for the second recipe: ")
        if is_valid_url(userInput2):
            break
        print(f"{userInput2} is not a valid url. Ensure it includes the full "
              f"url including http:// or https://")

    recipe1Scrape = fetch_recipe(userInput1)
    recipe1 = Recipe(recipe1Scrape["title"], userInput1,
                     recipe1Scrape["ingredients"], recipe1Scrape["steps"])
    recipe2Scrape = fetch_recipe(userInput2)
    recipe2 = Recipe(recipe2Scrape["title"], userInput2,
                     recipe2Scrape["ingredients"], recipe2Scrape["steps"])

    print(recipe1.compare_recipe(recipe2))




def is_valid_url(urlStr: str) -> bool:
    """
    verifies if urlStr is a valid http/https url and returns
    True if valid otherwise returns False
    """
    try:
        result = urlparse(urlStr)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == "__main__":
    main()
