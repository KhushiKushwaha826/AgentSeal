"""
test_hashing.py

Tests for app/services/hashing.py.

We check the most important rule of the whole project:
the SAME input data must always produce the SAME hash, and
DIFFERENT input data must produce a DIFFERENT hash.
"""

from app.services.hashing import generate_hash


def test_same_data_produces_same_hash():
    hash1 = generate_hash("agent-01", 5000, "APPROVED", "Laptop", "Rahul")
    hash2 = generate_hash("agent-01", 5000, "APPROVED", "Laptop", "Rahul")

    assert hash1 == hash2


def test_different_data_produces_different_hash():
    hash1 = generate_hash("agent-01", 5000, "APPROVED", "Laptop", "Rahul")
    hash2 = generate_hash("agent-01", 50000, "APPROVED", "Laptop", "Rahul")

    assert hash1 != hash2


def test_hash_is_sha256_length():
    # A SHA-256 hash in hex form is always 64 characters long.
    result = generate_hash("agent-01", 5000, "APPROVED", "Laptop", "Rahul")
    assert len(result) == 64
