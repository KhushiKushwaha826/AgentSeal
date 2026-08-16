"""
verification.py (schemas)

Defines the shape of the response returned by the
GET /decisions/{id}/verify endpoint.
"""

from pydantic import BaseModel


class VerificationResponse(BaseModel):
    decision_id: int
    status: str          # "VERIFIED" or "TAMPERED"
    message: str
    original_hash: str
    current_hash: str
