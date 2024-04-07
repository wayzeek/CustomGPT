import os
import re
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

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
        return RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
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
        
        document_splits = []  # To store splits for current document
        for page in pages:
            splits = splitter.split_text(page.page_content)
            document_splits.extend(splits)
            for split in splits:
                print("-----------------------------------")
                print(split)
                print("-----------------------------------")
        
        split_documents.extend(document_splits)
        print(f"Document {pdf_name} split.")
    return split_documents

load_and_split_data("../raw_data/")