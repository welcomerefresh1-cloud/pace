import uuid
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator
from utils.timezone import get_current_time_gmt8, GMT8


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
    password: str = Field(min_length=8, max_length=255)
    user_type: UserType = Field(default=UserType.USER)
    
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


class UserLogin(SQLModel):
    username: str
    password: str
