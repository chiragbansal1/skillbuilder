"""
SQLModel table definitions for skill storage.

Three tables:
- Skill        — the live version of a skill
- SkillVersion — archived snapshots every time a skill is updated
- SkillFile    — documentation, code, or tool files attached to a skill
"""
from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel, Field


class Skill(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    content: str                  # full SKILL.md text
    author: str
    version: int = 1
    hidden: bool = False          # if True, excluded from Library and Run page
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SkillVersion(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    skill_id: int = Field(foreign_key="skill.id")
    version: int                  # which version this snapshot is
    content: str                  # the SKILL.md text at that version
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SkillFile(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    skill_id: int = Field(foreign_key="skill.id")
    filename: str                 # e.g. "nda_guidelines.md", "output_schema.json"
    file_type: str                # "doc" | "code" | "tool"
    content: str                  # text content of the file
    created_at: datetime = Field(default_factory=datetime.utcnow)
