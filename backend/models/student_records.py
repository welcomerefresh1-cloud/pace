import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import field_serializer, field_validator, BaseModel
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
    course_code: Optional[uuid.UUID] = Field(default=None, foreign_key="courses.course_code", ondelete="SET NULL")
    alumni_code: Optional[uuid.UUID] = Field(default=None, foreign_key="alumni.alumni_code", unique=True, ondelete="SET NULL")
    created_at: datetime = Field(default_factory=get_current_time_gmt8)
    updated_at: datetime = Field(default_factory=get_current_time_gmt8)
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class StudentRecordCreate(StudentRecordBase):
    course_abbv: str  # Reference to course by abbreviation
    alumni_id: str  # Link to alumni
    
    @field_validator('year_graduated')
    @classmethod
    def validate_year_graduated(cls, v):
        """Validate year graduated is not in the future"""
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(f'Year graduated cannot be in the future (max: {current_year})')
        if v < 1950:
            raise ValueError('Year graduated must be 1950 or later')
        return v
    
    @field_validator('course_abbv', 'alumni_id', mode='before')
    @classmethod
    def uppercase_ids(cls, v):
        """Convert values to uppercase for case-insensitive matching"""
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
    
    @field_validator('year_graduated')
    @classmethod
    def validate_year_graduated(cls, v):
        """Validate year graduated is not in the future if provided"""
        if v is not None:
            current_year = datetime.now().year
            if v > current_year:
                raise ValueError(f'Year graduated cannot be in the future (max: {current_year})')
            if v < 1950:
                raise ValueError('Year graduated must be 1950 or later')
        return v
    
    @field_validator('alumni_id', mode='before')
    @classmethod
    def uppercase_alumni_id(cls, v):
        """Convert alumni_id to uppercase for case-insensitive matching"""
        if isinstance(v, str):
            return v.upper()
        return v


class StudentRecordPublic(StudentRecordBase):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    
    @field_serializer('created_at', 'updated_at', 'deleted_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        if value is None:
            return None
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')


# Bulk operation models

# Safe display models (exclude sensitive fields from responses)
class StudentRecordCreateSafeDisplay(BaseModel):
    """Student record creation data for response"""
    student_id: str
    course_abbv: str
    alumni_id: str


class StudentRecordUpdateSafeDisplay(BaseModel):
    """Student record update data for response"""
    student_id: str
    year_graduated: Optional[int] = None
    gwa: Optional[float] = None


class StudentRecordBulkCreateItem(BaseModel):
    """Individual item result from bulk create operation"""
    index: int = Field(..., description="Index in the request list (0-based)")
    item: StudentRecordCreateSafeDisplay = Field(..., description="The student record data submitted")
    success: bool = Field(..., description="Whether this item was created successfully")
    code: str = Field(..., description="Error code (if failed) or success code")
    message: str = Field(..., description="Detailed message about the result")
    data: Optional[StudentRecordPublic] = Field(default=None, description="Created student record (if successful)")


class StudentRecordBulkCreate(BaseModel):
    """Bulk create request for student records"""
    items: List[StudentRecordCreate] = Field(..., min_items=1, max_items=100, description="List of student records to create (1-100 items)")


class StudentRecordBulkCreateResponse(BaseModel):
    """Bulk create response for student records"""
    total_items: int = Field(..., description="Total items in request")
    successful: int = Field(..., description="Number of items successfully created")
    failed: int = Field(..., description="Number of items that failed")
    results: List[StudentRecordBulkCreateItem] = Field(..., description="Detailed results for each item")


# Bulk update models
class StudentRecordBulkUpdateItem(BaseModel):
    """Student record update item in bulk request"""
    student_id: str = Field(..., description="Student ID to update")
    year_graduated: Optional[int] = Field(default=None, description="Updated year graduated")
    gwa: Optional[float] = Field(default=None, description="Updated GWA")
    avg_prof_grade: Optional[float] = Field(default=None, description="Updated professional average grade")
    avg_elec_grade: Optional[float] = Field(default=None, description="Updated elective average grade")
    ojt_grade: Optional[float] = Field(default=None, description="Updated OJT grade")
    leadership_pos: Optional[bool] = Field(default=None, description="Leadership position flag")
    act_member_pos: Optional[bool] = Field(default=None, description="Activity member position flag")
    alumni_id: Optional[str] = Field(default=None, description="Link to alumni (if updating)")
    
    @field_validator('year_graduated')
    @classmethod
    def validate_year_graduated(cls, v):
        """Validate year graduated is not in the future if provided"""
        if v is not None:
            current_year = datetime.now().year
            if v > current_year:
                raise ValueError(f'Year graduated cannot be in the future (max: {current_year})')
            if v < 1950:
                raise ValueError('Year graduated must be 1950 or later')
        return v
    
    @field_validator('alumni_id', mode='before')
    @classmethod
    def uppercase_alumni_id(cls, v):
        """Convert alumni_id to uppercase for case-insensitive matching"""
        if isinstance(v, str):
            return v.upper()
        return v


class StudentRecordBulkUpdateResult(BaseModel):
    """Individual item result from bulk update operation"""
    index: int = Field(..., description="Index in the request list (0-based)")
    item: StudentRecordUpdateSafeDisplay = Field(..., description="The student record data submitted")
    success: bool = Field(..., description="Whether this item was updated successfully")
    code: str = Field(..., description="Error code (if failed) or success code")
    message: str = Field(..., description="Detailed message about the result")
    data: Optional[StudentRecordPublic] = Field(default=None, description="Updated student record (if successful)")


class StudentRecordBulkUpdate(BaseModel):
    """Bulk update request for student records"""
    items: List[StudentRecordBulkUpdateItem] = Field(..., min_items=1, max_items=100, description="List of student records to update (1-100 items)")


class StudentRecordBulkUpdateResponse(BaseModel):
    """Bulk update response for student records"""
    total_items: int = Field(..., description="Total items in request")
    successful: int = Field(..., description="Number of items successfully updated")
    failed: int = Field(..., description="Number of items that failed")
    results: List[StudentRecordBulkUpdateResult] = Field(..., description="Detailed results for each item")


# Bulk delete models
class StudentRecordBulkDeleteResult(BaseModel):
    """Individual item result from bulk delete operation"""
    index: int = Field(..., description="Index in the request list (0-based)")
    student_id: str = Field(..., description="Student ID that was deleted")
    success: bool = Field(..., description="Whether this item was deleted successfully")
    code: str = Field(..., description="Error code (if failed) or success code")
    message: str = Field(..., description="Detailed message about the result")


class StudentRecordBulkDelete(BaseModel):
    """Bulk delete request for student records"""
    ids: List[str] = Field(..., min_items=1, max_items=100, description="List of student IDs to delete (1-100 items)")


class StudentRecordBulkDeleteResponse(BaseModel):
    """Bulk delete response for student records"""
    total_items: int = Field(..., description="Total items in request")
    successful: int = Field(..., description="Number of items successfully deleted")
    failed: int = Field(..., description="Number of items that failed")
    results: List[StudentRecordBulkDeleteResult] = Field(..., description="Detailed results for each item")
