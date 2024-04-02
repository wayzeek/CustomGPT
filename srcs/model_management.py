import pickle
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub

# Function to save an object to a file
def save_to_file(obj, filename):
    print(f"Saving {filename}...")
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
    print(f"{filename} saved.")

# Function to load an object from a file
def load_from_file(filename):
    print(f"Loading {filename}...")
    with open(filename, 'rb') as f:
        print(f"{filename} loaded.")
        return pickle.load(f)

# Function to index data and load model
def index_and_load_model(split_documents):
    print("Indexing and loading model...")
    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(split_documents, embedding)
    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", huggingfacehub_api_token=os.getenv("HF_KEY"))
    return db, llm