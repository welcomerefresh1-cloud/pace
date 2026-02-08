from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.users import User, UserType
from models.courses import Course
from models.student_records import StudentRecord
from models.alumni import Alumni, AlumniCreate, AlumniUpdate, AlumniPublic
from models.composite import CompleteAlumniRegistration, CompleteAlumniResponse
from models.responses import AlumniFullProfile
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginatedResponse, PaginationMetadata
from utils.logging import log_error, log_integrity_error

router = APIRouter(prefix="/alumni", tags=["alumni"])


@router.post("/register")
def register_complete_alumni(
    data: CompleteAlumniRegistration,
    session: Session = Depends(get_session)
):
    """
    Create a complete alumni profile in one transaction:
    1. Create User account
    2. Create Alumni profile (linked to User)
    
    Student record can be created separately via POST /student-records
    This ensures data integrity - if any step fails, nothing is saved.
    """
    try:
        # Generate user_id based on user_type
        user_type = UserType.USER
        last_user = session.exec(
            select(User).where(User.user_type == user_type).order_by(User.user_id.desc())
        ).first()
        
        # Auto increment user_id
        if last_user:
            last_num = int(last_user.user_id.split("-")[1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        user_id = f"USER-{new_num:06d}"  # Format: USER-000001
        
        # Generate alumni_id
        last_alumni = session.exec(
            select(Alumni).order_by(Alumni.alumni_id.desc())
        ).first()
        
        # Auto increment alumni_id
        if last_alumni and last_alumni.alumni_id.startswith("ALMN-"):
            last_alumni_num = int(last_alumni.alumni_id.split("-")[1])
            new_alumni_num = last_alumni_num + 1
        else:
            new_alumni_num = 1
        
        alumni_id = f"ALMN-{new_alumni_num:06d}"  # Format: ALMN-000001
        
        # Step 1: Create User
        new_user = User(
            user_id=user_id,
            username=data.username,
            email=data.email,
            password=data.password,  # Already hashed by validator
            user_type=UserType.USER
        )
        session.add(new_user)
        session.flush()  # Get UUID without committing
        
        # Step 2: Create Alumni (linked to User, without student_code)
        new_alumni = Alumni(
            alumni_id=alumni_id,
            last_name=data.last_name,
            first_name=data.first_name,
            middle_name=data.middle_name,
            gender=data.gender,
            age=data.age,
            user_code=new_user.user_code
        )
        session.add(new_alumni)
        
        # Commit everything at once
        session.commit()
        
        return StandardResponse(
            success=True,
            code=SuccessCode.ALUMNI_CREATED.value,
            message="Alumni profile created successfully",
            data={
                "user_id": new_user.user_id,
                "alumni_id": new_alumni.alumni_id
            }
        )
        
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        print(f"DEBUG IntegrityError: {str(e)}")  # Log the actual error
        # Check which field caused the violation by looking at constraint name
        if "ix_users_email" in error_str or "users_email_key" in error_str:
            log_integrity_error("alumni", "register_complete_alumni", ErrorCode.DUPLICATE_EMAIL.value, "Email already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_EMAIL.value,
                    message="Email already in use"
                ).model_dump(mode='json')
            )
        elif "ix_users_username" in error_str or "users_username_key" in error_str:
            log_integrity_error("alumni", "register_complete_alumni", ErrorCode.DUPLICATE_USERNAME.value, "Username already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_USERNAME.value,
                    message="Username already in use"
                ).model_dump(mode='json')
            )
        elif "ix_alumni_alumni_id" in error_str or "alumni_alumni_id_key" in error_str:
            log_integrity_error("alumni", "register_complete_alumni", ErrorCode.DUPLICATE_ALUMNI_ID.value, "Alumni ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_ALUMNI_ID.value,
                    message="Alumni ID already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("alumni", "register_complete_alumni", ErrorCode.REGISTRATION_FAILED.value, "Registration failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.REGISTRATION_FAILED.value,
                    message="Registration failed"
                ).model_dump(mode='json')
            )
    except Exception as e:
        session.rollback()
        log_error("alumni", "register_complete_alumni", ErrorCode.REGISTRATION_FAILED.value, f"Unexpected error during registration: {str(e)}", e)
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.REGISTRATION_FAILED.value,
                message="Registration failed"
            ).model_dump(mode='json')
        )


@router.get("")
def get_all_alumni(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    search: str = Query(None, description="Search by first name, last name, email, or username"),
    gender: str = Query(None, description="Filter by gender (M, F, Other)"),
    sort_by: str = Query("alumni_id", description="Sort by field (alumni_id, first_name, last_name, created_at)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    session: Session = Depends(get_session)
):
    """Get all alumni records with filtering, searching, and sorting"""
    # Build query
    query = select(Alumni)
    
    # Apply search filter
    if search:
        search_like = f"%{search}%"
        # Search in alumni fields and related user email/username
        alumni_search = (
            (Alumni.first_name.ilike(search_like)) | 
            (Alumni.last_name.ilike(search_like))
        )
        query = query.where(alumni_search)
    
    # Apply gender filter
    if gender:
        query = query.where(Alumni.gender == gender.upper())
    
    # Get total count after filters
    total = session.exec(select(func.count(Alumni.alumni_code)).select_from(query.froms[0]).where(query.whereclause)).one() if query.whereclause else session.exec(select(func.count(Alumni.alumni_code))).one()
    
    # Apply sorting
    sort_order_desc = sort_order.lower() == "desc"
    if sort_by.lower() == "first_name":
        query = query.order_by(Alumni.first_name.desc() if sort_order_desc else Alumni.first_name)
    elif sort_by.lower() == "last_name":
        query = query.order_by(Alumni.last_name.desc() if sort_order_desc else Alumni.last_name)
    elif sort_by.lower() == "created_at":
        query = query.order_by(Alumni.created_at.desc() if sort_order_desc else Alumni.created_at)
    else:  # default to alumni_id
        query = query.order_by(Alumni.alumni_id.desc() if sort_order_desc else Alumni.alumni_id)
    
    # Apply pagination
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    alumni_list = session.exec(query).all()
    
    result = []
    for alumni in alumni_list:
        # Get related student record (optional)
        student = None
        course = None
        if alumni.student_code:
            student = session.exec(
                select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
            ).first()
            
            # Get related course (only if student exists)
            if student:
                course = session.exec(
                    select(Course).where(Course.course_code == student.course_code)
                ).first()
        
        # Get related user (if exists)
        user = None
        if alumni.user_code:
            user = session.exec(
                select(User).where(User.user_code == alumni.user_code)
            ).first()
        
        # Build full profile
        profile = AlumniFullProfile(
            alumni_id=alumni.alumni_id,
            last_name=alumni.last_name,
            first_name=alumni.first_name,
            middle_name=alumni.middle_name,
            gender=alumni.gender,
            age=alumni.age,
            user_id=user.user_id if user else None,
            username=user.username if user else None,
            email=user.email if user else None,
            student_id=student.student_id if student else None,
            year_graduated=student.year_graduated if student else None,
            gwa=student.gwa if student else None,
            avg_prof_grade=student.avg_prof_grade if student else None,
            avg_elec_grade=student.avg_elec_grade if student else None,
            ojt_grade=student.ojt_grade if student else None,
            leadership_pos=student.leadership_pos if student else None,
            act_member_pos=student.act_member_pos if student else None,
            course_id=course.course_id if course else None,
            course_name=course.course_name if course else None,
            created_at=alumni.created_at,
            updated_at=alumni.updated_at
        )
        result.append(profile)
    
    # Calculate pagination metadata
    returned = len(result)
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
        code=SuccessCode.ALUMNI_LIST_RETRIEVED.value,
        message=f"Retrieved {returned} alumni",
        data={"alumni": result, "pagination": pagination}
    )


@router.get("/{alumni_id}", response_model=AlumniFullProfile)
def get_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Get specific alumni by alumni_id with full profile"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        log_error("alumni", "get_alumni", ErrorCode.ALUMNI_NOT_FOUND.value, f"Alumni {alumni_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.ALUMNI_NOT_FOUND.value,
                message="Alumni not found"
            ).model_dump(mode='json')
        )
    
    # Get related student record (optional)
    student = None
    course = None
    if alumni.student_code:
        student = session.exec(
            select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
        ).first()
        
        # Get related course (only if student exists)
        if student:
            course = session.exec(
                select(Course).where(Course.course_code == student.course_code)
            ).first()
    
    # Get related user (if exists)
    user = None
    if alumni.user_code:
        user = session.exec(
            select(User).where(User.user_code == alumni.user_code)
        ).first()
    
    # Build full profile
    return AlumniFullProfile(
        alumni_id=alumni.alumni_id,
        last_name=alumni.last_name,
        first_name=alumni.first_name,
        middle_name=alumni.middle_name,
        gender=alumni.gender,
        age=alumni.age,
        user_id=user.user_id if user else None,
        username=user.username if user else None,
        email=user.email if user else None,
        student_id=student.student_id if student else None,
        year_graduated=student.year_graduated if student else None,
        gwa=student.gwa if student else None,
        avg_prof_grade=student.avg_prof_grade if student else None,
        avg_elec_grade=student.avg_elec_grade if student else None,
        ojt_grade=student.ojt_grade if student else None,
        leadership_pos=student.leadership_pos if student else None,
        act_member_pos=student.act_member_pos if student else None,
        course_id=course.course_id if course else None,
        course_name=course.course_name if course else None,
        created_at=alumni.created_at,
        updated_at=alumni.updated_at
    )


@router.put("/{alumni_id}", response_model=AlumniFullProfile)
def update_alumni(
    alumni_id: str,
    alumni_data: AlumniUpdate,
    session: Session = Depends(get_session)
):
    """Update alumni information"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        log_error("alumni", "update_alumni", ErrorCode.ALUMNI_NOT_FOUND.value, f"Alumni {alumni_id} not found")
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    # Update only provided fields
    if alumni_data.last_name is not None:
        alumni.last_name = alumni_data.last_name
    if alumni_data.first_name is not None:
        alumni.first_name = alumni_data.first_name
    if alumni_data.middle_name is not None:
        alumni.middle_name = alumni_data.middle_name
    if alumni_data.gender is not None:
        alumni.gender = alumni_data.gender.upper()
    if alumni_data.age is not None:
        alumni.age = alumni_data.age
    
    session.add(alumni)
    
    try:
        session.commit()
        session.refresh(alumni)
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("alumni", "update_alumni", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.INVALID_INPUT.value,
                "message": "Update failed: Invalid input or duplicate entry"
            }
        )
    
    # Fetch full profile for response
    student = None
    course = None
    if alumni.student_code:
        student = session.exec(
            select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
        ).first()
        
        if student:
            course = session.exec(
                select(Course).where(Course.course_code == student.course_code)
            ).first()
    
    user = None
    if alumni.user_code:
        user = session.exec(
            select(User).where(User.user_code == alumni.user_code)
        ).first()
    
    return AlumniFullProfile(
        alumni_id=alumni.alumni_id,
        last_name=alumni.last_name,
        first_name=alumni.first_name,
        middle_name=alumni.middle_name,
        gender=alumni.gender,
        age=alumni.age,
        user_id=user.user_id if user else None,
        username=user.username if user else None,
        email=user.email if user else None,
        student_id=student.student_id if student else None,
        year_graduated=student.year_graduated if student else None,
        gwa=student.gwa if student else None,
        avg_prof_grade=student.avg_prof_grade if student else None,
        avg_elec_grade=student.avg_elec_grade if student else None,
        ojt_grade=student.ojt_grade if student else None,
        leadership_pos=student.leadership_pos if student else None,
        act_member_pos=student.act_member_pos if student else None,
        course_id=course.course_id if course else None,
        course_name=course.course_name if course else None,
        created_at=alumni.created_at,
        updated_at=alumni.updated_at
    )


@router.delete("/{alumni_id}")
def delete_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Delete an alumni record"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        log_error("alumni", "delete_alumni", ErrorCode.ALUMNI_NOT_FOUND.value, f"Alumni {alumni_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.ALUMNI_NOT_FOUND.value,
                message="Alumni not found"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(alumni)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.ALUMNI_DELETED.value,
            message=f"Alumni {alumni_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("alumni", "delete_alumni", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Delete failed: Constraint violation or invalid operation"
            ).model_dump(mode='json')
        )
