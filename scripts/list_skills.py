"""
List all skills stored in the database.

Run: python -m scripts.list_skills
"""
from dotenv import load_dotenv
load_dotenv()

from core.storage.database import get_session
from core.storage.crud import list_skills


def main():
    session = get_session()
    try:
        skills = list_skills(session)
    finally:
        session.close()

    if not skills:
        print("No skills found. Run: python -m scripts.seed_db")
        return

    header = f"{'ID':<5} {'Name':<30} {'Author':<20} {'Ver':<5} {'Description'}"
    print(header)
    print("-" * len(header))
    for s in skills:
        desc = (s.description[:50] + "...") if len(s.description) > 50 else s.description
        print(f"{s.id:<5} {s.name:<30} {s.author:<20} {s.version:<5} {desc}")


if __name__ == "__main__":
    main()
