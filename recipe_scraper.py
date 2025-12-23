import requests
from recipe_scrapers import scrape_html

urls = ["https://sallysbakingaddiction.com/my-favorite-cornbread/", "https://www.lecremedelacrumb.com/best-super-moist-cornbread/","https://www.allrecipes.com/recipe/17891/golden-sweet-cornbread/" ]

# 1. Use a real User-Agent to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    for url in urls:
        # 2. Fetch the page with a timeout
        response = requests.get(url, headers=headers, timeout=10)

        # 3. Pass the URL and the HTML content to the scraper
        scraper = scrape_html(html=response.text, org_url=url)

        print("******")
        print(f"Title: {scraper.title()}")
        print(f"Total Time: {scraper.total_time()} mins")
        print(scraper.ingredients())
        print("\n\n")

except requests.exceptions.Timeout:
    print("The request timed out. The site might be blocking the connection.")
except Exception as e:
    print(f"An error occurred: {e}")


