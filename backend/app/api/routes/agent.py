"""
agent.py (routes)

Handles:
    - GET  /agent/status   (already existed)
    - POST /agent/decide   (new) — runs the AI agent on a plain
      English request, then saves the result as a real decision
      using the exact same hashing + database logic as
      POST /decisions, so it shows up identically everywhere else
      in the app (verify, anchor, tamper all work on it too).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Decision
from app.schemas.agent import AgentDecisionRequest
from app.schemas.decision import DecisionResponse
from app.services.hashing import generate_hash
from app.agent.agent import run_expense_agent

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/status")
def agent_status():
    return {"status": "AI agent is online and ready."}


@router.post("/decide", response_model=DecisionResponse)
def agent_decide(payload: AgentDecisionRequest, db: Session = Depends(get_db)):
    """
    Runs the LangChain/Groq agent on a plain-English request, then
    saves its decision to the database exactly like a normal
    POST /decisions call would.
    """
    result = run_expense_agent(
        agent_id=payload.agent_id,
        user=payload.user,
        amount=payload.amount,
        request_text=payload.request_text,
    )

    original_hash = generate_hash(
        agent_id=result["agent_id"],
        amount=result["amount"],
        decision=result["decision"],
        description=result["description"],
        user=result["user"],
    )

    new_decision = Decision(
        agent_id=result["agent_id"],
        amount=result["amount"],
        decision=result["decision"],
        description=result["description"],
        user=result["user"],
        original_hash=original_hash,
    )

    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    return new_decision