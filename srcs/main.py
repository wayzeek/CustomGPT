import os
import re
from googletrans import Translator
from data_processing import load_and_split_data
from model_management import save_to_file, load_from_file, index_and_load_model
from langchain.chains.question_answering import load_qa_chain

if not os.getenv("HF_KEY"):
    hf_api_key = str(input("Please enter your Hugging Face API key: "))
    os.environ["HF_KEY"] = hf_api_key
else:
    print("Hugging Face API key found.")

indexed_data_file = '../save/indexed_data.pkl'
model_file = '../save/model.pkl'

# Check if indexed data and model files exist
if not os.path.exists(indexed_data_file) or not os.path.exists(model_file):
    print("Indexed data or model not found.")
    raw_data_folder_path = "../raw_data/"
    split_documents = load_and_split_data(raw_data_folder_path)
    db, llm = index_and_load_model(split_documents)
    save_to_file(db, indexed_data_file)
    save_to_file(llm, model_file)
else:
    print("Loading indexed data and model from files...")
    db = load_from_file(indexed_data_file)
    llm = load_from_file(model_file)

chain = load_qa_chain(llm, chain_type="stuff")
print("Chain created.")

# Initialize the translator
translator = Translator()

# Main loop for querying
while True:
    query = str(input("Enter your query: "))
    docs = db.similarity_search(query)
    print("Thinking...")
    output = chain.invoke({"input_documents": docs, "question": query})

    # Extract helpful answer from output
    output_str = str(output)
    match = re.search(r'Helpful Answer:(.*?)(\s*})', output_str)
    if match:
        helpful_answer = match.group(1).strip() # Extract the matched group and remove leading/trailing whitespace
        helpful_answer = helpful_answer.rstrip("'")
        helpful_answer = helpful_answer.rstrip('"')
        # Translate the answer to French
        translated_answer = translator.translate(helpful_answer, dest='fr').text
        print(translated_answer)
    else:
        print("Aucune réponse utile trouvée.")
