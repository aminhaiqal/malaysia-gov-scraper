from typing import Optional
from .base import ScrapeStrategy
from ...core.models import Article
from ...core.http import fetch

class HTMLScrapeStrategy(ScrapeStrategy):
    """
    Scraping strategy for HTML pages.
    Uses a scraper object to parse HTML and extract Article objects.
    """

    def __init__(self, scraper):
        """
        Args:
            scraper: An object with method `get_article(raw_html, url) -> Article`.
        """
        self.scraper = scraper

    def process(self, link: str) -> Optional[Article]:
        """
        Fetch and parse HTML page to return an Article.
        """
        try:
            raw_html = fetch(link)
            return self.scraper.get_article(raw_html, link)
        except Exception as e:
            print(f"[HTMLScrapeStrategy] Failed to process {link}: {e}")
            return None
