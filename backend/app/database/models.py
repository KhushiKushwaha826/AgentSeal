"""
models.py

This file defines the database tables using SQLAlchemy models.
For the first version of AgentSeal, we only need ONE table:
"decisions".

Each row in this table represents one decision made by an AI agent,
along with the SHA-256 hash of that decision at the time it was
created. Later, we compare this "original_hash" against a freshly
computed hash to detect tampering.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Decision(Base):
    """
    Represents a single AI agent decision stored in the database.

    Fields:
        id            - auto-generated unique ID for this row
        agent_id      - which AI agent made this decision (e.g. "agent-01")
        amount        - the money amount involved in the decision
        decision      - the outcome, e.g. "APPROVED" or "REJECTED"
        description   - free text describing what the decision was about
        user          - the person/entity this decision relates to
        created_at    - timestamp of when the decision was created
        original_hash - SHA-256 hash generated at creation time.
                         This is our "source of truth" for tamper checks.
    """

    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    original_hash = Column(String, nullable=False)
