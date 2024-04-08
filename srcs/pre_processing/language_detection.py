from PyPDF2 import PdfFileReader
from langdetect import detect

def detect_language_from_pdf(pdf_path: str) -> str:
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        text = ""
        # Read the first 1000 characters from the PDF to sample the text
        for page_num in range(min(10, reader.numPages)):
            text += reader.getPage(page_num).extractText()
        # Detect the language of the sampled text
        language = detect(text)
    return language