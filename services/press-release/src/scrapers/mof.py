from urllib.parse import urljoin
from .base import BaseScraper
from ..core.html import parse_html
from ..core.models import Article
from ..core.cleaners import clean_text


class MOFScraper(BaseScraper):
    name = "mof"

    selectors = {
        "listing_links": "a[href]",
    }

    def list_links(self, html: str):
        soup = parse_html(html)
        selector = self.selectors.get("listing_links")
        links = []

        for a in soup.select(selector):
            href = a.get("href")
            if not href:
                continue

            full_url = urljoin(self.start_urls[0], href)
            if "/portal/en/news/press-release" in full_url:
                links.append(full_url)

        return links

    def get_article(self, html: str) -> Article:
        soup = parse_html(html)

        title = soup.select_one("h1[itemprop='headline']").string
        date = soup.select_one("time[itemprop='datePublished']").string
        body_node = soup.select_one("div[itemprop='articleBody']")
        body_html = str(body_node) if body_node else ""
        category = soup.find(class_="category-name").string

        article = soup.find("div", class_="article-details")
        pdfs = [
            urljoin(self.start_urls[0], a["href"])
            for a in article.find_all("a", href=True)
            if a["href"].lower().endswith(".pdf")
        ]

        return {
            "title": clean_text(title),
            "date": clean_text(date),
            "text": clean_text(body_html),
            "category": clean_text(category),
            "pdfs": pdfs
        }
