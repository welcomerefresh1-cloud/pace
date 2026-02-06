from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.degrees import Degree, DegreeCreate, DegreeUpdate, DegreePublic
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginatedResponse, PaginationMetadata
from utils.logging import log_error, log_integrity_error

router = APIRouter(prefix="/degrees", tags=["degrees"])


@router.post("", response_model=DegreePublic)
def create_degree(
    degree_data: DegreeCreate,
    session: Session = Depends(get_session)
):
    """Create a new degree program"""
    new_degree = Degree.model_validate(degree_data)
    session.add(new_degree)
    
    try:
        session.commit()
        session.refresh(new_degree)
        return StandardResponse(
            success=True,
            code=SuccessCode.DEGREE_CREATED.value,
            message="Degree created successfully",
            data=DegreePublic.model_validate(new_degree)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_degrees_degree_id" in error_str or "degrees_degree_id_key" in error_str:
            log_integrity_error("degrees", "create_degree", ErrorCode.DUPLICATE_DEGREE_ID.value, "Degree ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_DEGREE_ID.value,
                    message="Degree ID already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("degrees", "create_degree", ErrorCode.INVALID_INPUT.value, "Degree creation failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Degree with these details already exists"
                ).model_dump(mode='json')
            )


@router.get("")
def get_all_degrees(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    session: Session = Depends(get_session)
):
    """Get all degree programs with pagination"""
    # Get total count
    total = session.exec(select(func.count(Degree.degree_code))).one()
    
    # Get paginated data
    query = select(Degree)
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    degrees = session.exec(query).all()
    
    # Calculate pagination metadata
    returned = len(degrees)
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
        code=SuccessCode.DEGREES_RETRIEVED.value,
        message=f"Retrieved {returned} degrees",
        data={"degrees": [DegreePublic.model_validate(d) for d in degrees], "pagination": pagination}
    )


@router.get("/{degree_id}", response_model=DegreePublic)
def get_degree(degree_id: str, session: Session = Depends(get_session)):
    """Get a specific degree by degree_id"""
    degree = session.exec(
        select(Degree).where(Degree.degree_id == degree_id.upper())
    ).first()
    
    if not degree:
        log_error("degrees", "get_degree", ErrorCode.DEGREE_NOT_FOUND.value, f"Degree {degree_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.DEGREE_NOT_FOUND.value,
                message="Degree not found"
            ).model_dump(mode='json')
        )
    return degree


@router.put("/{degree_id}", response_model=DegreePublic)
def update_degree(
    degree_id: str,
    degree_data: DegreeUpdate,
    session: Session = Depends(get_session)
):
    """Update degree information"""
    degree = session.exec(
        select(Degree).where(Degree.degree_id == degree_id.upper())
    ).first()
    
    if not degree:
        log_error("degrees", "update_degree", ErrorCode.DEGREE_NOT_FOUND.value, f"Degree {degree_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.DEGREE_NOT_FOUND.value,
                message="Degree not found"
            ).model_dump(mode='json')
        )
    
    # Update only provided fields
    if degree_data.degree_name is not None:
        degree.degree_name = degree_data.degree_name
    
    session.add(degree)
    
    try:
        session.commit()
        session.refresh(degree)
        return StandardResponse(
            success=True,
            code=SuccessCode.DEGREE_UPDATED.value,
            message="Degree updated successfully",
            data=DegreePublic.model_validate(degree)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_degrees_degree_id" in error_str or "degrees_degree_id_key" in error_str:
            log_integrity_error("degrees", "update_degree", ErrorCode.DUPLICATE_DEGREE_ID.value, "Degree ID already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_DEGREE_ID.value,
                    message="Degree ID already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("degrees", "update_degree", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Update failed: Invalid input or constraint violation"
                ).model_dump(mode='json')
            )


@router.delete("/{degree_id}")
def delete_degree(degree_id: str, session: Session = Depends(get_session)):
    """Delete a degree program"""
    degree = session.exec(
        select(Degree).where(Degree.degree_id == degree_id.upper())
    ).first()
    
    if not degree:
        log_error("degrees", "delete_degree", ErrorCode.DEGREE_NOT_FOUND.value, f"Degree {degree_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.DEGREE_NOT_FOUND.value,
                message="Degree not found"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(degree)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.DEGREE_DELETED.value,
            message=f"Degree {degree_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("degrees", "delete_degree", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Delete failed: Constraint violation or invalid operation"
            ).model_dump(mode='json')
        )
