from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.courses import Course, CourseCreate, CourseUpdate, CoursePublic
from models.college_dept import CollegeDept
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginationMetadata
from utils.logging import log_error, log_integrity_error

router = APIRouter(prefix="/courses", tags=["courses"])


def generate_course_id(session: Session) -> str:
    """Generate course_id with auto-increment"""
    last_course = session.exec(
        select(Course).order_by(Course.course_id.desc())
    ).first()
    
    if last_course and last_course.course_id.startswith("CRS-"):
        last_num = int(last_course.course_id.split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f"CRS-{new_num:06d}"  # Format: CRS-000001


@router.post("")
def create_course(
    course_data: CourseCreate,
    session: Session = Depends(get_session)
):
    """Create a new course"""
    # Verify college department exists and get its code
    college_dept = session.exec(
        select(CollegeDept).where(CollegeDept.college_dept_abbv == course_data.college_dept_abbv.upper())
    ).first()
    
    if not college_dept:
        log_error("courses", "create_course", ErrorCode.COLLEGE_DEPT_NOT_FOUND.value, f"College department {course_data.college_dept_abbv} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                message="College department not found"
            ).model_dump(mode='json')
        )
    
    # Generate course_id
    course_id = generate_course_id(session)
    
    # Create course
    course_dict = course_data.model_dump(exclude={"college_dept_abbv"})
    course_dict["course_id"] = course_id
    course_dict["college_dept_code"] = college_dept.college_dept_code
    
    new_course = Course.model_validate(course_dict)
    session.add(new_course)
    
    try:
        session.commit()
        session.refresh(new_course)
        
        # Build response with college dept info
        return StandardResponse(
            success=True,
            code=SuccessCode.COURSE_CREATED.value,
            message="Course created successfully",
            data=CoursePublic(
                **new_course.model_dump(exclude={"college_dept_code"}),
                college_dept_id=college_dept.college_dept_id,
                college_dept_name=college_dept.college_dept_name
            )
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_courses_course_id" in error_str or "courses_course_id_key" in error_str:
            log_integrity_error("courses", "create_course", ErrorCode.DUPLICATE_COURSE_ID.value, "Course ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_ID.value,
                    message="Course ID already in use"
                ).model_dump(mode='json')
            )
        elif "ix_courses_course_abbv" in error_str or "courses_course_abbv_key" in error_str:
            log_integrity_error("courses", "create_course", ErrorCode.DUPLICATE_COURSE_ABBV.value, "Course abbreviation already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_ABBV.value,
                    message="Course abbreviation already in use"
                ).model_dump(mode='json')
            )
        elif "ix_courses_course_name" in error_str or "courses_course_name_key" in error_str:
            log_integrity_error("courses", "create_course", ErrorCode.DUPLICATE_COURSE_NAME.value, "Course name already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_NAME.value,
                    message="Course name already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("courses", "create_course", ErrorCode.INVALID_INPUT.value, "Course creation failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Course with these details already exists"
                ).model_dump(mode='json')
            )


@router.get("")
def get_all_courses(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    search: str = Query(None, description="Search by course abbreviation or name"),
    college_dept_abbv: str = Query(None, description="Filter by college department abbreviation"),
    sort_by: str = Query("course_id", description="Sort by field (course_id, course_abbv, course_name)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    session: Session = Depends(get_session)
):
    """Get all courses with filtering, searching, and sorting"""
    # Build query
    query = select(Course)
    
    # Apply search filter
    if search:
        search_like = f"%{search}%"
        query = query.where(
            (Course.course_abbv.ilike(search_like)) | 
            (Course.course_name.ilike(search_like)) |
            (Course.course_desc.ilike(search_like))
        )
    
    # Apply college_dept filter
    if college_dept_abbv:
        college_dept = session.exec(
            select(CollegeDept).where(CollegeDept.college_dept_abbv == college_dept_abbv.upper())
        ).first()
        if college_dept:
            query = query.where(Course.college_dept_code == college_dept.college_dept_code)
    
    # Get total count after filters
    total = session.exec(select(func.count(Course.course_code)).select_from(query.froms[0]).where(query.whereclause)).one() if query.whereclause else session.exec(select(func.count(Course.course_code))).one()
    
    # Apply sorting
    sort_order_desc = sort_order.lower() == "desc"
    if sort_by.lower() == "course_abbv":
        query = query.order_by(Course.course_abbv.desc() if sort_order_desc else Course.course_abbv)
    elif sort_by.lower() == "course_name":
        query = query.order_by(Course.course_name.desc() if sort_order_desc else Course.course_name)
    else:  # default to course_id
        query = query.order_by(Course.course_id.desc() if sort_order_desc else Course.course_id)
    
    # Apply pagination
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    courses = session.exec(query).all()
    
    # Build response with college dept info
    result = []
    for course in courses:
        college_dept = session.exec(
            select(CollegeDept).where(CollegeDept.college_dept_code == course.college_dept_code)
        ).first()
        
        result.append(CoursePublic(
            **course.model_dump(exclude={"college_dept_code"}),
            college_dept_id=college_dept.college_dept_id if college_dept else "UNKNOWN",
            college_dept_name=college_dept.college_dept_name if college_dept else "Unknown Department"
        ))
    
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
        code=SuccessCode.COURSES_RETRIEVED.value,
        message=f"Retrieved {returned} courses",
        data={"courses": result, "pagination": pagination}
    )


@router.get("/{course_id}")
def get_course(course_id: str, session: Session = Depends(get_session)):
    """Get a specific course by course_id"""
    course = session.exec(
        select(Course).where(Course.course_id == course_id.upper())
    ).first()
    
    if not course:
        log_error("courses", "get_course", ErrorCode.COURSE_NOT_FOUND.value, f"Course {course_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COURSE_NOT_FOUND.value,
                message="Course not found"
            ).model_dump(mode='json')
        )
    
    # Get college dept info
    college_dept = session.exec(
        select(CollegeDept).where(CollegeDept.college_dept_code == course.college_dept_code)
    ).first()
    
    return StandardResponse(
        success=True,
        code=SuccessCode.COURSE_RETRIEVED.value,
        message=f"Course {course_id} retrieved successfully",
        data=CoursePublic(
            **course.model_dump(exclude={"college_dept_code"}),
            college_dept_id=college_dept.college_dept_id if college_dept else "UNKNOWN",
            college_dept_name=college_dept.college_dept_name if college_dept else "Unknown Department"
        )
    )


@router.put("/{course_id}")
def update_course(
    course_id: str,
    course_data: CourseUpdate,
    session: Session = Depends(get_session)
):
    """Update course information"""
    course = session.exec(
        select(Course).where(Course.course_id == course_id.upper())
    ).first()
    
    if not course:
        log_error("courses", "update_course", ErrorCode.COURSE_NOT_FOUND.value, f"Course {course_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COURSE_NOT_FOUND.value,
                message="Course not found"
            ).model_dump(mode='json')
        )
    
    # If college_dept_abbv is provided, verify it exists and update
    if course_data.college_dept_abbv is not None:
        college_dept = session.exec(
            select(CollegeDept).where(CollegeDept.college_dept_abbv == course_data.college_dept_abbv.upper())
        ).first()
        
        if not college_dept:
            log_error("courses", "update_course", ErrorCode.COLLEGE_DEPT_NOT_FOUND.value, f"College department {course_data.college_dept_abbv} not found")
            raise HTTPException(
                status_code=404,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                    message="College department not found"
                ).model_dump(mode='json')
            )
        
        course.college_dept_code = college_dept.college_dept_code
    
    # Update only provided fields
    if course_data.course_abbv is not None:
        course.course_abbv = course_data.course_abbv
    if course_data.course_name is not None:
        course.course_name = course_data.course_name
    if course_data.course_desc is not None:
        course.course_desc = course_data.course_desc
    
    # Update the updated_at timestamp
    from datetime import datetime, timezone
    course.updated_at = datetime.now(timezone.utc)
    
    session.add(course)
    
    try:
        session.commit()
        session.refresh(course)
        
        # Get college dept info for response
        college_dept = session.exec(
            select(CollegeDept).where(CollegeDept.college_dept_code == course.college_dept_code)
        ).first()
        
        return StandardResponse(
            success=True,
            code=SuccessCode.COURSE_UPDATED.value,
            message="Course updated successfully",
            data=CoursePublic(
                **course.model_dump(exclude={"college_dept_code"}),
                college_dept_id=college_dept.college_dept_id if college_dept else "UNKNOWN",
                college_dept_name=college_dept.college_dept_name if college_dept else "Unknown Department"
            )
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_courses_course_id" in error_str or "courses_course_id_key" in error_str:
            log_integrity_error("courses", "update_course", ErrorCode.DUPLICATE_COURSE_ID.value, "Course ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_ID.value,
                    message="Course ID already in use"
                ).model_dump(mode='json')
            )
        elif "ix_courses_course_abbv" in error_str or "courses_course_abbv_key" in error_str:
            log_integrity_error("courses", "update_course", ErrorCode.DUPLICATE_COURSE_ABBV.value, "Course abbreviation already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_ABBV.value,
                    message="Course abbreviation already in use"
                ).model_dump(mode='json')
            )
        elif "ix_courses_course_name" in error_str or "courses_course_name_key" in error_str:
            log_integrity_error("courses", "update_course", ErrorCode.DUPLICATE_COURSE_NAME.value, "Course name already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COURSE_NAME.value,
                    message="Course name already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("courses", "update_course", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Update failed: Invalid input or constraint violation"
                ).model_dump(mode='json')
            )


@router.delete("/{course_id}")
def delete_course(course_id: str, session: Session = Depends(get_session)):
    """Delete a course"""
    course = session.exec(
        select(Course).where(Course.course_id == course_id.upper())
    ).first()
    
    if not course:
        log_error("courses", "delete_course", ErrorCode.COURSE_NOT_FOUND.value, f"Course {course_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COURSE_NOT_FOUND.value,
                message="Course not found"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(course)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.COURSE_DELETED.value,
            message=f"Course {course_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("courses", "delete_course", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Delete failed: Constraint violation or invalid operation"
            ).model_dump(mode='json')
        )
