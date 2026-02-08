from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.users import User, UserCreate, UserUpdate, UserPublic, UserType, SuccessResponse
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from models.pagination import PaginatedResponse, PaginationMetadata
from utils.auth import verify_password
from utils.logging import log_error, log_integrity_error, log_auth_error
from datetime import datetime

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


@router.post("")
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
        password=user_data.password,  # Already hashed by validator
        user_type=user_data.user_type
    )
    session.add(new_user)
    
    try:
        session.commit()
        session.refresh(new_user)
        return StandardResponse(
            success=True,
            code=SuccessCode.USER_CREATED.value,
            message=f"User {user_id} created successfully",
            data=UserPublic.model_validate(new_user)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        # Check which field caused the violation by looking at constraint name
        if "ix_users_email" in error_str or "users_email_key" in error_str:
            log_integrity_error("users", "create_user", ErrorCode.DUPLICATE_EMAIL.value, "Email already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_EMAIL.value,
                    message="Email already in use"
                ).model_dump(mode='json')
            )
        elif "ix_users_username" in error_str or "users_username_key" in error_str:
            log_integrity_error("users", "create_user", ErrorCode.DUPLICATE_USERNAME.value, "Username already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_USERNAME.value,
                    message="Username already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("users", "create_user", ErrorCode.INVALID_INPUT.value, "User creation failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="User with these details already exists"
                ).model_dump(mode='json')
            )


@router.get("")
def get_all_users(
    limit: int = Query(10, ge=0, description="Records per page (0 = all records)"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    search: str = Query(None, description="Search by username or email"),
    user_type: str = Query(None, description="Filter by user type (USER, STAFF, ADMIN)"),
    sort_by: str = Query("user_id", description="Sort by field (user_id, username, email, created_at)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    session: Session = Depends(get_session)
):
    """Get all users with filtering, searching, and sorting"""
    # Build query
    query = select(User)
    
    # Apply search filter
    if search:
        search_like = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_like)) | (User.email.ilike(search_like))
        )
    
    # Apply user_type filter
    if user_type:
        query = query.where(User.user_type == user_type.upper())
    
    # Get total count after filters
    total = session.exec(select(func.count(User.user_code)).select_from(query.froms[0]).where(query.whereclause)).one() if query.whereclause else session.exec(select(func.count(User.user_code))).one()
    
    # Apply sorting
    sort_order_desc = sort_order.lower() == "desc"
    if sort_by.lower() == "username":
        query = query.order_by(User.username.desc() if sort_order_desc else User.username)
    elif sort_by.lower() == "email":
        query = query.order_by(User.email.desc() if sort_order_desc else User.email)
    elif sort_by.lower() == "created_at":
        query = query.order_by(User.created_at.desc() if sort_order_desc else User.created_at)
    else:  # default to user_id
        query = query.order_by(User.user_id.desc() if sort_order_desc else User.user_id)
    
    # Apply pagination
    if limit > 0:
        query = query.offset(offset).limit(limit)
    
    users = session.exec(query).all()
    
    # Convert User objects to UserPublic
    public_users = [UserPublic.model_validate(user) for user in users]
    
    # Calculate pagination metadata
    returned = len(users)
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
        code=SuccessCode.USERS_RETRIEVED.value,
        message=f"Retrieved {returned} users",
        data={"users": public_users, "pagination": pagination}
    )


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: str, session: Session = Depends(get_session)):
    """Get a specific user by user_id"""
    user = session.exec(
        select(User).where(User.user_id == user_id.upper())
    ).first()
    
    if not user:
        log_error("users", "get_user", ErrorCode.USER_NOT_FOUND.value, f"User {user_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.USER_NOT_FOUND.value,
                message="User not found"
            ).model_dump(mode='json')
        )
    return user


@router.put("/{user_id}")
def update_user(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_session)
):
    """Update a user's information. If changing password, current_password is required."""
    user = session.exec(
        select(User).where(User.user_id == user_id.upper())
    ).first()
    
    if not user:
        log_error("users", "update_user", ErrorCode.USER_NOT_FOUND.value, f"User {user_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.USER_NOT_FOUND.value,
                message="User not found"
            ).model_dump(mode='json')
        )
    
    # If password change is requested, verify current password
    if user_data.password is not None:
        if user_data.current_password is None:
            log_error("users", "update_user", ErrorCode.MISSING_CURRENT_PASSWORD.value, "Current password required but not provided")
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.MISSING_CURRENT_PASSWORD.value,
                    message="Current password required to change password"
                ).model_dump(mode='json')
            )
        
        # Verify the current password
        if not verify_password(user_data.current_password, user.password):
            log_auth_error("update_user", user.username, ErrorCode.INVALID_CREDENTIALS.value, "Incorrect current password")
            raise HTTPException(
                status_code=401,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_CREDENTIALS.value,
                    message="Current password is incorrect"
                ).model_dump(mode='json')
            )
    
    # Update only provided fields
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password is not None:
        # Password is already hashed by validator in UserUpdate
        user.password = user_data.password
    
    session.add(user)
    
    try:
        session.commit()
        
        # Return user-friendly success message
        return StandardResponse(
            success=True,
            code=SuccessCode.USER_UPDATED.value,
            message=f"User {user.user_id} updated successfully",
            data=UserPublic.model_validate(user)
        )
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        if "ix_users_email" in error_str or "users_email_key" in error_str:
            log_integrity_error("users", "update_user", ErrorCode.DUPLICATE_EMAIL.value, "Email already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_EMAIL.value,
                    message="Email already in use"
                ).model_dump(mode='json')
            )
        elif "ix_users_username" in error_str or "users_username_key" in error_str:
            log_integrity_error("users", "update_user", ErrorCode.DUPLICATE_USERNAME.value, "Username already in use", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.DUPLICATE_USERNAME.value,
                    message="Username already in use"
                ).model_dump(mode='json')
            )
        else:
            log_integrity_error("users", "update_user", ErrorCode.INVALID_INPUT.value, "Update failed", str(e))
            raise HTTPException(
                status_code=400,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_INPUT.value,
                    message="Update failed: Duplicate entry"
                ).model_dump(mode='json')
            )


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    password: str,
    session: Session = Depends(get_session)
):
    """Delete a user account (requires password confirmation)"""
    user = session.exec(
        select(User).where(User.user_id == user_id.upper())
    ).first()
    
    if not user:
        log_error("users", "delete_user", ErrorCode.USER_NOT_FOUND.value, f"User {user_id} not found")
        raise HTTPException(
            status_code=404,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.USER_NOT_FOUND.value,
                message="User not found"
            ).model_dump(mode='json')
        )
    
    # Verify password before deletion
    if not verify_password(password, user.password):
        log_auth_error("delete_user", user.username, ErrorCode.INVALID_CREDENTIALS.value, "Incorrect password on deletion")
        raise HTTPException(
            status_code=401,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_CREDENTIALS.value,
                message="Password is incorrect"
            ).model_dump(mode='json')
        )
    
    try:
        session.delete(user)
        session.commit()
        return StandardResponse(
            success=True,
            code=SuccessCode.USER_DELETED.value,
            message=f"User {user_id} deleted successfully"
        )
    except IntegrityError as e:
        session.rollback()
        log_integrity_error("users", "delete_user", ErrorCode.INVALID_INPUT.value, "Delete failed", str(e))
        raise HTTPException(
            status_code=400,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_INPUT.value,
                message="Delete failed: Constraint violation or invalid operation"
            ).model_dump(mode='json')
        )
