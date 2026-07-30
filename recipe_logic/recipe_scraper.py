import requests
from recipe_scrapers import scrape_html
from recipe_scrapers._exceptions import RecipeSchemaNotFound
from curl_cffi import requests as impersonate_requests
import cloudscraper

def fetch_recipe(url: str) -> dict | None:
    """
    Attempts to scrape a recipe from a URL using multiple methods.
    Returns a dict with title, time, ingredients, steps, or None if all methods fail.
    """
    try:
        resp = requests.get(url,
                            headers={"User-Agent": "curl/8.7.1",
                                     "Accept": "*/*"},
                            timeout=15)
        resp.raise_for_status()
        scraper = scrape_html(html=resp.text, org_url=url)
        return _build_recipe(scraper)
    except Exception:
        pass

    # fallback 2: curl_cffi impersonation (bypasses some TLS fingerprinting)
    try:
        response = impersonate_requests.get(url, impersonate="chrome120", timeout=15)
        response.raise_for_status()
        scraper = scrape_html(html=response.text, org_url=url)
        return _build_recipe(scraper)
    except (RecipeSchemaNotFound,
            requests.exceptions.RequestException,
            Exception):
        pass

    # fallback 3: cloudscraper (handles Cloudflare challenges)
    try:
        scraper_cloud = cloudscraper.create_scraper()
        response = scraper_cloud.get(url, timeout=15)
        response.raise_for_status()
        scraper = scrape_html(html=response.text, org_url=url)
        return _build_recipe(scraper)
    except Exception:
        pass

    # all methods fail
    return None

def _build_recipe(scraper) -> dict:
    """Helper to build the recipe dict from a scraper object."""
    return {
        "title": scraper.title(),
        "time": f"{scraper.total_time()} minutes",
        "ingredients": scraper.ingredients(),
        "steps": scraper.instructions_list(),
    }