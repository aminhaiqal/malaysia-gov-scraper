from urllib.parse import urljoin
from .base import BaseScraper
from ..core.html import parse_html, extract_text
from ..core.cleaners import clean_text


class MITIScraper(BaseScraper):
    name = "miti"

    def list_links(self, html: str):
        soup = parse_html(html)
        selector = "a[href]"
        links = []

        for a in soup.select(selector):
            href = a.get("href")
            if not href:
                continue

            full_url = urljoin(self.start_urls[0], href)
            if "/miti/resources/Media%20Release" in full_url:
                links.append(full_url)

        return links


    def get_article(self, html: str, url: str):
        pass