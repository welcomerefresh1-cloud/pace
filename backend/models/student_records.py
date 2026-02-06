import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator
from utils.timezone import get_current_time_gmt8, GMT8


class StudentRecordBase(SQLModel):
    student_id: str = Field(max_length=10, unique=True, index=True)
    year_graduated: int
    gwa: float
    avg_prof_grade: Optional[float] = None
    avg_elec_grade: Optional[float] = None
    ojt_grade: Optional[float] = None
    leadership_pos: Optional[bool] = None
    act_member_pos: Optional[bool] = None


class StudentRecord(StudentRecordBase, table=True):
    __tablename__ = "student_records"
    
    student_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    degree_code: uuid.UUID = Field(foreign_key="degrees.degree_code")
    alumni_code: uuid.UUID = Field(foreign_key="alumni.alumni_code", unique=True)
    created_at: datetime = Field(default_factory=get_current_time_gmt8)


class StudentRecordCreate(StudentRecordBase):
    degree_id: str  # Reference to degree by degree_id
    alumni_id: str  # Link to alumni
    
    @field_validator('degree_id', 'alumni_id', mode='before')
    @classmethod
    def uppercase_ids(cls, v):
        """Convert IDs to uppercase for case-insensitive matching"""
        if isinstance(v, str):
            return v.upper()
        return v


class StudentRecordUpdate(SQLModel):
    year_graduated: Optional[int] = None
    gwa: Optional[float] = None
    avg_prof_grade: Optional[float] = None
    avg_elec_grade: Optional[float] = None
    ojt_grade: Optional[float] = None
    leadership_pos: Optional[bool] = None
    act_member_pos: Optional[bool] = None
    alumni_id: Optional[str] = None  # Optional link to alumni
    
    @field_validator('alumni_id', mode='before')
    @classmethod
    def uppercase_alumni_id(cls, v):
        """Convert alumni_id to uppercase for case-insensitive matching"""
        if isinstance(v, str):
            return v.upper()
        return v


class StudentRecordPublic(StudentRecordBase):
    created_at: datetime
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')
