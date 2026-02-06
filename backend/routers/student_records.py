from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.student_records import StudentRecord, StudentRecordCreate, StudentRecordUpdate, StudentRecordPublic
from models.degrees import Degree
from models.alumni import Alumni
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginatedResponse, PaginationMetadata
from utils.logging import log_error, log_integrity_error

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
        log_error("student_records", "create_student_record", ErrorCode.DEGREE_NOT_FOUND.value, f"Degree {student_data.degree_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.DEGREE_NOT_FOUND.value,
                message="Degree not found"
            ).model_dump(mode='json')
        )
    
    # Verify alumni exists
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == student_data.alumni_id)
    ).first()
    
    if not alumni:
        log_error("student_records", "create_student_record", ErrorCode.ALUMNI_NOT_FOUND.value, f"Alumni {student_data.alumni_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.ALUMNI_NOT_FOUND.value,
                message="Alumni not found"
            ).model_dump(mode='json')
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
        return StandardResponse(
            success=True,
            code=SuccessCode.STUDENT_RECORD_CREATED.value,
            message="Student record created successfully",
            data=StudentRecordPublic.model_validate(new_student)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_student_records_student_id" in error_str or "student_records_student_id_key" in error_str:
            log_integrity_error("student_records", "create_student_record", ErrorCode.DUPLICATE_STUDENT_ID.value, "Student ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_STUDENT_ID.value,
                    message="Student ID already in use"
                ).model_dump(mode='json')
            )
        elif "student_records_alumni_code_key" in error_str:
            log_integrity_error("student_records", "create_student_record", ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value, "Alumni already has student record", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value,
                    message="This alumni already has a student record"
                ).model_dump(mode='json')
            )
        elif "student_records_degree_code_fkey" in error_str or "degree_code" in error_str:
            log_integrity_error("student_records", "create_student_record", ErrorCode.DEGREE_NOT_FOUND.value, "Specified degree does not exist", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DEGREE_NOT_FOUND.value,
                    message="Specified degree does not exist"
                ).model_dump(mode='json')
            )
        elif "student_records_alumni_code_fkey" in error_str or "alumni_code" in error_str:
            log_integrity_error("student_records", "create_student_record", ErrorCode.ALUMNI_NOT_FOUND.value, "Specified alumni does not exist", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.ALUMNI_NOT_FOUND.value,
                    message="Specified alumni does not exist"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("student_records", "create_student_record", ErrorCode.INVALID_INPUT.value, "Student record creation failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Student record creation failed: Invalid input or constraint violation"
                ).model_dump(mode='json')
            )


@router.get("")
def get_all_student_records(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    session: Session = Depends(get_session)
):
    """Get all student records with pagination"""
    # Get total count
    total = session.exec(select(func.count(StudentRecord.student_code))).one()
    
    # Get paginated data
    query = select(StudentRecord)
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    students = session.exec(query).all()
    
    # Calculate pagination metadata
    returned = len(students)
    has_next = (offset + returned) < total if limit > 0 else False
    
    pagination = PaginationMetadata(
        total=total,
        limit=limit,
        offset=offset,
        returned=returned,
        has_next=has_next
    )
    
    return StandardResponse(
        success=True,
        code=SuccessCode.STUDENT_RECORDS_RETRIEVED.value,
        message=f"Retrieved {returned} student records",
        data={"student_records": [StudentRecordPublic.model_validate(s) for s in students], "pagination": pagination}
    )

@router.get("/{student_id}", response_model=StudentRecordPublic)
def get_student_record(student_id: str, session: Session = Depends(get_session)):
    
    """Get a student record by student ID"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id.upper())
    ).first()

    if not student:
        log_error("student_records", "get_student_record", ErrorCode.STUDENT_RECORD_NOT_FOUND.value, f"Student record {student_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                message="Student record not found"
            ).model_dump(mode='json')
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
        log_error("student_records", "update_student_record", ErrorCode.STUDENT_RECORD_NOT_FOUND.value, f"Student record {student_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                message="Student record not found"
            ).model_dump(mode='json')
        )
    
    # If alumni_id is provided, verify it exists and update the link
    if student_data.alumni_id is not None:
        alumni = session.exec(
            select(Alumni).where(Alumni.alumni_id == student_data.alumni_id)
        ).first()
        
        if not alumni:
            log_error("student_records", "update_student_record", ErrorCode.ALUMNI_NOT_FOUND.value, f"Alumni {student_data.alumni_id} not found")
            raise HTTPException(
                status_code=404,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.ALUMNI_NOT_FOUND.value,
                    message="Alumni not found"
                ).model_dump(mode='json')
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
        return StandardResponse(
            success=True,
            code=SuccessCode.STUDENT_RECORD_UPDATED.value,
            message="Student record updated successfully",
            data=StudentRecordPublic.model_validate(student)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "student_records_alumni_code_key" in error_str:
            log_integrity_error("student_records", "update_student_record", ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value, "Alumni already has student record", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.ALUMNI_ALREADY_HAS_STUDENT_RECORD.value,
                    message="This alumni already has a student record"
                ).model_dump(mode='json')
            )
        elif "student_records_degree_code_fkey" in error_str or "degree_code" in error_str:
            log_integrity_error("student_records", "update_student_record", ErrorCode.DEGREE_NOT_FOUND.value, "Specified degree does not exist", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DEGREE_NOT_FOUND.value,
                    message="Specified degree does not exist"
                ).model_dump(mode='json')
            )
        elif "student_records_alumni_code_fkey" in error_str or "alumni_code" in error_str:
            log_integrity_error("student_records", "update_student_record", ErrorCode.ALUMNI_NOT_FOUND.value, "Specified alumni does not exist", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.ALUMNI_NOT_FOUND.value,
                    message="Specified alumni does not exist"
                ).model_dump(mode='json')
            )
        elif "ix_student_records_student_id" in error_str or "student_records_student_id_key" in error_str:
            log_integrity_error("student_records", "update_student_record", ErrorCode.DUPLICATE_STUDENT_ID.value, "Student ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_STUDENT_ID.value,
                    message="Student ID already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("student_records", "update_student_record", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Update failed: Invalid input or constraint violation"
                ).model_dump(mode='json')
            )


@router.delete("/{student_id}")
def delete_student_record(student_id: str, session: Session = Depends(get_session)):
    """Delete a student record"""
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_id == student_id.upper())
    ).first()
    
    if not student:
        log_error("student_records", "delete_student_record", ErrorCode.STUDENT_RECORD_NOT_FOUND.value, f"Student record {student_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.STUDENT_RECORD_NOT_FOUND.value,
                message="Student record not found"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(student)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.STUDENT_RECORD_DELETED.value,
            message=f"Student record {student_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("student_records", "delete_student_record", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.INVALID_INPUT.value,
                "message": "Delete failed: Constraint violation or invalid operation"
            }
        )