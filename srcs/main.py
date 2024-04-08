import os
import getpass
from pre_processing.pdf_processing import load_and_split_data
from model_management import save_to_file, load_from_file, index_and_load_model
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from deep_translator import GoogleTranslator
from aesthetic import clear_screen, print_banner, color_text

indexed_data_file = os.path.abspath(".saved_models/indexed_data.pkl")
model_file = os.path.abspath(".saved_models/model.pkl")

clear_screen()
print_banner()
# Check if indexed data and model files exist
if not os.path.exists(indexed_data_file) or not os.path.exists(model_file):
    print(color_text("Indexed data or model not found.", "red"))
    raw_data_folder_path = os.path.abspath("raw_data/")
    split_documents = load_and_split_data(raw_data_folder_path)
    db, llm = index_and_load_model(split_documents)
    save_to_file(db, indexed_data_file)
    save_to_file(llm, model_file)
else:
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
    
    chatbot_color = color_text("Chatbot", "magenta")
    # Print the question and answer
    print(f"\n{chatbot_color} : {answer}\n")
