import fitz
import requests
import io


def extract_pdf_text_from_url(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    fp = io.BytesIO(resp.content)
    doc = fitz.open(stream=fp, filetype="pdf")
    text_lines = []
    for page in doc:
        text = page.get_text()
        if text:
            text_lines.extend([ln.strip() for ln in text.splitlines() if ln.strip()])
    return "\n".join(text_lines)