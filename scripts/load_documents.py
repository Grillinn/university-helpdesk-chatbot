# chatbot/load_documents.py
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = '../data/admission_info'
PERSIST_DIR = '../data/chroma_db'

def load_and_process_documents(data_path: str = DATA_PATH, persist_dir: str = PERSIST_DIR):
    """
    Loads documents from the specified path, processes them,
    creates embeddings, and stores them in a Chroma vector database.
    """
    documents = []
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".docx") or file.endswith(".doc"):
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents.")

    # Split documents into chunks (optional but recommended for better RAG)
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    # Initialize embeddings using HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create and persist the Chroma vector database
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectordb.persist()
    print(f"Embeddings stored in ChromaDB at {persist_dir}")

if __name__ == "__main__":
    load_and_process_documents()
    print("Document loading and processing complete.")