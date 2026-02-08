from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.college_dept import CollegeDept, CollegeDeptCreate, CollegeDeptUpdate, CollegeDeptPublic
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginationMetadata
from utils.logging import log_error, log_integrity_error

router = APIRouter(prefix="/college-depts", tags=["college-depts"])


def generate_college_dept_id(session: Session) -> str:
    """Generate college_dept_id with auto-increment"""
    last_college_dept = session.exec(
        select(CollegeDept).order_by(CollegeDept.college_dept_id.desc())
    ).first()
    
    if last_college_dept and last_college_dept.college_dept_id.startswith("CLG-"):
        last_num = int(last_college_dept.college_dept_id.split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f"CLG-{new_num:06d}"  # Format: CLG-000001


@router.post("")
def create_college_dept(
    college_dept_data: CollegeDeptCreate,
    session: Session = Depends(get_session)
):
    """Create a new college department"""
    # Generate college_dept_id
    college_dept_id = generate_college_dept_id(session)
    
    # Create college dept
    college_dept_dict = college_dept_data.model_dump()
    college_dept_dict["college_dept_id"] = college_dept_id
    
    new_college_dept = CollegeDept.model_validate(college_dept_dict)
    session.add(new_college_dept)
    
    try:
        session.commit()
        session.refresh(new_college_dept)
        return StandardResponse(
            success=True,
            code=SuccessCode.COLLEGE_DEPT_CREATED.value,
            message="College department created successfully",
            data=CollegeDeptPublic.model_validate(new_college_dept)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_college_depts_college_dept_id" in error_str or "college_depts_college_dept_id_key" in error_str:
            log_integrity_error("college_depts", "create_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_ID.value, "College department ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_ID.value,
                    message="College department ID already in use"
                ).model_dump(mode='json')
            )
        elif "ix_college_depts_college_dept_abbv" in error_str or "college_depts_college_dept_abbv_key" in error_str:
            log_integrity_error("college_depts", "create_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value, "College department abbreviation already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value,
                    message="College department abbreviation already in use"
                ).model_dump(mode='json')
            )
        elif "ix_college_depts_college_dept_name" in error_str or "college_depts_college_dept_name_key" in error_str:
            log_integrity_error("college_depts", "create_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value, "College department name already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value,
                    message="College department name already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("college_depts", "create_college_dept", ErrorCode.INVALID_INPUT.value, "College department creation failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="College department with these details already exists"
                ).model_dump(mode='json')
            )


@router.get("")
def get_all_college_depts(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    session: Session = Depends(get_session)
):
    """Get all college departments with pagination"""
    # Get total count
    total = session.exec(select(func.count(CollegeDept.college_dept_code))).one()
    
    # Get paginated data
    query = select(CollegeDept)
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    college_depts = session.exec(query).all()
    
    # Calculate pagination metadata
    returned = len(college_depts)
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
        code=SuccessCode.COLLEGE_DEPTS_RETRIEVED.value,
        message=f"Retrieved {returned} college departments",
        data={"college_depts": [CollegeDeptPublic.model_validate(d) for d in college_depts], "pagination": pagination}
    )


@router.get("/{college_dept_id}", response_model=CollegeDeptPublic)
def get_college_dept(college_dept_id: str, session: Session = Depends(get_session)):
    """Get a specific college department by college_dept_id"""
    college_dept = session.exec(
        select(CollegeDept).where(CollegeDept.college_dept_id == college_dept_id.upper())
    ).first()
    
    if not college_dept:
        log_error("college_depts", "get_college_dept", ErrorCode.COLLEGE_DEPT_NOT_FOUND.value, f"College department {college_dept_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                message="College department not found"
            ).model_dump(mode='json')
        )
    return college_dept


@router.put("/{college_dept_id}")
def update_college_dept(
    college_dept_id: str,
    college_dept_data: CollegeDeptUpdate,
    session: Session = Depends(get_session)
):
    """Update college department information"""
    college_dept = session.exec(
        select(CollegeDept).where(CollegeDept.college_dept_id == college_dept_id.upper())
    ).first()
    
    if not college_dept:
        log_error("college_depts", "update_college_dept", ErrorCode.COLLEGE_DEPT_NOT_FOUND.value, f"College department {college_dept_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                message="College department not found"
            ).model_dump(mode='json')
        )
    
    # Update only provided fields
    if college_dept_data.college_dept_abbv is not None:
        college_dept.college_dept_abbv = college_dept_data.college_dept_abbv
    if college_dept_data.college_dept_name is not None:
        college_dept.college_dept_name = college_dept_data.college_dept_name
    if college_dept_data.college_dept_desc is not None:
        college_dept.college_dept_desc = college_dept_data.college_dept_desc
    
    # Update the updated_at timestamp
    from datetime import datetime, timezone
    college_dept.updated_at = datetime.now(timezone.utc)
    
    session.add(college_dept)
    
    try:
        session.commit()
        session.refresh(college_dept)
        return StandardResponse(
            success=True,
            code=SuccessCode.COLLEGE_DEPT_UPDATED.value,
            message="College department updated successfully",
            data=CollegeDeptPublic.model_validate(college_dept)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_college_depts_college_dept_id" in error_str or "college_depts_college_dept_id_key" in error_str:
            log_integrity_error("college_depts", "update_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_ID.value, "College department ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_ID.value,
                    message="College department ID already in use"
                ).model_dump(mode='json')
            )
        elif "ix_college_depts_college_dept_abbv" in error_str or "college_depts_college_dept_abbv_key" in error_str:
            log_integrity_error("college_depts", "update_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value, "College department abbreviation already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value,
                    message="College department abbreviation already in use"
                ).model_dump(mode='json')
            )
        elif "ix_college_depts_college_dept_name" in error_str or "college_depts_college_dept_name_key" in error_str:
            log_integrity_error("college_depts", "update_college_dept", ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value, "College department name already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value,
                    message="College department name already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("college_depts", "update_college_dept", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Update failed: Invalid input or constraint violation"
                ).model_dump(mode='json')
            )


@router.delete("/{college_dept_id}")
def delete_college_dept(college_dept_id: str, session: Session = Depends(get_session)):
    """Delete a college department"""
    college_dept = session.exec(
        select(CollegeDept).where(CollegeDept.college_dept_id == college_dept_id.upper())
    ).first()
    
    if not college_dept:
        log_error("college_depts", "delete_college_dept", ErrorCode.COLLEGE_DEPT_NOT_FOUND.value, f"College department {college_dept_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                message="College department not found"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(college_dept)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.COLLEGE_DEPT_DELETED.value,
            message=f"College department {college_dept_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("college_depts", "delete_college_dept", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Delete failed: Constraint violation or invalid operation"
            ).model_dump(mode='json')
        )
