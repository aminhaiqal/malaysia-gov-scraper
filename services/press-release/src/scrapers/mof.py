from .base import BaseScraper
from ..core.http import fetch
from ..core.html import parse_html, extract_text
from ..core.cleaners import clean_text


class MOFScraper(BaseScraper):
    name = "mof"
    
    def list_links(self, html: str):
        soup = parse_html(html)
        selector = self.selectors.get("listing_links")
        links = [a.get("href") for a in soup.select(selector) if a.get("href")]
        return links

    def parse_article(self, html: str):
        soup = parse_html(html)
        title = extract_text(soup, self.selectors.get("title", "h1"))
        date = extract_text(soup, self.selectors.get("date", ".date"))
        body = extract_text(soup, self.selectors.get("body", ".field--name-body"))
        pdf_selector = self.selectors.get("pdf", "a[href$='.pdf']")
        pdfs = [a.get("href") for a in soup.select(pdf_selector)]
        return {
            "title": clean_text(title),
            "date": clean_text(date),
            "text": clean_text(body),
            "pdfs": pdfs
        }