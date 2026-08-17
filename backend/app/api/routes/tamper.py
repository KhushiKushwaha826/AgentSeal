from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Decision

router = APIRouter(
    prefix="/decisions",
    tags=["Tamper Simulation"]
)


class TamperRequest(BaseModel):
    agent_id: str
    amount: float
    decision: str
    description: str
    user: str


@router.post("/{decision_id}/tamper")
def tamper_decision(
    decision_id: int,
    payload: TamperRequest,
    db: Session = Depends(get_db)
):
    decision = (
        db.query(Decision)
        .filter(Decision.id == decision_id)
        .first()
    )

    if decision is None:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    # Original values
    old_data = {
        "agent_id": decision.agent_id,
        "amount": decision.amount,
        "decision": decision.decision,
        "description": decision.description,
        "user": decision.user,
    }

    # IMPORTANT:
    # original_hash is intentionally NOT changed.
    decision.agent_id = payload.agent_id
    decision.amount = payload.amount
    decision.decision = payload.decision
    decision.description = payload.description
    decision.user = payload.user

    db.commit()
    db.refresh(decision)

    return {
        "message": "Decision data was tampered with.",
        "decision_id": decision.id,
        "old_data": old_data,
        "new_data": {
            "agent_id": decision.agent_id,
            "amount": decision.amount,
            "decision": decision.decision,
            "description": decision.description,
            "user": decision.user,
        },
        "original_hash_preserved": True,
    }