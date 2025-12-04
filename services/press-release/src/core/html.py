from bs4 import BeautifulSoup
from typing import Optional, Union

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def extract_text(node: Union[BeautifulSoup, str], selector: Optional[str] = None) -> str:
    if not node:
        return ""

    # If selector specified → narrow search
    if selector:
        node = node.select_one(selector)
        if not node:
            return ""

    # Remove unwanted tags
    for tag in node(["script", "style", "noscript"]):
        tag.decompose()

    # Replace <br> with newlines
    for br in node.find_all("br"):
        br.replace_with("\n")

    # Treat paragraphs as separate lines
    for p in node.find_all("p"):
        if p.text.strip():
            p.append("\n")

    # Get cleaned text
    text = node.get_text()
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join([line for line in lines if line])  # remove empty lines

    return cleaned.strip()
