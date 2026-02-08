import uuid
import re
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator
from utils.timezone import get_current_time_gmt8, GMT8
from utils.auth import hash_password


class UserType(str, Enum):
    USER = "USER"
    STAFF = "STAFF"
    ADMIN = "ADMIN"


class UserBase(SQLModel):
    user_id: str = Field(max_length=12, unique=True, index=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    user_type: UserType = Field(default=UserType.USER)


class User(UserBase, table=True):
    __tablename__ = "users"
    
    user_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str = Field(max_length=255)  # Hashed password
    created_at: datetime = Field(default_factory=get_current_time_gmt8)


class UserCreate(SQLModel):
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    password: str = Field(min_length=8, max_length=72)
    user_type: UserType = Field(default=UserType.USER)
    
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
    
    @field_validator('user_type', mode='before')
    @classmethod
    def validate_user_type(cls, v):
        """Convert user_type to uppercase for case-insensitive input"""
        if isinstance(v, str):
            return v.upper()
        return v


class UserPublic(UserBase):
    user_type: UserType
    created_at: datetime
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    current_password: Optional[str] = Field(default=None, min_length=8, max_length=72)
    password: Optional[str] = Field(default=None, min_length=8, max_length=72)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format if provided"""
        if v is not None:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
            return v.lower()
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength if provided, then hash"""
        if v is not None:
            if len(v) < 8:
                raise ValueError('Password must be at least 8 characters long')
            if not re.search(r'[A-Z]', v):
                raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r'[a-z]', v):
                raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r'\d', v):
                raise ValueError('Password must contain at least one number')
            return hash_password(v)  # Hash after validation passes
        return v


class SuccessResponse(SQLModel):
    code: str
    message: str


class UserLogin(SQLModel):
    username: str
    password: str
