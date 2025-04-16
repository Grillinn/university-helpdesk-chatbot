# agents/document_checker.py
from typing import List, Dict
from sqlalchemy.orm import Session
from backend import models  # Import your SQLAlchemy models
from backend.database import SessionLocal  # Import for creating a database session
import json

class DocumentChecker:
    def check_student_documents(self, students_data: List[Dict]) -> List[Dict]:
        """Checks if all required documents are present for each student."""
        results = []
        required_documents = ["marksheet_10th", "marksheet_12th", "id_proof", "photo"] # Define your required documents

        db = SessionLocal()
        try:
            for student in students_data:
                application_id = student.get("application_id")
                if not application_id:
                    results.append({"Application ID": "N/A", "issues": ["Missing Application ID in data"]})
                    continue

                student_record = db.query(models.Student).filter(models.Student.application_id == application_id).first()
                if not student_record:
                    results.append({"Application ID": application_id, "issues": ["Student record not found in database"]})
                    continue

                submitted_documents = {
                    "marksheet_10th": student_record.document_submission_status and "10th Marksheet" in student_record.document_submission_status,
                    "marksheet_12th": student_record.document_submission_status and "12th Marksheet" in student_record.document_submission_status,
                    "id_proof": student_record.document_submission_status and "ID Proof" in student_record.document_submission_status,
                    "photo": student_record.document_submission_status and "Photo" in student_record.document_submission_status,
                }

                missing = [doc for doc, submitted in submitted_documents.items() if not submitted]
                issues = missing  # For now, missing documents are the primary "issue"

                results.append({"Application ID": application_id, "issues": issues})

            return results
        finally:
            db.close()

    def answer_document_queries(self, query: str) -> str:
        """Answers questions related to document submissions."""
        db = SessionLocal()
        try:
            query_lower = query.lower()

            if "what documents are needed" in query_lower:
                required_documents = ["10th Marksheet", "12th Marksheet", "ID Proof", "Passport-sized Photograph"] # More user-friendly names
                return f"The required documents for application are: {', '.join(required_documents)}."

            elif "how many students didn't submit documents" in query_lower:
                # Assuming 'Pending' in document_submission_status means no documents submitted
                not_submitted_count = db.query(models.Student).filter(models.Student.document_submission_status == "Pending").count()
                return f"{not_submitted_count} students have not submitted any documents."

            elif "how many submitted wrong documents" in query_lower:
                # This is a placeholder - actual wrong document detection is complex
                # For now, we'll count those with issues (missing for simplicity)
                wrong_submission_count = db.query(models.Student).filter(models.Student.document_submission_status.like("Issues:%")).count()
                return f"{wrong_submission_count} students have submitted documents with issues (e.g., missing)."

            elif "status of application" in query_lower:
                app_id = query_lower.split("application")[-1].strip().replace("#", "").strip()
                if app_id:
                    student = db.query(models.Student).filter(models.Student.application_id == app_id).first()
                    if student:
                        return f"The document submission status for Application ID {app_id} is: {student.document_submission_status}."
                    else:
                        return f"Application ID {app_id} not found."
                else:
                    return "Please specify an Application ID to check the status."

            elif "list of students with missing" in query_lower:
                document_type = query_lower.split("missing")[-1].strip()
                students_with_missing = db.query(models.Student).filter(models.Student.document_submission_status.like(f"%Missing {document_type}%")).all()
                if students_with_missing:
                    student_ids = [s.application_id for s in students_with_missing]
                    return f"Students with missing '{document_type}': {', '.join(student_ids)}"
                else:
                    return f"No students found with missing '{document_type}'."

            else:
                return "I can answer questions about required documents, students with missing documents, and the document status of specific applications."

        finally:
            db.close()

# Example usage (requires a running database with student data)
if __name__ == "__main__":
    checker = DocumentChecker()

    # Simulate fetching student data from the database
    def get_sample_students_data():
        db = SessionLocal()
        try:
            students = db.query(models.Student).limit(5).all()
            student_dicts = [{"application_id": s.application_id} for s in students] # Only application ID for checking
            return student_dicts
        finally:
            db.close()

    sample_students = get_sample_students_data()
    if sample_students:
        check_results = checker.check_student_documents(sample_students)
        print("Document Check Results:", check_results)

    query1 = "What documents are needed for the application?"
    answer1 = checker.answer_document_queries(query1)
    print(f"\nQuestion: {query1}\nAnswer: {answer1}")

    query2 = "How many students didn't submit documents?"
    answer2 = checker.answer_queries(query2)
    print(f"\nQuestion: {query2}\nAnswer: {answer2}")

    query3 = "What is the status of application APP1001?"
    answer3 = checker.answer_queries(query3)
    print(f"\nQuestion: {query3}\nAnswer: {answer3}")