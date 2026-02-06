from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.degrees import Degree, DegreeCreate, DegreePublic
from models.errors import ErrorCode

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
        return new_degree
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_degrees_degree_id" in error_str or "degrees_degree_id_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_DEGREE_ID.value,
                    "message": "Degree ID already in use"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.INVALID_INPUT.value,
                    "message": "Degree with these details already exists"
                }
            )


@router.get("", response_model=list[DegreePublic])
def get_all_degrees(session: Session = Depends(get_session)):
    """Get all degree programs"""
    degrees = session.exec(select(Degree)).all()
    return degrees
