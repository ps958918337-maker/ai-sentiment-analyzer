"""URL text extraction service using BeautifulSoup."""

import requests
from bs4 import BeautifulSoup


class ScraperError(Exception):
    """Custom exception for scraping failures."""
    pass


def extract_text_from_url(url: str, timeout: int = 10) -> str:
    """
    Fetch a URL and extract readable text content.

    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds

    Returns:
        Extracted text content from the page

    Raises:
        ScraperError: If the URL cannot be fetched or parsed
    """
    # Validate URL format
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise ScraperError(f"Could not connect to {url}")
    except requests.exceptions.Timeout:
        raise ScraperError(f"Request timed out for {url}")
    except requests.exceptions.HTTPError as e:
        raise ScraperError(f"HTTP error {e.response.status_code} for {url}")
    except requests.exceptions.RequestException as e:
        raise ScraperError(f"Failed to fetch URL: {str(e)}")

    try:
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Get text and clean it up
        text = soup.get_text(separator=" ", strip=True)

        # Collapse whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        if not text:
            raise ScraperError("No readable text content found on the page")

        # Limit text length to prevent analysis of massive pages
        max_chars = 5000
        if len(text) > max_chars:
            text = text[:max_chars]

        return text

    except ScraperError:
        raise
    except Exception as e:
        raise ScraperError(f"Failed to parse page content: {str(e)}")
