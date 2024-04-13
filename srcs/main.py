import os
import shutil
import getpass
import textwrap
from pre_processing.pdf_processing import load_and_split_data
from model_management import save_to_file, load_from_file, index_and_load_model
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from deep_translator import GoogleTranslator
from aesthetic import clear_screen, print_banner, color_text

# Function to clear the directories
def clear_directories(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

indexed_data_file = os.path.abspath(".saved_models/indexed_data.pkl")
model_file = os.path.abspath(".saved_models/model.pkl")

clear_screen()
print_banner()
# Check if indexed data and model files exist
if not os.path.exists(indexed_data_file) or not os.path.exists(model_file):
    print(color_text("Indexed data or model not found.", "red"))
    # Create the directories if they do not exist
    os.makedirs(".processed_data/", exist_ok=True)
    os.makedirs(".saved_models/", exist_ok=True)
    raw_data_folder_path = os.path.abspath("data/")
    split_documents = load_and_split_data(raw_data_folder_path)
    db, llm = index_and_load_model(split_documents)
    save_to_file(db, indexed_data_file)
    save_to_file(llm, model_file)
else:
    print(color_text("Indexed data and model found.", "green"))
    # Prompt the user to clear the directories
    clear_data_answer = None
    while clear_data_answer != "yes" and clear_data_answer != "no":
        clear_data = input(color_text("Do you want to clear the existing data and start fresh? (yes/no): ", "magenta"))
        if clear_data.lower() == 'yes':
            clear_directories(".processed_data/")
            clear_directories(".saved_models/")
        elif clear_data.lower() == 'no':
            break
        else:
            print(color_text("Please enter 'yes' or 'no'.", "red"))
    print(color_text("Loading indexed data and model from files...", "yellow"))
    db = load_from_file(indexed_data_file)
    llm = load_from_file(model_file)

retriever = db.as_retriever()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False,
)

chat_history = []

answer_language = None
while answer_language not in ['en', 'fr', 'es', 'de', 'it', 'uk', 'ru', 'zh', 'ja']:
    answer_language = input(color_text("Enter the language code for the answer language (en, fr, es, de, it, uk, ru, zh, ja): ", "magenta")).strip().lower()
    if answer_language not in ['en', 'fr', 'es', 'de', 'it', 'uk', 'ru', 'zh', 'ja']:
        print(color_text("Please enter a valid language code.", "red"))

nickname = color_text(getpass.getuser(), "yellow")
ask_query = nickname + " : "
clear_screen()
print_banner()
# Main loop for querying
while True:
    query = str(input(ask_query))
    if answer_language != 'en':
        query_processed = GoogleTranslator(source=answer_language, target='en').translate(query)
    else:
        query_processed = query
    chat_history.append(query_processed)
    result = qa.invoke({"question": query_processed, "chat_history": chat_history})
    
    # Extract the helpful answer from the result
    answer = result['answer']
    
    if answer_language != 'en':
        answer = GoogleTranslator(source='auto', target=answer_language).translate(answer)
    
    # Use textwrap to adjust the answer to fit terminal width
    terminal_width = os.get_terminal_size().columns  # Get current terminal width
    wrapped_answer = textwrap.fill(answer, width=terminal_width / 1.5)
    
    chatbot_color = color_text("Chatbot", "magenta")
    # Print the question and answer
    print(f"\n{chatbot_color} : {wrapped_answer}\n")
