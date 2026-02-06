import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


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
    user_code: Optional[uuid.UUID] = Field(default=None, foreign_key="users.user_code")
    student_code: uuid.UUID = Field(foreign_key="student_records.student_code")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AlumniCreate(AlumniBase):
    user_code: Optional[uuid.UUID] = None
    student_code: uuid.UUID


class AlumniPublic(AlumniBase):
    created_at: datetime
    updated_at: datetime


class AlumniUpdate(SQLModel):
    last_name: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=50)
    middle_name: Optional[str] = Field(default=None, max_length=50)
    gender: Optional[str] = Field(default=None, max_length=10)
    age: Optional[int] = None
