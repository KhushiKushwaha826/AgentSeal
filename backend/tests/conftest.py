"""
conftest.py

Pytest automatically looks for this file and shares anything defined
here across all test files. We use it to create a fresh, temporary
test database and a FastAPI test client, so our tests don't touch
your real "agentledger.db" file.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db

# A separate SQLite database just for testing, kept in memory so it
# disappears automatically after the tests finish.
TEST_DATABASE_URL = "sqlite:///./test_agentledger.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Replaces the real database with our test database during tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """
    Provides a fresh database and a test client for each test
    function, so tests don't interfere with each other.
    """
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
