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

    def get_article(self, html: str, url: str) -> Article:
        if not url:
            return None
        
        soup = parse_html(html)

        title = soup.select_one("h1[itemprop='headline']")
        title = clean_text(title.string if title else "")

        date = soup.select_one("time[itemprop='datePublished']")
        date = clean_text(date.string if date else "")

        body_node = soup.select_one("div[itemprop='articleBody']")
        raw_body_html = str(body_node) if body_node else ""
        cleaned_body = clean_text(raw_body_html)

        category_node = soup.find(class_="category-name")
        category = clean_text(category_node.string if category_node else "")

        # Collect PDF attachments
        article_details = soup.find("div", class_="article-details")
        pdfs = []
        if article_details:
            pdfs = [
                urljoin(self.start_urls[0], a["href"])
                for a in article_details.find_all("a", href=True)
                if a["href"].lower().endswith(".pdf")
            ]

        return Article(
            id=str(hash(url)),
            title=title,
            ministry=self.name.upper(),
            date=date,
            source="HTML",
            url=url,
            text=raw_body_html,
            cleaned_text=cleaned_body,
            category=category,
            pdfs=pdfs,
            metadata={}
        )
