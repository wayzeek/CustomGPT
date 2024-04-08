import pickle
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from aesthetic import color_text

# Function to save an object to a file
def save_to_file(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

# Function to load an object from a file
def load_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Function to index data and load model
def index_and_load_model(split_documents):
    if not os.getenv("HF_KEY"):
        hf_api_key = str(input(color_text("Please enter your Hugging Face API key: ", "magenta")))
        os.environ["HF_KEY"] = hf_api_key
    print(color_text("Indexing and loading model...\nBased on the length of the documents, this may take a while.", "yellow"))
    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_texts(split_documents, embedding)
    # Use HuggingFaceEndpoint instead of HuggingFaceHub
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", huggingfacehub_api_token=os.getenv("HF_KEY"))
    print(color_text("Model loaded successfully.", "green"))
    return db, llm