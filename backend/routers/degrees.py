from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from models.degrees import Degree, DegreeCreate, DegreePublic

router = APIRouter(prefix="/degrees", tags=["degrees"])


@router.post("", response_model=DegreePublic)
def create_degree(
    degree_data: DegreeCreate,
    session: Session = Depends(get_session)
):
    """Create a new degree program"""
    new_degree = Degree.model_validate(degree_data)
    session.add(new_degree)
    session.commit()
    session.refresh(new_degree)
    return new_degree


@router.get("", response_model=list[DegreePublic])
def get_all_degrees(session: Session = Depends(get_session)):
    """Get all degree programs"""
    degrees = session.exec(select(Degree)).all()
    return degrees
