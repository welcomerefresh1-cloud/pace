from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from models.student_records import StudentRecord, StudentRecordCreate, StudentRecordPublic

router = APIRouter(prefix="/student-records", tags=["student-records"])


@router.get("", response_model=list[StudentRecordPublic])
def get_all_student_records(session: Session = Depends(get_session)):
    """Get all student records"""
    students = session.exec(select(StudentRecord)).all()
    return students

@router.get("/{student_id}", response_model=StudentRecordPublic)
def get_student_record(student_id: str, session: Session = Depends(get_session)):
    
    """Get a student record by student ID"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id)
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    return student