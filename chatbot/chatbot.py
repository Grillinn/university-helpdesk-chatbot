from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from typing import Optional

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
PERSIST_DIR = '../data/chroma_db'

print(f"Loaded Gemini API Key: {gemini_api_key}") # Debugging

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vector database
vectordb = None
retriever = None
try:
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    retriever = vectordb.as_retriever()
    print("Chroma database loaded successfully.")
except Exception as e:
    print(f"Error loading Chroma database: {e}")

# Initialize Gemini Pro LLM
gemini_llm = None
if gemini_api_key:
    try:
        gemini_llm = ChatGoogleGenerativeAI(model_name="gemini-pro", google_api_key=gemini_api_key)
        print("Gemini Pro LLM initialized successfully.")
    except Exception as e:
        print(f"Error initializing Gemini Pro LLM: {e}")
        print(f"Initialization error details: {e}") # More detailed error
else:
    print("GEMINI_API_KEY environment variable not set.")

# Create RetrievalQA chain if retriever and LLM are available
rag_chain = None
if retriever and gemini_llm:
    try:
        rag_chain = RetrievalQA.from_llm(llm=gemini_llm, retriever=retriever)
        print("RAG chain initialized successfully.")
    except Exception as e:
        print(f"Error initializing RAG chain: {e}")

def query_rag(query: str, db=None) -> Optional[str]:
    """
    Queries the retrieval-based question answering system.
    """
    if rag_chain:
        try:
            response = rag_chain.run(query)
            return response
        except Exception as e:
            print(f"Error querying RAG chain: {e}")
            return "Sorry, I encountered an error while trying to answer your question."
    else:
        return "Sorry, the knowledge base is currently unavailable."

def query_status_progress(application_id: str) -> str:
    """
    Placeholder function for querying application status or progress.
    Replace this with your actual implementation.
    """
    print(f"Received status/progress query for ID: {application_id}")
    return f"Status for application ID {application_id}: Pending (This is a placeholder)."

if __name__ == "__main__":
    print("\n--- Running chatbot.py directly (example usage) ---")
    example_query = "What are the key dates for undergraduate admissions?"
    response = query_rag(example_query)
    print(f"Question: {example_query}")
    print(f"Answer: {response}")

    if gemini_llm:
        example_no_context = "Tell me a fun fact about universities."
        response_no_context = gemini_llm.predict(example_no_context)
        print(f"\nQuestion (no context): {example_no_context}")
        print(f"Answer: {response_no_context}")

        progress_id = "2025-ABC-123"
        progress_response = query_status_progress(progress_id)
        print(f"\nChecking status for ID: {progress_id}")
        print(f"Status: {progress_response}")