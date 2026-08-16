"""
tamper.py (routes)

Handles:
    - POST /decisions/{id}/tamper

This endpoint exists ONLY for demonstration purposes during the
hackathon. It intentionally changes the "amount" field in the
database WITHOUT updating the original_hash. This simulates someone
tampering with the data after it was recorded.

After calling this endpoint, calling GET /decisions/{id}/verify
should return "TAMPERED", because the current data no longer matches
the original hash.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Decision

router = APIRouter(prefix="/decisions", tags=["Tamper Simulation"])


@router.post("/{decision_id}/tamper")
def tamper_decision(decision_id: int, db: Session = Depends(get_db)):
    """
    Simulates a tamper attack by changing the "amount" field directly
    in the database. This is intentionally simple: it multiplies the
    current amount by 10 (e.g. 5000 -> 50000), just for the demo.

    NOTE: We deliberately do NOT update original_hash here.
    That's the whole point — the stored hash should now be "out of
    sync" with the real data, which is exactly what tampering looks
    like in the real world.
    """
    decision = db.query(Decision).filter(Decision.id == decision_id).first()

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    old_amount = decision.amount
    decision.amount = decision.amount * 10  # e.g. 5000 -> 50000

    db.commit()
    db.refresh(decision)

    return {
        "message": "Decision data was tampered with for demo purposes.",
        "decision_id": decision.id,
        "old_amount": old_amount,
        "new_amount": decision.amount,
        "hint": "Now call GET /decisions/{id}/verify to see it fail.",
    }
