import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SkillsBase(SQLModel):
    skill_id: str = Field(max_length=11, unique=True, index=True)
    soft_skills_avg: Optional[float] = None
    hard_skills_avg: Optional[float] = None


class Skills(SkillsBase, table=True):
    __tablename__ = "skills"
    
    skill_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    alumni_code: uuid.UUID = Field(foreign_key="alumni.alumni_code")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SkillsCreate(SkillsBase):
    alumni_code: uuid.UUID


class SkillsPublic(SkillsBase):
    skill_code: uuid.UUID
    alumni_code: uuid.UUID
    created_at: datetime


# Skills List (Individual Skills)
class SkillsListBase(SQLModel):
    skill_name: str = Field(max_length=100)
    skill_value: Optional[float] = Field(default=None, ge=0, le=100)


class SkillsList(SkillsListBase, table=True):
    __tablename__ = "skills_list"
    
    sl_code: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    skill_code: uuid.UUID = Field(foreign_key="skills.skill_code")


class SkillsListCreate(SkillsListBase):
    skill_code: uuid.UUID


class SkillsListPublic(SkillsListBase):
    sl_code: uuid.UUID
    skill_code: uuid.UUID
