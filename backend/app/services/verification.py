"""
verification.py (services)

This file contains the logic for checking whether a decision's data
has been tampered with.

It does NOT touch the database directly or handle HTTP — that is the
job of the route file (app/api/routes/verification.py). This file
just focuses on the "compare two hashes" logic, so it's easy to
read, test, and reuse.
"""

from app.database.models import Decision
from app.services.hashing import generate_hash


def verify_decision(decision: Decision) -> dict:
    """
    Takes a Decision object (as it currently exists in the database)
    and checks if it matches its original hash.

    Steps:
        1. Re-generate a hash using the decision's CURRENT data.
        2. Compare it against the "original_hash" saved at creation time.
        3. Return a simple dictionary describing the result.
    """
    current_hash = generate_hash(
        agent_id=decision.agent_id,
        amount=decision.amount,
        decision=decision.decision,
        description=decision.description,
        user=decision.user,
    )

    if current_hash == decision.original_hash:
        status = "VERIFIED"
        message = "Decision data is unchanged."
    else:
        status = "TAMPERED"
        message = "Decision data has been modified."

    return {
        "decision_id": decision.id,
        "status": status,
        "message": message,
        "original_hash": decision.original_hash,
        "current_hash": current_hash,
    }
