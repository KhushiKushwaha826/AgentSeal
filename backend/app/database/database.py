"""
database.py

This file sets up the connection to our SQLite database using
SQLAlchemy. Every other file that needs to talk to the database
imports things from here.

Think of it like this:
- "engine"      -> the actual connection to the .db file
- "SessionLocal" -> a factory that gives us a new "conversation"
                    (session) with the database whenever we need one
- "Base"        -> the parent class our models (tables) inherit from
- "get_db"      -> a helper FastAPI uses to give each request its
                    own database session, and close it afterwards
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL

# "check_same_thread" is only needed for SQLite. It lets FastAPI use
# the same database connection across different requests safely
# for this simple project.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a "session factory". Every time we call
# SessionLocal(), we get a fresh database session to work with.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our database models (tables) will inherit from this Base class.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session to a route,
    and makes sure it gets closed afterward, even if an error happens.

    Usage in a route:
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
