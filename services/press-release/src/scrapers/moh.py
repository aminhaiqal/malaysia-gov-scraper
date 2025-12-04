from .base import BaseScraper
from ..core.html import parse_html, extract_text
from ..core.cleaners import clean_text


class MOHScraper(BaseScraper):
    name = "moh"

def list_links(self, html: str):
    soup = parse_html(html)
    return [a.get('href') for a in soup.select('.news-list a') if a.get('href')]


def parse_article(self, html: str):
    soup = parse_html(html)
    title = extract_text(soup, 'h2')
    date = extract_text(soup, '.meta time')
    content = extract_text(soup, 'article')
    return {
        'title': clean_text(title),
        'date': clean_text(date),
        'text': clean_text(content),
        'pdfs': [a.get('href') for a in soup.select('a[href$=".pdf"]')]
    }