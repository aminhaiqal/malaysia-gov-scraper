from abc import ABC, abstractmethod
from typing import List


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
    def parse_article(self, html: str) -> dict:
        """Return parsed data: title, date, text, pdfs etc."""