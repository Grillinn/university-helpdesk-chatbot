# backend/routes/student.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import models, database, services
import pandas as pd
import io

router = APIRouter()

@router.post("/students/", response_model=models.StudentResponse)
def create_student(student: models.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.application_id == student.application_id).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student with this application ID already exists")
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[models.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@router.get("/students/{student_id}", response_model=models.StudentResponse)
def read_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.put("/students/{student_id}", response_model=models.StudentResponse)
def update_student(student_id: int, student: models.StudentUpdate, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}

@router.post("/students/upload/", response_model=List[models.StudentResponse])
async def upload_students_from_excel(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith((".xlsx", ".csv")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv are allowed.")
    try:
        contents = await file.read()
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            df = pd.read_csv(io.BytesIO(contents))

        created_students = []
        for index, row in df.iterrows():
            try:
                student_data = row.to_dict()
                # Basic validation - adjust as needed
                if not all(key in student_data for key in ["Application ID", "Full Name", "Email", "Phone", "Branch", "Physics", "Chemistry", "Math", "Total %", "Document Submission Status", "Loan Applied"]):
                    raise ValueError(f"Missing required fields in row {index + 2}")

                student = models.StudentCreate(**student_data)
                db_student = db.query(models.Student).filter(models.Student.application_id == student.application_id).first()
                if not db_student:
                    db_student = models.Student(**student.dict())
                    db.add(db_student)
                    db.commit()
                    db.refresh(db_student)
                    created_students.append(db_student)
                else:
                    print(f"Warning: Student with Application ID {student.application_id} already exists and was skipped.")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error processing row {index + 2}: {e}")

        return created_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the uploaded file: {e}")