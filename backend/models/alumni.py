import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator
from utils.timezone import get_current_time_gmt8, GMT8


class AlumniBase(SQLModel):
    alumni_id: str = Field(max_length=11, unique=True, index=True)
    last_name: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    middle_name: Optional[str] = Field(default=None, max_length=50)
    gender: str = Field(max_length=10)
    age: int


class Alumni(AlumniBase, table=True):
    __tablename__ = "alumni"
    
    alumni_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_code: Optional[uuid.UUID] = Field(default=None, foreign_key="users.user_code", ondelete="CASCADE")
    student_code: Optional[uuid.UUID] = Field(default=None, foreign_key="student_records.student_code", unique=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=get_current_time_gmt8)
    updated_at: datetime = Field(default_factory=get_current_time_gmt8)


class AlumniCreate(AlumniBase):
    user_code: Optional[uuid.UUID] = None
    student_code: uuid.UUID
    
    @field_validator('gender', mode='before')
    @classmethod
    def capitalize_gender(cls, v):
        """Convert gender to uppercase for case-insensitive input"""
        if isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        """Validate age is valid"""
        if v < 0:
            raise ValueError('Invalid age')
        return v


class AlumniPublic(AlumniBase):
    created_at: datetime
    updated_at: datetime
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')


class AlumniUpdate(SQLModel):
    last_name: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=50)
    middle_name: Optional[str] = Field(default=None, max_length=50)
    gender: Optional[str] = Field(default=None, max_length=10)
    age: Optional[int] = None
    
    @field_validator('gender', mode='before')
    @classmethod
    def capitalize_gender(cls, v):
        """Convert gender to uppercase for case-insensitive input"""
        if v is not None and isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        """Validate age is valid if provided"""
        if v is not None and v < 0:
            raise ValueError('Invalid age')
        return v
