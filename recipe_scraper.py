import requests
from recipe_scrapers import scrape_html

urls = ["https://sallysbakingaddiction.com/my-favorite-cornbread/", "https://www.lecremedelacrumb.com/best-super-moist-cornbread/","https://www.allrecipes.com/recipe/17891/golden-sweet-cornbread/" ]

 # user-agent to look like real traffic 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_recipe(url:str) -> dict:
    """
    fetch a recipe from a url with the ingredients as a list in a dictionary and the steps as a 
    str in a dictionary
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:

        response = requests.get(url, headers=headers, timeout=10)
        scraper = scrape_html(html=response.text, org_url=url)
            # print(f"Title: {scraper.title()}")
            # print(f"Total Time: {scraper.total_time()} mins")
            # print(scraper.ingredients())
            # print(scraper.instructions())
            # print("\n\n")
        recipe = {
            "title": scraper.title(),
            "time": f"{scraper.total_time()} minutes",
            "ingredients": scraper.ingredients(),
            "steps": scraper.instructions()
        }
        recipe["steps"] = clean_steps(recipe["steps"])
        return recipe

    except requests.exceptions.Timeout:
        print("The request timed out. The site might be blocking the connection.")
    except Exception as e:
        print(f"An error occurred: {e}")


def clean_steps(steps: str) -> list:
    """
    Cleans up steps by using a newline to split into a list
    """
    step_list = []
    start_pos = 0
    end_pos = 0
    for i in range(len(steps)):
        if steps[i] == '\n':
            step_list.append(steps[start_pos:end_pos])
            end_pos += 1
            start_pos = end_pos
        else:
            end_pos += 1

    return step_list

