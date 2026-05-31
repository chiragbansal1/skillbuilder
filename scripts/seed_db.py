"""
Seed the database with sample skills.

Auto-discovers skills by scanning the skills/ directory for skill.json manifests.
To add a new skill: create a folder under skills/, add SKILL.md and skill.json,
then re-run this script. No changes to this file needed.

Safe to re-run — skips skills that already exist in the DB.

Run: python -m scripts.seed_db
"""
import json
from pathlib import Path
from sqlmodel import select
from core.storage.database import create_db_and_tables, get_session
from core.storage.models import Skill
from core.storage.crud import create_skill, add_skill_file

SKILLS_DIR = Path("skills")


def seed():
    create_db_and_tables()
    print("Tables created.\n")

    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "skill.json").exists()
    )

    if not skill_dirs:
        print("No skill.json files found under skills/. Nothing to seed.")
        return

    with get_session() as session:
        for skill_dir in skill_dirs:
            manifest = json.loads((skill_dir / "skill.json").read_text(encoding="utf-8"))
            name = manifest["name"]

            # Sync hidden flag if skill already exists, then skip content re-seed
            existing = session.exec(
                select(Skill).where(Skill.name == name)
            ).first()
            if existing:
                hidden = manifest.get("hidden", False)
                if existing.hidden != hidden:
                    existing.hidden = hidden
                    session.add(existing)
                    session.commit()
                    print(f"SYNC  {name} (id={existing.id}) hidden={hidden}")
                else:
                    print(f"SKIP  {name} (already exists, id={existing.id})")
                continue

            content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            skill = create_skill(
                session=session,
                name=name,
                description=manifest["description"],
                content=content,
                author=manifest["author"],
                hidden=manifest.get("hidden", False),
            )
            print(f"ADDED {skill.name} (id={skill.id})")

            for f in manifest.get("files", []):
                file_path = skill_dir / f["path"]
                if not file_path.exists():
                    print(f"      ! MISSING {f['path']} — skipping")
                    continue
                add_skill_file(
                    session=session,
                    skill_id=skill.id,
                    filename=f["filename"],
                    file_type=f["file_type"],
                    content=file_path.read_text(encoding="utf-8"),
                )
                print(f"      + attached {f['filename']} ({f['file_type']})")

    print("\nDone.")


if __name__ == "__main__":
    seed()
