# backend/services/loan_service.py
from typing import List, Dict
from ..models import Student
from agents.loan_agent import LoanAgent

class LoanService:
    def __init__(self):
        self.loan_agent = LoanAgent()

    def assess_loan_eligibility(self, students_data: List[Student]) -> List[Dict]:
        student_dicts = [student.__dict__ for student in students_data]
        return self.loan_agent.assess_loan_eligibility(student_dicts)