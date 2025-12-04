from bs4 import BeautifulSoup
from typing import Optional


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def extract_text(node, selector: Optional[str] = None) -> str:
    if selector:
        el = node.select_one(selector)
        return el.get_text(separator="\n").strip() if el else ""
    return node.get_text(separator="\n").strip()