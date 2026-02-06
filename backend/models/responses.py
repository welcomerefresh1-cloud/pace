from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import field_serializer


class AlumniFullProfile(SQLModel):
    """Complete alumni profile with all related information"""
    # Alumni info
    alumni_id: str
    last_name: str
    first_name: str
    middle_name: Optional[str]
    gender: str
    age: int
    
    # User account info
    user_id: Optional[str]
    username: Optional[str]
    email: Optional[str]
    
    # Student record info
    student_id: str
    year_graduated: int
    gwa: float
    avg_prof_grade: Optional[float]
    avg_elec_grade: Optional[float]
    ojt_grade: Optional[float]
    leadership_pos: Optional[bool]
    act_member_pos: Optional[bool]
    
    # Degree info
    degree_id: str
    degree_name: str
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Format datetime as YYYY-MM-DD HH:MM:SS without microseconds"""
        return value.strftime('%Y-%m-%d %H:%M:%S')
