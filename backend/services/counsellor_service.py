# backend/services/counsellor_service.py
from typing import List, Dict  # Import Dict
from ..models import Student
from agents.counsellor import Counsellor # Import the non-CrewAI class

class CounsellorService:
    def __init__(self):
        self.counsellor = Counsellor()

    def send_general_updates(self, students_data: List[Student], update_message: str) -> List[Dict]:
        student_dicts = [student.__dict__ for student in students_data]
        result = self.counsellor.send_general_updates(student_dicts, update_message)
        return result

    def respond_to_query(self, student_query: str, student_details: dict) -> str:
        result = self.counsellor.respond_to_query(student_query, student_details)
        return result