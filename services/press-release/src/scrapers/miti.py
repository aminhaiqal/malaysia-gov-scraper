from .base import BaseScraper
from ..core.html import parse_html, extract_text
from ..core.cleaners import clean_text


class MITIScraper(BaseScraper):
    name = "miti"

def list_links(self, html: str):
    soup = parse_html(html)
    return [a.get('href') for a in soup.select('.news-card a') if a.get('href')]


def parse_article(self, html: str):
    soup = parse_html(html)
    title = extract_text(soup, '.news-title')
    date = extract_text(soup, '.news-date')
    content = extract_text(soup, '.news-content')
    return {
        'title': clean_text(title),
        'date': clean_text(date),
        'text': clean_text(content),
        'pdfs': [a.get('href') for a in soup.select('a[href*="pdf"]')]
    }