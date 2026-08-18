"""
hashing.py

This is the MOST IMPORTANT file in AgentSeal. It is responsible
for turning a decision's data into a single SHA-256 hash.

WHY DOES THIS MATTER?
----------------------
A hash is like a "fingerprint" of data. If even ONE character of the
input changes, the hash comes out completely different. This lets us
detect tampering:

    1. When a decision is created, we hash its data and save the
       hash as "original_hash".
    2. Later, we take the CURRENT data in the database and hash it
       again the exact same way.
    3. If the two hashes match -> the data has NOT changed -> VERIFIED
    4. If the two hashes are different -> something changed -> TAMPERED

THE MOST IMPORTANT RULE
-------------------------
The same input data must ALWAYS produce the same hash. This means we
must be very consistent about:
    - which fields we include
    - what ORDER we put them in
    - how we format each field (e.g. numbers, spacing)

If we are not consistent, verification would give wrong answers even
when nothing was actually tampered with. That's why all the hashing
logic lives in ONE function below, instead of being repeated in
multiple places.
"""

import hashlib


def build_decision_string(agent_id: str, amount: float, decision: str,
                           description: str, user: str) -> str:
    """
    Combines the important decision fields into ONE consistent string.

    We use a fixed order and a simple separator ("|") between fields.
    This string is what actually gets hashed. Because the order and
    formatting never change, hashing the same values will always
    produce the same string, and therefore the same hash.

    NOTE: "description" can be empty/None, so we convert it to an
    empty string first to avoid errors and keep formatting consistent.
    """
    description = description or ""

    combined = (
        f"agent_id={agent_id}|"
        f"amount={amount}|"
        f"decision={decision}|"
        f"description={description}|"
        f"user={user}"
    )
    return combined


def generate_hash(agent_id: str, amount: float, decision: str,
                   description: str, user: str) -> str:
    """
    Generates a SHA-256 hash from the decision's important fields.

    Steps:
        1. Build a consistent string from the fields (see above).
        2. Convert that string into bytes (hashlib needs bytes,
           not a normal Python string).
        3. Run it through SHA-256.
        4. Return the hash as a readable hex string
           (e.g. "3f29a1...").
    """
    combined_string = build_decision_string(
        agent_id, amount, decision, description, user
    )

    # .encode() turns the string into bytes, which hashlib requires.
    hash_object = hashlib.sha256(combined_string.encode())

    # .hexdigest() gives us the hash as a normal readable string.
    return hash_object.hexdigest()
