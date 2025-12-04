from .base import BaseScraper
from core.html import parse_html, extract_text
from core.cleaners import clean_text


class BNMScraper(BaseScraper):
    name = "bnm"

def list_links(self, html: str):
    soup = parse_html(html)
    return [a.get('href') for a in soup.select('.card a') if a.get('href')]

def parse_article(self, html: str):
    soup = parse_html(html)
    title = extract_text(soup, 'h3')
    date = extract_text(soup, '.published')
    content = extract_text(soup, '.content')
    return {
        'title': clean_text(title),
        'date': clean_text(date),
        'text': clean_text(content),
        'pdfs': [a.get('href') for a in soup.select('a[href$=".pdf"]')]
    }