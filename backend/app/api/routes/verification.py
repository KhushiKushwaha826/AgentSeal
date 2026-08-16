"""
verification.py (routes)

Handles:
    - GET /decisions/{id}/verify

This route fetches a decision from the database and asks the
verification service to check whether it has been tampered with.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Decision
from app.schemas.verification import VerificationResponse
from app.services.verification import verify_decision

router = APIRouter(prefix="/decisions", tags=["Verification"])


@router.get("/{decision_id}/verify", response_model=VerificationResponse)
def verify_decision_route(decision_id: int, db: Session = Depends(get_db)):
    """
    Checks whether a decision's data still matches its original hash.
    """
    decision = db.query(Decision).filter(Decision.id == decision_id).first()

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    result = verify_decision(decision)
    return result
