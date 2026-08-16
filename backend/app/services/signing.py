"""
signing.py

NOTE: Digital signing is NOT used by the main AgentLedger flow yet.
Hashing + verification (see hashing.py and verification.py) is
enough to demonstrate tamper detection for the hackathon.

This file has a SIMPLE, optional example of how we could later sign
a decision's hash with ECDSA (Elliptic Curve Digital Signature
Algorithm), so only someone with the correct private key could have
"approved" it. This adds an extra layer of trust on top of hashing,
but it is NOT wired into any API route right now, to keep the first
version simple.

TODO (later, not now):
- Generate and safely store a real private key (not like below).
- Call sign_hash() when a decision is created.
- Call verify_signature() during the /verify endpoint.
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


def generate_demo_keypair():
    """
    Creates a temporary private/public key pair, only for demo/testing
    purposes. In a real system, the private key would be generated
    ONCE and stored securely (not regenerated every time).
    """
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key


def sign_hash(private_key, hash_hex: str) -> bytes:
    """
    Signs a hash string using ECDSA. Returns the raw signature bytes.
    """
    signature = private_key.sign(
        hash_hex.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return signature


def verify_signature(public_key, hash_hex: str, signature: bytes) -> bool:
    """
    Checks whether a given signature is valid for the given hash,
    using the provided public key. Returns True/False.
    """
    try:
        public_key.verify(
            signature,
            hash_hex.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        # cryptography raises an exception if the signature is invalid
        return False
