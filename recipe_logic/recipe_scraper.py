import requests
from recipe_scrapers import scrape_html
from curl_cffi import requests as impersonate_requests
import cloudscraper
import ipaddress
import socket
from urllib.parse import urljoin, urlparse

REDIRECT_STATUS_CODES = {301, 302, 303, 307, 308}
MAX_REDIRECTS = 5

def validate_public_url(url: str) -> bool:
    """Validate that a URL resolves only to public HTTP(S) addresses."""
    if not isinstance(url, str):
        raise TypeError(f"url must be a string, not {type(url)}")

    if not url or any(character.isspace() for character in url):
        raise ValueError("URL must not be empty or contain whitespace")

    try:
        parsed_url = urlparse(url)
        port = parsed_url.port
    except ValueError as error:
        raise ValueError("URL is malformed") from error

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("URL must use HTTP or HTTPS")

    if not parsed_url.hostname:
        raise ValueError("URL must include a hostname")

    if parsed_url.username is not None or parsed_url.password is not None:
        raise ValueError("URL must not contain credentials")

    if port not in {None, 80, 443}:
        raise ValueError("URL must use port 80 or 443")

    request_port = port or (443 if parsed_url.scheme == "https" else 80)

    try:
        addresses = socket.getaddrinfo(
            parsed_url.hostname,
            request_port,
            type=socket.SOCK_STREAM,
        )
    except (OSError, UnicodeError) as error:
        raise ValueError("URL hostname could not be resolved") from error

    if not addresses:
        raise ValueError("URL hostname did not resolve to an address")

    for address_info in addresses:
        address = ipaddress.ip_address(address_info[4][0])

        if not address.is_global:
            raise ValueError("URL resolves to a non-public address")

    return True

def _get_with_safe_redirects(request_get, url: str, **kwargs):
    """Fetch a URL while validating every redirect destination."""
    current_url = url

    for redirect_count in range(MAX_REDIRECTS + 1):
        validate_public_url(current_url)

        response = request_get(
            current_url,
            allow_redirects=False,
            **kwargs,
        )

        if response.status_code not in REDIRECT_STATUS_CODES:
            return response

        location = response.headers.get("Location")
        response.close()

        if not location:
            raise ValueError("Redirect response is missing a Location header")

        if redirect_count == MAX_REDIRECTS:
            raise ValueError("URL exceeded the redirect limit")

        current_url = urljoin(current_url, location)

    raise ValueError("URL exceeded the redirect limit")

def fetch_recipe(url: str) -> dict | None:
    """
    Attempts to scrape a recipe from a URL using multiple methods.
    Returns a dict with title, time, ingredients, steps, or None if all
    methods fail.
    """
    validate_public_url(url)

    try:
        response = _get_with_safe_redirects(
            requests.get,
            url,
            headers={
                "User-Agent": "curl/8.7.1",
                "Accept": "*/*",
            },
            timeout=15,
        )
        response.raise_for_status()
        scraper = scrape_html(html=response.text, org_url=url)
        return _build_recipe(scraper)
    except Exception:
        pass

    # Fallback 2: curl_cffi impersonation
    try:
        response = _get_with_safe_redirects(
            impersonate_requests.get,
            url,
            impersonate="chrome120",
            timeout=15,
        )
        response.raise_for_status()
        scraper = scrape_html(html=response.text, org_url=url)
        return _build_recipe(scraper)
    except Exception:
        pass

    # Fallback 3: cloudscraper
    try:
        scraper_cloud = cloudscraper.create_scraper()
        response = _get_with_safe_redirects(
            scraper_cloud.get,
            url,
            timeout=15,
        )
        response.raise_for_status()
        scraper = scrape_html(html=response.text, org_url=url)
        return _build_recipe(scraper)
    except Exception:
        pass

    return None

def _build_recipe(scraper) -> dict:
    """Helper to build the recipe dict from a scraper object."""
    return {
        "title": scraper.title(),
        "time": f"{scraper.total_time()} minutes",
        "ingredients": scraper.ingredients(),
        "steps": scraper.instructions_list(),
    }