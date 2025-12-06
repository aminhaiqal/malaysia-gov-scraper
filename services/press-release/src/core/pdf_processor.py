import fitz
import pytesseract
from pdf2image import convert_from_path
import requests
from tempfile import NamedTemporaryFile
from .models import Article
from ..embeddings.chunk import embed_chunks

class PDFProcessor:
    """
    Extract text from PDF (OCR if needed) from URL using temporary file.
    """
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF. If scanned (no text), uses OCR."""
        text = ""
        ocr_needed = False

        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text().strip()
                if page_text:
                    text += page_text + "\n"
                else:
                    ocr_needed = True

        if ocr_needed:
            images = convert_from_path(pdf_path)
            for image in images:
                ocr_text = pytesseract.image_to_string(image)
                if ocr_text.strip():
                    text += ocr_text + "\n"

        return text.strip()

    def process_pdf_from_url(self, url: str) -> Article:
        """Download PDF from URL using NamedTemporaryFile, extract text, chunk & embed."""
        with NamedTemporaryFile(suffix=".pdf") as tmp_file:
            response = requests.get(url)
            response.raise_for_status()
            tmp_file.write(response.content)
            tmp_file.flush()

            text = self.extract_text(tmp_file.name)

        return Article(
            id=str(hash(url)),
            source="PDF",
            url=url,
            text=text,
            pdfs=[url],
        )
