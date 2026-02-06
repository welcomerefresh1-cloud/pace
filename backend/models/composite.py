from typing import Optional
from sqlmodel import SQLModel
from pydantic import field_validator
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
    
    @field_validator('password', mode='before')
    @classmethod
    def hash_password_on_creation(cls, v):
        """Hash password before storing"""
        if isinstance(v, str):
            return hash_password(v)
        return v


class CompleteAlumniResponse(SQLModel):
    user_id: str
    alumni_id: str
    message: str
