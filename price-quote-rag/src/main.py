import logging
from pathlib import Path
from time import sleep

from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from utils.resource_reader import ResourceReader
from rag.price_rag import PriceRag

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("price_rag.log"),
        logging.StreamHandler()
    ]
)

def main():
    try:
        logging.info("Starting Price RAG...")
        logging.info("Reading support runbooks...")
        current_file = Path(__file__).resolve()
        resource_folder = current_file.parent.parent / "resources" / "supportRunbooks"
        reader = ResourceReader(resource_folder)
        documents = reader.read_files()
        logging.info("Finished reading support runbooks...")

        logging.info("Splitting support runbooks into texts....")
        texts = reader.read_file_contents(documents)

        logging.info("Initializing Embeddings....")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        logging.info("Finished initializing Embeddings...")

        logging.info(f"Initializing Vector store....")
        store = Chroma.from_documents(texts, embeddings)
        logging.info("Finished initializing Vector store...")

        llm_name = "llama3"
        logging.info("Initializing LLM...")
        llm = Ollama(model=llm_name, base_url="http://localhost:11434")
        logging.info(f"LLM initialized with model {llm_name}")

        logging.info(f"Initializing Price RAG....")
        rag = PriceRag(llm, store.as_retriever())
        logging.info(f"Price RAG initialized...")
        
        print("Welcome to the Price service RAG Q&A system. Type 'exit' to quit.")

        sleep(1)

        chat_history = []
        line = 0

        while True:

            if line == 0:
                question = input("\nEnter your question: ").strip()
                query = question
            else:
                query = input("\nYour saying: ").strip()
        
            if query.lower() == 'exit':
                print("Thank you for using Price service RAG Q&A system. Goodbye!")
                break
        
            if query:
                answer = rag.ask_question(query, chat_history)
                if line == 0:
                    print(f"\nQuestion: {query}")
                print(f"Answer: {answer['answer']}")
                print("Sources:")
                
                # Use a set to store unique sources
                unique_sources = set(answer['sources'])
        
                for source in unique_sources:
                    print(f"- {source}")

                # for source in answer['sources']:
                #     print(f"- {source}")
            else:
                print("Please enter a valid question.")

            line = line + 1

    except Exception as e:
        logging.error(f"Error while starting Price RAG: {e}")
        raise

if __name__ == '__main__':
    main()