"""
agent.py

PLACEHOLDER FILE — no LLM agent is integrated yet.

Later, this file will contain the logic for an AI agent (using an
LLM API and possibly a framework like LangChain) that can make
decisions on its own. Those decisions would then get sent into our
existing POST /decisions endpoint, so the rest of the system
(hashing, verification, tamper detection) doesn't need to change at
all.

Planned flow (not implemented yet):

    LLM Agent
        v
    Decision
        v
    FastAPI
        v
    Hash
        v
    Blockchain

For now, decisions are created manually by sending a request
directly to POST /decisions (see app/api/routes/decisions.py).
"""

# Nothing to implement yet.
