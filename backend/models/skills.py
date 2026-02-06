import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_serializer
from utils.timezone import get_current_time_gmt8, GMT8


class SkillsBase(SQLModel):
    skill_id: str = Field(max_length=11, unique=True, index=True)
    soft_skills_avg: Optional[float] = None
    hard_skills_avg: Optional[float] = None


class Skills(SkillsBase, table=True):
    __tablename__ = "skills"
    
    skill_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    alumni_code: uuid.UUID = Field(foreign_key="alumni.alumni_code", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=get_current_time_gmt8)


class SkillsCreate(SkillsBase):
    alumni_code: uuid.UUID


class SkillsPublic(SkillsBase):
    created_at: datetime
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Convert to GMT+8 and format as YYYY-MM-DD HH:MM:SS without microseconds"""
        # Convert UTC datetime to GMT+8
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        gmt8_time = value.astimezone(GMT8)
        return gmt8_time.strftime('%Y-%m-%d %H:%M:%S')


# Skills List (Individual Skills)
class SkillsListBase(SQLModel):
    skill_name: str = Field(max_length=100)
    skill_value: Optional[float] = Field(default=None, ge=0, le=100)


class SkillsList(SkillsListBase, table=True):
    __tablename__ = "skills_list"
    
    sl_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    skill_code: uuid.UUID = Field(foreign_key="skills.skill_code", ondelete="CASCADE")


class SkillsListCreate(SkillsListBase):
    skill_code: uuid.UUID


class SkillsListPublic(SkillsListBase):
    pass
