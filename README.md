# University Admission Helpdesk with Gemini Pro

This project provides an AI-powered helpdesk for university admissions, leveraging the Gemini Pro language model from Google AI. It allows prospective students to ask questions about admission requirements, application processes, and other relevant information. The system uses Retrieval-Augmented Generation (RAG) to ground the model's responses in provided university documents.

## Overview

The project consists of the following main components:

* **`backend` (FastAPI):** An API built with FastAPI that handles incoming questions from the frontend. It interacts with the Gemini Pro model and the knowledge base.
* **`chatbot` (Python):** Contains the core logic for loading the knowledge base (ChromaDB), embedding documents, and querying the Gemini Pro model using RAG.
* **`frontend` (Streamlit):** Provides two user interfaces:
    * **Admin Interface (`app.py`):** Allows administrators to upload documents that will be used as the knowledge base.
    * **Student Chatbot (`chatbot_app.py`):** Enables prospective students to ask questions and receive AI-powered answers.
* **`scripts` (Python):** Contains utility scripts, such as `load_documents.py` to process and embed your university documents.
* `.env`: Stores environment variables, such as your Gemini Pro API key.
* `requirements.txt`: Lists the Python dependencies for the project.

## Setup and Installation

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd University_Admission_Helpdesk
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    .\venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    * Create a `.env` file in the root directory of the project.
    * Add your Gemini Pro API key to the `.env` file:
        ```env
        GEMINI_API_KEY="YOUR_GEMINI_PRO_API_KEY"
        ```
        Replace `YOUR_GEMINI_PRO_API_KEY` with your actual API key obtained from [Google AI Studio](https://makersuite.google.com/app/apikey).

5.  **Load and Process Documents (Knowledge Base):**
    * Place your university admission documents (PDF, TXT, etc.) in a directory (e.g., `data/documents`).
    * Run the `load_documents.py` script from the `scripts` directory to process these documents, generate embeddings, and store them in ChromaDB:
        ```bash
        cd scripts
        python load_documents.py ../data/documents ../data/chroma_db
        cd ..
        ```
        Ensure the script completes without errors and indicates that embeddings have been stored.

## Running the Project

You will need to run the backend and the frontend applications separately.

**1. Start the FastAPI Backend:**

   ```bash
   cd backend
   uvicorn backend.main:app --reload

   This will start the backend API server, usually accessible at http://127.0.0.1:8000. Keep this terminal window running.

2. Start the Streamlit Admin Frontend:

Open a new terminal window, activate your virtual environment, and navigate to the frontend directory:

Bash

cd frontend
streamlit run app.py
This will open the admin interface ("Diya, Your Admission Assistant") in your web browser, usually at http://localhost:8501.

3. Start the Streamlit Student Chatbot Frontend:

Open another new terminal window, activate your virtual environment, and navigate to the frontend directory:

Bash

cd frontend
streamlit run chatbot_app.py
This will open the student chatbot interface in your web browser, potentially at the same port (http://localhost:8501) if the admin app is closed, or on a different port. Check the terminal output for the URL.

Interacting with the Applications
Admin Interface ("Diya, Your Admission Assistant"): Use this interface to upload new documents to update the knowledge base. It might also provide other administrative functionalities (depending on the implementation).
Student Chatbot: Use the chat interface to ask questions about university admissions. The AI should respond based on the information extracted from the documents you uploaded.
Project Structure
University_Admission_Helpdesk/
├── backend/
│   ├── main.py         # FastAPI application entry point
│   └── routes/
│       ├── admin.py    # Routes for admin functionalities
│       ├── chatbot.py  # Routes for chatbot queries
│       └── student.py  # (Optional) Routes for student-specific features
├── chatbot/
│   └── chatbot.py      # Core chatbot logic (RAG implementation)
├── data/
│   ├── chroma_db/      # Directory where ChromaDB stores the knowledge base
│   └── documents/      # (Optional) Directory to store source documents
├── frontend/
│   ├── app.py          # Streamlit admin interface
│   └── chatbot_app.py  # Streamlit student chatbot interface
├── scripts/
│   └── load_documents.py # Script to load and process documents
├── .env                # Environment variables (API key)
├── .gitignore
└── requirements.txt    # Python dependencies
Contributing
(Add contribution guidelines if you plan to accept contributions)

License
(Add license information if applicable)

Acknowledgements
FastAPI for the backend framework.
Streamlit for the frontend framework.
Langchain for simplifying LLM interactions and RAG implementation.
Hugging Face Transformers for embeddings.
ChromaDB for the vector database.
Google AI for the Gemini Pro language model.