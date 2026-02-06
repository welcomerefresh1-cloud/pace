from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from core.database import get_session
from models.users import User
from models.auth import LoginRequest, TokenResponse, CurrentUser
from models.response_codes import ErrorCode, SuccessCode, StandardResponse
from utils.auth import verify_password, create_access_token, decode_access_token
from utils.logging import log_auth_error

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Login endpoint - authenticate user with username/password and return JWT token
    
    Returns:
        - access_token: JWT token for authenticated requests
        - token_type: Always "bearer"
        - user_id: The authenticated user's ID
        - user_type: The user's type (USER, STAFF, ADMIN)
    """
    # Find user by username
    user = session.exec(
        select(User).where(User.username == credentials.username)
    ).first()
    
    if not user:
        log_auth_error("login", credentials.username, ErrorCode.INVALID_CREDENTIALS.value, "Invalid username or password - user not found")
        raise HTTPException(
            status_code=401,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_CREDENTIALS.value,
                message="Invalid username or password"
            ).model_dump(mode='json')
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password):
        log_auth_error("login", credentials.username, ErrorCode.INVALID_CREDENTIALS.value, "Invalid username or password - incorrect password")
        raise HTTPException(
            status_code=401,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_CREDENTIALS.value,
                message="Invalid username or password"
            ).model_dump(mode='json')
        )
    
    # Create JWT token
    token = create_access_token(
        data={
            "user_id": user.user_id,
            "user_type": user.user_type.value,
            "user_code": str(user.user_code)
        }
    )
    
    return StandardResponse(
        success=True,
        code=SuccessCode.LOGIN_SUCCESSFUL.value,
        message="Login successful",
        data=TokenResponse(
            access_token=token,
            token_type="bearer",
            user_id=user.user_id,
            user_type=user.user_type.value
        )
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Dependency to extract and validate JWT token from Authorization header
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: CurrentUser = Depends(get_current_user)):
            return {"user": current_user.user_id}
    """
    token = credentials.credentials
    
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        user_type = payload.get("user_type")
        user_code = payload.get("user_code")
        
        if not user_id or not user_type:
            log_auth_error("get_current_user", "UNKNOWN", ErrorCode.INVALID_TOKEN.value, "Invalid token - missing user_id or user_type")
            raise HTTPException(
                status_code=401,
                detail=StandardResponse(
                    success=False,
                    code=ErrorCode.INVALID_TOKEN.value,
                    message="Invalid token"
                ).model_dump(mode='json')
            )
        
        return CurrentUser(
            user_id=user_id,
            user_type=user_type,
            user_code=user_code
        )
    except ValueError as e:
        log_auth_error("get_current_user", "UNKNOWN", ErrorCode.INVALID_TOKEN.value, f"Invalid token - {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=StandardResponse(
                success=False,
                code=ErrorCode.INVALID_TOKEN.value,
                message=str(e)
            ).model_dump(mode='json')
        )
