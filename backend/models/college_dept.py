import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator, field_serializer
from datetime import datetime, timezone
from utils.timezone import GMT8


class CollegeDeptBase(SQLModel):
    college_dept_abbv: str = Field(max_length=20, unique=True, index=True)
    college_dept_name: str = Field(max_length=200, unique=True, index=True)
    college_dept_desc: Optional[str] = Field(default=None, max_length=500)


class CollegeDept(CollegeDeptBase, table=True):
    __tablename__ = "college_depts"
    
    college_dept_id: str = Field(max_length=12, unique=True, index=True)
    college_dept_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CollegeDeptCreate(CollegeDeptBase):
    college_dept_desc: Optional[str] = Field(default=None, max_length=500)
    
    @field_validator('college_dept_abbv', mode='before')
    @classmethod
    def capitalize_college_dept_abbv(cls, v):
        """Convert college_dept_abbv to uppercase"""
        if isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator('college_dept_abbv', 'college_dept_name')
    @classmethod
    def validate_non_empty(cls, v):
        """Ensure abbreviation and name are not empty"""
        if isinstance(v, str) and not v.strip():
            raise ValueError('This field cannot be empty')
        return v


class CollegeDeptUpdate(SQLModel):
    college_dept_abbv: Optional[str] = Field(default=None, max_length=20)
    college_dept_name: Optional[str] = Field(default=None, max_length=200)
    college_dept_desc: Optional[str] = Field(default=None, max_length=500)
    
    @field_validator('college_dept_abbv', mode='before')
    @classmethod
    def capitalize_college_dept_abbv(cls, v):
        """Convert college_dept_abbv to uppercase"""
        if v is not None and isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator('college_dept_abbv', 'college_dept_name')
    @classmethod
    def validate_non_empty(cls, v):
        """Ensure abbreviation and name are not empty if provided"""
        if v is not None and isinstance(v, str) and not v.strip():
            raise ValueError('This field cannot be empty')
        return v


class CollegeDeptPublic(CollegeDeptBase):
    college_dept_id: str
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
