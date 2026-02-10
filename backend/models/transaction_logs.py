import uuid
from datetime import datetime, timezone
from typing import Optional, Any, Dict
from sqlmodel import SQLModel, Field
from pydantic import field_serializer
from utils.timezone import get_current_time_gmt8, GMT8


class TransactionLog(SQLModel, table=True):
    """Transaction log for tracking all CREATE, UPDATE, DELETE, RESTORE operations"""
    __tablename__ = "transaction_logs"
    
    tl_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tl_id: str = Field(max_length=12, unique=True, index=True)  # Human-readable ID like TL-000001
    tl_name: str = Field(max_length=500)  # Descriptive action name (e.g., "CREATED user USER-000001")
    before: Optional[Dict[str, Any]] = Field(default=None)  # JSON snapshot before operation
    after: Optional[Dict[str, Any]] = Field(default=None)  # JSON snapshot after operation
    tl_date: datetime = Field(default_factory=get_current_time_gmt8)  # Timestamp in GMT+8
    performed_by: Optional[uuid.UUID] = Field(default=None)  # UUID of user who performed action


class TransactionLogCreate(SQLModel):
    """Request model for creating transaction log entries"""
    tl_id: str = Field(max_length=12)
    tl_name: str = Field(max_length=500)
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None
    performed_by: Optional[uuid.UUID] = None


class TransactionLogPublic(SQLModel):
    """Public response model for transaction logs"""
    tl_id: str
    tl_name: str
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None
    tl_date: datetime
    performed_by: Optional[uuid.UUID] = None
    
    @field_serializer('tl_date')
    def serialize_datetime(self, value: datetime) -> str:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')
