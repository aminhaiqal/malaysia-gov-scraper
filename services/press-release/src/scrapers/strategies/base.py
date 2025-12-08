from abc import ABC, abstractmethod
from typing import Optional
from ...core.models import Article

class ScrapeStrategy(ABC):
    """
    Abstract base class for a scraping strategy.
    Each concrete strategy must implement `process()` which returns an Article object.
    """

    @abstractmethod
    def process(self, link: str) -> Optional[Article]:
        """
        Process a single link and return an Article object.
        
        Args:
            link (str): URL of the page or PDF to scrape.

        Returns:
            Article or None
        """
        pass