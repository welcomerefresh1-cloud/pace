from enum import Enum
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Any
from datetime import datetime
from utils.timezone import get_current_time_gmt8


class ErrorCode(str, Enum):
    """Error codes for API responses"""
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


class SuccessCode(str, Enum):
    """Success codes for API responses"""
    # User operations
    USER_CREATED = "USER_CREATED"
    USER_UPDATED = "USER_UPDATED"
    USER_RETRIEVED = "USER_RETRIEVED"
    USERS_RETRIEVED = "USERS_RETRIEVED"
    USER_DELETED = "USER_DELETED"
    
    # Alumni operations
    ALUMNI_CREATED = "ALUMNI_CREATED"
    ALUMNI_RETRIEVED = "ALUMNI_RETRIEVED"
    ALUMNI_LIST_RETRIEVED = "ALUMNI_LIST_RETRIEVED"
    ALUMNI_UPDATED = "ALUMNI_UPDATED"
    ALUMNI_DELETED = "ALUMNI_DELETED"
    
    # Student record operations
    STUDENT_RECORD_CREATED = "STUDENT_RECORD_CREATED"
    STUDENT_RECORD_RETRIEVED = "STUDENT_RECORD_RETRIEVED"
    STUDENT_RECORDS_RETRIEVED = "STUDENT_RECORDS_RETRIEVED"
    STUDENT_RECORD_UPDATED = "STUDENT_RECORD_UPDATED"
    STUDENT_RECORD_DELETED = "STUDENT_RECORD_DELETED"
    
    # Degree operations
    DEGREE_CREATED = "DEGREE_CREATED"
    DEGREE_RETRIEVED = "DEGREE_RETRIEVED"
    DEGREES_RETRIEVED = "DEGREES_RETRIEVED"
    DEGREE_UPDATED = "DEGREE_UPDATED"
    DEGREE_DELETED = "DEGREE_DELETED"
    
    # Authentication
    LOGIN_SUCCESSFUL = "LOGIN_SUCCESSFUL"
    TOKEN_VALIDATED = "TOKEN_VALIDATED"


class StandardResponse(BaseModel):
    """Standardized response wrapper for all API endpoints"""
    success: bool = Field(..., description="Whether the operation was successful")
    code: str = Field(..., description="Response code (ErrorCode or SuccessCode)")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Any] = Field(default=None, description="Response data (optional)")
    timestamp: datetime = Field(default_factory=get_current_time_gmt8, description="Response timestamp in GMT+8")
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp as YYYY-MM-DD HH:MM:SS"""
        return value.strftime('%Y-%m-%d %H:%M:%S')


class ErrorResponse(BaseModel):
    """Standardized error response"""
    code: ErrorCode
    message: str
