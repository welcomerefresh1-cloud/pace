from typing import Optional, List
from sqlmodel import SQLModel
from pydantic import field_validator, BaseModel, Field
import re
from utils.auth import hash_password


class CompleteAlumniRegistration(SQLModel):
    
    # User fields (user_id is auto-generated, user_type is always USER)
    username: str
    email: str
    password: str
    
    # Alumni fields (alumni_id is auto-generated)
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    age: int
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()  # Store emails in lowercase
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength, then hash"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return hash_password(v)  # Hash after validation passes


class CompleteAlumniResponse(SQLModel):
    user_id: str
    alumni_id: str
    message: str


# Bulk alumni registration models

# Safe display models (exclude passwords from responses)
class BulkAlumniRegistrationItemSafeDisplay(BaseModel):
    """Alumni registration data for response (no password included)"""
    username: str
    email: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    age: int


class BulkAlumniRegistrationItem(BaseModel):
    """Individual alumni registration data for bulk registration (input model)"""
    username: str
    email: str
    password: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    age: int
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v  # Return unhashed for now, hash during actual registration


class BulkAlumniRegistrationResult(BaseModel):
    """Individual item result from bulk alumni registration"""
    index: int
    item: BulkAlumniRegistrationItemSafeDisplay
    success: bool
    code: str
    message: str
    user_id: Optional[str] = None
    alumni_id: Optional[str] = None


class BulkAlumniRegister(BaseModel):
    """Bulk alumni registration request"""
    items: List[BulkAlumniRegistrationItem] = Field(..., min_items=1, max_items=100, description="List of alumni to register (1-100 items)")


class BulkAlumniRegisterResponse(BaseModel):
    """Bulk alumni registration response"""
    total_items: int
    successful: int
    failed: int
    results: List[BulkAlumniRegistrationResult]


# Bulk alumni update models
class BulkAlumniUpdateItem(BaseModel):
    """Alumni update item in bulk request"""
    alumni_id: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None


class BulkAlumniUpdateResult(BaseModel):
    """Individual item result from bulk alumni update operation"""
    index: int
    alumni_id: str
    success: bool
    code: str
    message: str
    data: Optional[dict] = None  # Full profile if successful


class BulkAlumniUpdate(BaseModel):
    """Bulk alumni update request"""
    items: List[BulkAlumniUpdateItem] = Field(..., min_items=1, max_items=100, description="List of alumni to update (1-100 items)")


class BulkAlumniUpdateResponse(BaseModel):
    """Bulk alumni update response"""
    total_items: int
    successful: int
    failed: int
    results: List[BulkAlumniUpdateResult]


# Bulk alumni delete models
class BulkAlumniDeleteResult(BaseModel):
    """Individual item result from bulk alumni delete operation"""
    index: int
    alumni_id: str
    success: bool
    code: str
    message: str


class BulkAlumniDelete(BaseModel):
    """Bulk alumni delete request"""
    ids: List[str] = Field(..., min_items=1, max_items=100, description="List of alumni IDs to delete (1-100 items)")


class BulkAlumniDeleteResponse(BaseModel):
    """Bulk alumni delete response"""
    total_items: int
    successful: int
    failed: int
    results: List[BulkAlumniDeleteResult]
