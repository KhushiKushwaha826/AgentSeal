from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Decision
from app.schemas.decision import DecisionCreate, DecisionResponse
from app.services.hashing import generate_hash

router = APIRouter(prefix="/decisions", tags=["Decisions"])


@router.post("", response_model=DecisionResponse)
def create_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    """
    Creates a new decision:
        1. Take the validated request data (payload).
        2. Generate a SHA-256 hash from the important fields.
        3. Save the decision + hash to the database.
        4. Return the saved decision.
    """
    original_hash = generate_hash(
        agent_id=payload.agent_id,
        amount=payload.amount,
        decision=payload.decision,
        description=payload.description,
        user=payload.user,
    )

    new_decision = Decision(
        agent_id=payload.agent_id,
        amount=payload.amount,
        decision=payload.decision,
        description=payload.description,
        user=payload.user,
        original_hash=original_hash,
    )

    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    return new_decision

# ======================================================
# GET ALL DECISIONS
# ======================================================

@router.get("/", response_model=list[DecisionResponse])
def get_all_decisions(db: Session = Depends(get_db)):

    decisions = (
        db.query(Decision)
        .order_by(Decision.id.desc())
        .all()
    )

    return decisions




@router.get("/{decision_id}", response_model=DecisionResponse)
def get_decision(decision_id: int, db: Session = Depends(get_db)):
    """
    Fetches a single decision by its ID.
    Returns a 404 error if it doesn't exist.
    """
    decision = db.query(Decision).filter(Decision.id == decision_id).first()

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    return decision
