# backend/models.py
from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    application_id: str
    full_name: str
    email: str
    phone: str
    branch: str
    physics: int
    chemistry: int
    math: int
    total_percentage: float
    document_submission_status: str
    loan_applied: str
    loan_eligibility_score: Optional[int] = 0
    final_admission_status: Optional[str] = "Pending"
    email_sent: Optional[str] = "No"

class StudentUpdate(BaseModel):
    document_submission_status: Optional[str] = None
    loan_eligibility_score: Optional[int] = None
    final_admission_status: Optional[str] = None
    email_sent: Optional[str] = None

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True