import shutil
import re
import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from custom_splitters import SpacyTextSplitter
from language_detection import detect_language_from_pdf

def modify_pdf_content(pdf_path, headers_to_split_on):
    """
    Modify PDF content by adding markdown headers based on user-defined configurations.
    """
    print(f"Processing PDF: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        pdf = PdfFileReader(file)
        writer = PdfFileWriter()

        for page_number in range(pdf.getNumPages()):
            page = pdf.getPage(page_number)
            text = page.extractText()

            # Dynamically add markdown headers based on the user-defined configuration
            for header_symbol, header_title in headers_to_split_on:
                # Allows for any character (especially numbers, Roman numerals, and punctuation like ':') following the title
                # Use '[^\s]*' to match any characters except whitespace character following the title
                # This ensures the regex is not too greedy while allowing for numbers, Roman numerals, etc.
                regex_pattern = r"\b" + re.escape(header_title) + r"[^\s]*"
                replacement = f"{header_symbol} {header_title}"
                text = re.sub(regex_pattern, replacement, text, flags=re.IGNORECASE)
            writer.addPage(page)
        output_path = pdf_path.replace('raw_data', 'processed_data')
        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

    print(f"PDF processed and saved as {output_path}")

def get_markdown_header_config(previous_headers=None):
    """
    Ask the user for the number of header levels and titles for each level, with an option to reuse previous configurations.
    """
    
    use_previous = None
    header_levels = 1
    
    if previous_headers is not None:
        while use_previous != "yes" and use_previous != "no":
            use_previous = input("Use the same header configuration as before? (yes/no): ").strip().lower()
            if use_previous != "yes" and use_previous != "no":
                print("Please enter 'yes' or 'no'.")
        if use_previous == "yes":
            return previous_headers
    while header_levels <= 1 :
        header_levels = int(input("How many levels of headers are there? "))
        if header_levels >= 1:
            print("Please enter a number greater than 1")
    headers_to_split_on = []

    for i in range(header_levels):
        header_symbol = "#" * (i + 1)  # Incrementing number of '#' symbols for each level
        header_title = input(f"Enter the title for Header Level {i + 1} ({header_symbol}): ").strip()
        headers_to_split_on.append((header_symbol, header_title))

    return headers_to_split_on

def get_appropriated_splitter(pdf_name):
    """
    Process all PDFs in the specified folder, configuring appropriate splitting based on user input.
    """
    previous_headers = None
    pdf_type = None

    
    while (pdf_type != "yes") and (pdf_type != "no"):
        pdf_type =  input(f"Is your file {pdf_name} structured by headers ? (yes/no): ").strip()
        if pdf_type != "yes" and pdf_type != "no":
            print("Please enter 'yes' or 'no'.")
    if pdf_type == "yes":
        print(f"\nConfiguring headers for: {pdf_name}")
        if previous_headers is None:
            headers_to_split_on = get_markdown_header_config()
        else:
            headers_to_split_on = get_markdown_header_config(previous_headers)
        previous_headers = headers_to_split_on  # Store the current configuration for potential reuse
        modify_pdf_content(os.path.abspath("raw_data/") + "/" + pdf_name, headers_to_split_on)
        return MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            strip_headers=True)
    elif pdf_type == "no":
        shutil.copy(os.path.abspath("raw_data/") + "/" + pdf_name, os.path.abspath("processed_data/") + "/" + pdf_name)
        chunk_chosen = None
        
        while chunk_chosen != 'sm' and chunk_chosen != 'md' and chunk_chosen != 'lg':
            chunk_chosen = input("Choose the chunk size (sm/md/lg): ").strip().lower()
            if chunk_chosen != 'sm' and chunk_chosen != 'md' and chunk_chosen != 'lg':
                print("Please enter 'sm', 'md', or 'lg'.")
        if chunk_chosen == 'sm':
            chunk_size = 500
        elif chunk_chosen == 'md':
            chunk_size = 1500 
        elif chunk_chosen == 'lg':
            chunk_size = 5000  
        
        language = detect_language_from_pdf(os.path.abspath("processed_data/") + "/" + pdf_name)
        print(f"Detected language: {language} for {pdf_name}")
        return SpacyTextSplitter(
            chunk_size=chunk_size,
            language=language
        )