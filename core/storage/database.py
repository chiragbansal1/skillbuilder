"""
Database engine setup and session management.

Uses SQLite via SQLModel. The DB file (skillforge.db) is created in the
project root when create_db_and_tables() is first called.
"""
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///skillforge.db"

engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    """Create all tables if they don't exist. Safe to call multiple times."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Return a new database session. Caller is responsible for closing it."""
    return Session(engine)
