from enum import Enum
from sqlmodel import SQLModel

# DEPRECATED

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
    
    # Authentication/Authorization errors
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    MISSING_CURRENT_PASSWORD = "MISSING_CURRENT_PASSWORD"
    
    # Validation errors
    INVALID_INPUT = "INVALID_INPUT"
    
    # Generic errors
    REGISTRATION_FAILED = "REGISTRATION_FAILED"


class ErrorResponse(SQLModel):
    """Standardized error response"""
    code: ErrorCode
    message: str
