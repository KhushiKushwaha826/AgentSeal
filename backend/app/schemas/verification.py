"""
verification.py (schemas)

Defines the shape of the response returned by the
GET /decisions/{id}/verify endpoint.

The on_chain_* fields are new (Day 3): they're optional so the
response still works even for decisions that were never anchored
to the blockchain yet.
"""

from pydantic import BaseModel


class VerificationResponse(BaseModel):
    decision_id: int
    status: str          # "VERIFIED" or "TAMPERED"
    message: str
    original_hash: str
    current_hash: str

    # New: blockchain verification fields
    on_chain_verified: bool = False
    chain_signer: str | None = None
    chain_tx_hash: str | None = None