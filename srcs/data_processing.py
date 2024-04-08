import os
import re
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from custom_splitters import SpacyTextSplitter
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
        modify_pdf_content("../raw_data/" + pdf_name, headers_to_split_on)
        return MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            strip_headers=True)
    elif pdf_type == "no":
        shutil.copy("../raw_data/" + pdf_name, "../processed_data/" + pdf_name)
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
        
        language = detect_language_from_pdf("../processed_data/" + pdf_name)
        print(f"Detected language: {language} for {pdf_name}")
        return SpacyTextSplitter(
            chunk_size=chunk_size,
            language=language
        )

def load_and_split_data(pdf_folder_path, log_path="log.txt"):
    """
    Load and split data from PDFs in the specified folder and log details about how documents are split to a file.
    """
    processed_data_folder_path = "../processed_data/"
    split_documents = []

    for pdf_name in os.listdir(pdf_folder_path):
        splitter = get_appropriated_splitter(pdf_name)
        loader = PyPDFLoader(os.path.join(processed_data_folder_path, pdf_name))
        pages = loader.load()
        if (type(splitter) == MarkdownHeaderTextSplitter):
            pages_to_split = []
            for page in pages:
                splits = splitter.split_text(page.page_content)
                pages_to_split.extend(splits)
            language = detect_language_from_pdf("../processed_data/" + pdf_name)
            print(f"Detected language: {language} for {pdf_name}")
            splitter = SpacyTextSplitter(chunk_size=1000, language=language)
            pages = pages_to_split
        document_splits = []  # To store splits for current document
        for page in pages:
            splits = splitter.split_text(page.page_content)
            document_splits.extend(splits)
        
        split_documents.extend(document_splits)
        print(f"Document {pdf_name} split.")
    return split_documents

load_and_split_data("../raw_data/")