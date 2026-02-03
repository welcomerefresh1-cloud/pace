from typing import Optional
from sqlmodel import SQLModel
import uuid


class CompleteAlumniRegistration(SQLModel):
    
    # User fields (user_id is auto-generated)
    username: str
    email: str
    password: str
    
    # Student Record fields
    student_id: str
    year_graduated: int
    gwa: float
    avg_prof_grade: Optional[float] = None
    avg_elec_grade: Optional[float] = None
    ojt_grade: Optional[float] = None
    leadership_pos: Optional[bool] = None
    act_member_pos: Optional[bool] = None
    degree_id: str  # Human-readable degree ID (e.g., 'DEG-001')
    
    # Alumni fields (alumni_id is auto-generated)
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    age: int


class CompleteAlumniResponse(SQLModel):
    user_code: uuid.UUID
    student_code: uuid.UUID
    alumni_code: uuid.UUID
    message: str
