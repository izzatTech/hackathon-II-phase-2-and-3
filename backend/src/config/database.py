"""
Database configuration module for the Todo application.
Sets up connection to PostgreSQL database using SQLModel.
"""

from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: A database session
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.

    Yields:
        Session: A database session
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_db_and_tables():
    """
    Create database tables.
    This function should be called on application startup.
    """
    from backend.src.models.user import User
    from backend.src.models.task import Task
    from backend.src.models.session import SessionModel
    from sqlmodel import SQLModel

    # Import all models here to ensure they're registered with SQLModel
    SQLModel.metadata.create_all(engine)