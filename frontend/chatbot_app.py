# frontend/chatbot_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def get_admission_status(application_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}/chatbot/status/{application_id}")
        response.raise_for_status()
        status_data = response.json()
        st.markdown(f"**Application ID:** {status_data.get('application_id', 'N/A')}")
        st.markdown(f"**Full Name:** {status_data.get('full_name', 'N/A')}")
        st.markdown(f"**Branch:** {status_data.get('branch', 'N/A')}")
        st.markdown(f"**Document Status:** {status_data.get('document_submission_status', 'N/A')}")
        st.markdown(f"**Admission Status:** {status_data.get('final_admission_status', 'N/A')}")
        st.markdown(f"**Loan Applied:** {status_data.get('loan_applied', 'N/A')}")
        st.markdown(f"**Loan Eligibility Score:** {status_data.get('loan_eligibility_score', 'N/A')}")
        return status_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching status for Application ID '{application_id}': {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def query_admission_info(query: str):
    try:
        response = requests.get(f"{BACKEND_URL}/chatbot/query/?query={query}")
        response.raise_for_status()
        answer_data = response.json()
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "assistant", "content": answer_data.get('answer', 'No answer found.')})
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying admission info: {e}")
        st.session_state.chat_history.append({"role": "assistant", "content": f"Error: Could not get answer. {e}"})
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.session_state.chat_history.append({"role": "assistant", "content": f"Error: An unexpected error occurred. {e}"})

def upload_file():
    uploaded_file = st.file_uploader("Upload a file for context (e.g., PDF, TXT)", type=["pdf", "txt"])
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.info(f"File '{uploaded_file.name}' uploaded. You can now ask questions related to it.")
        return True
    return False

def main():
    st.title("Student Admission Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    st.sidebar.subheader("Actions")
    menu = ["Chat with AI", "Get Application Status"]
    choice = st.sidebar.selectbox("Select an option", menu)

    st.sidebar.subheader("File Upload")
    upload_file()

    st.subheader("Chat Interface")

    if choice == "Get Application Status":
        st.info("Enter your Application ID to get the current status.")
        application_id = st.text_input("Your Application ID:")
        if st.button("Check Status"):
            if application_id:
                get_admission_status(application_id)
            else:
                st.warning("Please enter your Application ID.")

    elif choice == "Chat with AI":
        st.info("Ask any question about the admission process.")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("Your question:")
        if query:
            query_admission_info(query)
            st.rerun() # Rerun to display the latest messages

    st.sidebar.subheader("Admission Status Summary")
    if st.sidebar.button("Get Full Admission Status Summary"):
        try:
            response = requests.get(f"{BACKEND_URL}/admin/admission_summary")
            response.raise_for_status()
            summary_data = response.json().get('summary', {})
            st.sidebar.subheader("Summary:")
            st.sidebar.markdown(f"**Total Applications:** {summary_data.get('total_applications', 'N/A')}")
            st.sidebar.markdown("**Applications by Stage:**")
            applications_by_stage = summary_data.get('applications_by_stage', {})
            if applications_by_stage:
                for stage, count in applications_by_stage.items():
                    st.sidebar.markdown(f"- {stage}: {count}")
            else:
                st.sidebar.markdown("No stage information available.")
            # Add more summary details as needed
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Error fetching admission summary: {e}")
        except Exception as e:
            st.sidebar.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()