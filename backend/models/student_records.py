import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


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
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudentRecordCreate(StudentRecordBase):
    degree_code: uuid.UUID


class StudentRecordPublic(StudentRecordBase):
    created_at: datetime
