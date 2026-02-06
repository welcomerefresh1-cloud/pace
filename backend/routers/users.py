from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from models.users import User, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserPublic)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user account"""
    # TODO: Hash password before storing (add bcrypt later)
    new_user = User.model_validate(user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("", response_model=list[UserPublic])
def get_all_users(session: Session = Depends(get_session)):
    """Get all users"""
    users = session.exec(select(User)).all()
    return users
