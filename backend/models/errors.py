from enum import Enum
from sqlmodel import SQLModel


class ErrorCode(str, Enum):
    """Custom error codes for API responses"""
    # Duplicate/Conflict errors
    DUPLICATE_EMAIL = "DUPLICATE_EMAIL"
    DUPLICATE_USERNAME = "DUPLICATE_USERNAME"
    DUPLICATE_STUDENT_ID = "DUPLICATE_STUDENT_ID"
    DUPLICATE_ALUMNI_ID = "DUPLICATE_ALUMNI_ID"
    DUPLICATE_DEGREE_ID = "DUPLICATE_DEGREE_ID"
    ALUMNI_ALREADY_HAS_STUDENT_RECORD = "ALUMNI_ALREADY_HAS_STUDENT_RECORD"
    
    # Not found errors
    DEGREE_NOT_FOUND = "DEGREE_NOT_FOUND"
    ALUMNI_NOT_FOUND = "ALUMNI_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    STUDENT_RECORD_NOT_FOUND = "STUDENT_RECORD_NOT_FOUND"
    
    # Validation errors
    INVALID_INPUT = "INVALID_INPUT"
    
    # Generic errors
    REGISTRATION_FAILED = "REGISTRATION_FAILED"


class ErrorResponse(SQLModel):
    """Standardized error response"""
    code: ErrorCode
    message: str
