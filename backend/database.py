# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    branch = Column(Enum("CSE", "ECE", "IT"))
    physics = Column(Integer)
    chemistry = Column(Integer)
    math = Column(Integer)
    total_percentage = Column(Float)
    document_submission_status = Column(String)
    loan_applied = Column(Enum("Yes", "No"))
    loan_eligibility_score = Column(Integer)
    final_admission_status = Column(String)
    email_sent = Column(Enum("Yes", "No"))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()