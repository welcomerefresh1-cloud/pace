from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.college_dept import (
    CollegeDept, CollegeDeptCreate, CollegeDeptUpdate, CollegeDeptPublic,
    CollegeDeptBulkCreate, CollegeDeptBulkCreateResponse, CollegeDeptBulkCreateItem,
    CollegeDeptBulkUpdate, CollegeDeptBulkUpdateResponse, CollegeDeptBulkUpdateResult,
    CollegeDeptBulkDelete, CollegeDeptBulkDeleteResponse, CollegeDeptBulkDeleteResult
)
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


@router.post("/bulk")
def bulk_create_college_depts(
    bulk_data: CollegeDeptBulkCreate,
    session: Session = Depends(get_session)
):
    """Bulk create college departments"""
    results = []
    successful_count = 0
    failed_count = 0
    
    for index, college_dept_item in enumerate(bulk_data.items):
        try:
            # Generate college_dept_id
            college_dept_id = generate_college_dept_id(session)
            
            # Create college dept
            college_dept_dict = college_dept_item.model_dump()
            college_dept_dict["college_dept_id"] = college_dept_id
            
            new_college_dept = CollegeDept.model_validate(college_dept_dict)
            session.add(new_college_dept)
            session.flush()  # Flush to get the ID but don't commit yet
            session.refresh(new_college_dept)
            
            # Record successful creation
            results.append(CollegeDeptBulkCreateItem(
                index=index,
                item=college_dept_item,
                success=True,
                code=SuccessCode.COLLEGE_DEPT_CREATED.value,
                message="College department created successfully",
                data=CollegeDeptPublic.model_validate(new_college_dept)
            ))
            successful_count += 1
        
        except IntegrityError as e:
            session.rollback()
            error_str = str(e).lower()
            
            if "ix_college_depts_college_dept_abbv" in error_str or "college_depts_college_dept_abbv_key" in error_str:
                error_code = ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value
                error_msg = f"College department abbreviation '{college_dept_item.college_dept_abbv}' already exists"
            elif "ix_college_depts_college_dept_name" in error_str or "college_depts_college_dept_name_key" in error_str:
                error_code = ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value
                error_msg = f"College department name '{college_dept_item.college_dept_name}' already exists"
            else:
                error_code = ErrorCode.INVALID_INPUT.value
                error_msg = "College department creation failed due to constraint violation"
            
            results.append(CollegeDeptBulkCreateItem(
                index=index,
                item=college_dept_item,
                success=False,
                code=error_code,
                message=error_msg,
                data=None
            ))
            failed_count += 1
        
        except ValueError as e:
            error_msg = str(e)
            error_code = ErrorCode.INVALID_INPUT.value
            
            results.append(CollegeDeptBulkCreateItem(
                index=index,
                item=college_dept_item,
                success=False,
                code=error_code,
                message=error_msg,
                data=None
            ))
            failed_count += 1
    
    # Commit all successful operations
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Bulk create operation failed during commit"
            ).model_dump(mode='json')
        )
    
    bulk_response = CollegeDeptBulkCreateResponse(
        total_items=len(bulk_data.items),
        successful=successful_count,
        failed=failed_count,
        results=results
    )
    
    return StandardResponse(
        success=failed_count == 0,  # True only if all succeeded
        code=SuccessCode.COLLEGE_DEPTS_BULK_CREATED.value,
        message=f"Bulk create completed: {successful_count} successful, {failed_count} failed",
        data=bulk_response
    )


@router.put("/bulk")
def bulk_update_college_depts(
    bulk_data: CollegeDeptBulkUpdate,
    session: Session = Depends(get_session)
):
    """Bulk update college departments"""
    results = []
    successful_count = 0
    failed_count = 0
    
    for index, update_item in enumerate(bulk_data.items):
        try:
            # Find college department
            college_dept = session.exec(
                select(CollegeDept).where(CollegeDept.college_dept_id == update_item.college_dept_id.upper())
            ).first()
            
            if not college_dept:
                results.append(CollegeDeptBulkUpdateResult(
                    index=index,
                    college_dept_id=update_item.college_dept_id,
                    success=False,
                    code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                    message=f"College department '{update_item.college_dept_id}' not found",
                    data=None
                ))
                failed_count += 1
                continue
            
            # Update only provided fields
            if update_item.college_dept_abbv is not None:
                college_dept.college_dept_abbv = update_item.college_dept_abbv
            if update_item.college_dept_name is not None:
                college_dept.college_dept_name = update_item.college_dept_name
            if update_item.college_dept_desc is not None:
                college_dept.college_dept_desc = update_item.college_dept_desc
            
            # Update timestamp
            from datetime import datetime, timezone
            college_dept.updated_at = datetime.now(timezone.utc)
            
            session.add(college_dept)
            session.flush()
            session.refresh(college_dept)
            
            # Record successful update
            results.append(CollegeDeptBulkUpdateResult(
                index=index,
                college_dept_id=update_item.college_dept_id,
                success=True,
                code=SuccessCode.COLLEGE_DEPT_UPDATED.value,
                message="College department updated successfully",
                data=CollegeDeptPublic.model_validate(college_dept)
            ))
            successful_count += 1
        
        except IntegrityError as e:
            session.rollback()
            error_str = str(e).lower()
            
            if "ix_college_depts_college_dept_abbv" in error_str or "college_depts_college_dept_abbv_key" in error_str:
                error_code = ErrorCode.DUPLICATE_COLLEGE_DEPT_ABBV.value
                error_msg = f"College department abbreviation already in use"
            elif "ix_college_depts_college_dept_name" in error_str or "college_depts_college_dept_name_key" in error_str:
                error_code = ErrorCode.DUPLICATE_COLLEGE_DEPT_NAME.value
                error_msg = f"College department name already in use"
            else:
                error_code = ErrorCode.INVALID_INPUT.value
                error_msg = "Update failed due to constraint violation"
            
            results.append(CollegeDeptBulkUpdateResult(
                index=index,
                college_dept_id=update_item.college_dept_id,
                success=False,
                code=error_code,
                message=error_msg,
                data=None
            ))
            failed_count += 1
        
        except ValueError as e:
            error_msg = str(e)
            error_code = ErrorCode.INVALID_INPUT.value
            
            results.append(CollegeDeptBulkUpdateResult(
                index=index,
                college_dept_id=update_item.college_dept_id,
                success=False,
                code=error_code,
                message=error_msg,
                data=None
            ))
            failed_count += 1
    
    # Commit all successful operations
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Bulk update operation failed during commit"
            ).model_dump(mode='json')
        )
    
    bulk_response = CollegeDeptBulkUpdateResponse(
        total_items=len(bulk_data.items),
        successful=successful_count,
        failed=failed_count,
        results=results
    )
    
    return StandardResponse(
        success=failed_count == 0,
        code=SuccessCode.COLLEGE_DEPTS_BULK_UPDATED.value,
        message=f"Bulk update completed: {successful_count} successful, {failed_count} failed",
        data=bulk_response
    )


@router.delete("/bulk")
def bulk_delete_college_depts(
    bulk_data: CollegeDeptBulkDelete,
    session: Session = Depends(get_session)
):
    """Bulk delete college departments"""
    results = []
    successful_count = 0
    failed_count = 0
    
    for index, college_dept_id in enumerate(bulk_data.ids):
        try:
            # Find college department
            college_dept = session.exec(
                select(CollegeDept).where(CollegeDept.college_dept_id == college_dept_id.upper())
            ).first()
            
            if not college_dept:
                results.append(CollegeDeptBulkDeleteResult(
                    index=index,
                    college_dept_id=college_dept_id,
                    success=False,
                    code=ErrorCode.COLLEGE_DEPT_NOT_FOUND.value,
                    message=f"College department '{college_dept_id}' not found"
                ))
                failed_count += 1
                continue
            
            # Delete college department
            session.delete(college_dept)
            session.flush()
            
            # Record successful deletion
            results.append(CollegeDeptBulkDeleteResult(
                index=index,
                college_dept_id=college_dept_id,
                success=True,
                code=SuccessCode.COLLEGE_DEPT_DELETED.value,
                message="College department deleted successfully"
            ))
            successful_count += 1
        
        except IntegrityError as e:
            session.rollback()
            error_code = ErrorCode.INVALID_INPUT.value
            error_msg = "Delete failed: Constraint violation or related data exists"
            
            results.append(CollegeDeptBulkDeleteResult(
                index=index,
                college_dept_id=college_dept_id,
                success=False,
                code=error_code,
                message=error_msg
            ))
            failed_count += 1
        
        except Exception as e:
            session.rollback()
            error_code = ErrorCode.INVALID_INPUT.value
            error_msg = f"Delete failed: {str(e)}"
            
            results.append(CollegeDeptBulkDeleteResult(
                index=index,
                college_dept_id=college_dept_id,
                success=False,
                code=error_code,
                message=error_msg
            ))
            failed_count += 1
    
    # Commit all successful operations
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Bulk delete operation failed during commit"
            ).model_dump(mode='json')
        )
    
    bulk_response = CollegeDeptBulkDeleteResponse(
        total_items=len(bulk_data.ids),
        successful=successful_count,
        failed=failed_count,
        results=results
    )
    
    return StandardResponse(
        success=failed_count == 0,
        code=SuccessCode.COLLEGE_DEPTS_BULK_DELETED.value,
        message=f"Bulk delete completed: {successful_count} successful, {failed_count} failed",
        data=bulk_response
    )


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
    search: str = Query(None, description="Search by abbreviation or name"),
    sort_by: str = Query("college_dept_id", description="Sort by field (college_dept_id, college_dept_abbv, college_dept_name)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    session: Session = Depends(get_session)
):
    """Get all college departments with filtering, searching, and sorting"""
    # Build query
    query = select(CollegeDept)
    
    # Apply search filter
    if search:
        search_like = f"%{search}%"
        query = query.where(
            (CollegeDept.college_dept_abbv.ilike(search_like)) | 
            (CollegeDept.college_dept_name.ilike(search_like)) |
            (CollegeDept.college_dept_desc.ilike(search_like))
        )
    
    # Get total count after filters
    total = session.exec(select(func.count(CollegeDept.college_dept_code)).select_from(query.froms[0]).where(query.whereclause)).one() if query.whereclause else session.exec(select(func.count(CollegeDept.college_dept_code))).one()
    
    # Apply sorting
    sort_order_desc = sort_order.lower() == "desc"
    if sort_by.lower() == "college_dept_abbv":
        query = query.order_by(CollegeDept.college_dept_abbv.desc() if sort_order_desc else CollegeDept.college_dept_abbv)
    elif sort_by.lower() == "college_dept_name":
        query = query.order_by(CollegeDept.college_dept_name.desc() if sort_order_desc else CollegeDept.college_dept_name)
    else:  # default to college_dept_id
        query = query.order_by(CollegeDept.college_dept_id.desc() if sort_order_desc else CollegeDept.college_dept_id)
    
    # Apply pagination
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


@router.get("/{college_dept_id}")
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
    return StandardResponse(
        success=True,
        code=SuccessCode.COLLEGE_DEPT_RETRIEVED.value,
        message=f"College department {college_dept_id} retrieved successfully",
        data=CollegeDeptPublic.model_validate(college_dept)
    )


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
