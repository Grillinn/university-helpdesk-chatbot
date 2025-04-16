# backend/services/document_service.py
from typing import List, Dict
from ..models import Student
from agents.document_checker import DocumentChecker # Import the non-CrewAI class

class DocumentService:
    def __init__(self):
        self.document_checker = DocumentChecker()

    def check_student_documents(self, students_data: List[Student]) -> List[Dict]:
        student_dicts = [{"application_id": student.application_id} for student in students_data]
        return self.document_checker.check_student_documents(student_dicts)

    def answer_document_queries(self, query: str) -> str:
        return self.document_checker.answer_document_queries(query)