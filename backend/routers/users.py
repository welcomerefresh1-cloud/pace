from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.users import User, UserCreate, UserPublic, UserType
from models.errors import ErrorCode, ErrorResponse

router = APIRouter(prefix="/users", tags=["users"])


def generate_user_id(user_type: UserType, session: Session) -> str:
    """Generate user_id based on user_type with auto-increment"""
    prefix = user_type.value  # USER, STAFF, or ADMIN
    
    # Find the last user of this type
    last_user = session.exec(
        select(User).where(User.user_type == user_type).order_by(User.user_id.desc())
    ).first()
    
    if last_user:
        # Extract number and increment
        last_num = int(last_user.user_id.split("-")[1])
        new_num = last_num + 1
    else:
        # Start from 1 if no users of this type exist
        new_num = 1
    
    return f"{prefix}-{new_num:06d}"  # USER-000001, STAFF-000001, ADMIN-000001


@router.post("", response_model=UserPublic)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user account"""
    # Generate user_id based on user_type
    user_id = generate_user_id(user_data.user_type, session)
    
    # Create user with generated ID
    new_user = User(
        user_id=user_id,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,  # TODO: Hash this
        user_type=user_data.user_type
    )
    session.add(new_user)
    
    try:
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        # Check which field caused the violation by looking at constraint name
        if "ix_users_email" in error_str or "users_email_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_EMAIL.value,
                    "message": "Email already in use"
                }
            )
        elif "ix_users_username" in error_str or "users_username_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_USERNAME.value,
                    "message": "Username already in use"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.INVALID_INPUT.value,
                    "message": "User with these details already exists"
                }
            )


@router.get("", response_model=list[UserPublic])
def get_all_users(session: Session = Depends(get_session)):
    """Get all users"""
    users = session.exec(select(User)).all()
    return users
