import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator, field_serializer
from datetime import datetime, timezone
from utils.timezone import GMT8


class CourseBase(SQLModel):
    course_abbv: str = Field(max_length=20, unique=True, index=True)
    course_name: str = Field(max_length=200, unique=True, index=True)
    course_desc: Optional[str] = Field(default=None, max_length=500)


class Course(CourseBase, table=True):
    __tablename__ = "courses"
    
    course_id: str = Field(max_length=12, unique=True, index=True)
    course_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    college_dept_code: uuid.UUID = Field(foreign_key="college_depts.college_dept_code", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CourseCreate(CourseBase):
    college_dept_abbv: str  # College department abbreviation (e.g., CCS)
    course_desc: Optional[str] = Field(default=None, max_length=500)
    
    @field_validator('course_abbv', 'college_dept_abbv', mode='before')
    @classmethod
    def capitalize_abbvs(cls, v):
        """Convert abbreviations to uppercase"""
        if isinstance(v, str):
            return v.upper()
        return v


class CourseUpdate(SQLModel):
    course_abbv: Optional[str] = Field(default=None, max_length=20)
    course_name: Optional[str] = Field(default=None, max_length=200)
    course_desc: Optional[str] = Field(default=None, max_length=500)
    college_dept_abbv: Optional[str] = Field(default=None)  # Allow updating the college department
    
    @field_validator('course_abbv', 'college_dept_abbv', mode='before')
    @classmethod
    def capitalize_abbvs(cls, v):
        """Convert abbreviations to uppercase"""
        if v is not None and isinstance(v, str):
            return v.upper()
        return v


class CoursePublic(CourseBase):
    course_id: str
    college_dept_id: str  # Return human-readable ID
    college_dept_name: str  # Include the college department name
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
