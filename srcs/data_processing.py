import re
from PyPDF2 import PdfFileReader, PdfFileWriter

# Function to modify PDF content by adding markdown headers
def modify_pdf_content(pdf_path):
    print(f"Processing PDF: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        pdf = PdfFileReader(file)
        writer = PdfFileWriter()
        for page in range(pdf.getNumPages()):
            text = pdf.getPage(page).extractText()
            # Remove lines starting with "Code Civil -"
            text = re.sub(r"(?i)^[ \t]*Code.*\n?", "", text, flags=re.MULTILINE)
            
            # Add markdown headers for structure
            text = re.sub(r"Livre (\w+)", r"# Livre \1", text)
            text = re.sub(r"Titre (\w+)", r"## Titre \1", text)
            text = re.sub(r"Chapitre (\w+)", r"### Chapitre \1", text)
            text = re.sub(r"Article (\w+)", r"#### Article \1", text)
            writer.addPage(pdf.getPage(page))
        output_path = pdf_path.replace('raw_data', 'data')
        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)
    print(f"PDF processed and saved as {output_path}")
