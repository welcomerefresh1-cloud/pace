from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.student_records import StudentRecord, StudentRecordCreate, StudentRecordUpdate, StudentRecordPublic
from models.degrees import Degree
from models.alumni import Alumni
from models.errors import ErrorCode

router = APIRouter(prefix="/student-records", tags=["student-records"])


@router.post("", response_model=StudentRecordPublic)
def create_student_record(
    student_data: StudentRecordCreate,
    session: Session = Depends(get_session)
):
    """Create a new student record linked to an alumni"""
    # Verify degree exists
    degree = session.exec(
        select(Degree).where(Degree.degree_id == student_data.degree_id)
    ).first()
    
    if not degree:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.DEGREE_NOT_FOUND.value,
                "message": "Degree not found"
            }
        )
    
    # Verify alumni exists
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == student_data.alumni_id)
    ).first()
    
    if not alumni:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    # Convert Pydantic model to dict and extract non-StudentRecord fields
    student_dict = student_data.model_dump(exclude={"alumni_id", "degree_id"})
    student_dict["degree_code"] = degree.degree_code
    student_dict["alumni_code"] = alumni.alumni_code
    
    new_student = StudentRecord.model_validate(student_dict)
    session.add(new_student)
    
    # Update alumni's student_code reference for backwards compatibility
    alumni.student_code = None  # Will be set after flush
    session.add(alumni)
    
    try:
        session.flush()  # Get student_code
        alumni.student_code = new_student.student_code
        session.commit()
        session.refresh(new_student)
        return new_student
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_student_records_student_id" in error_str or "student_records_student_id_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_STUDENT_ID.value,
                    "message": "Student ID already in use"
                }
            )
        elif "student_records_alumni_code_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value,
                    "message": "This alumni already has a student record"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.INVALID_INPUT.value,
                    "message": "Student record with these details already exists"
                }
            )


@router.get("", response_model=list[StudentRecordPublic])
def get_all_student_records(session: Session = Depends(get_session)):
    """Get all student records"""
    students = session.exec(select(StudentRecord)).all()
    return students

@router.get("/{student_id}", response_model=StudentRecordPublic)
def get_student_record(student_id: str, session: Session = Depends(get_session)):
    
    """Get a student record by student ID"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id.upper())
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                "message": "Student record not found"
            }
        )
    return student


@router.put("/{student_id}", response_model=StudentRecordPublic)
def update_student_record(
    student_id: str,
    student_data: StudentRecordUpdate,
    session: Session = Depends(get_session)
):
    """Update a student record"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id.upper())
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                "message": "Student record not found"
            }
        )
    
    # If alumni_id is provided, verify it exists and update the link
    if student_data.alumni_id is not None:
        alumni = session.exec(
            select(Alumni).where(Alumni.alumni_id == student_data.alumni_id)
        ).first()
        
        if not alumni:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                    "message": "Alumni not found"
                }
            )
        
        # Update student's alumni_code link and alumni's student_code for backwards compatibility
        student.alumni_code = alumni.alumni_code
        alumni.student_code = student.student_code
        session.add(alumni)
    
    # Update only provided fields
    if student_data.year_graduated is not None:
        student.year_graduated = student_data.year_graduated
    if student_data.gwa is not None:
        student.gwa = student_data.gwa
    if student_data.avg_prof_grade is not None:
        student.avg_prof_grade = student_data.avg_prof_grade
    if student_data.avg_elec_grade is not None:
        student.avg_elec_grade = student_data.avg_elec_grade
    if student_data.ojt_grade is not None:
        student.ojt_grade = student_data.ojt_grade
    if student_data.leadership_pos is not None:
        student.leadership_pos = student_data.leadership_pos
    if student_data.act_member_pos is not None:
        student.act_member_pos = student_data.act_member_pos
    
    session.add(student)
    
    try:
        session.commit()
        session.refresh(student)
        return student
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "student_records_alumni_code_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value,
                    "message": "This alumni already has a student record"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.INVALID_INPUT.value,
                    "message": "Update failed: Invalid input or duplicate entry"
                }
            )


@router.delete("/{student_id}")
def delete_student_record(student_id: str, session: Session = Depends(get_session)):
    """Delete a student record"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id.upper())
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                "message": "Student record not found"
            }
        )
    
    session.delete(student)
    session.commit()
    
    return {
        "message": f"Student record {student_id} deleted successfully"
    }