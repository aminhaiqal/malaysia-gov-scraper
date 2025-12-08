from typing import Optional
from .base import ScrapeStrategy
from ...core.models import Article
from ...core.pdf_processor import PDFProcessor

PROCESSOR = PDFProcessor()

class PDFScrapeStrategy(ScrapeStrategy):
    """
    Scraping strategy for PDF links.
    Uses PROCESSOR.process_pdf_from_url() to extract text and metadata.
    """

    def process(self, link: str) -> Optional[Article]:
        """
        Process a PDF URL and return an Article.
        """
        try:
            return PROCESSOR.process_pdf_from_url(link)
        except Exception as e:
            print(f"[PDFScrapeStrategy] Failed to process PDF {link}: {e}")
            return None
