from typing import Optional
from sqlmodel import SQLModel
from pydantic import field_validator
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
