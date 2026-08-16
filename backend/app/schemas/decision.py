"""
decision.py (schemas)

These are Pydantic models. They are NOT database tables — they define
the "shape" of data that comes IN to our API (requests) and goes OUT
of our API (responses).

Using schemas like this gives us automatic validation. For example,
if someone sends "amount" as text instead of a number, FastAPI will
reject the request automatically before our code even runs.
"""

from datetime import datetime
from pydantic import BaseModel


class DecisionCreate(BaseModel):
    """
    Shape of the data required to CREATE a new decision.
    This is what the client sends in the POST /decisions request body.
    """
    agent_id: str
    amount: float
    decision: str
    description: str | None = None
    user: str


class DecisionResponse(BaseModel):
    """
    Shape of the data we SEND BACK after a decision is created or
    fetched. Includes everything from DecisionCreate, plus the fields
    that the server generates itself (id, created_at, original_hash).
    """
    id: int
    agent_id: str
    amount: float
    decision: str
    description: str | None = None
    user: str
    created_at: datetime
    original_hash: str

    class Config:
        # This lets Pydantic read data directly from a SQLAlchemy
        # model (an ORM object), not just from a plain dict.
        from_attributes = True
