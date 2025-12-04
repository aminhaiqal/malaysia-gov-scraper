from .base import BaseScraper
from core.http import fetch
from core.html import parse_html, extract_text
from core.cleaners import clean_text


class MOFScraper(BaseScraper):
    name = "mof"
    
    def list_links(self, html: str):
        soup = parse_html(html)
        links = []
        for a in soup.select(".views-row a"):
            href = a.get("href")
            if href:
                links.append(href)
            return links

    def parse_article(self, html: str):
        soup = parse_html(html)
        title = extract_text(soup, "h1")
        date = extract_text(soup, ".date")
        content = extract_text(soup, ".field--name-body")
        return {
            "title": clean_text(title),
            "date": clean_text(date),
            "text": clean_text(content),
            "pdfs": [a.get('href') for a in soup.select("a[href$='.pdf']")]
        }