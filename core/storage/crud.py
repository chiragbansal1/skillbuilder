"""
CRUD operations for skill storage.

All functions take an explicit Session so the caller controls transactions.
"""
from datetime import datetime
from sqlmodel import Session, select
from core.storage.models import Skill, SkillVersion, SkillFile


# --- Skill ------------------------------------------------------------------

def create_skill(
    session: Session,
    name: str,
    description: str,
    content: str,
    author: str,
) -> Skill:
    skill = Skill(name=name, description=description, content=content, author=author)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


def get_skill_by_id(session: Session, skill_id: int) -> Skill | None:
    return session.get(Skill, skill_id)


def list_skills(session: Session) -> list[Skill]:
    return session.exec(select(Skill)).all()


def delete_skill(session: Session, skill_id: int) -> bool:
    skill = session.get(Skill, skill_id)
    if not skill:
        return False
    # Remove related records first to respect foreign keys
    for sv in session.exec(select(SkillVersion).where(SkillVersion.skill_id == skill_id)).all():
        session.delete(sv)
    for sf in session.exec(select(SkillFile).where(SkillFile.skill_id == skill_id)).all():
        session.delete(sf)
    session.delete(skill)
    session.commit()
    return True


def update_skill(session: Session, skill_id: int, content: str) -> Skill | None:
    skill = session.get(Skill, skill_id)
    if not skill:
        return None

    # Archive the current version before overwriting
    session.add(SkillVersion(
        skill_id=skill.id,
        version=skill.version,
        content=skill.content,
    ))

    skill.content = content
    skill.version += 1
    skill.updated_at = datetime.utcnow()
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


# --- SkillVersion -----------------------------------------------------------

def list_skill_versions(session: Session, skill_id: int) -> list[SkillVersion]:
    statement = select(SkillVersion).where(SkillVersion.skill_id == skill_id)
    return session.exec(statement).all()


# --- SkillFile --------------------------------------------------------------

def add_skill_file(
    session: Session,
    skill_id: int,
    filename: str,
    file_type: str,
    content: str,
) -> SkillFile:
    skill_file = SkillFile(
        skill_id=skill_id,
        filename=filename,
        file_type=file_type,
        content=content,
    )
    session.add(skill_file)
    session.commit()
    session.refresh(skill_file)
    return skill_file


def get_skill_files(session: Session, skill_id: int) -> list[SkillFile]:
    statement = select(SkillFile).where(SkillFile.skill_id == skill_id)
    return session.exec(statement).all()
