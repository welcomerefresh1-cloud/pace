from typing import Optional
from sqlmodel import SQLModel


class CompleteAlumniRegistration(SQLModel):
    
    # User fields (user_id is auto-generated, user_type is always USER)
    username: str
    email: str
    password: str
    
    # Alumni fields (alumni_id is auto-generated)
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    age: int


class CompleteAlumniResponse(SQLModel):
    user_id: str
    alumni_id: str
    message: str
