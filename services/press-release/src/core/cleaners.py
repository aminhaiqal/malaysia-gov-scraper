import re
from html import unescape

_TAG_RE = re.compile(r"<[^>]+>")

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    # Decode HTML entities (e.g. &amp; → &)
    text = unescape(text)
    
    # Remove all HTML tags
    text = _TAG_RE.sub("", text)

    # Normalize whitespace
    text = re.sub(r"\r\n", "\n", text)
    
    # Collapse multiple newlines
    text = re.sub(r"\n\s*\n\s*", "\n\n", text)
    
    # Remove long runs of repeated dashes / artifacts
    text = re.sub(r"[-]{3,}", "-", text)

    # Replace non-breaking spaces
    text = text.replace("\xa0", " ")

    # Trim leading/trailing whitespace
    return text.strip()
