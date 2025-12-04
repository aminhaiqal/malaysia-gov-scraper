import re


def clean_text(text: str) -> str:
    if not text:
        return ""
    
    # Normalize whitespace
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    
    # Remove long runs of repeated chars
    text = re.sub(r"[-]{3,}", "-", text)
    # Trim
    return text.strip()