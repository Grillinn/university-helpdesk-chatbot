# frontend/app.py
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Ensure this matches your backend URL

st.title("Diya: Your Admission Assistant")

if "director_chat_history" not in st.session_state:
    st.session_state["director_chat_history"] = [{"role": "assistant", "content": "Hey how are you doing today? Please let me know how can I help you with admission updates or any questions you might have."}]

def format_admission_summary(summary_data):
    """Formats the admission summary data into a readable string."""
    summary_text = "## Current Admission Status Summary\n\n"
    summary_text += f"**Total Applications Received:** {summary_data.get('total_applications', 'N/A')}\n"
    summary_text += "**Applications by Stage:**\n"
    for stage, count in summary_data.get('applications_by_stage', {}).items():
        summary_text += f"- {stage}: {count}\n"
    # Add more details as needed
    return summary_text

def display_chat_history():
    for message in st.session_state["director_chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

display_chat_history()

# File Uploader
st.subheader("Upload File for Context")
uploaded_file = st.file_uploader("Choose a file (PDF, TXT, etc.)", type=["pdf", "txt"])
if uploaded_file:
    st.info(f"File '{uploaded_file.name}' uploaded. You can now ask questions related to it.")
    # In a real application, you would likely send this file to the backend

st.subheader("Chat with Diya")
director_live_query = st.chat_input("Your message...")
if director_live_query:
    st.session_state["director_chat_history"].append({"role": "director", "content": director_live_query})
    display_chat_history() # Update chat display immediately

    if director_live_query.lower() == "show admission summary":
        try:
            response = requests.get(f"{BACKEND_URL}/admin/admission_summary")
            response.raise_for_status()
            summary_data = response.json()["summary"]
            summary_text = format_admission_summary(summary_data)
            st.session_state["director_chat_history"].append({"role": "assistant", "content": summary_text})
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching admission summary: {e}")
            st.session_state["director_chat_history"].append({"role": "assistant", "content": "Sorry, I couldn't retrieve the admission summary at the moment."})
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state["director_chat_history"].append({"role": "assistant", "content": "An unexpected error occurred while trying to get the summary."})
    else:
        # Send director's live query to the backend for regular chat
        try:
            response = requests.post(f"{BACKEND_URL}/admin/chat", json={"query": director_live_query})
            response.raise_for_status()
            chatbot_response = response.json()["response"]
            st.session_state["director_chat_history"].append({"role": "assistant", "content": chatbot_response})
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with backend: {e}")
            st.session_state["director_chat_history"].append({"role": "assistant", "content": "Sorry, I'm having trouble connecting to the server right now."})
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state["director_chat_history"].append({"role": "assistant", "content": "An unexpected error occurred while processing your request."})

    st.rerun()

if st.button("Clear Chat"):
    st.session_state["director_chat_history"] = []
    st.session_state["director_chat_history"].append({"role": "assistant", "content": "Hey how are you doing today? Please let me know how can I help you with admission updates or any questions you might have."})
    st.rerun()