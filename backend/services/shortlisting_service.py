# backend/services/shortlister_service.py
from typing import List, Dict
from ..models import Student
from agents.shortlister import Shortlister

class ShortlisterService:
    def __init__(self):
        self.shortlister = Shortlister()

    def shortlist_students(self, students_data: List[Student], cutoff_percentage: float) -> List[Dict]:
        student_dicts = [student.__dict__ for student in students_data]
        return self.shortlister.shortlist_students(student_dicts, cutoff_percentage)