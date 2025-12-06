from src.core.pdf_processor import PDFProcessor

# Instantiate processor
processor = PDFProcessor()

# Example PDF URL (replace with any PDF URL you want to test)
pdf_url = "https://www.miti.gov.my/miti/resources/Media%20Release/PR_KAMPUNG_ANGKAT_MADANI_MITI_KAMPUNG_TEBUK_MUFRAD.pdf"

# Process PDF
article = processor.process_pdf_from_url(pdf_url)

# Print results
print("Extracted text:\n")
print(article.text)
print("\nPDF URLs:")
print(article.pdfs)
