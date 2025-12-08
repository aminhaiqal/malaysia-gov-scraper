from .base import ScrapeStrategy
from .html_strategy import HTMLScrapeStrategy
from .pdf_strategy import PDFScrapeStrategy

class ScrapeStrategyFactory:
    """
    Factory class to select the appropriate scraping strategy based on URL.
    """

    @staticmethod
    def get_strategy(link: str, scraper) -> ScrapeStrategy:
        """
        Return an instance of ScrapeStrategy (HTML or PDF).

        Args:
            link (str): The URL to process.
            scraper: Scraper object for HTML pages.

        Returns:
            ScrapeStrategy instance
        """
        if link.lower().endswith(".pdf"):
            return PDFScrapeStrategy()
        return HTMLScrapeStrategy(scraper)
