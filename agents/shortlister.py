# agents/shortlister.py
from typing import List, Dict
from sqlalchemy.orm import Session
from backend import models  # Import your SQLAlchemy models
from backend.database import SessionLocal  # Import for creating a database session

class Shortlister:
    def shortlist_students(self, students_data: List[Dict], cutoff_percentage: float) -> List[Dict]:
        """Shortlists students based on a given cutoff percentage."""
        shortlisted_students = []
        db = SessionLocal()
        try:
            for student in students_data:
                application_id = student.get("application_id")
                if not application_id:
                    continue

                student_record = db.query(models.Student).filter(models.Student.application_id == application_id).first()
                if not student_record:
                    continue

                if student_record.total_percentage >= cutoff_percentage:
                    student_record.final_admission_status = "Shortlisted"
                    db.add(student_record)
                    shortlisted_students.append({"Application ID": application_id, "total_percentage": student_record.total_percentage})
                else:
                    student_record.final_admission_status = "Not Shortlisted"
                    db.add(student_record)
            db.commit()
            return shortlisted_students
        finally:
            db.close()

if __name__ == "__main__":
    # Example usage (requires a running database with student data)
    shortlister = Shortlister()
    cutoff = 80.0

    def get_sample_students_data():
        db = SessionLocal()
        try:
            students = db.query(models.Student).limit(10).all()
            student_dicts = [{"application_id": s.application_id, "total_percentage": s.total_percentage} for s in students]
            return student_dicts
        finally:
            db.close()

    sample_students = get_sample_students_data()
    if sample_students:
        shortlisted = shortlister.shortlist_students(sample_students, cutoff)
        print(f"Shortlisted Students (Cutoff: {cutoff}%):")
        for student in shortlisted:
            print(f"Application ID: {student['Application ID']}, Percentage: {student['total_percentage']}")