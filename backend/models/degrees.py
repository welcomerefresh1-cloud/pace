import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class DegreeBase(SQLModel):
    degree_id: str = Field(max_length=11, unique=True, index=True)
    degree_name: str = Field(max_length=100)


class Degree(DegreeBase, table=True):
    __tablename__ = "degrees"
    
    degree_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DegreeCreate(DegreeBase):
    @field_validator('degree_id', mode='before')
    @classmethod
    def capitalize_degree_id(cls, v):
        """Convert degree_id to uppercase"""
        if isinstance(v, str):
            return v.upper()
        return v


class DegreePublic(DegreeBase):
    pass
