# agents/counsellor.py
from typing import List, Dict

class Counsellor:
    def send_general_updates(self, students_data: List[Dict], update_message: str) -> List[Dict]:
        """Generates personalized update messages for each student."""
        email_details = []
        for student in students_data:
            subject = "Important Admission Update"
            body = f"""
            Dear {student.get('full_name', 'Student')},

            We have an important update regarding your admission process:

            {update_message}

            Please log in to your portal for more details.

            Sincerely,
            The Admission Team
            """
            email_details.append({
                "Email": student.get('email'),
                "Subject": subject,
                "Body": body
            })
        return email_details

    def respond_to_query(self, student_query: str, student_details: Dict) -> str:
        """
        Placeholder for responding to specific student queries.
        In a real application, this would likely involve more complex logic,
        potentially using an LLM directly or accessing student-specific data.
        """
        return f"Thank you for your query: '{student_query}'. We will get back to you shortly with a detailed response."

if __name__ == "__main__":
    # Example usage
    sample_students = [
        {"full_name": "Alice Smith", "email": "alice.smith@example.com"},
        {"full_name": "Bob Johnson", "email": "bob.johnson@example.com"},
    ]
    counsellor = Counsellor()
    update_message = "The deadline for fee payment has been extended to April 20th, 2025."
    email_details = counsellor.send_general_updates(sample_students, update_message)
    for detail in email_details:
        print(f"To: {detail['Email']}")
        print(f"Subject: {detail['Subject']}")
        print(f"Body:\n{detail['Body']}\n---")

    sample_query = "What is the last date to submit documents?"
    sample_student_info = {"full_name": "Charlie Brown", "branch": "CSE"}
    query_response = counsellor.respond_to_query(sample_query, sample_student_info)
    print(f"\nQuery Response: {query_response}")