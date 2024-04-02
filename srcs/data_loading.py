import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Function to load and split data from PDFs
def load_and_split_data(pdf_folder_path):
    loaders = [PyPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]
    print(f"Markdowned PDFs loaded: {loaders}")
    # Define headers to split on for document structure
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    print("Splitting documents...")
    split_documents = []
    for loader in loaders:
        pages = loader.load()
        for page in pages:
            split_documents.extend(markdown_splitter.split_text(page.page_content))
    print("Documents split.")
    return split_documents