import os
import getpass
import textwrap
from srcs.utils.utils import clear_screen, print_banner, color_text
from deep_translator import GoogleTranslator
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from srcs.data_management.data_management import check_and_load_data

def chatbot_interface():
    clear_screen()
    print_banner()
    db, llm = check_and_load_data()

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

    while True:
        query = str(input(ask_query))
        if answer_language != 'en':
            query_processed = GoogleTranslator(source=answer_language, target='en').translate(query)
        else:
            query_processed = query
        chat_history.append(query_processed)
        result = qa.invoke({"question": query_processed, "chat_history": chat_history})
        
        answer = result['answer']
        
        if answer_language != 'en':
            answer = GoogleTranslator(source='auto', target=answer_language).translate(answer)
        
        terminal_width = os.get_terminal_size().columns
        wrapped_answer = textwrap.fill(answer, width=terminal_width / 1.5)
        
        chatbot_color = color_text("Chatbot", "magenta")
        print(f"\n{chatbot_color} : {wrapped_answer}\n")