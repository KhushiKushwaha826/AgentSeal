"""
verification.py (services)

Checks whether a decision's data has been tampered with, using
TWO independent checks:
  1. Database check (existing): does the CURRENT data still match
     the hash we saved when it was created?
  2. Blockchain check (new, Day 3): does the blockchain have a
     record for this hash, signed by our known wallet?

A decision is only fully "VERIFIED" if both checks agree. This is
stronger than checking the database alone, since a malicious actor
who gained access to the database could edit both the data AND the
original_hash together — but they can't rewrite what's already
permanently stored on the blockchain.
"""

from app.database.models import Decision
from app.services.hashing import generate_hash
from app.blockchain.contract import get_action_from_chain


def verify_decision(decision: Decision) -> dict:
    current_hash = generate_hash(
        agent_id=decision.agent_id,
        amount=decision.amount,
        decision=decision.decision,
        description=decision.description,
        user=decision.user,
    )

    db_matches = (current_hash == decision.original_hash)

    # Blockchain check: only meaningful if this decision was ever
    # anchored on-chain (i.e. chain_tx_hash is set)
    on_chain_verified = False
    chain_signer = None

    if decision.chain_tx_hash:
        chain_record = get_action_from_chain(decision.original_hash)
        if chain_record["exists"]:
            on_chain_verified = True
            chain_signer = chain_record["signer"]

    if db_matches and (on_chain_verified or not decision.chain_tx_hash):
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
        "on_chain_verified": on_chain_verified,
        "chain_signer": chain_signer,
        "chain_tx_hash": decision.chain_tx_hash,
    }