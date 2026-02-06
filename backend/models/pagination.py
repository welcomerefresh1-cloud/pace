from typing import TypeVar, Generic, List
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationMetadata(BaseModel):
    """Pagination metadata for paginated responses"""
    total: int = Field(..., description="Total number of records in database")
    limit: int = Field(..., description="Number of records per page (0 = all)")
    offset: int = Field(..., description="Number of records skipped")
    returned: int = Field(..., description="Number of records returned in this response")
    has_next: bool = Field(..., description="Whether there are more records after this page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    data: List[T] = Field(..., description="List of records")
    pagination: PaginationMetadata = Field(..., description="Pagination metadata")
