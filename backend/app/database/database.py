"""
database.py

Database connection setup for AgentSeal.

- SQLite is used for local development.
- PostgreSQL is used when deployed on Render.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL


# PostgreSQL URLs from some providers may use postgres://.
# SQLAlchemy expects postgresql://.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# SQLite needs check_same_thread=False.
# PostgreSQL does NOT support this option.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)


# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all database models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session
    and closes it after the request is finished.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()