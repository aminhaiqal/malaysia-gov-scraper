from abc import ABC, abstractmethod
from typing import List
from ..core.models import Article


class BaseScraper(ABC):
    name: str = "base"
    start_urls: List[str] = []

    def __init__(self, config: dict):
        self.config = config
        self.start_urls = config.get("start_urls", [])
        self.selectors = config.get("selectors", {})

    @abstractmethod
    def list_links(self, html: str) -> List[str]:
        """Return article links found in an index page."""

    @abstractmethod
    def get_article(self, html: str) -> List[Article]:
        """Return parsed data: title, date, text, pdfs etc."""