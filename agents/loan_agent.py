# agents/loan_agent.py
from typing import List, Dict
from sqlalchemy.orm import Session
from backend import models  # Import your SQLAlchemy models
from backend.database import SessionLocal  # Import for creating a database session

class LoanAgent:
    def assess_loan_eligibility(self, students_data: List[Dict]) -> List[Dict]:
        """Assesses loan eligibility for students based on predefined criteria."""
        assessment_results = []
        db = SessionLocal()
        try:
            for student in students_data:
                application_id = student.get("application_id")
                if not application_id:
                    assessment_results.append({"Application ID": "N/A", "loan_eligibility_score": 0, "reason": "Missing Application ID"})
                    continue

                student_record = db.query(models.Student).filter(models.Student.application_id == application_id).first()
                if not student_record:
                    assessment_results.append({"Application ID": application_id, "loan_eligibility_score": 0, "reason": "Student record not found"})
                    continue

                # Define loan eligibility criteria (adjust as needed)
                eligibility_score = 0
                reason = ""

                if student_record.total_percentage >= 70:
                    eligibility_score += 50
                else:
                    reason += "Total percentage below threshold; "

                if student_record.math >= 60:
                    eligibility_score += 30
                else:
                    reason += "Math score below threshold; "

                # Add more criteria as needed (e.g., branch, other subject scores)

                # Update the student record with the assessment
                student_record.loan_eligibility_score = eligibility_score
                db.add(student_record)

                assessment_results.append({
                    "Application ID": application_id,
                    "loan_eligibility_score": eligibility_score,
                    "reason": reason.strip() if reason else "Eligible based on criteria"
                })
            db.commit()
            return assessment_results
        finally:
            db.close()

if __name__ == "__main__":
    # Example usage (requires a running database with student data)
    loan_agent = LoanAgent()

    def get_sample_students_data():
        db = SessionLocal()
        try:
            students = db.query(models.Student).limit(5).all()
            student_dicts = [{"application_id": s.application_id, "total_percentage": s.total_percentage, "math": s.math} for s in students]
            return student_dicts
        finally:
            db.close()

    sample_students = get_sample_students_data()
    if sample_students:
        eligibility_results = loan_agent.assess_loan_eligibility(sample_students)
        print("Loan Eligibility Assessment Results:")
        for result in eligibility_results:
            print(f"Application ID: {result['Application ID']}, Score: {result['loan_eligibility_score']}, Reason: {result['reason']}")